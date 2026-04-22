import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import pytesseract
from tqdm import tqdm
import shutil
import random
import string

# --- CONFIGURATION ---
TESTSET_DIR = "/app/DI/scripts/remove_nosie_rotation/cube_docs_imgs"
CONFIDENCE_THRESHOLD = 5.0
MAX_WORKERS = 16
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".tiff")

# Output folders
SUCCESS_DIR = os.path.join(TESTSET_DIR, "../cube_all_rotation_needs_rotation")
FAILED_DIR = os.path.join(TESTSET_DIR, "../cube_all_rotation_no_rotation_needed")
os.makedirs(SUCCESS_DIR, exist_ok=True)
os.makedirs(FAILED_DIR, exist_ok=True)

def random_suffix(length=18):
    """Generate a random alphanumeric prefix"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def needs_rotation(image_path, confidence_threshold=CONFIDENCE_THRESHOLD):
    """Detects if an image needs rotation, copies it to the appropriate folder,
       and creates a corrected rotated version if needed."""
    
    # Generate a single random prefix at the start
    prefix = random_suffix()
    
    try:
        img = Image.open(image_path)
        osd = pytesseract.image_to_osd(img, lang='osd', config='--oem 0')

        rotation_angle = 0
        rotate_confidence = 0.0

        for line in osd.split('\n'):
            if 'Rotate:' in line:
                rotation_angle = int(line.split(':')[-1].strip())
            elif 'Orientation confidence:' in line:
                rotate_confidence = float(line.split(':')[-1].strip())

        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)

        if rotate_confidence >= confidence_threshold and rotation_angle != 0:
            # Copy original with random prefix
            copy_name = f"{prefix}_{name}{ext}"
            shutil.copy(image_path, os.path.join(SUCCESS_DIR, copy_name))

            # Create rotated version with same prefix and _rotated suffix
            rotated_img = img.rotate(-rotation_angle, expand=True)  # negative for correct orientation
            rotated_name = f"{prefix}_{name}_rotated{ext}"
            rotated_img.save(os.path.join(SUCCESS_DIR, rotated_name))

            return True
        else:
            # Copy to failed folder with random prefix
            copy_name = f"{prefix}_{name}{ext}"
            shutil.copy(image_path, os.path.join(FAILED_DIR, copy_name))
            return False

    except Exception as e:
        # Copy to failed folder on error with random prefix
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        copy_name = f"{prefix}_{name}{ext}"
        shutil.copy(image_path, os.path.join(FAILED_DIR, copy_name))
        return False

def get_all_images(base_dir, extensions=IMAGE_EXTENSIONS): 
    """Recursively collect all images under base_dir that need rotation checking."""
    image_paths = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            image_paths.append(os.path.join(root, f))
    return image_paths

def check_rotations_batch(image_paths, max_workers=MAX_WORKERS):
    """Check rotation for a batch of images in parallel with progress bar"""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_path = {executor.submit(needs_rotation, path): path for path in image_paths}
        for future in tqdm(as_completed(future_to_path), total=len(image_paths), desc="Detecting rotation"):
            path = future_to_path[future]
            needs_rot = future.result()
            results.append((path, needs_rot))
    return results

if __name__ == "__main__":
    all_images = get_all_images(TESTSET_DIR)

    print(len(all_images))
    rotation_flags = check_rotations_batch(all_images)

    rotated_count = sum(1 for _, rot in rotation_flags if rot)
    not_rotated_count = len(rotation_flags) - rotated_count

    print("\n--- Rotation Detection Report ---")
    print(f"Total images checked: {len(rotation_flags)}")
    print(f"Images needing rotation (copied to {SUCCESS_DIR}): {rotated_count}")
    print(f"Images upright or skipped (copied to {FAILED_DIR}): {not_rotated_count}")
