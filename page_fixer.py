# pip install python-doctr
# 

import os
import numpy as np
from PIL import Image
from doctr.models import ocr_predictor

os.environ["DOCTR_CACHE_DIR"] = os.environ.get(
    "DOCTR_CACHE_DIR",
    "/home/data/TalkToDocs-Ingest/debug/cube_checkpoints/page_fixer"
)


# -----------------------------------------------------------------------------
# Shared image helpers
# -----------------------------------------------------------------------------

def rotate_pil(img: Image.Image, angle: float) -> Image.Image:
    return img.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)




# -----------------------------------------------------------------------------
# docTR part
# -----------------------------------------------------------------------------

def build_doctr_predictor():
    return ocr_predictor(
        pretrained=True,
        assume_straight_pages=False,
        detect_orientation=True,
        straighten_pages=False,
    )

def extract_doctr_page_orientation(result):
    """
    Try to read orientation angle from docTR result in a version-tolerant way.
    """
    try:
        page = result.pages[0]
    except Exception:
        return None

    candidates = []

    for attr in ["orientation", "page_orientation", "_orientation"]:
        if hasattr(page, attr):
            candidates.append(getattr(page, attr))

    for cand in candidates:
        if cand is None:
            continue

        if isinstance(cand, (int, float)):
            return float(cand)

        if isinstance(cand, dict):
            for key in ["value", "angle", "degrees", "orientation"]:
                if key in cand and isinstance(cand[key], (int, float)):
                    return float(cand[key])

        for key in ["value", "angle", "degrees", "orientation"]:
            if hasattr(cand, key):
                val = getattr(cand, key)
                if isinstance(val, (int, float)):
                    return float(val)

    return None


def detect_with_doctr(image_path: str, model) -> dict:
    img = Image.open(image_path).convert("RGB")
    np_img = np.array(img)

    result = model([np_img])
    angle = extract_doctr_page_orientation(result)

    return {
        "angle": angle,
        "raw_result": result,
    }


def normalize_doctr_angle(angle):
    if angle is None:
        return None
    return ((angle + 180) % 360) - 180


# -----------------------------------------------------------------------------
# Main logic
# -----------------------------------------------------------------------------

def fix_orientation(image_path: str, doctr_model) -> dict:
    img = Image.open(image_path).convert("RGB")

    # Use docTR for orientation detection
    doctr_out = detect_with_doctr(image_path, doctr_model)
    doctr_angle = normalize_doctr_angle(doctr_out["angle"])

    if doctr_angle is None:
        return {
            "method": "none",
            "angle_used": None,
            "output_path": None,
            "details": {
                "error": "docTR did not expose a readable orientation angle."
            },
        }

    correction_angle = -doctr_angle

    if abs(correction_angle) < 0.5:
        return {
            "method": "doctr",
            "angle_used": 0.0,
            "output_path": image_path,
            "details": doctr_out,
        }

    fixed = rotate_pil(img, correction_angle)

    return {
        "method": "doctr",
        "angle_used": correction_angle,
        "details": doctr_out,
    }


def print_result(result: dict):
    print(f"Method used   : {result['method']}")
    print(f"Angle used    : {result['angle_used']}")
    print(f"Output path   : {result['output_path']}")

    angle = result.get("angle_used")
    if angle is None:
        print("Decision      : could not determine orientation")
    elif abs(angle) < 0.5:
        print("Decision      : already upright")
    else:
        print(f"Decision      : rotated by {angle} degrees")



def test_on_image(image_path: str):
    model = build_doctr_predictor()

    print("=" * 80)
    print(f"TEST IMAGE: {image_path}")
    print("=" * 80)

    result = fix_orientation(image_path, model)
    print_result(result)
    print()


if __name__ == "__main__":
    image_path = "image.png"
    test_on_image(image_path)