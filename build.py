#!/usr/bin/env python3
"""
Connected Clip Show — Build Script

Run from anywhere:
    python3 episodes/clip-show/build.py

Or from clip-show/:
    python3 build.py
"""

import json, subprocess, sys
from pathlib import Path

# Use venv Python/Jinja2 if available, otherwise fall back to system
VENV_PYTHON = Path(__file__).parent.parent.parent / ".venv" / "bin" / "python3"
if VENV_PYTHON.exists() and str(VENV_PYTHON) != sys.executable:
    import subprocess as _sp
    result = _sp.run([str(VENV_PYTHON), __file__] + sys.argv[1:])
    sys.exit(result.returncode)

from jinja2 import Environment, FileSystemLoader

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
EPISODES_DIR = SCRIPT_DIR.parent
AUDIO_DIR    = SCRIPT_DIR / "audio"
CACHE_FILE   = SCRIPT_DIR / "cache.json"
CURATED_FILE = SCRIPT_DIR / "curated.json"
TEMPLATE     = SCRIPT_DIR / "template.html"
OUTPUT_HTML  = SCRIPT_DIR / "index.html"
CACHE_VERSION = 1

AUDIO_DIR.mkdir(exist_ok=True)

# ── Year → episode-range mapping (from RSS pubDate) ──────────────────────────
YEAR_RANGES = {
    2014: (1,   20),  2015: (21,  71),  2016: (72,  122), 2017: (123, 173),
    2018: (174, 224), 2019: (225, 274), 2020: (275, 326), 2021: (327, 378),
    2022: (379, 430), 2023: (431, 482), 2024: (483, 532), 2025: (533, 583),
    2026: (584, 9999),
}

ERA_RANGES = [(1,100), (101,200), (201,300), (301,400), (401,500), (501,600)]

def ep_to_year(ep):
    for year, (lo, hi) in YEAR_RANGES.items():
        if lo <= ep <= hi:
            return year
    return None

# ── Timestamp helpers ────────────────────────────────────────────────────────
def ts_to_seconds(ts):
    ts = ts.replace(",", ".")
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

# ── Cache ────────────────────────────────────────────────────────────────────
def load_cache():
    if CACHE_FILE.exists():
        data = json.loads(CACHE_FILE.read_text())
        if data.get("version") == CACHE_VERSION:
            return data
    return {"version": CACHE_VERSION, "audio": {}}

def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

# ── Audio extraction ─────────────────────────────────────────────────────────
def extract_audio(cache, clip_key, mp3_path, start_ts, end_ts, out_path):
    if out_path.exists() and cache["audio"].get(clip_key) == "ok":
        return True

    start_sec = max(0, ts_to_seconds(start_ts) - 0.3)
    end_sec   = ts_to_seconds(end_ts) + 0.5

    cmd = [
        "ffmpeg", "-i", str(mp3_path),
        "-ss", str(start_sec), "-to", str(end_sec),
        "-c", "copy", str(out_path),
        "-y", "-loglevel", "error"
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 1000:
        cache["audio"][clip_key] = "ok"
        return True
    print(f"  ⚠️  ffmpeg failed for {out_path.name}: {result.stderr.decode()[:120]}")
    return False

# ── Main processing ──────────────────────────────────────────────────────────
def process():
    cache = load_cache()

    with open(CURATED_FILE) as f:
        clips = json.load(f)

    print(f"Loaded {len(clips)} curated clips")

    # Tag each clip with its year
    for clip in clips:
        clip["year"] = ep_to_year(clip["episode"])

    # Group by episode for efficient mp3 lookup
    ep_clips = {}
    for i, clip in enumerate(clips):
        ep_clips.setdefault(clip["episode"], []).append((i, clip))

    extracted = skipped = failed_no_mp3 = failed_bad_ts = 0

    for ep_num in sorted(ep_clips):
        mp3_candidates = list(EPISODES_DIR.glob(f"{ep_num} *.mp3"))
        if not mp3_candidates:
            for _, clip in ep_clips[ep_num]:
                clip["audio_file"] = None
            failed_no_mp3 += len(ep_clips[ep_num])
            continue

        mp3_path = mp3_candidates[0]

        for i, clip in ep_clips[ep_num]:
            start_sec = ts_to_seconds(clip["start"])
            end_sec   = ts_to_seconds(clip["end"])
            if end_sec < 20 and start_sec < 20:
                clip["audio_file"] = None
                failed_bad_ts += 1
                continue

            start_ms = int(ts_to_seconds(clip["start"]) * 1000)
            end_ms   = int(ts_to_seconds(clip["end"])   * 1000)
            fname    = f"ep{ep_num:03d}_{start_ms}_{end_ms}.mp3"
            out_path = AUDIO_DIR / fname

            if out_path.exists() and cache["audio"].get(fname) == "ok":
                clip["audio_file"] = fname
                skipped += 1
            elif extract_audio(cache, fname, mp3_path, clip["start"], clip["end"], out_path):
                clip["audio_file"] = fname
                extracted += 1
                print(f"  Ep{ep_num:03d} extracted → {fname}")
            else:
                clip["audio_file"] = None

    save_cache(cache)

    has_audio = sum(1 for c in clips if c.get("audio_file"))
    print(f"\n✓ Audio: {extracted} extracted, {skipped} cached, "
          f"{failed_bad_ts} skipped (broken timestamps), {failed_no_mp3} skipped (no mp3)")
    print(f"  {has_audio}/{len(clips)} clips have audio")

    # Pinned clips always float to top
    pinned   = [c for c in clips if c.get("pinned")]
    unpinned = [c for c in clips if not c.get("pinned")]
    return pinned + unpinned

# ── HTML generation ──────────────────────────────────────────────────────────
def build_html(clips):
    unpinned = [c for c in clips if not c.get("pinned")]

    # Compute clip counts for filter UI
    year_counts = {}
    for year, (lo, hi) in YEAR_RANGES.items():
        count = sum(1 for c in unpinned if lo <= c["episode"] <= hi)
        if count:
            year_counts[year] = count

    era_counts = {}
    for lo, hi in ERA_RANGES:
        count = sum(1 for c in unpinned if lo <= c["episode"] <= hi)
        if count:
            era_counts[(lo, hi)] = count

    env = Environment(loader=FileSystemLoader(str(SCRIPT_DIR)), autoescape=False)
    tmpl = env.get_template("template.html")

    html = tmpl.render(
        clips=clips,
        clips_json=json.dumps(clips),
        year_ranges=YEAR_RANGES,
        year_counts=year_counts,
        era_counts=era_counts,
        total=len(clips),
        with_audio=sum(1 for c in clips if c.get("audio_file")),
    )

    OUTPUT_HTML.write_text(html)
    print(f"✓ HTML written → {OUTPUT_HTML.name}  ({OUTPUT_HTML.stat().st_size // 1024}KB)")

# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 52)
    print("  Connected Clip Show — Build")
    print("=" * 52)
    clips = process()
    build_html(clips)
    print("\nDone. Open clip-show/index.html in your browser.")
