"""
Advanced Stress Testing Script for Document Ingestion Pipeline
=============================================================

Fair-comparison design
-----------------------
PDFs have wildly different page counts, so raw request counts are misleading.
This script:
  1. Pre-scans the PDF folder and records the true page count of every file.
  2. Groups PDFs into size buckets (small / medium / large) by page count.
  3. At every concurrency stage the *same fixed workload* is sent:
       - identical set of N PDFs chosen once (stratified across size buckets,
         seeded for reproducibility), so every stage sees the same total pages.
  4. Reports both request-level AND page-normalised metrics so you can compare
     apples-to-apples across stages.

Usage
-----
python stress_test.py \
    --pdf-folder /home/elkady/cube_data/all_pdfs \
    --base-url http://localhost:61203 \
    --jwt-token "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
    --concurrency 5 10 20 50 100 150 200 250 300 350 400 450 500 1000

Requirements
------------
    pip install requests rich psutil matplotlib pdfplumber
"""

import argparse
import os
import sys
import time
import json
import math
import random
import threading
import statistics
import subprocess
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# ── pdfplumber (page-count pre-scan) ─────────────────────────────────────────
try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

# ── rich (pretty output) ──────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    class _Con:
        def print(self, *a, **kw): print(*a)
        def rule(self, *a, **kw):  print("=" * 70)
    console = _Con()

# ── matplotlib ────────────────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False


# =============================================================================
# 1. Data structures
# =============================================================================

@dataclass
class PDFInfo:
    path: str
    name: str
    page_count: int
    size_bytes: int
    bucket: str = ""          # small / medium / large

@dataclass
class RequestResult:
    request_id: str
    pdf_name: str
    page_count: int
    submit_latency_ms: float
    total_latency_ms: float    = 0.0
    server_duration_sec: float = 0.0
    pages_done: int            = 0
    img_per_sec: float         = 0.0
    status: str                = "unknown"
    error: str                 = ""
    http_status: int           = 200

@dataclass
class SystemSnapshot:
    ts: float
    cpu_percent: float
    ram_used_mb: float
    gpu_util_pct: list
    gpu_mem_used_mb: list
    gpu_mem_total_mb: list

@dataclass
class StageResult:
    concurrency: int
    n_requests: int
    total_pages_sent: int
    successes: int
    failures: int
    submit_p50_ms: float       = 0.0
    submit_p95_ms: float       = 0.0
    total_p50_ms: float        = 0.0
    total_p95_ms: float        = 0.0
    total_max_ms: float        = 0.0
    wall_time_sec: float       = 0.0
    rps: float                 = 0.0
    pages_per_sec_wall: float  = 0.0
    pages_per_sec_server: float= 0.0
    cpu_avg_pct: float         = 0.0
    cpu_max_pct: float         = 0.0
    ram_peak_mb: float         = 0.0
    gpu_util_avg_pct: list     = field(default_factory=list)
    gpu_util_max_pct: list     = field(default_factory=list)
    gpu_mem_peak_mb: list      = field(default_factory=list)
    gpu_mem_total_mb: list     = field(default_factory=list)
    pipeline_metrics_post: dict= field(default_factory=dict)
    bucket_stats: dict         = field(default_factory=dict)


# =============================================================================
# 2. PDF catalogue (pre-scan + stratified workload)
# =============================================================================

def count_pdf_pages(path: str) -> int:
    if not HAS_PDFPLUMBER:
        return 1
    try:
        with pdfplumber.open(path) as pdf:
            return len(pdf.pages)
    except Exception:
        return 0

def build_catalogue(folder: str) -> list:
    paths = sorted(Path(folder).glob("*.pdf"))
    if not paths:
        console.print(f"[red]No PDFs found in {folder}[/red]")
        sys.exit(1)

    console.print(f"\n[cyan]Scanning {len(paths)} PDFs for page counts...[/cyan]")
    catalogue = []
    for i, p in enumerate(paths, 1):
        pages = count_pdf_pages(str(p))
        if pages == 0:
            console.print(f"  [yellow]Skipping unreadable: {p.name}[/yellow]")
            continue
        catalogue.append(PDFInfo(
            path=str(p), name=p.name,
            page_count=pages, size_bytes=p.stat().st_size,
        ))
        if i % 20 == 0 or i == len(paths):
            console.print(f"  {i}/{len(paths)} scanned...")

    # Assign size buckets via terciles
    counts = sorted(c.page_count for c in catalogue)
    p33 = counts[len(counts) // 3]
    p66 = counts[2 * len(counts) // 3]
    for info in catalogue:
        if info.page_count <= p33:
            info.bucket = "small"
        elif info.page_count <= p66:
            info.bucket = "medium"
        else:
            info.bucket = "large"

    by_bucket = {"small": [], "medium": [], "large": []}
    for c in catalogue:
        by_bucket[c.bucket].append(c.page_count)

    console.print(f"\n[green]Catalogue ready: {len(catalogue)} valid PDFs[/green]")
    for b, pgs in by_bucket.items():
        if pgs:
            console.print(
                f"  {b:7s}: {len(pgs):4d} PDFs | "
                f"pages min={min(pgs)} median={sorted(pgs)[len(pgs)//2]} max={max(pgs)}"
            )
    return catalogue


def build_fixed_workload(catalogue: list, n_requests: int, seed: int = 42) -> list:
    """
    Stratified sample — proportional representation of each size bucket.
    Same seed = same workload across ALL concurrency stages = fair comparison.
    """
    rng = random.Random(seed)
    buckets = {"small": [], "medium": [], "large": []}
    for info in catalogue:
        buckets[info.bucket].append(info)

    total = len(catalogue)
    selected = []
    for b, items in buckets.items():
        if not items:
            continue
        quota = max(1, round(n_requests * len(items) / total))
        chosen = rng.choices(items, k=quota) if quota > len(items) else rng.sample(items, quota)
        selected.extend(chosen)

    rng.shuffle(selected)
    if len(selected) < n_requests:
        selected.extend(rng.choices(catalogue, k=n_requests - len(selected)))
    selected = selected[:n_requests]
    rng.shuffle(selected)

    total_pages = sum(i.page_count for i in selected)
    avg_pages   = total_pages / len(selected)

    console.print(
        f"\n[bold]Fixed workload (seed={seed}):[/bold] {len(selected)} PDFs | "
        f"{total_pages} total pages | avg {avg_pages:.1f} pages/PDF\n"
        f"[dim](Identical workload reused every stage for fair comparison)[/dim]"
    )

    # Rough runtime estimate so the user knows what they're in for
    # Assume ~5s per page as a conservative upper bound for serial processing
    est_serial_min = total_pages * 5 / 60
    console.print(
        f"[yellow]Estimated worst-case stage duration (concurrency=1, 5s/page): "
        f"~{est_serial_min:.0f} min. "
        f"Higher concurrency will be proportionally faster up to the server's limit.[/yellow]"
    )

    return selected


# =============================================================================
# 3. System metrics collector
# =============================================================================

class SystemMetricsCollector:
    def __init__(self, compose_project: str, sample_interval: float = 1.0):
        self.compose_project   = compose_project
        self.sample_interval   = sample_interval
        self._snapshots        = []
        self._stop_event       = threading.Event()
        self._thread           = None

        try:
            import psutil
            self._psutil = psutil
        except ImportError:
            console.print("[yellow]psutil not installed - CPU/RAM disabled.  pip install psutil[/yellow]")
            self._psutil = None

        self._gpu_container = self._find_gpu_container()

    def _find_gpu_container(self):
        """
        Find a GPU model container (layout / line / textrec).
        Explicitly excludes pipeline / ui / non-GPU containers.
        Falls back to host nvidia-smi if none found.
        """
        try:
            out = subprocess.check_output(
                ["docker", "ps", "--format", "{{.Names}}"],
                stderr=subprocess.DEVNULL
            ).decode().strip().split("\n")
            project = self.compose_project.lower()

            # All containers belonging to this compose project
            project_containers = [c for c in out if project in c.lower()]

            # GPU model containers — must match a model keyword
            GPU_KEYWORDS     = ("layout", "line", "textrec", "model")
            # Non-GPU containers — explicitly excluded
            EXCLUDE_KEYWORDS = ("pipeline", "ui", "streamlit", "nginx", "redis")

            gpu_containers = [
                c for c in project_containers
                if any(kw in c.lower() for kw in GPU_KEYWORDS)
                and not any(ex in c.lower() for ex in EXCLUDE_KEYWORDS)
            ]

            if gpu_containers:
                # Prefer layout (usually the biggest GPU consumer)
                chosen = next(
                    (c for c in gpu_containers if "textrec" in c.lower()),
                    gpu_containers[0]
                )
                console.print(
                    f"[cyan]GPU metrics via container: {chosen}[/cyan]\n"
                    f"[dim]  (all model containers found: {gpu_containers})[/dim]"
                )
                return chosen

            # No GPU container found — fall back to host nvidia-smi
            console.print(
                "[yellow]No GPU model container found in project "
                f"'{self.compose_project}'.\n"
                f"  Containers seen: {project_containers}\n"
                "  Falling back to host nvidia-smi (may show 0 if GPU is inside Docker).[/yellow]"
            )
            return None
        except Exception as e:
            console.print(f"[yellow]Container detection failed ({e}); using host nvidia-smi[/yellow]")
            return None

    def _sample_gpu(self):
        util, used, total = [], [], []
        cmd_prefix = ["docker", "exec", self._gpu_container] if self._gpu_container else []
        try:
            out = subprocess.check_output(
                cmd_prefix + [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu,memory.used,memory.total",
                    "--format=csv,noheader,nounits",
                ],
                stderr=subprocess.DEVNULL, timeout=3,
            ).decode().strip()
            for line in out.split("\n"):
                parts = [x.strip() for x in line.split(",")]
                if len(parts) == 3:
                    util.append(float(parts[0]))
                    used.append(float(parts[1]))
                    total.append(float(parts[2]))
        except Exception:
            pass
        return util, used, total

    def _sample(self):
        cpu, ram = 0.0, 0.0
        if self._psutil:
            cpu = self._psutil.cpu_percent(interval=None)
            vm  = self._psutil.virtual_memory()
            ram = vm.used / 1024 / 1024
        g_util, g_used, g_total = self._sample_gpu()
        return SystemSnapshot(
            ts=time.time(), cpu_percent=cpu, ram_used_mb=ram,
            gpu_util_pct=g_util, gpu_mem_used_mb=g_used, gpu_mem_total_mb=g_total,
        )

    def _run(self):
        if self._psutil:
            self._psutil.cpu_percent(interval=None)   # prime first call
        while not self._stop_event.is_set():
            self._snapshots.append(self._sample())
            self._stop_event.wait(timeout=self.sample_interval)

    def start(self):
        self._snapshots.clear()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        return list(self._snapshots)

    @staticmethod
    def summarize(snapshots):
        if not snapshots:
            return {}
        cpu = [s.cpu_percent for s in snapshots]
        ram = [s.ram_used_mb for s in snapshots]
        n_gpu = max((len(s.gpu_util_pct) for s in snapshots), default=0)
        gpu_util_avg, gpu_util_max, gpu_mem_peak, gpu_mem_total = [], [], [], []
        for g in range(n_gpu):
            utils = [s.gpu_util_pct[g]    for s in snapshots if g < len(s.gpu_util_pct)]
            mems  = [s.gpu_mem_used_mb[g]  for s in snapshots if g < len(s.gpu_mem_used_mb)]
            tots  = [s.gpu_mem_total_mb[g] for s in snapshots if g < len(s.gpu_mem_total_mb)]
            gpu_util_avg.append(round(statistics.mean(utils), 1) if utils else 0.0)
            gpu_util_max.append(round(max(utils),             1) if utils else 0.0)
            gpu_mem_peak.append(round(max(mems),              1) if mems else 0.0)
            gpu_mem_total.append(round(max(tots),             1) if tots else 0.0)
        return {
            "cpu_avg_pct":      round(statistics.mean(cpu), 1),
            "cpu_max_pct":      round(max(cpu),             1),
            "ram_peak_mb":      round(max(ram),             1),
            "gpu_util_avg_pct": gpu_util_avg,
            "gpu_util_max_pct": gpu_util_max,
            "gpu_mem_peak_mb":  gpu_mem_peak,
            "gpu_mem_total_mb": gpu_mem_total,
        }


# =============================================================================
# 4. HTTP helpers
# =============================================================================

def build_headers(jwt_token):
    return {"Authorization": f"Bearer {jwt_token}"} if jwt_token else {}

def submit_pdf(base_url, pdf_path, headers, timeout=30):
    t0 = time.perf_counter()
    with open(pdf_path, "rb") as f:
        resp = requests.post(
            f"{base_url}/process-pdf",
            files={"file": (os.path.basename(pdf_path), f, "application/pdf")},
            headers=headers, timeout=timeout,
        )
    lat_ms = (time.perf_counter() - t0) * 1000
    if resp.status_code == 200:
        return resp.json().get("request_id", ""), lat_ms, resp.status_code
    return "", lat_ms, resp.status_code

def poll_until_done(base_url, request_id, headers, poll_interval=2.0, timeout=600.0):
    """Poll /task-status/{id} — default 10-minute timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(
                f"{base_url}/task-status/{request_id}",
                headers=headers, timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("status") in ("done", "failed"):
                    return data
        except Exception:
            pass
        time.sleep(poll_interval)
    return {"status": "timeout", "error": "10-min polling timeout exceeded"}

def get_pipeline_metrics(base_url, headers):
    try:
        r = requests.get(f"{base_url}/metrics", headers=headers, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}


# =============================================================================
# 5. Single request
# =============================================================================

def run_one(info: PDFInfo, base_url, headers, poll_interval, request_timeout) -> RequestResult:
    result = RequestResult(
        request_id="", pdf_name=info.name,
        page_count=info.page_count, submit_latency_ms=0.0,
    )
    t0 = time.perf_counter()
    try:
        rid, sub_lat, http_status = submit_pdf(base_url, info.path, headers)
        result.submit_latency_ms = sub_lat
        result.http_status       = http_status

        if http_status != 200 or not rid:
            result.status = "submit_failed"
            result.error  = f"HTTP {http_status}"
            result.total_latency_ms = (time.perf_counter() - t0) * 1000
            return result

        result.request_id = rid
        final = poll_until_done(base_url, rid, headers, poll_interval, request_timeout)
        result.total_latency_ms     = (time.perf_counter() - t0) * 1000
        result.status               = final.get("status", "unknown")
        result.error                = final.get("error", "")
        result.pages_done           = final.get("pages_done", 0) or 0
        result.server_duration_sec  = final.get("duration_sec", 0.0) or 0.0
        result.img_per_sec          = final.get("img_per_sec", 0.0) or 0.0
    except Exception as e:
        result.status = "exception"
        result.error  = str(e)
        result.total_latency_ms = (time.perf_counter() - t0) * 1000
    return result


# =============================================================================
# 6. Stage runner
# =============================================================================

def run_stage(
    concurrency, workload, base_url, headers,
    poll_interval, request_timeout, collector, ramp_up_sec,
) -> StageResult:

    total_pages = sum(i.page_count for i in workload)
    console.rule(
        f"[bold cyan]Concurrency={concurrency}  |  "
        f"{len(workload)} PDFs  |  {total_pages} pages[/bold cyan]"
    )

    results = []
    lock = threading.Lock()
    done_count = [0]

    def _task(info, delay):
        if delay > 0:
            time.sleep(delay)
        r = run_one(info, base_url, headers, poll_interval, request_timeout)
        with lock:
            results.append(r)
            done_count[0] += 1
            sym = "[green]OK[/green]" if r.status == "done" else "[red]FAIL[/red]"
            console.print(
                f"  {sym} ({done_count[0]}/{len(workload)}) "
                f"{r.pdf_name}  pages={r.page_count}  "
                f"submit={r.submit_latency_ms:.0f}ms  "
                f"total={r.total_latency_ms/1000:.1f}s  "
                f"status={r.status}"
            )
        return r

    # Staggered delays: spread first wave over ramp_up_sec
    step = ramp_up_sec / max(concurrency, 1)
    delays = [math.floor(i / concurrency) * step for i in range(len(workload))]

    collector.start()
    wall_t0 = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(_task, info, delays[i]) for i, info in enumerate(workload)]
        for f in as_completed(futures):
            f.result()

    wall_elapsed = time.time() - wall_t0
    snapshots    = collector.stop()
    sys_stats    = collector.summarize(snapshots)
    post_metrics = get_pipeline_metrics(base_url, headers)

    ok   = [r for r in results if r.status == "done"]
    fail = [r for r in results if r.status != "done"]

    def pct(data, p):
        if not data: return 0.0
        s = sorted(data)
        return round(s[min(int(len(s) * p / 100), len(s)-1)], 2)

    sub_lats   = [r.submit_latency_ms for r in results]
    total_lats = [r.total_latency_ms  for r in results]
    total_pages_ok = sum(r.pages_done for r in ok)

    # Per-bucket latency breakdown (fairness insight)
    # Build a name->bucket lookup from the workload list
    name_to_bucket = {info.name: info.bucket for info in workload}
    bucket_stats = {}
    for bucket in ("small", "medium", "large"):
        br = [r for r in ok if name_to_bucket.get(r.pdf_name) == bucket]
        if br:
            lats = [r.total_latency_ms / 1000 for r in br]
            pgs  = [r.page_count for r in br]
            bucket_stats[bucket] = {
                "count":        len(br),
                "avg_pages":    round(statistics.mean(pgs), 1),
                "lat_p50_sec":  round(statistics.median(lats), 2),
                "lat_p95_sec":  pct([x * 1000 for x in lats], 95) / 1000,
                "lat_max_sec":  round(max(lats), 2),
            }

    stage = StageResult(
        concurrency=concurrency,
        n_requests=len(workload),
        total_pages_sent=total_pages,
        successes=len(ok),
        failures=len(fail),
        submit_p50_ms=pct(sub_lats, 50),
        submit_p95_ms=pct(sub_lats, 95),
        total_p50_ms =pct(total_lats, 50),
        total_p95_ms =pct(total_lats, 95),
        total_max_ms =round(max(total_lats), 1) if total_lats else 0.0,
        wall_time_sec=round(wall_elapsed, 2),
        rps=round(len(results) / wall_elapsed, 3) if wall_elapsed > 0 else 0.0,
        pages_per_sec_wall=round(total_pages_ok / wall_elapsed, 3) if wall_elapsed > 0 else 0.0,
        pages_per_sec_server=round(sum(r.img_per_sec for r in ok), 2),
        cpu_avg_pct=sys_stats.get("cpu_avg_pct", 0.0),
        cpu_max_pct=sys_stats.get("cpu_max_pct", 0.0),
        ram_peak_mb=sys_stats.get("ram_peak_mb", 0.0),
        gpu_util_avg_pct=sys_stats.get("gpu_util_avg_pct", []),
        gpu_util_max_pct=sys_stats.get("gpu_util_max_pct", []),
        gpu_mem_peak_mb =sys_stats.get("gpu_mem_peak_mb",  []),
        gpu_mem_total_mb=sys_stats.get("gpu_mem_total_mb", []),
        pipeline_metrics_post=post_metrics,
        bucket_stats=bucket_stats,
    )
    _print_stage(stage)
    return stage


# =============================================================================
# 7. Rich printing
# =============================================================================

def _print_stage(s: StageResult):
    if not HAS_RICH:
        print(f"\n  RPS={s.rps:.2f} pages/s={s.pages_per_sec_wall:.2f} "
              f"P50={s.total_p50_ms/1000:.1f}s P95={s.total_p95_ms/1000:.1f}s "
              f"CPU={s.cpu_avg_pct}% RAM={s.ram_peak_mb:.0f}MB")
        return

    t = Table(title=f"Stage Summary — {s.concurrency} concurrent users",
              show_header=True, header_style="bold")
    t.add_column("Metric",  style="bold", min_width=35)
    t.add_column("Value",   min_width=22)

    rows = [
        ("Requests sent",                  str(s.n_requests)),
        ("Total pages in workload",        str(s.total_pages_sent)),
        ("Success / Failure",              f"[green]{s.successes}[/green] / [red]{s.failures}[/red]"),
        ("Wall-clock time",                f"{s.wall_time_sec:.1f} s"),
        ("-- Throughput --",               ""),
        ("  Requests / sec",               f"{s.rps:.3f}"),
        ("  Pages / sec (wall clock) [*]", f"[bold green]{s.pages_per_sec_wall:.3f}[/bold green]"),
        ("  Pages / sec (server-side sum)",f"{s.pages_per_sec_server:.2f}"),
        ("-- Latency --",                  ""),
        ("  Total P50",                    f"{s.total_p50_ms/1000:.2f} s"),
        ("  Total P95",                    f"{s.total_p95_ms/1000:.2f} s"),
        ("  Total Max",                    f"{s.total_max_ms/1000:.2f} s"),
        ("  Submit P50 / P95",             f"{s.submit_p50_ms:.0f} ms / {s.submit_p95_ms:.0f} ms"),
        ("-- Host Resources --",           ""),
        ("  CPU avg / max",                f"{s.cpu_avg_pct}% / {s.cpu_max_pct}%"),
        ("  RAM peak",                     f"{s.ram_peak_mb:.0f} MB"),
    ]
    for i, (u_avg, u_max, m_pk, m_tot) in enumerate(
        zip(s.gpu_util_avg_pct, s.gpu_util_max_pct, s.gpu_mem_peak_mb, s.gpu_mem_total_mb)
    ):
        rows += [
            (f"-- GPU {i} --",               ""),
            (f"  Util avg / max",             f"{u_avg}% / {u_max}%"),
            (f"  Mem used peak / total",      f"{m_pk:.0f} MB / {m_tot:.0f} MB"),
        ]
    if s.bucket_stats:
        rows.append(("-- Per-Bucket Breakdown (success only) --", ""))
        for b, bs in s.bucket_stats.items():
            rows.append((
                f"  {b} (avg {bs['avg_pages']:.0f} pages)",
                f"P50={bs['lat_p50_sec']:.2f}s  P95={bs['lat_p95_sec']:.2f}s  "
                f"Max={bs['lat_max_sec']:.2f}s  n={bs['count']}"
            ))

    for k, v in rows:
        t.add_row(k, v)
    console.print(t)
    console.print("[dim][*] Pages/sec uses wall-clock time — primary fairness metric[/dim]\n")


def print_comparison(stages):
    console.rule("[bold]FINAL COMPARISON ACROSS ALL CONCURRENCY LEVELS[/bold]")
    if not HAS_RICH:
        hdr = (f"{'Users':>6}  {'OK':>5}  {'Fail':>5}  {'RPS':>7}  "
               f"{'Pages/s':>8}  {'P50s':>6}  {'P95s':>6}  "
               f"{'CPU%':>6}  {'RAM MB':>8}  {'GPU0%':>7}  {'GPU0 MB':>8}")
        print(hdr); print("-" * len(hdr))
        for s in stages:
            g  = f"{s.gpu_util_avg_pct[0]:.0f}" if s.gpu_util_avg_pct else "N/A"
            gm = f"{s.gpu_mem_peak_mb[0]:.0f}"  if s.gpu_mem_peak_mb  else "N/A"
            print(
                f"{s.concurrency:>6}  {s.successes:>5}  {s.failures:>5}  "
                f"{s.rps:>7.2f}  {s.pages_per_sec_wall:>8.2f}  "
                f"{s.total_p50_ms/1000:>6.1f}  {s.total_p95_ms/1000:>6.1f}  "
                f"{s.cpu_avg_pct:>6.1f}  {s.ram_peak_mb:>8.0f}  {g:>7}  {gm:>8}"
            )
        return

    t = Table(show_header=True, header_style="bold magenta")
    base_cols = ["Users","OK","Fail","RPS","Pages/s [*]",
                 "P50(s)","P95(s)","Max(s)","CPU avg%","RAM peak MB"]
    for c in base_cols:
        t.add_column(c)
    n_gpu = max((len(s.gpu_util_avg_pct) for s in stages), default=0)
    for g in range(n_gpu):
        t.add_column(f"GPU{g} avg%")
        t.add_column(f"GPU{g} max%")
        t.add_column(f"GPU{g} mem peak MB")
        t.add_column(f"GPU{g} mem total MB")

    for s in stages:
        row = [
            str(s.concurrency), str(s.successes), str(s.failures),
            f"{s.rps:.2f}", f"[bold green]{s.pages_per_sec_wall:.2f}[/bold green]",
            f"{s.total_p50_ms/1000:.1f}", f"{s.total_p95_ms/1000:.1f}",
            f"{s.total_max_ms/1000:.1f}",
            f"{s.cpu_avg_pct:.1f}", f"{s.ram_peak_mb:.0f}",
        ]
        for g in range(n_gpu):
            row.append(str(s.gpu_util_avg_pct[g]) if g < len(s.gpu_util_avg_pct) else "N/A")
            row.append(str(s.gpu_util_max_pct[g]) if g < len(s.gpu_util_max_pct) else "N/A")
            row.append(f"{s.gpu_mem_peak_mb[g]:.0f}"  if g < len(s.gpu_mem_peak_mb)  else "N/A")
            row.append(f"{s.gpu_mem_total_mb[g]:.0f}" if g < len(s.gpu_mem_total_mb) else "N/A")
        t.add_row(*row)

    console.print(t)
    console.print("[dim][*] Pages/sec: same fixed stratified workload every stage — fair comparison[/dim]")


# =============================================================================
# 8. Save report + plots
# =============================================================================

def save_report(stages, path):
    report = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "fairness_note": (
            "Same stratified workload (identical PDF set) is sent at every "
            "concurrency level. pages_per_sec_wall is the primary comparison metric."
        ),
        "stages": [asdict(s) for s in stages],
    }
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    console.print(f"\n[green]Report saved: {path}[/green]")


def plot_results(stages, out_dir):
    if not HAS_PLOT:
        console.print("[yellow]matplotlib not installed - skipping plots[/yellow]")
        return

    xs = [s.concurrency for s in stages]

    def _ax(ax, ys, title, ylabel, color="steelblue"):
        ax.plot(xs, ys, marker="o", color=color, linewidth=2, markersize=5)
        ax.set_title(title, fontweight="bold", fontsize=10)
        ax.set_xlabel("Concurrent Users", fontsize=8)
        ax.set_ylabel(ylabel, fontsize=8)
        ax.grid(True, alpha=0.3)
        for x, y in zip(xs, ys):
            ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                        xytext=(0, 6), ha="center", fontsize=6)

    # Main 3x2 grid
    fig, axes = plt.subplots(3, 2, figsize=(14, 15))
    fig.suptitle("Stress Test: Performance vs Concurrency\n"
                 "(same stratified workload every stage)", fontsize=14, fontweight="bold")
    _ax(axes[0][0], [s.rps for s in stages],                "Throughput (req/sec)",        "req/sec",  "seagreen")
    _ax(axes[0][1], [s.pages_per_sec_wall for s in stages], "Pages/sec [fairness metric]", "pages/sec","teal")
    _ax(axes[1][0], [s.total_p50_ms/1000 for s in stages],  "Total Latency P50",           "seconds",  "steelblue")
    _ax(axes[1][1], [s.total_p95_ms/1000 for s in stages],  "Total Latency P95",           "seconds",  "tomato")
    _ax(axes[2][0], [s.cpu_avg_pct for s in stages],        "CPU Avg %",                   "%",         "darkorange")
    _ax(axes[2][1], [s.ram_peak_mb for s in stages],        "RAM Peak MB",                 "MB",        "mediumpurple")
    plt.tight_layout()
    p1 = os.path.join(out_dir, "stress_main.png")
    plt.savefig(p1, dpi=150); plt.close()
    console.print(f"[green]Plot saved: {p1}[/green]")

    # GPU plots
    n_gpu = max((len(s.gpu_util_avg_pct) for s in stages), default=0)
    if n_gpu:
        fig2, axes2 = plt.subplots(n_gpu, 3, figsize=(16, 5 * n_gpu), squeeze=False)
        fig2.suptitle("GPU Metrics vs Concurrency", fontsize=13, fontweight="bold")
        for g in range(n_gpu):
            u_avg = [s.gpu_util_avg_pct[g] if g < len(s.gpu_util_avg_pct) else 0 for s in stages]
            u_max = [s.gpu_util_max_pct[g] if g < len(s.gpu_util_max_pct) else 0 for s in stages]
            m_pk  = [s.gpu_mem_peak_mb[g]  if g < len(s.gpu_mem_peak_mb)  else 0 for s in stages]
            _ax(axes2[g][0], u_avg, f"GPU {g} Util Avg %",  "%",  "darkorange")
            _ax(axes2[g][1], u_max, f"GPU {g} Util Max %",  "%",  "orangered")
            _ax(axes2[g][2], m_pk,  f"GPU {g} Mem Peak MB", "MB", "darkred")
        plt.tight_layout()
        p2 = os.path.join(out_dir, "stress_gpu.png")
        plt.savefig(p2, dpi=150); plt.close()
        console.print(f"[green]GPU plot saved: {p2}[/green]")

    # Failure rate bar chart
    fig3, ax = plt.subplots(figsize=(10, 4))
    fail_pct = [100.0 * s.failures / s.n_requests for s in stages]
    colors   = ["red" if f > 0 else "green" for f in fail_pct]
    ax.bar([str(x) for x in xs], fail_pct, color=colors, alpha=0.75)
    ax.set_title("Failure Rate % by Concurrency Level", fontweight="bold")
    ax.set_xlabel("Concurrent Users"); ax.set_ylabel("Failure %")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    p3 = os.path.join(out_dir, "stress_failures.png")
    plt.savefig(p3, dpi=150); plt.close()
    console.print(f"[green]Failure chart saved: {p3}[/green]")


# =============================================================================
# 9. CLI
# =============================================================================

def parse_args():
    p = argparse.ArgumentParser(
        description="Fair-comparison stress test for Document Ingestion Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--pdf-folder",    required=True,
                   help="Folder with PDF files of various sizes")
    p.add_argument("--base-url",      default="http://localhost:61203")
    p.add_argument("--jwt-token",     default=None,
                   help="JWT bearer token")
    p.add_argument("--concurrency",   nargs="+", type=int,
                   default=[5, 10, 20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000],
                   help="Concurrency levels to test")
    p.add_argument("--requests-per-stage", type=int, default=30,
                   help=(
                       "Total PDFs sent per stage. The SAME stratified set is reused "
                       "at every concurrency level for a fair comparison. "
                       "This is the TOTAL count, NOT per-user. "
                       "Start with 30-50; higher values give better statistics but take longer. "
                       "With large PDFs and 10-min timeouts, 50 requests at concurrency=5 "
                       "could take ~50 min for that stage alone."
                   ))
    p.add_argument("--poll-interval",    type=float, default=2.0,
                   help="Seconds between /task-status polls")
    p.add_argument("--request-timeout",  type=float, default=600.0,
                   help="Max wait per PDF in seconds (default=600 = 10 min)")
    p.add_argument("--ramp-up-sec",      type=float, default=3.0,
                   help="Seconds to spread initial wave of submits per stage")
    p.add_argument("--cooldown-sec",     type=float, default=10.0,
                   help="Wait between stages to let queues drain")
    p.add_argument("--docker-project",   default="fixing_bugs_3",
                   help="Docker Compose project name for GPU container detection")
    p.add_argument("--metrics-interval", type=float, default=1.0,
                   help="System metrics sampling interval (seconds)")
    p.add_argument("--output-dir",       default="stress_results_2",
                   help="Directory for report + plots")
    p.add_argument("--seed",             type=int, default=42,
                   help="Random seed for reproducible workload")
    return p.parse_args()


# =============================================================================
# 10. Main
# =============================================================================

def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # ── Pre-flight: warn about potentially very long runs ────────────────────
    n_req_stage    = max(args.requests_per_stage, 10)
    n_stages       = len(args.concurrency)
    min_conc       = min(args.concurrency)
    worst_case_min = (n_req_stage / min_conc) * (args.request_timeout / 60)

    console.print(
        f"\n[bold yellow]Pre-flight summary[/bold yellow]\n"
        f"  Stages          : {n_stages} concurrency levels ({sorted(args.concurrency)})\n"
        f"  Requests/stage  : {n_req_stage}  (total PDFs per stage, NOT per-user)\n"
        f"  Request timeout : {args.request_timeout:.0f}s ({args.request_timeout/60:.1f} min) per PDF\n"
        f"  Worst-case stage: concurrency={min_conc}, "
        f"up to [red]{worst_case_min:.0f} min[/red] if every PDF hits the timeout\n"
    )
    if worst_case_min > 30:
        console.print(
            "[red bold]WARNING: Slowest stage could take {:.0f} min in the worst case.\n"
            "Consider --requests-per-stage 20 to keep stages under 10 min "
            "while still getting valid statistics.[/red bold]".format(worst_case_min)
        )
        try:
            answer = input("Continue? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = "n"
        if answer != "y":
            console.print("[yellow]Aborted.[/yellow]")
            sys.exit(0)

    # 1. Pre-scan PDFs
    catalogue = build_catalogue(args.pdf_folder)

    # 2. Build ONE fixed stratified workload (reused every stage)
    # Concurrency = parallelism, NOT total count. Do not inflate to max(concurrency).
    n_req    = max(args.requests_per_stage, 10)
    workload = build_fixed_workload(catalogue, n_requests=n_req, seed=args.seed)

    # 3. Health check
    headers = build_headers(args.jwt_token)
    try:
        r = requests.get(f"{args.base_url}/health", headers=headers, timeout=10)
        assert r.status_code == 200
        console.print(f"[green]Server healthy: {args.base_url}[/green]")
    except Exception as e:
        console.print(f"[red]Health check failed: {e}[/red]")
        sys.exit(1)

    # 4. Metrics collector
    collector = SystemMetricsCollector(
        compose_project=args.docker_project,
        sample_interval=args.metrics_interval,
    )

    # 5. Run all concurrency stages
    all_stages = []
    levels = sorted(args.concurrency)

    for c in levels:
        stage = run_stage(
            concurrency=c,
            workload=workload,          # same fixed workload every time
            base_url=args.base_url,
            headers=headers,
            poll_interval=args.poll_interval,
            request_timeout=args.request_timeout,   # 600s = 10 min
            collector=collector,
            ramp_up_sec=args.ramp_up_sec,
        )
        all_stages.append(stage)

        if c != levels[-1]:
            console.print(f"[yellow]Cooling down {args.cooldown_sec}s...[/yellow]")
            time.sleep(args.cooldown_sec)

    # 6. Final report
    print_comparison(all_stages)
    report_path = os.path.join(args.output_dir, "stress_report.json")
    save_report(all_stages, report_path)
    plot_results(all_stages, args.output_dir)

    console.print(f"\n[bold green]Stress test complete.[/bold green]")
    console.print(f"Results in: [cyan]{os.path.abspath(args.output_dir)}[/cyan]")


if __name__ == "__main__":
    main()