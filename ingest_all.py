import os
import json
import time
import threading
from glob import glob
from queue import Queue

from PyPDF2 import PdfReader
from tqdm import tqdm
import requests

# ---------------------------
# Configuration
# ---------------------------

"""
cube_files:
    Imports
        pdf_files or folder contains PDF files
    Exports
        pdf_files or folder contains PDF files

# data_10 keeps the same fodler hierarchy of cube_files, but JSON
"""
BASE_DIR = "/home/mozn/data/cvat_data/cube_files"   # Base folder with PDFs


PAGE_LIMIT = 500                                    # Max pages to process
MAX_WORKERS = 50                                    # Parallel requests
DIR_OUT_ROOT = "data_10"                            # Where JSON results go
MAX_SAMPLES_PER_FOLDER = None                       # Limit PDFs per folder for testing

CACHE_FILE = "pdf_page_counts.json"                 # File to store page counts

PORT = 21203
API_URL_PROCESS = f"http://192.168.1.78:{PORT}/process-pdf"
API_URL_STATUS = f"http://192.168.1.78:{PORT}/task-status"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkcHMtc2VydmljZSIsImF1ZCI6ImRzLWFwaSIsImlhdCI6MTc3MDgwMzY5MywiZXhwIjoxODA2ODAzNjkzfQ.Ru_8D0QvWgN1UVcSmqWmioXnsBqVBr8hn_c8tYeVZ4c"

# ---------------------------
# Throughput tracking
# ---------------------------
start_time = time.time()
pages_processed = 0
pages_lock = threading.Lock()

# ---------------------------
# Concurrency & Rate Control
# ---------------------------
submission_queue = Queue()
in_flight = {}
in_flight_lock = threading.Lock()
semaphore = threading.Semaphore(MAX_WORKERS)
stop_event = threading.Event()

last_request_time = 0
rate_lock = threading.Lock()
RATE_LIMIT = 2  # Max requests per second

# ---------------------------
# Cache helpers
# ---------------------------
def load_cache():
    """Load cached page counts from file"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """Save page count cache to file"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

page_cache = load_cache()

# ---------------------------
# PDF helpers
# ---------------------------
def get_pdf_length(pdf_path):
    """Return number of pages in a PDF, using cache if available"""
    if pdf_path in page_cache:
        return page_cache[pdf_path]

    try:
        pages = len(PdfReader(pdf_path).pages)
        page_cache[pdf_path] = pages
        return pages
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}")
        page_cache[pdf_path] = 0
        return 0

def get_pdfs_under_page_limit(base_dir, page_limit, max_samples_per_folder=None):
    """
    Scan 'Exports' and 'Imports' folders and return PDFs under page_limit
    Returns list of (folder_type, pdf_path)
    """
    result = []
    for folder in ["Exports", "Imports"]:
        folder_path = os.path.join(base_dir, folder, "**/*.pdf")
        pdf_files = glob(folder_path, recursive=True)

        if max_samples_per_folder:
            pdf_files = pdf_files[:max_samples_per_folder]

        print(f"Processing folder: {folder} ({len(pdf_files)} PDFs found)")
        for pdf_path in tqdm(pdf_files, desc=f"{folder} PDFs"):
            pages = get_pdf_length(pdf_path)
            if 0 < pages < page_limit:
                result.append((folder, pdf_path))
    return result

# ---------------------------
# Rate limiter
# ---------------------------
def rate_limited():
    """Ensure we don't exceed RATE_LIMIT requests per second"""
    global last_request_time

    with rate_lock:
        now = time.time()
        min_interval = 1.0 / RATE_LIMIT
        elapsed = now - last_request_time

        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)

        last_request_time = time.time()

# ---------------------------
# API helpers
# ---------------------------
def send_pdf_for_processing(pdf_path):
    """Send PDF to API for processing"""
    headers = {"Authorization": f"Bearer {TOKEN}"}

    with open(pdf_path, "rb") as f:
        files = {
            "file": (
                os.path.basename(pdf_path),
                f,
                "application/pdf",
            ),
            "file_metadata": (
                None,
                json.dumps({
                    "page_numbers": list(range(1, get_pdf_length(pdf_path) + 1))
                }),
                "application/json",
            ),
        }

        response = requests.post(API_URL_PROCESS, headers=headers, files=files)
    response.raise_for_status()
    return response.json()

def check_status(request_id):
    """Check processing status"""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{API_URL_STATUS}/{request_id}"

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

# ---------------------------
# Workers
# ---------------------------
def submit_worker():
    """Submit PDFs to the API while respecting concurrency and rate limit"""
    while not submission_queue.empty():
        semaphore.acquire()

        try:
            folder_type, pdf_path = submission_queue.get_nowait()
        except:
            semaphore.release()
            break

        page_count = get_pdf_length(pdf_path)

        json_file_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".json"
        target_folder = os.path.join(DIR_OUT_ROOT, folder_type)
        os.makedirs(target_folder, exist_ok=True)
        json_path = os.path.join(target_folder, json_file_name)

        if os.path.exists(json_path):
            # print(f"Skipping {pdf_path}, JSON exists")
            semaphore.release()
            continue

        try:
            rate_limited()  # Max requests per second
            time.sleep(1)
            resp = send_pdf_for_processing(pdf_path)
            request_id = resp.get("request_id")

            with in_flight_lock:
                in_flight[request_id] = {
                    "pdf_path": pdf_path,
                    "json_path": json_path,
                    "page_count": page_count
                }

            print(f"Submitted {pdf_path} → {request_id} | In-flight: {len(in_flight)}")

        except Exception as e:
            print(f"Failed submitting {pdf_path}: {e}")
            semaphore.release()

import time
def result_worker():
    """Poll submitted requests and write their results (or failures) to JSON"""
    global pages_processed

    while not stop_event.is_set() or in_flight:
        time.sleep(0.2)

        with in_flight_lock:
            request_ids = list(in_flight.keys())

        for request_id in request_ids:
            try:
                time.sleep(1)
                # print(f"check for {request_id}")
                # continue
                status = check_status(request_id)
            except Exception as e:
                # Network hiccup; retry on next loop
                print(f"Error checking status {request_id}: {e}")
                continue

            if status.get("status") not in ["done", "failed"]:
                continue

            with in_flight_lock:
                metadata = in_flight.pop(request_id, None)

            if metadata:
                # Always attempt to write the JSON, even on failure
                try:
                    with open(metadata["json_path"], "w", encoding="utf-8") as f:
                        json.dump(status, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"Failed writing JSON for {metadata['pdf_path']}: {e}")

                if status.get("status") == "done":
                    with pages_lock:
                        pages_processed += metadata["page_count"]
                        elapsed = time.time() - start_time
                        rate = pages_processed / elapsed if elapsed > 0 else 0

                    print(
                        f"Completed {metadata['pdf_path']} | "
                        f"In-flight: {len(in_flight)} | "
                        f"Total pages: {pages_processed} | "
                        f"Rate: {rate:.2f} pages/sec"
                    )
                else:
                    print(
                        f"Failed {metadata['pdf_path']} | "
                        f"In-flight: {len(in_flight)} | "
                        f"Response saved (or attempted) to JSON"
                    )

                # Release semaphore so next job can proceed
                semaphore.release()

# ---------------------------
# Main workflow
# ---------------------------
if __name__ == "__main__":

    # Step 1: Gather PDFs under page limit
    pdfs_to_process = get_pdfs_under_page_limit(BASE_DIR, PAGE_LIMIT, MAX_SAMPLES_PER_FOLDER)
    print(f"Total PDFs to process: {len(pdfs_to_process)}")

    # Save/update page count cache
    save_cache(page_cache)

    # Sort by page count (smallest first)
    pdfs_to_process.sort(key=lambda t: page_cache.get(t[1], 0))

    # Fill the submission queue
    for item in pdfs_to_process:
        submission_queue.put(item)

    # Start worker threads
    submit_thread = threading.Thread(target=submit_worker)
    result_thread = threading.Thread(target=result_worker)

    submit_thread.start()
    result_thread.start()

    submit_thread.join()
    stop_event.set()
    result_thread.join()

    print("All PDFs processed.")
