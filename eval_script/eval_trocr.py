import os
import evaluate
import time
from tqdm import tqdm

import io

from PIL import Image
import os
from arabic_cleaning.cleaning_utils import (
    cleanse_document,
    normalize_similar_chars,
    remove_diacritics_tatweel,
    reduce_multiple_spaces,
)
from typing import List, Tuple
#import re
import regex as re  # not the built-in re module!

import requests
import base64
from pathlib import Path

class TextRecogAPIModel():
    def __init__(self, endpoint_url: str, batch_size: int, timeout: int):
        self.endpoint_url = endpoint_url
        self.batch_size = batch_size
        self.timeout = timeout

    def _encode_image(self, image_path: str) -> str:
        """
        Convert image to grayscale (3-channel) and encode as JPEG base64.
        """
        img = Image.open(image_path).convert("L").convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format= "PNG")#"JPEG", quality=95)  ##TODO: when they could be equivalent???
        return base64.b64encode(buf.getvalue()).decode("utf-8")

    def predict(self, image_path: str) -> str:
        return self.predict_batch([image_path])[0]

    def predict_batch(self, image_paths: List[str]) -> List[str]:
        try:
            return self._predict_batch_internal(image_paths)
        except Exception as e:
            print(f"Batch failed ({len(image_paths)} images): {e}")
            print("Falling back to single-image requests...")
            preds = []
            for p in image_paths:
                try:
                    preds.append(self._predict_batch_internal([p])[0])
                except Exception as ie:
                    print(f"  Failed image {p}: {ie}")
                    preds.append("")
            return preds

    def _predict_batch_internal(self, image_paths: List[str]) -> List[str]:
        batch_payload = []
        for image_path in image_paths:
            batch_payload.append(
                {
                    "id": Path(image_path).name,
                    "img": self._encode_image(image_path),
                }
            )

        payload = {"batch": batch_payload}

        response = requests.post(
            self.endpoint_url,
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()

        resp_json = response.json()
        if not resp_json.get("success", False):
            raise RuntimeError(resp_json)

        preds_by_id = {
            item["id"]: item.get("prediction", "")
            for item in resp_json.get("data", [])
        }

        return [
            preds_by_id.get(Path(p).name, "").strip()
            for p in image_paths
        ]


def normalize_text(text: str) -> str:
    """
    Normalize Arabic/English numbers, letters, punctuation, and separators.
    """
    # Arabic to English digits
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    digit_map = str.maketrans(arabic_digits, english_digits)

    # letters replacement
    replacements = {
        "ى": "ي",        
        "…": "...",  # Replace ellipsis
        "٬": ",",   # Arabic thousands separator to English comma
        "،" : ",",
        "’" : "'", 
        "٪" : "%"           
    }
    # Apply digit normalization
    text = text.translate(digit_map)
    # Apply replacements
    for src, tgt in replacements.items():
        text = text.replace(src, tgt)
    # Normalize different types of brackets to standard ones
    braces_map = {
        "【": "[", "】": "]",
        "〔": "[", "〕": "]",
        "〈": "<", "〉": ">",
        "《": "<", "》": ">",
        "｛": "{", "｝": "}",
        "«": '"', "»": '"',         
        "﴾": "(", "﴿": ")",       
        "›": ">", "‹": "<",             
    }
    for src, tgt in braces_map.items():
        text = text.replace(src, tgt)
    
    #text = re.sub(r"([0-9٠-٩/])\s+([ء-ي])", r"\1\2", text)

    return text

def clean_text(text):
    text = text.strip()
    text = normalize_text(text)
    pattern = r"[«»﴾﴿•£¥ﷺﷻ…‹›◆♦▪◻●❖©✓°◦]"
    text= re.sub(pattern, '', text)
    # remove spaces around all punctuation )
    text = re.sub(r'\s*(\p{P})\s*', r'\1', text)
    text = cleanse_document(text, cleansers=[reduce_multiple_spaces])
    text = cleanse_document(text, cleansers=[normalize_similar_chars])
    text = cleanse_document(text, cleansers=[remove_diacritics_tatweel])
    return text.strip()

# Load OCR data
def load_data(txt_file) -> List[Tuple[str, str]]:
    """
    Loads OCR ground truth data from a text file.
    Each line in the file should follow the format:
        filename.png企text企cvat_task_name企image_name_in_cvat
    Args:
        txt_file (str): Path to the data text file.

    Returns:
        List[Tuple[str, str]]: A list of (image_filename, text) tuples.
    """
    data = []
    with open(txt_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("企")
            image_name = parts[0]
            gt_text = parts[1]
            data.append((image_name, gt_text))
    return data



def evaluate_model(model, data, image_folder, save_path="evaluation_results.txt"):
    print(f"\nEvaluating {model.__class__.__name__}...")
    start_time = time.time()

    predictions = []
    ground_truths = []
    results = []

    PLACEHOLDER = "<EMPTY>"
    batch_size = getattr(model, "batch_size", 1)

    for i in tqdm(range(0, len(data), batch_size), desc="Processing batches"):
        batch = data[i : i + batch_size]

        image_paths = []
        image_names = []
        gt_texts = []

        for image_name, gt_text in batch:
            image_path = os.path.join(image_folder, image_name)
            if not os.path.exists(image_path):
                print(f"Image not found: {image_path}")
                continue

            image_paths.append(image_path)
            image_names.append(image_name)
            gt_texts.append(gt_text)

        if not image_paths:
            continue

        try:
            batch_preds = model.predict_batch(image_paths)
        except Exception as e:
            print(f"Batch failed: {e}")
            batch_preds = [""] * len(image_paths)

        for image_name, gt_text, pred_text in zip(
            image_names, gt_texts, batch_preds
        ):
            cleaned_pred = clean_text(pred_text)
            cleaned_gt = clean_text(gt_text)

            if cleaned_pred.strip() == "":
                cleaned_pred = PLACEHOLDER
            if cleaned_gt.strip() == "":
                cleaned_gt = PLACEHOLDER

            predictions.append(cleaned_pred)
            ground_truths.append(cleaned_gt)
            results.append((image_name, cleaned_gt, cleaned_pred))

    if not predictions:
        print("No predictions to evaluate.")
        return

    cer = evaluate.load("cer").compute(
        predictions=predictions, references=ground_truths
    )
    wer = evaluate.load("wer").compute(
        predictions=predictions, references=ground_truths
    )

    duration_sec = time.time() - start_time
    minutes, seconds = divmod(int(duration_sec), 60)

    print(f"\nEvaluation Results:")
    print(f"CER: {cer:.4f}")
    print(f"WER: {wer:.4f}")
    print(f"Total Evaluation Time: {minutes}m {seconds}s")

    with open(save_path, "w", encoding="utf-8") as f:
        for image_name, gt, pred in results:
            if gt != pred:
                f.write(f"Image: {image_name}\n")
                f.write(f"Ground Truth: {gt}\n")
                f.write(f"Prediction  : {pred}\n")
                f.write("-" * 50 + "\n")

        f.write(f"\nCER: {cer:.4f}\n")
        f.write(f"WER: {wer:.4f}\n")
        f.write(f"Total Evaluation Time: {minutes}m {seconds}s\n")

    print(f"Results saved to: {save_path}")

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir", type=str, help="")
    parser.add_argument("--ocr_dataset", type=str, help="")
    parser.add_argument("--text-model-url", type=str, default="")
    parser.add_argument("--results_file_name", type=str, help="results file path")

    args = parser.parse_args()

    eval_dataset = ( args.ocr_dataset )
    image_folder = args.img_dir
    data = load_data(eval_dataset)

    text_recog_url = args.text_model_url

    model = TextRecogAPIModel(
        endpoint_url=text_recog_url,
        batch_size=32,  
        timeout=300,
    )    

    evaluate_model(
    model,
    data,
    image_folder,
    save_path=args.results_file_name,
    )    

"""
python eval_trocr.py \
    --ocr_dataset "/ephemeral/home/data/TalkToDocs-Ingest/data/mozn_e2e_eval_data/task_248_dataset_2026_01_26_09_55_18_cvat for images 1.1/images_with_text.txt" \
    --img_dir "/ephemeral/home/data/TalkToDocs-Ingest/data/mozn_e2e_eval_data/task_248_dataset_2026_01_26_09_55_18_cvat for images 1.1/lines_images" \
    --text-model-url ""http://localhost:8102/text-recognition"" \
    --results_file_name "/ephemeral/home/abuzayed/e2e_evaluation_V2/trocr_16_e2e_data.txt"

"""