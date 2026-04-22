# Telangana Water Stress Dashboard

An interactive data visualization dashboard for analyzing water stress patterns across **25 districts of Telangana**, covering **2015–2024** with monthly granularity across **20,160 records**.

---

## Project Overview

**Purpose:** To help environmental analysts, policy makers, and government agencies monitor water scarcity, track seasonal variations, and identify high-risk regions through intuitive visual analytics.

**Data Source:** Simulated Telangana water stress dataset with realistic distributions across rainfall, groundwater, temperature, urbanization, and water usage metrics.

---

## Dataset

| Feature | Description |
|---|---|
| `district` | 25 Telangana districts |
| `year` | 2015 – 2024 |
| `month` | 1 – 12 |
| `population` | District population |
| `rainfall` | Monthly rainfall (mm) |
| `groundwater` | Groundwater level (m below surface) |
| `temperature` | Average temperature (°C) |
| `water_usage` | Daily water usage (MLD) |
| `storage_capacity` | Reservoir/dam capacity (MLD) |
| `urbanization_rate` | % urban population |
| `region_type` | Urban / Semi-Urban / Rural |
| `water_source` | Groundwater / Surface Water / Mixed |
| `rainfall_category` | High / Medium / Low |
| `season` | Winter / Summer / Monsoon |
| `wsi` | Water Stress Index (0–1, higher = more stressed) |
| `stress_level` | Low / Medium |
| `water_stress_ratio` | Usage / Availability ratio |
| `water_availability` | Available water resources (MLD) |
| `high_risk_flag` | Binary risk indicator |

---

## Dashboard Sections

### 1. Overview
- KPI cards: Avg WSI, Stress Ratio, Groundwater Level, Rainfall
- Yearly trend charts (WSI, Groundwater, Rainfall, Availability, Usage, Temperature)
- Stress level distribution (pie chart + district breakdown)
- Full correlation heatmap across all numeric features

### 2. Water Stress Deep Dive
- District-wise WSI and Stress Ratio bar charts
- Bubble scatter: WSI vs Stress Ratio (bubble size = population, color = urbanization)
- Year × District WSI heatmap

### 3. Rainfall & Groundwater Analysis
- Seasonal rainfall and groundwater trend lines
- Rainfall category distribution by district
- Rainfall vs Groundwater scatter (colored by WSI)
- District rainfall ranking chart

### 4. Water Usage & Availability
- Yearly water usage and availability trend lines
- District × region type grouped bar charts
- Side-by-side comparison: Usage, Availability, Storage Capacity

### 5. Seasonal Analysis
- Multi-metric seasonal comparison grid (WSI, Stress Ratio, Groundwater, Rainfall, Usage, Availability)
- WSI box plots by season
- Monthly WSI pattern with seasonal overlay

### 6. Urbanization & Water Source Impact
- WSI distribution by region type and water source (box plots)
- Urbanization rate and WSI trend by region type
- Stacked bar chart: water source mix per district
- Storage capacity vs water usage scatter

### 7. District Comparator
- Select up to 8 districts for side-by-side comparison
- Sortable data table with all key metrics
- Polar/radar charts for multi-metric comparison
- Comparative bar charts per metric

### 8. Raw Data Explorer
- Full filtered dataset view
- CSV download for any filtered slice

---

## Global Filters (Sidebar)

All pages are filtered by:
- **Year Range** — slider, 2015–2024
- **District** — select single or "All Districts"
- **Region Type** — Urban / Semi-Urban / Rural / All
- **Season** — Winter / Summer / Monsoon / All

---

## Tech Stack

- **Streamlit** — web framework
- **Plotly Express & GraphObjects** — interactive charts
- **Pandas** — data processing
- **Matplotlib** — styling support

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [community.cloud.streamlit.io](https://community.cloud.streamlit.io)
3. Click **New app** → select your repo → **Deploy**

---

## Project Structure

```
water_stress_project/
├── app.py                      # Streamlit dashboard
├── requirements.txt            # Python dependencies
├── telangana_water_data.csv    # Full dataset
├── data/
│   └── telangana_water_data.csv
├── README.md
└── .gitignore
```
