#!/usr/bin/env python3
"""
Connected Clip Show — Build Script
====================================
Clips are hand-curated in curated.json. Edit that file to add or change clips.

Run this script any time:
  - You add new entries to curated.json
  - New .mp3 files arrive for episodes already in curated.json

The script will:
  1. Read curated.json as the sole source of truth for clips
  2. For each clip, check the cache — skip if audio already extracted
  3. Run ffmpeg to extract audio only for clips that need it
  4. Rebuild index.html

Usage:
    cd "clip-show"
    python3 build.py

Outputs:
    cache.json          — tracks which audio clips have been extracted
    audio/ep054_0.mp3   — extracted audio clips
    index.html          — the clip show website
"""

import json, subprocess
from pathlib import Path

# ── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
EPISODES_DIR = SCRIPT_DIR.parent
AUDIO_DIR    = SCRIPT_DIR / "audio"
CACHE_FILE   = SCRIPT_DIR / "cache.json"
CURATED_FILE = SCRIPT_DIR / "curated.json"
OUTPUT_HTML  = SCRIPT_DIR / "index.html"
CACHE_VERSION = 1

AUDIO_DIR.mkdir(exist_ok=True)

# ── Timestamp helpers ────────────────────────────────────────────────────────

def ts_to_seconds(ts):
    """'00:01:23,456'  →  83.456"""
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
    """Extract one clip with ffmpeg. Returns True if file is ready."""
    if out_path.exists() and cache["audio"].get(clip_key) == "ok":
        return True  # already done

    start_sec = max(0, ts_to_seconds(start_ts) - 0.3)
    end_sec   = ts_to_seconds(end_ts) + 0.5

    cmd = [
        "ffmpeg", "-i", str(mp3_path),
        "-ss", str(start_sec),
        "-to", str(end_sec),
        "-c", "copy",
        str(out_path),
        "-y", "-loglevel", "error"
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0 and out_path.exists() and out_path.stat().st_size > 1000:
        cache["audio"][clip_key] = "ok"
        return True
    print(f"  ⚠️  ffmpeg failed for {out_path.name}: {result.stderr.decode()[:120]}")
    return False

# ── Main ─────────────────────────────────────────────────────────────────────

def process():
    cache = load_cache()

    with open(CURATED_FILE) as f:
        clips = json.load(f)

    print(f"Loaded {len(clips)} curated clips")

    # Group clips by episode so we only check the mp3 once per episode
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
            print(f"  Ep{ep_num:03d} — no mp3 found, skipping audio")
            continue

        mp3_path = mp3_candidates[0]

        for i, clip in ep_clips[ep_num]:
            # Detect broken timestamps (max ~14s means the dote has no real timing)
            start_sec = ts_to_seconds(clip["start"])
            end_sec   = ts_to_seconds(clip["end"])
            if end_sec < 20 and start_sec < 20:
                clip["audio_file"] = None
                failed_bad_ts += 1
                continue

            # Filename based on start+end ms — stable across clip reorderings
            start_ms  = int(ts_to_seconds(clip["start"]) * 1000)
            end_ms    = int(ts_to_seconds(clip["end"])   * 1000)
            fname     = f"ep{ep_num:03d}_{start_ms}_{end_ms}.mp3"
            out_path  = AUDIO_DIR / fname
            clip_key  = fname  # use filename as cache key

            if out_path.exists() and cache["audio"].get(clip_key) == "ok":
                clip["audio_file"] = fname
                skipped += 1
            elif extract_audio(cache, clip_key, mp3_path, clip["start"], clip["end"], out_path):
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

    # Pin any clips with "pinned": true to the front
    pinned   = [c for c in clips if c.get("pinned")]
    unpinned = [c for c in clips if not c.get("pinned")]
    clips = pinned + unpinned

    return clips

# ── HTML ─────────────────────────────────────────────────────────────────────

def build_html(clips):
    clips_json = json.dumps(clips, indent=2)
    total = len(clips)
    with_audio = sum(1 for c in clips if c.get("audio_file"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Everyone Needs a Hobby — Connected 600</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
  :root {{
    --myke:    #a78bfa; --fed:     #fbbf24; --stephen: #60a5fa; --unk: #9ca3af;
    --bg:      #0a0a0f; --surface: #13131a; --border:  #1e1e2e;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--bg); color:#e2e8f0; font-family:'Inter',sans-serif; min-height:100vh; overflow-x:hidden; }}

  /* INTRO */
  #intro {{
    position:fixed; inset:0; z-index:100; background:var(--bg);
    display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px;
    transition:opacity .8s;
  }}
  #intro.gone {{ opacity:0; pointer-events:none; }}
  .relay-label {{ font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:6px; text-transform:uppercase; color:#2d2d40; margin-bottom:6px; }}
  .big-600 {{
    font-size:clamp(90px,19vw,190px); font-weight:900; line-height:1; letter-spacing:-5px;
    background:linear-gradient(130deg,#a78bfa 0%,#60a5fa 45%,#fbbf24 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    animation:glow 3s ease-in-out infinite;
  }}
  @keyframes glow {{
    0%,100% {{ filter:drop-shadow(0 0 30px rgba(167,139,250,.2)); }}
    50%      {{ filter:drop-shadow(0 0 60px rgba(167,139,250,.5)); }}
  }}
  .show-name {{ font-size:clamp(14px,2.5vw,24px); font-weight:300; letter-spacing:10px; text-transform:uppercase; color:#6b7280; }}
  .clip-show-tag {{ font-size:clamp(13px,2vw,20px); font-weight:700; letter-spacing:4px; text-transform:uppercase; color:#fbbf24; margin-top:4px; }}
  .hosts-row {{ display:flex; gap:28px; margin-top:14px; }}
  .host-chip {{ display:flex; align-items:center; gap:7px; font-size:11px; font-weight:600; letter-spacing:2px; text-transform:uppercase; color:#374151; }}
  .host-pip {{ width:7px; height:7px; border-radius:50%; }}
  .start-btn {{
    margin-top:36px; padding:13px 42px; background:transparent;
    border:1px solid #252535; border-radius:3px; color:#9ca3af;
    font-family:'Inter',sans-serif; font-size:12px; font-weight:600;
    letter-spacing:4px; text-transform:uppercase; cursor:pointer; transition:all .2s;
  }}
  .start-btn:hover {{ border-color:#a78bfa; color:#a78bfa; box-shadow:0 0 24px rgba(167,139,250,.15); }}

  /* FLASH MONTAGE */
  #montage {{
    position:fixed; inset:0; z-index:90; background:var(--bg);
    display:none; align-items:center; justify-content:center;
    flex-direction:column; gap:20px; cursor:pointer;
    transition:background .4s ease;
  }}
  #montage.on {{ display:flex; }}
  .m-card {{
    display:flex; flex-direction:column; gap:16px; align-items:center;
    max-width:72vw; padding:40px 48px; border-radius:12px;
    background:rgba(255,255,255,.035);
    backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px);
    border:1px solid rgba(255,255,255,.06);
    pointer-events:none;
  }}
  .m-meta {{ font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:3px; text-transform:uppercase; color:#6b7280; opacity:0; transition:opacity .25s; }}
  .m-quote {{
    font-size:clamp(18px,3.5vw,44px); font-weight:700; text-align:center;
    line-height:1.4;
    opacity:0; transform:translateY(8px); transition:opacity .25s ease, transform .25s ease;
  }}
  .m-speaker {{ font-size:11px; font-weight:700; letter-spacing:5px; text-transform:uppercase; opacity:0; transition:opacity .25s; }}
  .m-audio {{ opacity:0; transition:opacity .3s; margin-top:4px; pointer-events:auto; }}
  .m-audio audio {{ height:28px; opacity:.55; filter:invert(1) hue-rotate(180deg); }}
  .m-quote.show,.m-speaker.show,.m-meta.show,.m-audio.show {{ opacity:1; transform:translateY(0); }}
  .m-close {{
    position:fixed; top:0; right:0; padding:24px 28px;
    font-size:10px; letter-spacing:3px; text-transform:uppercase; color:#374151;
    cursor:pointer; font-weight:600; background:none; border:none;
    font-family:'Inter',sans-serif; transition:color .2s;
  }}
  .m-close:hover {{ color:#9ca3af; }}
  .m-hint {{ position:fixed; bottom:16px; left:50%; transform:translateX(-50%); font-size:10px; letter-spacing:2px; text-transform:uppercase; color:#2d3748; pointer-events:none; white-space:nowrap; }}
  .m-counter {{ position:fixed; top:22px; left:28px; font-family:'JetBrains Mono',monospace; font-size:10px; color:#374151; letter-spacing:2px; }}
  .m-nav-hint {{
    position:fixed; bottom:40px; left:50%; transform:translateX(-50%);
    display:flex; gap:8px; align-items:center; opacity:0;
    transition:opacity .4s; pointer-events:none;
  }}
  .m-nav-hint.show {{ opacity:1; }}
  .m-nav-arrow {{
    width:36px; height:36px; border-radius:50%;
    border:1px solid rgba(255,255,255,.1); display:flex; align-items:center; justify-content:center;
    font-size:14px; color:#4b5563;
  }}

  /* MAIN */
  #main {{ opacity:0; transition:opacity .8s; padding-bottom:100px; }}
  #main.show {{ opacity:1; }}
  .topbar {{
    position:sticky; top:0; z-index:50;
    display:flex; align-items:center; justify-content:space-between;
    padding:16px 32px; background:rgba(10,10,15,.96); backdrop-filter:blur(12px);
    border-bottom:1px solid var(--border);
  }}
  .topbar-title {{ font-size:11px; font-weight:700; letter-spacing:3px; text-transform:uppercase; color:#6b7280; }}
  .topbar-title em {{ color:#a78bfa; font-style:normal; }}
  .btn-row {{ display:flex; gap:10px; }}
  .tbtn {{
    padding:7px 14px; background:transparent; border:1px solid var(--border);
    border-radius:3px; color:#4b5563; font-family:'Inter',sans-serif;
    font-size:11px; font-weight:600; letter-spacing:2px; text-transform:uppercase;
    cursor:pointer; transition:all .2s;
  }}
  .tbtn:hover,.tbtn.on {{ border-color:#a78bfa; color:#a78bfa; background:rgba(167,139,250,.07); }}

  /* GRID */
  .section-hdr {{ display:flex; align-items:center; gap:20px; padding:44px 32px 20px; }}
  .section-label {{ font-size:10px; font-weight:700; letter-spacing:6px; text-transform:uppercase; color:#374151; white-space:nowrap; }}
  .section-count {{ font-family:'JetBrains Mono',monospace; font-size:9px; color:#374151; letter-spacing:1px; }}
  .section-hr {{ flex:1; height:1px; background:var(--border); }}
  .grid {{
    display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
    gap:1px; margin:0 32px; border:1px solid var(--border); border-radius:8px; overflow:hidden;
  }}
  .card {{
    background:var(--surface); padding:22px 26px;
    display:flex; flex-direction:column; gap:12px; transition:background .2s;
  }}
  .card:hover {{ background:#15151f; }}
  .card.opener {{ grid-column:1/-1; padding:34px; }}
  .card.opener .q-text {{ font-size:18px; font-weight:300; line-height:1.75; color:#e2e8f0; }}
  .card-top {{ display:flex; align-items:center; justify-content:space-between; gap:8px; }}
  .spk-badge {{ display:flex; align-items:center; gap:7px; font-size:10px; font-weight:700; letter-spacing:3px; text-transform:uppercase; }}
  .spk-pip {{ width:6px; height:6px; border-radius:50%; flex-shrink:0; }}
  .ep-label {{
    font-family:'JetBrains Mono',monospace; font-size:10px; color:#8b95a6;
    letter-spacing:1px; text-align:right; flex-shrink:0;
  }}
  .ep-label .ep-num {{ display:block; font-weight:700; color:#9ca3af; }}
  .ep-label .ep-name {{ display:block; font-size:9px; color:#6b7280; font-style:italic; margin-top:2px; max-width:160px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
  .q-text {{ font-size:14px; line-height:1.65; color:#c4cad6; }}
  .q-text::before {{ content:"\u201C"; color:#4b5563; font-size:20px; line-height:0; vertical-align:-4px; margin-right:1px; }}
  .q-text::after  {{ content:"\u201D"; color:#4b5563; font-size:20px; line-height:0; vertical-align:-4px; margin-left:1px; }}
  .card-footer {{ display:flex; align-items:center; justify-content:flex-end; border-top:1px solid var(--border); padding-top:10px; gap:8px; }}
  .share-btn, .play-btn {{
    flex-shrink:0; padding:4px 10px; background:transparent; border:1px solid #252535;
    border-radius:2px; font-family:'Inter',sans-serif;
    font-size:9px; font-weight:600; letter-spacing:2px; text-transform:uppercase;
    cursor:pointer; transition:all .2s;
  }}
  .share-btn {{ color:#4b5563; }}
  .play-btn  {{ color:#374151; }}
  .share-btn:hover {{ border-color:#6b7280; color:#9ca3af; background:rgba(107,114,128,.07); }}
  .share-btn.copied {{ border-color:#4ade80; color:#4ade80; background:rgba(74,222,128,.07); }}
  .play-btn:hover   {{ border-color:#a78bfa; color:#a78bfa; background:rgba(167,139,250,.07); }}
  .play-btn.playing {{ border-color:#4ade80; color:#4ade80; background:rgba(74,222,128,.07); }}

  .myke     {{ color:var(--myke);    }} .myke .spk-pip     {{ background:var(--myke);    }}
  .federico {{ color:var(--fed);     }} .federico .spk-pip {{ background:var(--fed);     }}
  .stephen  {{ color:var(--stephen); }} .stephen .spk-pip  {{ background:var(--stephen); }}
  .unknown  {{ color:var(--unk);     }} .unknown .spk-pip  {{ background:var(--unk);     }}

  .site-footer {{ text-align:center; padding:60px 32px; font-size:10px; letter-spacing:3px; text-transform:uppercase; color:#2d2d40; }}
</style>
</head>
<body>

<div id="intro">
  <div class="relay-label">Relay &middot; Connected &middot; Est. 2014</div>
  <div class="big-600">600</div>
  <div class="show-name">Connected</div>
  <div class="clip-show-tag">Everyone Needs a Hobby</div>
  <div class="hosts-row">
    <div class="host-chip"><span class="host-pip" style="background:var(--myke)"></span>Myke</div>
    <div class="host-chip"><span class="host-pip" style="background:var(--fed)"></span>Federico</div>
    <div class="host-chip"><span class="host-pip" style="background:var(--stephen)"></span>Stephen</div>
  </div>
  <button class="start-btn" onclick="boot()">&#9654;&ensp;Play Clip Show</button>
</div>

<div id="montage">
  <div class="m-card">
    <div class="m-meta"    id="mm"></div>
    <div class="m-quote"   id="mq"></div>
    <div class="m-speaker" id="ms"></div>
    <div class="m-audio"   id="ma"></div>
  </div>
  <button class="m-close" onclick="closeMontage()">ESC &middot; Close</button>
  <div class="m-counter" id="mcounter"></div>
  <div class="m-nav-hint" id="mnavhint">
    <div class="m-nav-arrow">&larr;</div>
    <span style="font-size:9px;letter-spacing:3px;text-transform:uppercase;color:#374151;font-family:'Inter',sans-serif">tap or swipe</span>
    <div class="m-nav-arrow">&rarr;</div>
  </div>
</div>

<div id="main">
  <div class="topbar">
    <div class="topbar-title"><em>Everyone Needs a Hobby</em> &middot; Connected 600</div>
    <div class="btn-row">
      <button class="tbtn" onclick="launchMontage()">&#9889; Flash Mode</button>
      <button class="tbtn" id="shuf-btn" onclick="toggleShuffle()">Shuffle</button>
    </div>
  </div>
  <div id="body"></div>
  <div class="site-footer">Connected &middot; Relay &middot; {total} clips &middot; {with_audio} with audio</div>
</div>

<script>
const CLIPS = {clips_json};

const COLORS = {{ Myke:"#a78bfa", Federico:"#fbbf24", Stephen:"#60a5fa", Unknown:"#9ca3af" }};
function cls(s) {{ return (s||"unknown").toLowerCase(); }}
function col(s) {{ return COLORS[s] || COLORS.Unknown; }}

let activeAudio = null, activeBtn = null;

function playClip(file, btn) {{
  if (activeAudio) {{
    activeAudio.pause();
    if (activeBtn) {{ activeBtn.classList.remove("playing"); activeBtn.textContent = "\u25b6 play"; }}
    if (activeBtn === btn) {{ activeAudio = null; activeBtn = null; return; }}
  }}
  const a = new Audio("audio/" + file);
  a.play();
  btn.classList.add("playing"); btn.textContent = "\u25a0 stop";
  activeAudio = a; activeBtn = btn;
  a.onended = () => {{ btn.classList.remove("playing"); btn.textContent = "\u25b6 play"; activeAudio = null; activeBtn = null; }};
}}

function shareClip(text, speaker, ep, title, btn) {{
  const out = `\u201C${{text}}\u201D\\n\\u2014 ${{speaker}}, Connected Ep ${{ep}}: ${{title}}`;
  navigator.clipboard.writeText(out).then(() => {{
    btn.textContent = "\u2713 copied";
    btn.classList.add("copied");
    setTimeout(() => {{ btn.textContent = "share"; btn.classList.remove("copied"); }}, 1800);
  }});
}}

function boot() {{
  document.getElementById("intro").classList.add("gone");
  setTimeout(() => {{
    document.getElementById("intro").style.display = "none";
    document.getElementById("main").classList.add("show");
    render(CLIPS);
  }}, 800);
}}

let isShuffled = false;
function render(list) {{
  const body = document.getElementById("body");
  body.innerHTML = "";
  body.insertAdjacentHTML("beforeend",
    `<div class="section-hdr">
       <div class="section-label">From the Archives</div>
       <div class="section-count">${{list.length}} clips</div>
       <div class="section-hr"></div>
     </div>`);
  const grid = document.createElement("div");
  grid.className = "grid";
  list.forEach((c, i) => grid.insertAdjacentHTML("beforeend", buildCard(c, c.pinned === true)));
  body.appendChild(grid);
}}

function buildCard(c, opener) {{
  const epNum  = "EP." + String(c.episode).padStart(3, "0");
  const safeText    = c.text.replace(/'/g, "\\'").replace(/"/g, '&quot;');
  const safeSpeaker = (c.speaker||"").replace(/'/g, "\\'");
  const safeTitle   = c.title.replace(/'/g, "\\'");
  const audioBtn = c.audio_file
    ? `<button class="play-btn" onclick="playClip('${{c.audio_file}}',this)">\u25b6 play</button>`
    : "";
  return `<div class="card ${{opener ? "opener" : ""}}">
    <div class="card-top">
      <div class="spk-badge ${{cls(c.speaker)}}"><span class="spk-pip"></span>${{c.speaker}}</div>
      <div class="ep-label">
        <span class="ep-num">${{epNum}}</span>
        <span class="ep-name">${{c.title}}</span>
      </div>
    </div>
    <div class="q-text">${{c.text}}</div>
    <div class="card-footer">
      ${{audioBtn}}
    </div>
  </div>`;
}}

function toggleShuffle() {{
  isShuffled = !isShuffled;
  document.getElementById("shuf-btn").classList.toggle("on", isShuffled);
  render(isShuffled ? [...CLIPS].sort(() => Math.random() - .5) : CLIPS);
}}

// ── Flash montage ────────────────────────────────────────────────────────────
let mIdx = 0, mOrder = [], mActive = false;

function launchMontage() {{
  mOrder = [...CLIPS].sort(() => Math.random() - .5);
  mIdx = 0; mActive = true;
  if (activeAudio) {{ activeAudio.pause(); activeAudio = null; }}
  document.getElementById("montage").classList.add("on");
  // Show nav hint briefly then fade
  const hint = document.getElementById("mnavhint");
  hint.classList.add("show");
  setTimeout(() => hint.classList.remove("show"), 2800);
  showSlide();
}}

function showSlide() {{
  if (mIdx >= mOrder.length) {{ closeMontage(); return; }}
  const c = mOrder[mIdx];
  const color = col(c.speaker);
  ["mq","ms","mm","ma"].forEach(id => document.getElementById(id).classList.remove("show"));

  setTimeout(() => {{
    document.getElementById("mq").textContent = "\u201C" + c.text + "\u201D";
    document.getElementById("mq").style.color = color;
    document.getElementById("ms").textContent = c.speaker;
    document.getElementById("ms").style.color = color;
    document.getElementById("mm").textContent = "EP." + String(c.episode).padStart(3,"0") + " \u00b7 " + c.title;
    document.getElementById("mcounter").textContent = (mIdx + 1) + " / " + mOrder.length;

    // Richer background glow: two ellipses for depth
    document.getElementById("montage").style.background =
      `radial-gradient(ellipse at 50% 45%, ${{color}}30 0%, ${{color}}08 40%, transparent 68%),
       radial-gradient(ellipse at 50% 80%, ${{color}}18 0%, transparent 55%),
       #0a0a0f`;

    const ma = document.getElementById("ma");
    if (c.audio_file) {{
      ma.innerHTML = `<audio controls src="audio/${{c.audio_file}}" preload="none"></audio>`;
      ma.classList.add("show");
    }} else {{
      ma.innerHTML = "";
    }}
    ["mq","ms","mm"].forEach(id => document.getElementById(id).classList.add("show"));
  }}, 130);
}}

function closeMontage() {{
  mActive = false;
  document.getElementById("montage").classList.remove("on");
  document.getElementById("ma").innerHTML = "";
  document.getElementById("montage").style.background = "";
}}

// Keyboard navigation
document.addEventListener("keydown", e => {{
  if (!mActive) return;
  if (e.code === "Escape")     closeMontage();
  if (e.code === "ArrowRight" || e.code === "Space") {{ e.preventDefault(); mIdx++; showSlide(); }}
  if (e.code === "ArrowLeft")  {{ mIdx = Math.max(0, mIdx - 1); showSlide(); }}
}});

// Click to advance (but not on buttons or audio controls)
document.getElementById("montage").addEventListener("click", e => {{
  if (e.target.tagName === "BUTTON" || e.target.tagName === "AUDIO" ||
      e.target.closest("audio") || e.target.closest(".m-audio")) return;
  mIdx++; showSlide();
}});

// Touch swipe for mobile
(function() {{
  let tx = 0;
  const el = document.getElementById("montage");
  el.addEventListener("touchstart", e => {{ tx = e.touches[0].clientX; }}, {{passive:true}});
  el.addEventListener("touchend", e => {{
    if (!mActive) return;
    const dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) < 40) return; // not a real swipe
    if (dx < 0) {{ mIdx++; showSlide(); }}          // swipe left → next
    else        {{ mIdx = Math.max(0, mIdx - 1); showSlide(); }} // swipe right → prev
  }}, {{passive:true}});
}})();
</script>
</body>
</html>"""

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
