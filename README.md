# US College Tuition & Fees Dashboard

An interactive data visualization dashboard analyzing US college tuition trends, state comparisons, and total cost of attendance from 2000 to 2023.

**Live App:** [https://infoviz-dashboard.streamlit.app](https://infoviz-dashboard.streamlit.app)

---

## Overview

This dashboard was built for INFO 5602 — Information Visualization. It tells a complete data story across four charts, answering four research questions:

| Chart | Research Question |
|-------|-------------------|
| Line Chart | How has tuition changed over time across institution types? |
| Horizontal Bar Chart | Which states have the highest tuition costs? |
| Waterfall Chart | How does the total cost of attendance break down beyond tuition? |
| Heatmap | Which states have seen the steepest increases over two decades? |

---

## Dashboard Sections

### KPI Cards
Four headline metrics at a glance:
- Average public tuition (2023): **$10,940**
- Average private tuition (2023): **$39,400**
- Public tuition growth since 2000: **+213%**
- Total cost of attendance: **$25,420**

### Chart 1 — Tuition Trends (Line Chart)
Public vs. private tuition from 2000–2023. The shaded band highlights the widening gap between institution types.

### Chart 2 — Most Expensive States (Horizontal Bar Chart)
Top 10 states ranked by average in-state tuition in 2023, with a national average reference line.

### Chart 3 — Cost of Attendance Breakdown (Waterfall Chart)
Cumulative build-up of all cost components: tuition, fees, room, board, and books.

### Chart 4 — State Tuition Heatmap
10 states × 6 years showing how tuition intensity has shifted geographically from 2000 to 2023.

---

## Project Structure

```
info_viz_dashboard/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Pinned Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit theme and server config
├── .gitignore
└── README.md
```

---

## Running Locally

**Prerequisites:** Python 3.9+

```bash
# 1. Clone the repository
git clone https://github.com/HarishNandhan/info_viz_dashboard.git
cd info_viz_dashboard

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deploying to Streamlit Cloud

This app is configured for one-click deployment on [Streamlit Community Cloud](https://streamlit.io/cloud) (free tier).

1. Fork or push this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app**
4. Select:
   - **Repository:** `HarishNandhan/info_viz_dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **Deploy** — the app will be live within ~2 minutes

---

## Data Source

All data is hardcoded from the **National Center for Education Statistics (NCES)**.  
Figures represent average annual tuition for 4-year public institutions unless otherwise noted.

- Public tuition series: NCES Digest of Education Statistics, Table 330.10
- Private tuition series: NCES Digest of Education Statistics, Table 330.20
- State-level data: NCES IPEDS State Profiles

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [NumPy](https://numpy.org) | Numerical support |

---

## Color Palette

| Role | Hex |
|------|-----|
| Primary Blue | `#2E86AB` |
| Accent Coral | `#E84855` |
| Neutral Grey | `#F0F0F0` |
| Text | `#2D2D2D` |
| Background | `#FFFFFF` |
| Gridlines | `#E8E8E8` |
