# Advanced Stress Testing Script for Document Ingestion Pipeline

This tool performs fair, reproducible stress testing of a Document Ingestion / OCR pipeline that processes PDFs asynchronously.

It measures throughput, latency, system utilization (CPU/GPU/RAM), and pipeline performance across multiple concurrency levels.

The script is designed specifically for pipelines where PDFs have very different page counts, which makes naive request-per-second benchmarking misleading.

---

# Key Features

## Fair Benchmarking Design

PDFs vary widely in page count. Sending random requests at each concurrency level leads to unfair comparisons.

This script solves that by:

1. Pre-scanning PDFs to determine the true page count of each file.
2. Grouping PDFs into size buckets:
   - small
   - medium
   - large
3. Building one fixed stratified workload of PDFs.
4. Reusing the exact same workload at every concurrency level.

This ensures:

All concurrency levels process the same total pages.

The primary fairness metric becomes:

pages_per_sec_wall

which represents actual throughput of processed pages.

---

# Metrics Collected

The script collects both application-level and system-level metrics.

## Throughput Metrics

Metric | Description
------ | -----------
Requests/sec | HTTP request throughput
Pages/sec (wall clock) | Primary fairness metric
Pages/sec (server) | Sum of server-reported processing speeds

---

## Latency Metrics

Metric | Description
------ | -----------
Submit P50 / P95 | Time to submit request
Total P50 / P95 | Full processing latency
Total Max | Slowest request latency

---

## System Resource Metrics

Collected every second during testing.

Resource | Metrics
-------- | -------
CPU | avg %, max %
RAM | peak usage
GPU | utilization avg/max
GPU memory | peak memory usage

GPU metrics are collected using:

nvidia-smi

inside the detected model container (layout / line / textrec).

---

# Pipeline Metrics

If the pipeline exposes the endpoint:

GET /metrics

the script records additional server metrics at the end of each stage.

---

# Per-Bucket Analysis

To understand fairness across document sizes, the script reports latency per PDF bucket:

small  
medium  
large  

Example:

small (avg 2 pages): P50=1.3s P95=2.1s  
medium (avg 10 pages): P50=5.2s P95=7.8s  
large (avg 45 pages): P50=22.1s P95=35.4s  

This reveals whether large PDFs degrade disproportionately under load.

---

# Requirements

Install dependencies:

pip install requests rich psutil matplotlib pdfplumber

Optional but recommended:

nvidia-smi  
docker

---

# Input Requirements

The target pipeline must expose:

POST /process-pdf

Returns:

{
  "request_id": "<id>"
}

Status polling endpoint:

GET /task-status/{request_id}

Expected response example:

{
  "status": "done",
  "pages_done": 10,
  "duration_sec": 5.2,
  "img_per_sec": 1.9
}

Health check endpoint:

GET /health

---

# Usage

Example command:

python stress_test.py \
  --pdf-folder /home/elkady/cube_data/all_pdfs \
  --base-url http://localhost:51203 \
  --jwt-token "TOKEN" \
  --concurrency 4 8 16 32 64 256 512 \
  --requests-per-stage 550 \
  --request-timeout 1000 \
  --cooldown-sec 200 \
  --ramp-up-sec 2 \
  --docker-project fixing_bugs_3 \
  --output-dir ./stress_results_5

---

# Parameter Explanation

## Required Parameters

Parameter | Description
--------- | -----------
--pdf-folder | Folder containing PDF files
--base-url | Ingestion pipeline base URL

---

## Load Configuration

Parameter | Description
--------- | -----------
--concurrency | Number of parallel users
--requests-per-stage | Total PDFs sent per stage
--ramp-up-sec | Spread request submission
--cooldown-sec | Wait between stages

Example:

--concurrency 4 8 16 32 64 256 512

This runs 7 stress stages.

---

## Timeout Configuration

Parameter | Description
--------- | -----------
--request-timeout | Maximum wait time per PDF
--poll-interval | Status polling interval

Example:

--request-timeout 1000

Each PDF may run up to 1000 seconds.

---

## System Metrics Configuration

Parameter | Description
--------- | -----------
--docker-project | Docker compose project name
--metrics-interval | System metrics sampling interval

This is used to detect GPU containers automatically.

---

# Ramp-Up Behavior

Instead of sending all requests instantly, the script spreads the first wave across:

--ramp-up-sec

Example:

--ramp-up-sec 2

This prevents unrealistic request spikes.

---

# Output

Results are saved in the specified output directory.

Example:

./stress_results_5

Generated files include:

stress_report.json  
stress_main.png  
stress_gpu.png  
stress_failures.png  

---

# JSON Report

Contains full metrics for every stage.

Example structure:

{
  "generated_at": "...",
  "stages": [
    {
      "concurrency": 32,
      "successes": 550,
      "failures": 0,
      "pages_per_sec_wall": 41.2,
      "cpu_avg_pct": 82.4,
      "gpu_util_avg_pct": [91.3]
    }
  ]
}

---

# Plots Generated

Performance Plot

stress_main.png

Shows:

- requests/sec
- pages/sec
- latency
- CPU usage
- RAM usage

---

GPU Metrics Plot

stress_gpu.png

Shows:

- GPU utilization
- GPU peak memory

---

Failure Rate Plot

stress_failures.png

Shows request failures vs concurrency.

---

# Fair Comparison Principle

Traditional load tests compare:

requests/sec

But for document pipelines this is misleading because:

1 request could be 1 page or 200 pages.

This script compares stages using:

pages/sec (wall clock)

which reflects the actual work processed.

---

# Example Stage Output

Stage Summary — 64 concurrent users

Requests sent: 550  
Total pages: 9320  
Success / Failure: 550 / 0  

Throughput  
Requests/sec: 8.7  
Pages/sec: 74.3  

Latency  
P50: 7.2s  
P95: 13.1s  

Resources  
CPU avg: 84%  
GPU util avg: 92%  
GPU mem peak: 38 GB  

---

# Best Practices

Recommended values:

Parameter | Suggested Value
--------- | ---------------
requests-per-stage | 30–100
poll-interval | 2 seconds
ramp-up-sec | 2–5 seconds
cooldown-sec | 10–30 seconds

Large workloads (500+) provide better statistical stability but increase runtime.

---

# Typical Testing Strategy

Example concurrency progression:

4 → 8 → 16 → 32 → 64 → 128 → 256 → 512

Look for:

- throughput plateau
- GPU saturation
- latency explosion
- increasing failure rates

---

# Author

Designed for high-throughput OCR and document ingestion pipelines using asynchronous processing and GPU-accelerated models.