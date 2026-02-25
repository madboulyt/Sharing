"""
--------------------
1. Submit images to DI pipeline
2. Poll for results
3. Save TXT/JSON outputs
4. Evaluate OCR  (WER / CER)
"""

import argparse
import json
import re
import time
from pathlib import Path
from typing import Dict, List

import requests
import evaluate
from arabic_cleaning.cleaning_utils import (
    cleanse_document,
    normalize_similar_chars,
    remove_diacritics_tatweel,
    reduce_multiple_spaces,
)

# ----------------------------
# OCR Extraction
# ----------------------------
def extract_text_from_pipeline_result(result: list) -> List[str]:
    """Flatten OCR output into a list of lines."""
    if not isinstance(result, list):
        return []

    lines = []
    for page in result:
        for element in page.get("detected_elements", []):
            for line in element.get("lines", []):
                text = line.get("ocr_text", "").strip()
                if text:
                    lines.append(text)
    return lines


# ----------------------------
# Pipeline Submission
# ----------------------------
def submit_images(
    image_paths: List[Path],
    pipeline_url: str,
    max_retries: int,
    throttle: float,
) -> Dict[str, Path]:
    request_map = {}
    failed = []

    for img_path in image_paths:
        for attempt in range(max_retries):
            try:
                with img_path.open("rb") as f:
                    files = {
                        "file": (img_path.name, f),
                        "file_metadata": (
                            None,
                            json.dumps({"page_numbers": [1]}),
                            "application/json",
                        ),
                    }
                    r = requests.post(f"{pipeline_url}/process-pdf", files=files)

                if r.status_code == 429:
                    wait = 2 ** attempt
                    print(f"429 for {img_path.name}, retrying in {wait}s...")
                    time.sleep(wait)
                    continue

                r.raise_for_status()
                request_id = r.json()["request_id"]
                request_map[request_id] = img_path
                print(f"Queued {img_path.name} → {request_id}")
                time.sleep(throttle)
                break

            except Exception as e:
                print(f"Error submitting {img_path.name}: {e}")
                time.sleep(1)
        else:
            failed.append(img_path)

    if failed:
        print(f"Failed to queue {len(failed)} images")

    return request_map


# ----------------------------
# Polling
# ----------------------------
def poll_results(
    request_map: Dict[str, Path],
    pipeline_url: str,
    poll_interval: int,
    max_wait: int,
) -> Dict[str, dict]:
    results = {}
    pending = set(request_map.keys())
    start_time = {rid: time.time() for rid in pending}

    while pending:
        print(f"\nWaiting on {len(pending)} tasks...")
        finished = set()
        now = time.time()

        for rid in list(pending):
            elapsed = now - start_time[rid]

            if elapsed > max_wait:
                img_name = request_map[rid].name
                print(f"⏰ Timeout {rid}>> {img_name} after {int(elapsed)}s")
                finished.add(rid)
                continue

            try:
                r = requests.get(f"{pipeline_url}/task-status/{rid}", timeout = 10)
                if not r.ok:
                    print(f"⚠️ Status error {rid}: {r.text}")
                    continue

                status = r.json()
                state = status.get("status")

                if state == "done":
                    results[rid] = status.get("result")
                    print(f"✅ Done {rid}")
                    finished.add(rid)

                elif state == "failed":
                    print(f"❌ Failed {rid}: {status}")
                    finished.add(rid)

                else:
                    print(f"⏳ {rid} → {state} ({int(elapsed)}s)")

            except requests.RequestException as e:
                print(f"⚠️ Network error {rid}: {e}")
                continue 

        pending -= finished
        time.sleep(poll_interval)

    return results


# ----------------------------
# Text Normalization
# ----------------------------
def normalize_text(text: str) -> str:
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    text = text.translate(str.maketrans(arabic_digits, english_digits))

    replacements = {
        "ى": "ي", "…": "...", "٬": ",", "،": ",",
        "’": "'", "٪": "%"
    }
    for s, t in replacements.items():
        text = text.replace(s, t)

    braces = {
        "【":"[","】":"]","〔":"[","〕":"]",
        "〈":"<","〉":">","《":"<","》":">",
        "｛":"{","｝":"}","«":'"',"»":'"',
        "﴾":"(", "﴿":")","›":">", "‹":"<"
    }
    for s, t in braces.items():
        text = text.replace(s, t)

    return text


def clean_text(text: str) -> str:
    text = normalize_text(text.strip())
    text = re.sub(r"[«»﴾﴿•£¥ﷺﷻ…‹›◆♦▪◻●❖©✓°◦]", "", text)
    text = re.sub(r"\s*([^\w\s])\s*", r"\1", text)
    text = cleanse_document(text, [reduce_multiple_spaces])
    text = cleanse_document(text, [normalize_similar_chars])
    text = cleanse_document(text, [remove_diacritics_tatweel])
    return text.strip()


# ----------------------------
# Evaluation
# ----------------------------
def run_evaluation(gt_dir: Path, predictions: Dict[str, str]):
    refs, preds = [], []
    missing = 0

    for gt_file in sorted(gt_dir.glob("*.txt")):
        key = gt_file.stem
        if key not in predictions:
            print(f"Missing prediction for: {key}")
            missing += 1
            continue

        refs.append(clean_text(gt_file.read_text(encoding="utf-8")))
        preds.append(clean_text(predictions[key]))

    wer = evaluate.load("wer").compute(references=refs, predictions=preds)
    cer = evaluate.load("cer").compute(references=refs, predictions=preds)

    print("\n========== OCR EVALUATION ==========")
    print("Samples evaluated:", len(refs))
    print("Missing predictions:", missing)
    print("WER:", wer)
    print("CER:", cer)


# ----------------------------
# Main 
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="OCR Pipeline CLI")
    parser.add_argument("--pipeline-url", required=True)
    parser.add_argument("--image-dir", required=True)
    parser.add_argument("--gt-dir", required=True)
    parser.add_argument("--out-txt", help="Directory to write TXT outputs") ## add default path
    parser.add_argument("--out-json", help="Directory to write JSON outputs")

    parser.add_argument("--write-txt", action="store_true", help="Write OCR text outputs (.txt)")
    parser.add_argument("--write-json", action="store_true", help="Write OCR JSON outputs")

    parser.add_argument("--max-retries", type=int, default=5)
    parser.add_argument("--poll-interval", type=int, default=5)
    parser.add_argument("--max-wait", type=int, default=1200) 
    parser.add_argument("--throttle", type=float, default=0.2)
    args = parser.parse_args()

    if args.write_txt and not args.out_txt:
        parser.error("--write-txt requires --out-txt")

    if args.write_json and not args.out_json:
        parser.error("--write-json requires --out-json")
    image_dir = Path(args.image_dir)
    out_txt = Path(args.out_txt) if args.write_txt else None
    out_json = Path(args.out_json) if args.write_json else None

    if out_txt:
        out_txt.mkdir(parents=True, exist_ok=True)

    if out_json:
        out_json.mkdir(parents=True, exist_ok=True)

    images = sorted(image_dir.glob("*.*"))
    print(f"Found {len(images)} images")
############################### 1. Submit images to DI pipeline
    request_map = submit_images(
        images, args.pipeline_url, args.max_retries, args.throttle
    )
################################ 2. Poll for results
    results = poll_results(
        request_map, args.pipeline_url, args.poll_interval, args.max_wait
    )
###############################
# TODO: Add a flag to include/exclude Tables and/or Pictures. Currently, we assume all detected text are from text elements.
    predictions = {}
    for rid, result in results.items():
        img = request_map[rid]
        text = "\n".join(extract_text_from_pipeline_result(result))
        predictions[img.stem] = text
        if out_txt:
            (out_txt / f"{img.stem}.txt").write_text(text, encoding="utf-8")
            #print(f"Saved TXT for {img.name}")

        if out_json:
            (out_json / f"{img.stem}.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            #print(f"Saved JSON for {img.name}")
########################################
    run_evaluation(Path(args.gt_dir), predictions)
#########################################

if __name__ == "__main__":
    main()


"""
python evaluate_pipeline.py \
  --pipeline-url http://localhost:8103 \
  --image-dir "/ephemeral/home/data/TalkToDocs-Ingest/data/mozn_e2e_eval_data/task_248_dataset_2026_01_26_09_55_18_cvat for images 1.1/images" \
  --gt-dir "/ephemeral/home/data/TalkToDocs-Ingest/data/mozn_e2e_eval_data/task_248_dataset_2026_01_26_09_55_18_cvat for images 1.1/gt_texts_v3" \
  --write-txt \
  --out-txt "/ephemeral/home/data/TalkToDocs-Ingest/data/mozn_e2e_eval_data/task_248_dataset_2026_01_26_09_55_18_cvat for images 1.1/new_pipeline_preds/pred_texts3/" \
  --write-json \
  --out-json "/ephemeral/home/data/TalkToDocs-Ingest/data/mozn_e2e_eval_data/task_248_dataset_2026_01_26_09_55_18_cvat for images 1.1/new_pipeline_preds/preds_json3/"
"""