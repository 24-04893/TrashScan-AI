# TrashScan AI — streamlit run app.py

import os
import base64
from PIL import Image
import streamlit as st

# -- Page config
st.set_page_config(
    page_title="TrashScan AI",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_svg_icon(name: str) -> str:
    icon_path = os.path.join("icons", f"{name}.svg")
    if os.path.exists(icon_path):
        try:
            with open(icon_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/svg+xml;base64,{b64}"
        except Exception:
            pass
    return ""


if "started" not in st.session_state:
    st.session_state.started = False
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Classify"


if "nav" in st.query_params:
    st.session_state.active_nav = st.query_params["nav"]
    st.session_state.started = True

# -- Constants
ROBOFLOW_API_KEY  = "1qB6xK1hk8xhbOZ22H0F"
ROBOFLOW_MODEL_ID = "trashscan-4fiie/1"
CATEGORIES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# -- Disposal Knowledge Base
DISPOSAL_INFO = {
    "cardboard": {
        "recyclable": True,
        "accent": "#16a34a",
        "light": "#dcfce7",
        "bin": "Blue Recycling Bin",
        "bin_color": "#1d4ed8",
        "instructions": [
            "Flatten all boxes completely to save space",
            "Remove tape, labels, and stickers",
            "Remove plastic inserts, bubble wrap, or Styrofoam",
            "Keep cardboard DRY — wet cardboard cannot be recycled",
            "Do NOT recycle greasy pizza boxes — tear off clean parts only",
            "Break down large boxes into pieces (max 3 feet)",
        ],
        "env_tip": "Recycling 1 ton of cardboard saves 17 trees and 7,000 gallons of water!",
        "stat": "80% recyclable",
    },
    "glass": {
        "recyclable": True,
        "accent": "#059669",
        "light": "#d1fae5",
        "bin": "Green or Separate Glass Bin",
        "bin_color": "#15803d",
        "instructions": [
            "Empty all contents completely",
            "Rinse thoroughly with water until clean",
            "Remove metal caps, lids, and corks",
            "Do NOT break glass bottles or jars",
            "Remove any plastic sleeves or shrink wrap",
            "Do NOT recycle: window glass, mirrors, light bulbs, ceramics",
        ],
        "env_tip": "Glass is 100% infinitely recyclable. A recycled bottle becomes a new bottle in 30 days!",
        "stat": "100% recyclable",
    },
    "metal": {
        "recyclable": True,
        "accent": "#0284c7",
        "light": "#e0f2fe",
        "bin": "Blue Recycling Bin",
        "bin_color": "#0284c7",
        "instructions": [
            "Empty all contents completely",
            "Rinse thoroughly to remove food residue",
            "Crush cans if possible to save space",
            "Remove paper labels (recycle separately)",
            "Do NOT flatten aerosol cans — ensure completely empty first",
            "Remove plastic lids from metal cans",
        ],
        "env_tip": "Recycling aluminum uses 95% less energy than making new aluminum!",
        "stat": "95% energy saved",
    },
    "paper": {
        "recyclable": True,
        "accent": "#d97706",
        "light": "#fef3c7",
        "bin": "Blue or Dedicated Paper Bin",
        "bin_color": "#92400e",
        "instructions": [
            "Keep paper DRY — wet paper cannot be recycled",
            "Remove plastic windows from envelopes",
            "Remove tape, stickers, and adhesive labels",
            "Do NOT shred paper unless necessary",
            "Do NOT recycle: paper towels, napkins, tissues, receipts, waxed paper",
        ],
        "env_tip": "Recycling 1 ton of paper saves 17 trees and 7,000 gallons of water!",
        "stat": "70% is recyclable",
    },
    "plastic": {
        "recyclable": False,
        "accent": "#7c3aed",
        "light": "#ede9fe",
        "bin": "Blue Bin (Check Local Rules)",
        "bin_color": "#7c3aed",
        "instructions": [
            "Check resin number: #1 and #2 are recyclable, #3-7 are TRASH",
            "Empty all contents completely",
            "Rinse thoroughly — no food or liquid residue",
            "Crush bottles to save space",
            "Replace caps (screw back on before recycling)",
            "Remove pumps and sprayers (put in trash)",
            "Do NOT recycle plastic bags (store drop-off only), styrofoam, utensils",
        ],
        "env_tip": "Only 9% of all plastic ever produced has been recycled. Clean and sort correctly!",
        "stat": "9% recycled globally",
    },
    "trash": {
        "recyclable": False,
        "accent": "#64748b",
        "light": "#f1f5f9",
        "bin": "Black or Gray — General Waste",
        "bin_color": "#475569",
        "instructions": [
            "Double-bag wet, smelly, or sharp items",
            "Tie garbage bags securely to prevent spillage",
            "Do NOT put recyclables in the trash",
            "Never put hazardous waste in regular trash (batteries, chemicals, paint, electronics)",
            "Remove food scraps if composting is available",
            "Wrap broken glass in newspaper before disposal",
        ],
        "env_tip": "The average person throws away 4.5 pounds of trash per day. Reduce, reuse, recycle!",
        "stat": "Minimize waste",
    },
}

# -- Global CSS
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');


:root {
  --g900: #052e16;
  --g800: #14532d;
  --g700: #15803d;
  --g600: #16a34a;
  --g500: #22c55e;
  --g400: #4ade80;
  --g300: #86efac;
  --g200: #bbf7d0;
  --g100: #dcfce7;
  --g50:  #f0fdf4;
  --white: #ffffff;
  --slate50:  #f8fafc;
  --slate100: #f1f5f9;
  --slate200: #e2e8f0;
  --slate300: #cbd5e1;
  --slate400: #94a3b8;
  --slate600: #475569;
  --slate700: #334155;
  --slate900: #0f172a;
  --r-xl: 20px;
  --r-lg: 14px;
  --r-md: 10px;
  --r-sm: 7px;
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.10), 0 4px 8px rgba(0,0,0,0.06);
  --shadow-green: 0 4px 24px rgba(22,163,74,0.22);
  --transition: 0.22s cubic-bezier(0.4,0,0.2,1);
}


*, *::before, *::after { box-sizing: border-box; }
html, body {
  background: var(--g50) !important;
  color: var(--slate900) !important;
  font-family: 'Inter', sans-serif !important;
  -webkit-font-smoothing: antialiased;
}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background: var(--g50) !important;
}
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
.st-emotion-cache-1cypcdb { display: none !important; }


.block-container {
  padding-top: 2rem !important;
  padding-bottom: 2rem !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
  max-width: 100% !important;
}

h1,h2,h3,h4,h5,h6 {
  font-family: 'Inter', sans-serif !important;
  color: var(--slate900) !important;
}


[data-testid="stSidebar"] {
  background: var(--g900) !important;
  border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: var(--g200) !important; }
[data-testid="stSidebar"] .stMarkdown p { color: var(--g300) !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }


.sb-brand {
  background: linear-gradient(135deg, var(--g800), var(--g700));
  margin: -2rem -1.5rem 1.4rem !important;
  padding: 2.2rem 1.5rem 1.5rem !important;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
@keyframes floatIcon {
  0%,100% { transform: translateY(0) rotate(0deg); }
  50%      { transform: translateY(-5px) rotate(8deg); }
}
.sb-brand-title {
  font-size: 1.2rem; font-weight: 800;
  color: #ffffff !important; letter-spacing: -0.3px; line-height: 1.1;
}
.sb-brand-sub {
  font-size: 0.72rem; color: var(--g300) !important;
  text-transform: uppercase; letter-spacing: 1.5px; margin-top: 0.2rem;
}


.sb-nav-btn {
  display: flex; align-items: center; gap: 0.7rem;
  padding: 0.65rem 1rem;
  border-radius: var(--r-md);
  cursor: pointer;
  transition: background var(--transition);
  font-size: 0.88rem; font-weight: 500;
  color: var(--g300) !important;
  margin-bottom: 0.2rem;
  text-decoration: none;
}
.sb-nav-btn:hover { background: rgba(255,255,255,0.07); color: #fff !important; }
.sb-nav-btn.active { background: rgba(34,197,94,0.18); color: #fff !important; border-left: 3px solid var(--g500); }
.sb-nav-btn .nav-icon { font-size: 1.05rem; }
.sb-section-title {
  font-size: 0.62rem; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--g400) !important;
  margin: 1rem 0 0.4rem; padding: 0 0.3rem;
}


.sb-status {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.3rem 0.8rem; border-radius: 999px;
  font-size: 0.72rem; font-weight: 600;
  border: 1px solid; margin-top: 0.3rem;
}
.sb-status.ok   { background: rgba(34,197,94,0.12); border-color: rgba(34,197,94,0.3); color: var(--g400) !important; }
.sb-status.err  { background: rgba(239,68,68,0.12);  border-color: rgba(239,68,68,0.3);  color: #fca5a5 !important; }
.sb-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.sb-dot.ok  { background: var(--g500); box-shadow: 0 0 6px var(--g500); }
.sb-dot.err { background: #ef4444; }


.sb-cat {
  display: flex; align-items: center; gap: 0.55rem;
  padding: 0.38rem 0.6rem; border-radius: var(--r-sm);
  font-size: 0.8rem; color: var(--g200) !important;
  transition: background var(--transition);
}
.sb-cat:hover { background: rgba(255,255,255,0.06); }
.sb-cat-badge {
  font-size: 0.6rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.5px; padding: 0.1rem 0.4rem;
  border-radius: 999px; margin-left: auto;
}
.sb-cat-badge.yes { background: rgba(34,197,94,0.15); color: var(--g400) !important; border: 1px solid rgba(34,197,94,0.25); }
.sb-cat-badge.no  { background: rgba(148,163,184,0.12); color: var(--slate400) !important; border: 1px solid rgba(148,163,184,0.2); }


.topnav {
  background: var(--white);
  border: 1px solid var(--slate200);
  border-radius: 24px !important;
  padding: 0 3rem;
  height: 1.5in;
  display: flex; align-items: center; gap: 1rem;
  box-shadow: var(--shadow-md);
  position: relative;
  margin-bottom: 2.2rem;
  overflow: hidden;
}
.topnav::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--g700), var(--g500), var(--g300));
  z-index: 10;
}
.topnav-logo { font-size: 2.2rem; }
.topnav-title {
  font-size: 1.7rem; font-weight: 900; letter-spacing: -0.5px;
  color: var(--g800) !important;
}
.topnav-title span { color: var(--g500) !important; }
.topnav-sep { flex: 1; }
.topnav-badge {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: var(--g50); border: 1px solid var(--g200);
  color: var(--g700) !important;
  padding: 0.45rem 1.2rem; border-radius: 999px;
  font-size: 0.85rem; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;
}
.topnav-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--g500); box-shadow: 0 0 5px var(--g500);
  animation: pulse-dot 2s ease infinite;
}
@keyframes pulse-dot {
  0%,100% { opacity: 1; transform: scale(1); }
  50%      { opacity: 0.5; transform: scale(0.7); }
}


.sec-label {
  font-size: 0.62rem; font-weight: 700;
  letter-spacing: 2px; text-transform: uppercase;
  color: var(--g700) !important;
  margin-bottom: 0.75rem; margin-top: 0.1rem;
  display: flex; align-items: center; gap: 0.45rem;
}
.sec-label::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--g200), transparent);
}


.card {
  background: var(--white);
  border: 1px solid var(--slate200);
  border-radius: var(--r-xl);
  padding: 1.4rem 1.5rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition);
}
.card:hover { box-shadow: var(--shadow-md); }


.result-card {
  border-radius: var(--r-xl);
  padding: 1.8rem;
  margin-bottom: 1rem;
  border: 1.5px solid;
  position: relative; overflow: hidden;
  animation: slideUp 0.45s cubic-bezier(0.22,1,0.36,1);
  box-shadow: var(--shadow-md);
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
.result-card::after {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at top right, rgba(255,255,255,0.5), transparent 60%);
  pointer-events: none;
}


.s-pill {
  display: inline-flex; align-items: center; gap: 0.3rem;
  padding: 0.22rem 0.8rem; border-radius: 999px;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  margin-bottom: 0.5rem;
}
.s-pill.recycle { background: rgba(22,163,74,0.12); border: 1px solid rgba(22,163,74,0.35); color: var(--g700) !important; }
.s-pill.caution { background: rgba(217,119,6,0.12);  border: 1px solid rgba(217,119,6,0.35);  color: #92400e !important; }
.s-pill.trash   { background: rgba(100,116,139,0.1); border: 1px solid rgba(100,116,139,0.25); color: var(--slate600) !important; }


.conf-row  { display: flex; align-items: baseline; gap: 0.45rem; margin-top: 0.1rem; }
.conf-pct  { font-size: 1.15rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
.conf-lbl  { font-size: 0.78rem; color: rgba(0,0,0,0.38) !important; }
.conf-track {
  background: rgba(0,0,0,0.07); border-radius: 999px;
  height: 7px; margin: 0.7rem 0 0; overflow: hidden;
}
.conf-fill {
  height: 7px; border-radius: 999px;
  animation: barGrow 0.8s cubic-bezier(0.22,1,0.36,1) 0.25s both;
  transform-origin: left;
}
@keyframes barGrow {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}


.instr {
  background: var(--g50);
  border: 1px solid var(--g100);
  border-left: 3px solid var(--g500);
  border-radius: var(--r-md);
  padding: 0.55rem 0.9rem;
  margin-bottom: 0.38rem;
  font-size: 0.86rem; color: var(--slate700) !important;
  transition: all var(--transition);
  animation: fadeInLeft 0.3s ease both;
}
.instr:hover { background: var(--g100); transform: translateX(2px); }
@keyframes fadeInLeft {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}
.instr:nth-child(1) { animation-delay: 0.05s; }
.instr:nth-child(2) { animation-delay: 0.10s; }
.instr:nth-child(3) { animation-delay: 0.15s; }
.instr:nth-child(4) { animation-delay: 0.20s; }
.instr:nth-child(5) { animation-delay: 0.25s; }
.instr:nth-child(6) { animation-delay: 0.30s; }
.instr:nth-child(7) { animation-delay: 0.35s; }


.bin-badge {
  display: inline-flex; align-items: center; gap: 0.55rem;
  background: var(--white); border: 1px solid var(--slate200);
  border-radius: var(--r-md); padding: 0.42rem 0.9rem;
  font-size: 0.84rem; font-weight: 600; color: var(--slate700) !important;
  box-shadow: var(--shadow-xs); margin: 0.55rem 0;
}
.bin-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }


.eco-tip {
  background: linear-gradient(135deg, var(--g50), var(--g100));
  border: 1px solid var(--g200); border-left: 4px solid var(--g500);
  border-radius: var(--r-md); padding: 0.75rem 1rem;
  font-size: 0.84rem; color: var(--g800) !important; line-height: 1.55;
  margin: 0.65rem 0;
}


.score-cell {
  background: var(--white);
  border: 1.5px solid var(--slate200);
  border-radius: var(--r-lg); padding: 0.8rem 0.3rem;
  text-align: center; box-shadow: var(--shadow-xs);
  transition: all var(--transition);
}
.score-cell.top {
  background: var(--g50); border-color: var(--g500);
  box-shadow: 0 0 0 3px rgba(34,197,94,0.14), var(--shadow-sm);
  transform: translateY(-2px);
}
.score-name {
  font-size: 0.56rem; color: var(--slate400) !important;
  text-transform: uppercase; letter-spacing: 0.4px;
  margin: 0.2rem 0; display: block;
  font-family: 'JetBrains Mono', monospace;
}
.score-pct {
  font-size: 0.82rem; font-weight: 700;
  color: var(--slate400) !important; display: block;
  font-family: 'JetBrains Mono', monospace;
}
.score-pct.top { color: var(--g700) !important; }


.chips {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
  margin-top: 0.5rem;
}
.chip {
  background: var(--g100); border: 1px solid var(--g200);
  color: var(--g800) !important;
  padding: 0.4rem 0.5rem; border-radius: 999px;
  font-size: 0.72rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
  font-family: 'JetBrains Mono', monospace;
  transition: all var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.chip:hover { background: var(--g200); transform: translateY(-1px); }


.waiting-box {
  background: var(--white); border: 2px dashed var(--slate200);
  border-radius: var(--r-xl); padding: 4rem 2rem;
  text-align: center; box-shadow: var(--shadow-xs);
}
.waiting-icon {
  display: flex; justify-content: center;
  margin-bottom: 1rem;
}
@keyframes float {
  0%,100% { transform: translateY(0); }
  50%      { transform: translateY(-10px); }
}
.waiting-icon img { animation: float 3s ease-in-out infinite; }
.waiting-title { font-size: 1.05rem; font-weight: 600; color: var(--slate400) !important; margin: 0 0 0.35rem; }
.waiting-sub   { font-size: 0.83rem; color: var(--slate300) !important; }


.err-card {
  background: #fff1f2; border: 1px solid #fecdd3;
  border-radius: var(--r-xl); padding: 1.6rem 1.8rem;
}
.err-card h3 { color: #be123c !important; margin-top: 0; }
.err-card p  { color: var(--slate600) !important; }
.err-card code {
  background: var(--slate100); padding: 0.1rem 0.4rem;
  border-radius: 4px; font-family: 'JetBrains Mono', monospace;
  color: #1d4ed8 !important; font-size: 0.83rem;
}
.err-card pre {
  background: var(--slate900); color: var(--g400) !important;
  padding: 1rem; border-radius: var(--r-md);
  font-family: 'JetBrains Mono', monospace; font-size: 0.82rem;
}


.stRadio label, .stRadio span { color: var(--slate700) !important; }
.stFileUploader label { color: var(--slate700) !important; }
.stFileUploader span  { color: var(--slate400) !important; }
details summary { color: var(--slate700) !important; }
div[data-testid="stMarkdownContainer"] p { color: var(--slate700) !important; }
[data-testid="stCameraInput"] label { color: var(--slate700) !important; }
.streamlit-expanderHeader { color: var(--g700) !important; }


::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--g200); border-radius: 3px; }


[data-testid="stToastContainer"] {
  position: fixed !important;
  bottom: 1.5rem !important;
  right: 1.5rem !important;
  top: auto !important;
  left: auto !important;
  z-index: 999999 !important;
}
[data-testid="stToast"] {
  background: rgba(220, 252, 231, 0.70) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border: 1px solid rgba(34, 197, 94, 0.35) !important;
  border-radius: 14px !important;
  box-shadow: 0 4px 24px rgba(22, 163, 74, 0.18) !important;
}
[data-testid="stToast"] * {
  color: var(--g800) !important;
  font-family: 'Inter', sans-serif !important;
}


button[kind="primary"] {
  background: linear-gradient(135deg, var(--g600), var(--g700)) !important;
  border: none !important;
  box-shadow: 0 4px 15px rgba(22,163,74,0.3) !important;
  font-weight: 700 !important; border-radius: 10px !important;
  transition: all var(--transition) !important;
}
button[kind="primary"]:hover {
  background: linear-gradient(135deg, var(--g500), var(--g600)) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(22,163,74,0.4) !important;
}
button[kind="secondary"] {
  border: 1.5px solid var(--g600) !important;
  color: var(--g700) !important;
  background: transparent !important;
  font-weight: 700 !important; border-radius: 10px !important;
  transition: all var(--transition) !important;
}
button[kind="secondary"]:hover {
  background: var(--g50) !important;
  transform: translateY(-1px) !important;
}
[data-testid="stSidebar"] button[kind="secondary"] {
  color: #ffffff !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
  background: transparent !important;
}
[data-testid="stSidebar"] button[kind="secondary"] p,
[data-testid="stSidebar"] button[kind="secondary"] span,
[data-testid="stSidebar"] button[kind="secondary"] * {
  color: #ffffff !important;
}
[data-testid="stSidebar"] button[kind="secondary"]:hover {
  background: rgba(255, 255, 255, 0.08) !important;
  border-color: rgba(255, 255, 255, 0.5) !important;
  transform: translateY(-1px) !important;
}


[data-testid="stDialog"],
[data-testid="stDialog"] > div,
[data-testid="stDialog"] > div > div,
div[role="dialog"],
div[role="dialog"] > div {
  background: #ffffff !important;
  background-color: #ffffff !important;
}
[data-testid="stDialog"] > div,
div[role="dialog"] > div {
  border-radius: 28px !important;
  overflow: hidden !important;
}
[data-testid="stDialog"] > div > div {
  background:
    radial-gradient(ellipse at top right, rgba(34,197,94,0.18) 0%, transparent 55%),
    radial-gradient(ellipse at bottom left, rgba(74,222,128,0.14) 0%, transparent 50%),
    #ffffff !important;
  border-radius: 28px !important;
  overflow: hidden !important;
  border: 2px solid rgba(22,163,74,0.55) !important;
  box-shadow:
    0 8px 40px rgba(22,163,74,0.18),
    0 2px 8px rgba(0,0,0,0.08) !important;
}
[data-testid="stDialog"] h1,
[data-testid="stDialog"] h2,
[data-testid="stDialog"] h3,
[data-testid="stDialog"] h4,
[data-testid="stDialog"] p,
[data-testid="stDialog"] li,
[data-testid="stDialog"] span,
[data-testid="stDialog"] strong,
[data-testid="stDialog"] label,
[data-testid="stDialog"] * {
  color: var(--g800) !important;
}
[data-testid="stDialog"] [data-testid="stCaptionContainer"] p {
  color: var(--g700) !important;
  opacity: 0.75;
}
[data-testid="stDialog"] hr {
  border-color: rgba(34,197,94,0.25) !important;
}

[data-testid="stModal"] {
  background: rgba(240,253,244,0.6) !important;
  backdrop-filter: blur(8px) !important;
}
</style>
"""

# -- Start Page CSS
START_CSS = """
<style>

body, .stApp { background: var(--g50) !important; }

section[data-testid="stMain"] {
  transform: none !important;
  -webkit-transform: none !important;
  will-change: auto !important;
}
[data-testid="stMain"] > div:first-child {
  transform: none !important;
}


[data-testid="stMain"] [data-testid="stButton"] {
  position: fixed !important;
  top: 1.2rem !important;
  right: 1.5rem !important;
  z-index: 99999 !important;
  width: auto !important;
  margin: 0 !important;
}
[data-testid="stMain"] [data-testid="stButton"] button {
  min-width: 0 !important;
  width: auto !important;
  padding: 0.38rem 1rem !important;
  font-size: 0.82rem !important;
  font-weight: 600 !important;
  border-radius: 8px !important;
  border: 1.5px solid rgba(21,128,61,0.35) !important;
  color: var(--g700) !important;
  background: rgba(240,253,244,0.85) !important;
  box-shadow: 0 2px 8px rgba(21,128,61,0.10);
  letter-spacing: 0.3px !important;
}
[data-testid="stMain"] [data-testid="stButton"] button:hover {
  background: var(--g100) !important;
  border-color: var(--g600) !important;
  color: var(--g800) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(21,128,61,0.18) !important;
}


.start-bg {
  position: fixed; inset: 0; pointer-events: none; overflow: hidden; z-index: 0;
}
.blob {
  position: absolute; border-radius: 50%;
  filter: blur(70px); opacity: 0.35;
  animation: blobPulse 8s ease-in-out infinite;
}
.blob-1 {
  width: 500px; height: 500px;
  background: radial-gradient(circle, #22c55e, #15803d);
  top: -150px; right: -150px;
  animation-delay: 0s;
}
.blob-2 {
  width: 400px; height: 400px;
  background: radial-gradient(circle, #4ade80, #052e16);
  bottom: -100px; left: -100px;
  animation-delay: -5s;
}
.blob-3 {
  width: 280px; height: 280px;
  background: radial-gradient(circle, #86efac 0%, #16a34a 60%);
  top: 45%; left: 50%;
  animation-delay: -2.5s;
}
@keyframes blobPulse {
  0%,100% { transform: scale(1); opacity: 0.25; }
  50%      { transform: scale(1.1); opacity: 0.45; }
}
.blob-3 { animation: blobPulse3 8s ease-in-out infinite; }
@keyframes blobPulse3 {
  0%,100% { opacity: 0.2; transform: translate(-50%,-50%) scale(1); }
  50%      { opacity: 0.4; transform: translate(-50%,-50%) scale(1.1); }
}


.start-card {
  position: relative; z-index: 1;
  background: rgba(255,255,255,0.88);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.92);
  border-radius: 24px;
  overflow: hidden;
  padding: 3rem 3rem 2.6rem;
  text-align: left;
  box-shadow: 0 8px 40px rgba(21,128,61,0.12), 0 2px 8px rgba(0,0,0,0.06);
  max-width: 520px; width: 100%;
  margin: 0 auto;
  animation: cardAppear 0.65s cubic-bezier(0.22,1,0.36,1);
}
@keyframes cardAppear {
  from { opacity: 0; transform: translateY(28px) scale(0.97); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.start-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, #15803d, #22c55e, #86efac, #22c55e);
  border-radius: 24px 24px 0 0;
  background-size: 200%; animation: shimmer 3s linear infinite;
}
@keyframes shimmer {
  0%   { background-position: 200% center; }
  100% { background-position: -200% center; }
}


.start-eyebrow {
  font-size: 0.62rem; font-weight: 700; letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--g600) !important;
  margin-bottom: 0.65rem;
  animation: fadeUp 0.5s ease 0.1s both;
  display: flex; align-items: center; gap: 0.5rem;
}
.start-eyebrow::before {
  content: '';
  width: 18px; height: 2px;
  background: var(--g600);
  border-radius: 1px;
  display: inline-block;
  flex-shrink: 0;
}


.start-title {
  font-size: 2.85rem; font-weight: 900;
  letter-spacing: -1.5px; line-height: 1.05;
  margin: 0 0 0.9rem;
  color: var(--slate900) !important;
  -webkit-text-fill-color: unset;
  animation: fadeUp 0.5s ease 0.2s both;
}
.start-title span {
  background: linear-gradient(135deg, #14532d 0%, #22c55e 60%, #86efac 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}


.start-sub {
  font-size: 0.95rem; color: var(--slate400) !important;
  max-width: 100%; margin: 0 0 2rem;
  line-height: 1.65;
  animation: fadeUp 0.5s ease 0.3s both;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}


.start-btn-link {
  display: block;
  width: fit-content;
  padding: 0.62rem 1.6rem;
  background: linear-gradient(135deg, #16a34a, #15803d);
  color: #ffffff !important;
  text-decoration: none !important;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 700;
  font-family: 'Inter', sans-serif;
  letter-spacing: 0.2px;
  box-shadow: 0 4px 20px rgba(22,163,74,0.30), 0 0 0 1px rgba(34,197,94,0.15);
  transition: all 0.22s cubic-bezier(0.4,0,0.2,1);
  margin-bottom: 2rem;
  animation: fadeUp 0.5s ease 0.4s both;
}
.start-btn-link:hover {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  box-shadow: 0 6px 28px rgba(34,197,94,0.40), 0 0 0 1px rgba(34,197,94,0.25);
  transform: translateY(-2px);
  color: #ffffff !important;
  text-decoration: none !important;
}


.start-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(34,197,94,0.2) 30%, rgba(34,197,94,0.2) 70%, transparent);
  margin-bottom: 1.6rem;
  animation: fadeUp 0.5s ease 0.45s both;
}


.stats-row {
  display: flex; gap: 0; justify-content: flex-start;
  animation: fadeUp 0.5s ease 0.5s both;
}
.stat-item {
  flex: 1; text-align: center;
  padding: 0 0.5rem;
}
.stat-item:not(:last-child) {
  border-right: 1px solid var(--g200);
}
.stat-item:first-child { padding-left: 0; text-align: left; }
.stat-num {
  font-size: 1.3rem; font-weight: 800; letter-spacing: -0.5px;
  color: var(--g700) !important; display: block; line-height: 1;
  font-family: 'JetBrains Mono', monospace;
}
.stat-lbl {
  font-size: 0.6rem; color: var(--slate400) !important;
  text-transform: uppercase; letter-spacing: 1.5px;
  margin-top: 0.25rem; display: block;
}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_model():
    if not ROBOFLOW_API_KEY or ROBOFLOW_API_KEY == "YOUR_API_KEY_HERE":
        return None
    from inference_sdk import InferenceHTTPClient
    client = InferenceHTTPClient(
        api_url="https://classify.roboflow.com",
        api_key=ROBOFLOW_API_KEY,
    )
    return client


# -- Inference -----------------------------------------------------------------
def predict(model, pil_image: Image.Image):
    import io, base64
    buf = io.BytesIO()
    pil_image.convert("RGB").save(buf, format="JPEG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    result = model.infer(b64, model_id=ROBOFLOW_MODEL_ID)
    preds  = {p["class"].lower(): p["confidence"] for p in result["predictions"]}
    probs  = [preds.get(cat, 0.0) for cat in CATEGORIES]
    max_val = max(probs)
    idx     = probs.index(max_val)
    return CATEGORIES[idx], float(max_val), probs


# -- Result renderer -----------------------------------------------------------
def render_result(label: str, confidence: float, all_probs: list):
    info    = DISPOSAL_INFO[label]
    bar_pct = f"{confidence * 100:.1f}%"

    if label == "plastic":
        pill_cls, pill_text = "caution", "Check Resin Number"
    elif info["recyclable"]:
        pill_cls, pill_text = "recycle", "Recyclable"
    else:
        pill_cls, pill_text = "trash",   "General Waste"

    st.markdown(f"""
    <div class="result-card" style="
        background: linear-gradient(135deg, {info['light']} 0%, #ffffff 70%);
        border-color: {info['accent']}44;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
    ">
        <div style="flex: 1; min-width: 0;">
            <div><span class="s-pill {pill_cls}">{pill_text}</span></div>
            <div style="font-size:2.4rem;font-weight:900;letter-spacing:-1px;
                        color:{info['accent']};line-height:1.05;margin-bottom:0.15rem;">
                {label.upper()}
            </div>
            <div class="conf-row">
                <span class="conf-pct" style="color:{info['accent']};">{bar_pct}</span>
                <span class="conf-lbl">confidence</span>
            </div>
            <div class="conf-track">
                <div class="conf-fill" style="width:{bar_pct};background:linear-gradient(90deg,{info['accent']},{info['accent']}bb);"></div>
            </div>
        </div>
        <div style="flex-shrink: 0; display: flex; align-items: center; justify-content: center;">
            <img src="{get_svg_icon(label)}" style="width: 8rem; height: 8rem; object-fit: contain;" />
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Disposal Instructions</div>', unsafe_allow_html=True)
    for item in info["instructions"]:
        st.markdown(f'<div class="instr">{item}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="bin-badge">
        <div class="bin-dot" style="background:{info['bin_color']};"></div>
        {info['bin']}
    </div>
    <div class="eco-tip">
        <strong>Eco Fact</strong> &nbsp;— {info['env_tip']}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label" style="margin-top:1.1rem;">All Category Scores</div>', unsafe_allow_html=True)
    cols = st.columns(len(CATEGORIES))
    for i, (cat, prob) in enumerate(zip(CATEGORIES, all_probs)):
        pct     = prob * 100
        is_top  = (cat == label)
        ci      = DISPOSAL_INFO[cat]
        top_cls = "top" if is_top else ""
        pct_col = ci["accent"] if is_top else "#94a3b8"
        bg      = ci["light"] if is_top else "#ffffff"
        border  = ci["accent"] if is_top else "#e2e8f0"
        with cols[i]:
            st.markdown(f"""
            <div class="score-cell {top_cls}" style="background:{bg};border-color:{border};">
                <div style="display:flex; justify-content:center; margin-bottom:0.25rem;">
                    <img src="{get_svg_icon(cat)}" style="width: 1.8rem; height: 1.8rem; object-fit: contain;" />
                </div>
                <span class="score-name">{cat}</span>
                <span class="score-pct {top_cls}" style="color:{pct_col};">{pct:.1f}%</span>
            </div>
            """, unsafe_allow_html=True)


# -- About Dialog --------------------------------------------------------------
@st.dialog("About TrashScan AI", width="large")
def show_about_dialog():
    st.markdown("""
    **TrashScan AI** is an intelligent waste management tool designed to bridge the gap between
    technology and environmental sustainability. By leveraging a custom-trained Convolutional Neural
    Network (CNN) hosted on Roboflow, the platform delivers real-time, accurate waste classification
    to encourage and promote proper recycling habits. Our mission is to eliminate sorting confusion,
    reduce landfill waste, and make eco-friendly disposal second nature for everyone.
    """)

    st.divider()
    st.markdown("#### Key Features")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**6 Distinct Classes**")
        st.caption("Optimized to detect and categorize Cardboard, Glass, Metal, Paper, Plastic, and general Trash.")
    with c2:
        st.markdown("**Roboflow API Integration**")
        st.caption("Powered by seamless cloud inference for instant image recognition and fast response times.")
    with c3:
        st.markdown("**Smart Disposal Insights**")
        st.caption("Goes beyond identification by providing actionable bin guidance and eco-facts for every scanned item.")

    st.divider()
    st.markdown("#### Development Team")
    st.markdown("This project was developed with care by:")
    team = [
        "Aguillera, Juan Miguel B.",
        "Andal, Rob Edmond N.",
        "Arandia, Jedrick O.",
        "Masangcay, Jun Lorenz C.",
    ]
    for member in team:
        st.markdown(f"- {member}")


# -- Start Page ----------------------------------------------------------------
def show_start_page():
    st.markdown(START_CSS, unsafe_allow_html=True)

    # Decorative background blobs
    st.markdown("""
    <div class="start-bg">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
    </div>
    """, unsafe_allow_html=True)

    # About button — fixed top-right corner
    if st.button("About", key="about_btn"):
        show_about_dialog()

    # Main centered card
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="start-card">
            <div class="start-eyebrow">AI-Powered Waste Recognition</div>
            <h1 class="start-title">TrashScan <span>AI</span></h1>
            <p class="start-sub">
                The smart way to throw things away.
            </p>
            <a href="?nav=Classify" target="_self" class="start-btn-link">Start Classifying</a>
        </div>
        """, unsafe_allow_html=True)


# -- Sidebar -------------------------------------------------------------------
def render_sidebar(model):
    with st.sidebar:
        st.markdown(f"""
        <div class="sb-brand">
            <div style="display:flex; justify-content:center; margin-bottom:0.5rem; animation: floatIcon 4s ease-in-out infinite;">
                <img src="{get_svg_icon('logo')}" style="width: 45px; height: 45px; object-fit: contain;" />
            </div>
            <div class="sb-brand-title">TrashScan AI</div>
            <div class="sb-brand-sub">Environmental Classifier</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        st.markdown('<div class="sb-section-title">Navigation</div>', unsafe_allow_html=True)
        nav_items = [
            ("classify", "Classify"),
            ("reference", "Reference"),
            ("stats", "Stats"),
        ]
        for icon_name, label in nav_items:
            active_cls = "active" if st.session_state.active_nav == label else ""
            icon_url = get_svg_icon(icon_name)
            st.markdown(f"""
            <a href="?nav={label}" target="_self" class="sb-nav-btn {active_cls}">
                <img src="{icon_url}" class="nav-icon" style="width: 20px; height: 20px; object-fit: contain; filter: brightness(0) invert(1);" />
                <span>{label}</span>
            </a>
            """, unsafe_allow_html=True)

        st.divider()

        # API status
        st.markdown('<div class="sb-section-title">API Status</div>', unsafe_allow_html=True)
        if model is not None:
            st.markdown("""
            <div class="sb-status ok">
                <div class="sb-dot ok"></div>
                Roboflow Connected
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sb-status err">
                <div class="sb-dot err"></div>
                API Key Required
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Back to home
        if st.button("Welcome Page", key="home_btn", use_container_width=True):
            st.query_params.clear()
            st.session_state.started = False
            st.rerun()


# -- Reference Page ------------------------------------------------------------
def render_reference():
    st.markdown('<div class="sec-label">Complete Disposal Reference Guide</div>', unsafe_allow_html=True)
    for cat in CATEGORIES:
        info = DISPOSAL_INFO[cat]
        instr_html = "".join([f'<div class="instr">{item}</div>' for item in info["instructions"]])
        st.markdown(f"""
        <div class="card" style="border-top: 3px solid {info['accent']}; margin-bottom: 1.5rem;">
            <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:1rem;">
                <img src="{get_svg_icon(cat)}" style="width: 2.5rem; height: 2.5rem; object-fit: contain;" />
                <div>
                    <h3 style="margin:0; font-size:1.25rem; color:{info['accent']}; font-weight:800;">{cat.title()}</h3>
                    <div style="font-size:0.8rem; color:#64748b;">{info['bin']}</div>
                </div>
            </div>
            <div>
                {instr_html}
            </div>
            <div class="eco-tip" style="margin-top:1rem; margin-bottom:0;">
                <strong>Eco Fact</strong> — {info['env_tip']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# -- Stats Overview Page -------------------------------------------------------
def render_stats():
    st.markdown('<div class="sec-label">Category Overview</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, cat in enumerate(CATEGORIES):
        info = DISPOSAL_INFO[cat]
        recyclable_label = "Recyclable" if info["recyclable"] else "General Waste"
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card" style="text-align:center; border-top: 3px solid {info['accent']};">
                <div style="display:flex; justify-content:center; margin-bottom:0.5rem;">
                    <img src="{get_svg_icon(cat)}" style="width: 3.5rem; height: 3.5rem; object-fit: contain;" />
                </div>
                <div style="font-weight:800;font-size:1.05rem;color:{info['accent']};margin:0.3rem 0;">
                    {cat.title()}
                </div>
                <div style="font-size:0.75rem;color:#64748b;margin-bottom:0.5rem;">
                    {recyclable_label}
                </div>
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.5px;
                            background:{info['light']};color:{info['accent']};
                            padding:0.2rem 0.6rem;border-radius:999px;display:inline-block;">
                    {info['stat']}
                </div>
            </div>
            """, unsafe_allow_html=True)


# -- Main App ------------------------------------------------------------------
def main():
    if not st.session_state.started:
        show_start_page()
        return

    # Show tips toast once
    if "tips_shown" not in st.session_state:
        st.session_state.tips_shown = True
        st.toast("Tips: plain background, good lighting, one item, fill the frame", icon=None)

    with st.spinner("Loading classifier ..."):
        model = load_model()

    render_sidebar(model)

    # -- Top navigation bar ---------------------------------------------------
    st.markdown(f"""
    <div class="topnav">
        <span class="topnav-logo" style="display:flex;align-items:center;margin-right:0.3rem;"><img src="{get_svg_icon('logo')}" style="width: 38px; height: 38px; object-fit: contain;" /></span>
        <span class="topnav-title">Trash<span>Scan</span> AI</span>
        <span class="topnav-sep"></span>
        <span class="topnav-badge">
            <span class="topnav-dot"></span>
            CNN · Roboflow
        </span>
    </div>
    """, unsafe_allow_html=True)

    nav = st.session_state.active_nav

    # -- Reference page -------------------------------------------------------
    if nav == "Reference":
        render_reference()
        return

    # -- Stats page -----------------------------------------------------------
    if nav == "Stats":
        render_stats()
        return

    # -- Classify page --------------------------------------------------------
    col_l, col_r = st.columns([1, 1.3], gap="large")

    with col_l:
        st.markdown('<div class="sec-label">Image Input</div>', unsafe_allow_html=True)

        mode = st.radio(
            "Input method",
            ["Camera", "Upload Image"],
            horizontal=True,
            label_visibility="collapsed",
        )

        captured = None
        if mode == "Camera":
            cam = st.camera_input("Point camera at the item and click Take Photo")
            if cam:
                captured = Image.open(cam)
        else:
            up = st.file_uploader(
                "Upload a photo of your waste item",
                type=["jpg", "jpeg", "png", "webp"],
            )
            if up:
                captured = Image.open(up)

        if captured is not None:
            st.image(captured, caption="Captured image", use_container_width=True)

        st.markdown(f"""
        <div class="card" style="margin-top:1rem;">
            <div class="sec-label">Detectable Materials</div>
            <div class="chips">
                <div class="chip"><img src="{get_svg_icon('cardboard')}" style="width:16px;height:16px;margin-right:6px;object-fit:contain;" />Cardboard</div>
                <div class="chip"><img src="{get_svg_icon('glass')}" style="width:16px;height:16px;margin-right:6px;object-fit:contain;" />Glass</div>
                <div class="chip"><img src="{get_svg_icon('metal')}" style="width:16px;height:16px;margin-right:6px;object-fit:contain;" />Metal</div>
                <div class="chip"><img src="{get_svg_icon('paper')}" style="width:16px;height:16px;margin-right:6px;object-fit:contain;" />Paper</div>
                <div class="chip"><img src="{get_svg_icon('plastic')}" style="width:16px;height:16px;margin-right:6px;object-fit:contain;" />Plastic</div>
                <div class="chip"><img src="{get_svg_icon('trash')}" style="width:16px;height:16px;margin-right:6px;object-fit:contain;" />Trash</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="sec-label">Classification Result</div>', unsafe_allow_html=True)

        if model is None:
            st.markdown("""
            <div class="err-card">
                <h3>Roboflow API Key Required</h3>
                <p>Configure your <code>ROBOFLOW_API_KEY</code> in <code>app.py</code>
                   to connect to the Roboflow inference API.</p>
                <pre>ROBOFLOW_API_KEY = "YOUR_API_KEY_HERE"</pre>
            </div>
            """, unsafe_allow_html=True)

        elif captured is None:
            st.markdown(f"""
            <div class="waiting-box">
                <div class="waiting-icon">
                    <img src="{get_svg_icon('classify')}" style="width:3.8rem;height:3.8rem;object-fit:contain;opacity:0.4;" />
                </div>
                <div class="waiting-title">Awaiting image...</div>
                <div class="waiting-sub">Capture or upload a photo to classify your waste item</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            try:
                with st.spinner("Classifying ..."):
                    label, confidence, all_probs = predict(model, captured)
                render_result(label, confidence, all_probs)
            except Exception as e:
                st.markdown(f"""
                <div class="err-card">
                    <h3>Classification Error</h3>
                    <p>An error occurred while communicating with the Roboflow API:</p>
                    <pre>{e}</pre>
                    <p>Check your network connection, API key, and model ID.</p>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
