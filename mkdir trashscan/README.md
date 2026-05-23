# TrashScan AI

> **The smart way to throw things away.**

TrashScan AI is an intelligent, browser-based waste classification application built with Python and Streamlit. It uses a custom-trained Convolutional Neural Network (CNN) hosted on the Roboflow cloud inference platform to identify waste materials in real time from a camera capture or uploaded photo, then provides precise disposal instructions and eco-facts for every detected item.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Code Architecture](#code-architecture)
   - [Constants & Knowledge Base](#constants--knowledge-base)
   - [CSS System](#css-system)
   - [Core Functions](#core-functions)
   - [Page Renderers](#page-renderers)
   - [Main Entry Point](#main-entry-point)
5. [Waste Categories](#waste-categories)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Running the App](#running-the-app)
9. [Navigation & Pages](#navigation--pages)
10. [Development Team](#development-team)

---

## Features

| Feature | Description |
|---|---|
| **Real-Time Classification** | Classifies waste via live camera capture or image upload using a Roboflow-hosted CNN. |
| **6-Class Detection** | Identifies Cardboard, Glass, Metal, Paper, Plastic, and general Trash. |
| **Smart Disposal Instructions** | Provides step-by-step, item-specific recycling or disposal guidance. |
| **Bin Assignment** | Tells the user exactly which bin color and type to use for every item. |
| **Eco Facts** | Displays an environmental fact tied to the detected material after every scan. |
| **All-Category Score Grid** | Shows confidence scores for all 6 categories simultaneously after each prediction. |
| **Reference Guide** | A complete offline disposal guide for all 6 materials, accessible without scanning. |
| **Stats Overview** | A visual summary card grid of all 6 waste categories with recyclability status. |
| **Welcome / Landing Page** | Animated glassmorphism landing page with decorative green blob background effects. |
| **About Dialog** | In-app modal with project description, key features, and development team details. |
| **Toast Notifications** | Bottom-right glass toast with scanning tips on first session load. |
| **Live API Status** | Sidebar indicator showing whether the Roboflow API is connected or not. |
| **Responsive Layout** | Full-width Streamlit `wide` layout with responsive column-based design. |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.9+ |
| **Web Framework** | [Streamlit](https://streamlit.io/) |
| **ML Inference** | [Roboflow Inference SDK](https://github.com/roboflow/inference) (`inference-sdk`) |
| **Image Processing** | [Pillow (PIL)](https://pillow.readthedocs.io/) |
| **Fonts** | Inter, JetBrains Mono (via Google Fonts CDN) |
| **Styling** | Vanilla CSS injected via `st.markdown(unsafe_allow_html=True)` |
| **Model Hosting** | Roboflow Cloud (`classify.roboflow.com`) |
| **Icons** | Custom SVG files (base64-encoded and inlined) |

---

## Project Structure

```
mkdir trashscan/
│
├── app.py                  # Single-file application (all logic, CSS, and HTML)
│
├── icons/                  # SVG icon assets (base64-encoded at runtime)
│   ├── logo.svg            # Main app logo (sidebar & top nav)
│   ├── classify.svg        # Recycle / classify icon
│   ├── reference.svg       # Reference page nav icon
│   ├── stats.svg           # Stats page nav icon
│   ├── cardboard.svg       # Cardboard category icon
│   ├── glass.svg           # Glass category icon
│   ├── metal.svg           # Metal category icon
│   ├── paper.svg           # Paper category icon
│   ├── plastic.svg         # Plastic category icon
│   └── trash.svg           # Trash category icon
│
├── requirements.txt        # Python dependencies (if present)
├── pyrefly.toml            # Pyrefly config
└── README.md               # This file
```

---

## Code Architecture

### Constants & Knowledge Base

**File:** `app.py` — top of file

```python
ROBOFLOW_API_KEY  = "..."          # Roboflow API key for inference
ROBOFLOW_MODEL_ID = "trashscan-4fiie/1"  # Trained model ID and version
CATEGORIES = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
```

**`DISPOSAL_INFO`** — a Python dictionary keyed by category name. Each entry contains:

| Field | Type | Description |
|---|---|---|
| `recyclable` | `bool` | Whether the item is recyclable |
| `accent` | `str` | Hex color used for accents and result cards |
| `light` | `str` | Light background hex for result card gradient |
| `bin` | `str` | Human-readable bin name |
| `bin_color` | `str` | Hex color of the recommended bin |
| `instructions` | `list[str]` | Step-by-step disposal instructions |
| `env_tip` | `str` | Environmental eco-fact for the material |
| `stat` | `str` | Short recyclability statistic badge text |

---

### CSS System

The app uses two CSS string constants injected into Streamlit via `st.markdown(..., unsafe_allow_html=True)`.

#### `GLOBAL_CSS`
Injected once at app startup. Contains:
- **Google Fonts import** — Inter (UI font) and JetBrains Mono (monospace for numbers)
- **CSS custom properties** — full green palette (`--g50` through `--g900`), slate palette, border radius tokens, shadow tokens, and transition speed
- **Base resets** — box-sizing, font smoothing, background color
- **Streamlit overrides** — hides default header/toolbar, removes collapse control, sets block-container padding
- **Sidebar styles** — dark green (`#052e16`) brand panel, animated floating logo, nav buttons, status chip, category pill badges
- **Top navigation bar** — glassmorphism card with shimmer accent line, logo, badge, and pulsing live dot
- **Component styles** — result cards, score grid cells, confidence bars, instruction rows, bin badge, eco-tip block, material chips, waiting-state box, error card
- **Toast styles** — fixed bottom-right positioning, light green glassmorphism background
- **Button styles** — primary (green gradient) and secondary (outline), with sidebar overrides for white text
- **Dialog styles** — white background with radial green glows, 28px rounded corners, dark green text throughout

#### `START_CSS`
Injected only on the landing (welcome) page. Contains:
- Full-screen green blob background (`blob-1`, `blob-2`, `blob-3`) with `blobPulse` animation
- `position: fixed` correction for the About button (resets Streamlit's default transform context)
- Glassmorphism landing card (`.start-card`) with shimmer top accent line
- Card inner elements: `.start-eyebrow`, `.start-title`, `.start-sub`, `.start-btn-link`
- `fadeUp` and `cardAppear` entrance animations

---

### Core Functions

#### `get_svg_icon(name: str) -> str`
```python
@st.cache_data
def get_svg_icon(name: str) -> str
```
- Reads `icons/{name}.svg` from disk
- Encodes it as a base64 data URI (`data:image/svg+xml;base64,...`)
- Cached indefinitely with `@st.cache_data` — each icon is only read once per session
- Returns an empty string if the file does not exist

---

#### `load_model() -> InferenceHTTPClient | None`
```python
@st.cache_resource(show_spinner=False)
def load_model()
```
- Validates that `ROBOFLOW_API_KEY` is set and not the placeholder string
- Imports `InferenceHTTPClient` from `inference_sdk` and creates a client pointed at `https://classify.roboflow.com`
- Cached with `@st.cache_resource` — the client is created once and reused across all reruns
- Returns `None` if the API key is missing

---

#### `predict(model, pil_image) -> tuple[str, float, list]`
```python
def predict(model, pil_image: Image.Image)
```
- Converts the PIL image to RGB and encodes it as a base64 JPEG string
- Calls `model.infer(b64, model_id=ROBOFLOW_MODEL_ID)` to get predictions
- Maps prediction confidences to the fixed `CATEGORIES` order
- Returns a tuple of `(top_label, confidence_float, all_probs_list)`

---

#### `render_result(label, confidence, all_probs)`
```python
def render_result(label: str, confidence: float, all_probs: list)
```
Renders the full classification result UI:
1. **Result card** — color-coded gradient card with category name, confidence percentage, animated confidence bar, and category icon
2. **Status pill** — `Recyclable`, `General Waste`, or `Check Resin Number` (plastic)
3. **Disposal instructions** — animated list rows from `DISPOSAL_INFO[label]["instructions"]`
4. **Bin badge** — color dot + bin name
5. **Eco tip** — highlighted fact block from `DISPOSAL_INFO[label]["env_tip"]`
6. **All-category score grid** — 6-column grid of score cells for every category, with the top prediction highlighted

---

### Page Renderers

#### `show_start_page()`
Renders the animated welcome/landing page:
- Injects `START_CSS`
- Renders 3 animated blob divs as background decoration
- Places a fixed `About` button (top-right) that opens `show_about_dialog()`
- Renders the centered glassmorphism card with eyebrow label, title, tagline, and a `Start Classifying` link that navigates to `?nav=Classify`

#### `show_about_dialog()`
```python
@st.dialog("About TrashScan AI", width="large")
def show_about_dialog()
```
- Registered as a Streamlit dialog component
- Displays project description, 3-column key features section, and the development team list

#### `render_sidebar(model)`
Renders the persistent left sidebar (only when app is started):
- Brand panel with animated floating logo, app name, subtitle
- Navigation links: **Classify**, **Reference**, **Stats** (HTML `<a>` tags with `?nav=` query params)
- API status chip (green `Roboflow Connected` or red `API Key Required`)
- `Welcome Page` button that clears query params and returns to the landing page

#### `render_reference()`
Renders the **Reference** page:
- Iterates over all 6 categories
- For each: renders a card with the category icon, name, bin type, all disposal instructions, and eco-fact

#### `render_stats()`
Renders the **Stats** page:
- 3-column grid of summary cards for all 6 categories
- Each card: icon, category name, recyclability label, stat badge

---

### Main Entry Point

```python
def main():
    if not st.session_state.started:
        show_start_page()
        return

    # Show tips toast once per session
    if "tips_shown" not in st.session_state:
        st.session_state.tips_shown = True
        st.toast("Tips: plain background, good lighting, one item, fill the frame")

    model = load_model()
    render_sidebar(model)
    # Render top navigation bar
    # Route to Reference, Stats, or Classify page based on st.session_state.active_nav

if __name__ == "__main__":
    main()
```

**Session state variables:**

| Variable | Type | Purpose |
|---|---|---|
| `started` | `bool` | Whether the user has left the welcome page |
| `active_nav` | `str` | Currently active nav tab (`"Classify"`, `"Reference"`, or `"Stats"`) |
| `tips_shown` | `bool` | Prevents the tips toast from showing more than once |

**Navigation routing** uses Streamlit's `st.query_params`. When a nav link is clicked (`?nav=Classify`), the app reads the param on the next rerun and updates `st.session_state.active_nav`.

---

## Waste Categories

| Category | Recyclable | Recommended Bin | Stat |
|---|---|---|---|
| Cardboard | Yes | Blue Recycling Bin | 80% recyclable |
| Glass | Yes | Green / Glass Bin | 100% recyclable |
| Metal | Yes | Blue Recycling Bin | 95% energy saved |
| Paper | Yes | Blue / Paper Bin | 70% recyclable |
| Plastic | Conditional | Blue Bin (check local rules) | 9% recycled globally |
| Trash | No | Black / Gray General Waste | Minimize waste |

> **Plastic note:** The app uses a special `Check Resin Number` status pill for plastic, since recyclability depends on the resin code (#1–#2 recyclable, #3–#7 not).

---

## Installation

### Prerequisites

- Python **3.9** or higher
- `pip` package manager
- A Roboflow account and API key

### Steps

```bash
# 1. Clone or download the project
git clone <repo-url>
cd "mkdir trashscan"

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install streamlit pillow inference-sdk
```

---

## Configuration

Open `app.py` and set your Roboflow API key on line 45:

```python
ROBOFLOW_API_KEY  = "YOUR_API_KEY_HERE"
ROBOFLOW_MODEL_ID = "trashscan-4fiie/1"
```

To obtain a Roboflow API key:
1. Sign up at [roboflow.com](https://roboflow.com)
2. Go to **Settings → API** in your workspace dashboard
3. Copy your Private API Key and paste it above

---

## Running the App

```bash
# Standard run
streamlit run app.py

# If using a virtual environment on Windows
.venv\Scripts\python.exe -m streamlit run app.py
```

The app will open automatically at **`http://localhost:8501`** in your default browser.

### First-Run Tips

- Use a **plain background** behind the waste item for best accuracy
- Ensure **good lighting** — avoid shadows directly on the item
- Scan **one item at a time** and fill the frame with it
- Supported upload formats: `.jpg`, `.jpeg`, `.png`, `.webp`

---

## Navigation & Pages

```
Welcome Page  →  [Start Classifying]
                        │
                   ┌────┴─────────────────────┐
                   │         Sidebar           │
                   │  [Classify] [Reference]   │
                   │          [Stats]          │
                   │  API Status indicator     │
                   │  [Welcome Page] button    │
                   └──────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      Classify       Reference      Stats
    (camera/upload) (full guide) (category grid)
```

| Page | Route | Description |
|---|---|---|
| **Welcome** | `/` (no query params) | Landing page with animated blobs and start card |
| **Classify** | `?nav=Classify` | Two-column layout: image input left, result right |
| **Reference** | `?nav=Reference` | Full disposal guide for all 6 waste categories |
| **Stats** | `?nav=Stats` | Summary grid of all 6 categories with recyclability |

---

## Development Team

This project was developed with care by:

- **Aguillera, Juan Miguel B.**
- **Andal, Rob Edmond N.**
- **Arandia, Jedrick O.**
- **Masangcay, Jun Lorenz C.**
