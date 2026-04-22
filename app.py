import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JalAlert: Telangana Water Stress Dashboard",
    layout="wide",
    page_icon="💧",
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("telangana_water_data.csv")

df = load_data()

# ── Theme / style constants ───────────────────────────────────────────────────
BLUE   = "#1E88E5"
TEAL   = "#00ACC1"
ORANGE = "#FB8C00"
RED    = "#E53935"
GREEN  = "#43A047"
PURPLE = "#8E24AA"
GRAY   = "#607D8B"

COLOR_SEQUENCE = ["#1E88E5","#00ACC1","#FB8C00","#E53935","#43A047","#8E24AA","#F06292","#4DD0E1","#FFB74D","#A1887F"]

PAGE_ICON = "💧"
CHARTS_TEMPLATE = dict(
    layout=go.Layout(
        font=dict(family="Roboto, sans-serif", size=13, color="#37474F"),
        paper_bgcolor="#FAFAFA",
        plot_bgcolor="#FAFAFA",
        margin=dict(l=60, r=30, t=50, b=60),
    )
)

# ── Helper: metric card ───────────────────────────────────────────────────────
def metric_card(label, value, delta=None, color="#1E88E5"):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color}22, {color}11);
            border-left: 5px solid {color};
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 10px;
        ">
            <div style="font-size:12px; color:#607D8B; text-transform:uppercase; letter-spacing:1px;">{label}</div>
            <div style="font-size:28px; font-weight:700; color:#1C313A;">{value}</div>
            {f'<div style="font-size:12px; color:{color}; margin-top:4px;">{delta}</div>' if delta else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Helper: section header ────────────────────────────────────────────────────
def section_header(title, icon="📊"):
    st.markdown(f"<h2 style='border-bottom: 2px solid #1E88E5; padding-bottom:6px; margin-top:30px;'>{icon} {title}</h2>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
st.sidebar.markdown("## 💧 JalAlert")
st.sidebar.markdown("**Analysis Dashboard**")
st.sidebar.divider()

# Year filter
all_years = sorted(df["year"].unique())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(min(all_years)),
    max_value=int(max(all_years)),
    value=(int(min(all_years)), int(max(all_years))),
)
df_f = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])].copy()

# District filter
all_districts = ["All Districts"] + sorted(df_f["district"].unique())
selected_district = st.sidebar.selectbox("Select District", all_districts)
if selected_district != "All Districts":
    df_f = df_f[df_f["district"] == selected_district]

# Region type filter
all_regions = ["All Region Types"] + sorted(df_f["region_type"].unique())
selected_region = st.sidebar.selectbox("Select Region Type", all_regions)
if selected_region != "All Region Types":
    df_f = df_f[df_f["region_type"] == selected_region]

# Season filter
all_seasons = ["All Seasons"] + sorted(df_f["season"].unique())
selected_season = st.sidebar.selectbox("Select Season", all_seasons)
if selected_season != "All Seasons":
    df_f = df_f[df_f["season"] == selected_season]

st.sidebar.divider()
st.sidebar.caption(f"📁 {len(df_f):,} rows selected  |  Total: {len(df):,} rows")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW / HOME
# ══════════════════════════════════════════════════════════════════════════════
st.title(f"{PAGE_ICON} Telangana Water Stress — Overview")

col1, col2, col3, col4 = st.columns(4)
avg_wsi   = df_f["wsi"].mean()
avg_ratio = df_f["water_stress_ratio"].mean()
avg_ground = df_f["groundwater"].mean()
avg_rain   = df_f["rainfall"].mean()
total_pop  = df_f["population"].iloc[0] if len(df_f) > 0 else 0
high_risk  = df_f[df_f["stress_level"] == "Medium"].shape[0] if len(df_f) > 0 else 0

metric_card("Avg Water Stress Index (WSI)", f"{avg_wsi:.4f}", color=BLUE)
metric_card("Avg Water Stress Ratio", f"{avg_ratio:.4f}", color=TEAL)
metric_card("Avg Groundwater Level (m)", f"{avg_ground:.2f}", color=GREEN)
metric_card("Avg Rainfall (mm)", f"{avg_rain:.1f}", color=PURPLE)

with col1:
    st.markdown("")
    st.markdown("")
    st.metric("Avg WSI", f"{avg_wsi:.4f}", help="Water Stress Index — higher = more stress")
with col2:
    st.metric("Avg Stress Ratio", f"{avg_ratio:.4f}")
with col3:
    st.metric("Avg Groundwater", f"{avg_ground:.1f} m")
with col4:
    st.metric("Avg Rainfall", f"{avg_rain:.1f} mm")

st.divider()

# Row 2 — KPI cards
kc1, kc2, kc3, kc4 = st.columns(4)
kc1.metric("Districts", str(len(df_f["district"].unique())))
kc2.metric("Year Range", f"{year_range[0]}–{year_range[1]}")
kc3.metric("Rows in Filter", f"{len(df_f):,}")
# water availability
with kc4:
    avg_avail = df_f["water_availability"].mean()
    st.metric("Avg Water Availability", f"{avg_avail:.1f}")

st.divider()

# ── Trend over time (yearly) ──────────────────────────────────────────────────
section_header("Key Metrics Over Time (Yearly Average)", "📈")

yearly = df_f.groupby("year").agg(
    WSI=("wsi", "mean"),
    Stress_Ratio=("water_stress_ratio", "mean"),
    Groundwater=("groundwater", "mean"),
    Rainfall=("rainfall", "mean"),
    Water_Availability=("water_availability", "mean"),
    Water_Usage=("water_usage", "mean"),
    Temperature=("temperature", "mean"),
).reset_index()

tabs = st.tabs(["WSI Trend", "Groundwater", "Rainfall", "Water Availability", "Water Usage", "Temperature"])
for tab_name, col in zip(tabs, ["WSI","Groundwater","Rainfall","Water_Availability","Water_Usage","Temperature"]):
    with tab_name:
        fig = px.line(
            yearly, x="year", y=col,
            markers=True,
            color_discrete_sequence=[BLUE],
            template="plotly_white",
        )
        fig.update_traces(line=dict(width=3, shape="spline"), marker=dict(size=8))
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title=col,
            title=dict(text=f"{col} Over Time", font=dict(size=16)),
            margin=dict(l=60, r=30, t=60, b=50),
        )
        st.plotly_chart(fig, width="stretch")

# ── Stress level distribution ────────────────────────────────────────────────
section_header("Stress Level Distribution", "🔴")

cl1, cl2 = st.columns(2)

with cl1:
    stress_counts = df_f["stress_level"].value_counts().reset_index()
    stress_counts.columns = ["stress_level", "count"]
    fig = px.pie(
        stress_counts,
        names="stress_level",
        values="count",
        color="stress_level",
        color_discrete_map={"Medium": ORANGE, "Low": GREEN, "High": RED},
        hole=0.45,
        template="plotly_white",
    )
    fig.update_layout(title="Overall Stress Level Split", margin=dict(t=60))
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, width="stretch")

with cl2:
    district_stress = df_f.groupby(["district", "stress_level"]).size().reset_index(name="count")
    fig = px.bar(
        district_stress,
        x="district",
        y="count",
        color="stress_level",
        barmode="group",
        color_discrete_map={"Medium": ORANGE, "Low": GREEN, "High": RED},
        template="plotly_white",
    )
    fig.update_layout(
        title="Stress Level by District",
        xaxis_title="District",
        yaxis_title="Count",
        legend_title="Stress Level",
        margin=dict(b=120),
    )
    st.plotly_chart(fig, width="stretch")

# ── Correlation heatmap ──────────────────────────────────────────────────────
section_header("Correlation Heatmap", "🔗")

num_cols = ["rainfall", "groundwater", "temperature", "water_usage", "storage_capacity",
            "urbanization_rate", "wsi", "water_stress_ratio", "water_availability", "population_density"]
corr = df_f[num_cols].corr()

fig = go.Figure(data=go.Heatmap(
    z=corr.values,
    x=num_cols,
    y=num_cols,
    colorscale="RdBu",
    zmid=0,
    text=corr.values,
    texttemplate="%{text:.2f}",
    textfont=dict(size=8),
    colorbar=dict(title="Correlation"),
))
fig.update_layout(
    title="Correlation Matrix — Numeric Features",
    margin=dict(l=60, r=30, t=60, b=100),
    height=550,
)
st.plotly_chart(fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — WATER STRESS DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.title("🔍 Water Stress Deep Dive")

col1, col2 = st.columns(2)

with col1:
    district_wsi = df_f.groupby("district")["wsi"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(
        district_wsi,
        x="district",
        y="wsi",
        color="wsi",
        color_continuous_scale="Reds",
        template="plotly_white",
        labels={"wsi": "Avg WSI", "district": "District"},
    )
    fig.update_layout(title="Average WSI by District", margin=dict(b=120), coloraxis_showscale=False)
    st.plotly_chart(fig, width="stretch")

with col2:
    district_ratio = df_f.groupby("district")["water_stress_ratio"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(
        district_ratio,
        x="district",
        y="water_stress_ratio",
        color="water_stress_ratio",
        color_continuous_scale="Oranges",
        template="plotly_white",
        labels={"water_stress_ratio": "Avg Stress Ratio", "district": "District"},
    )
    fig.update_layout(title="Average Stress Ratio by District", margin=dict(b=120), coloraxis_showscale=False)
    st.plotly_chart(fig, width="stretch")

# WSI vs Stress Ratio scatter
section_header("WSI vs Stress Ratio — District Level", "🎯")
fig = px.scatter(
    df_f.groupby("district").agg(
        WSI=("wsi","mean"),
        Stress_Ratio=("water_stress_ratio","mean"),
        Groundwater=("groundwater","mean"),
        Population=("population","mean"),
        Urbanization=("urbanization_rate","mean"),
    ).reset_index(),
    x="WSI",
    y="Stress_Ratio",
    size="Population",
    color="Urbanization",
    color_continuous_scale="Viridis",
    hover_name="district",
    template="plotly_white",
    labels={"Urbanization": "Urbanization Rate (%)"},
)
fig.update_layout(
    title="District-level WSI vs Stress Ratio (bubble size = population)",
    margin=dict(l=60, r=30, t=60, b=50),
    height=500,
)
st.plotly_chart(fig, width="stretch")

# Year × district heatmap for WSI
section_header("WSI Heatmap — Year × District", "🗓️")
pivot_wsi = df_f.pivot_table(values="wsi", index="district", columns="year", aggfunc="mean")
fig = go.Figure(data=go.Heatmap(
    z=pivot_wsi.values,
    x=pivot_wsi.columns,
    y=pivot_wsi.index,
    colorscale="Reds",
    colorbar=dict(title="WSI"),
    text=pivot_wsi.values,
    texttemplate="%{text:.3f}",
    textfont=dict(size=7),
))
fig.update_layout(title="WSI by District and Year", margin=dict(l=120, r=30, t=60, b=80), height=600)
st.plotly_chart(fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — RAINFALL & GROUNDWATER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.title("🌧️ Rainfall & Groundwater Analysis")

r1, r2 = st.columns(2)

with r1:
    fig = px.line(
        df_f.groupby(["year", "season"])["rainfall"].mean().reset_index(),
        x="year",
        y="rainfall",
        color="season",
        markers=True,
        color_discrete_sequence=[TEAL, ORANGE, BLUE],
        template="plotly_white",
    )
    fig.update_layout(title="Avg Rainfall by Season", xaxis_title="Year", yaxis_title="Rainfall (mm)")
    st.plotly_chart(fig, width="stretch")

with r2:
    fig = px.line(
        df_f.groupby(["year", "season"])["groundwater"].mean().reset_index(),
        x="year",
        y="groundwater",
        color="season",
        markers=True,
        color_discrete_sequence=[TEAL, ORANGE, BLUE],
        template="plotly_white",
    )
    fig.update_layout(title="Avg Groundwater by Season", xaxis_title="Year", yaxis_title="Groundwater (m)")
    st.plotly_chart(fig, width="stretch")

r3, r4 = st.columns(2)

with r3:
    fig = px.bar(
        df_f.groupby(["district", "rainfall_category"]).size().reset_index(name="count"),
        x="district",
        y="count",
        color="rainfall_category",
        barmode="group",
        template="plotly_white",
        color_discrete_sequence=[BLUE, TEAL, ORANGE],
    )
    fig.update_layout(title="Records by Rainfall Category", xaxis_title="District", legend_title="Category", margin=dict(b=120))
    st.plotly_chart(fig, width="stretch")

with r4:
    fig = px.scatter(
        df_f.sample(min(3000, len(df_f))),
        x="rainfall",
        y="groundwater",
        color="wsi",
        color_continuous_scale="RdYlGn_r",
        hover_name="district",
        template="plotly_white",
        labels={"rainfall": "Rainfall (mm)", "groundwater": "Groundwater (m)"},
    )
    fig.update_layout(title="Rainfall vs Groundwater (colored by WSI)", height=420)
    st.plotly_chart(fig, width="stretch")

# Rainfall by district
section_header("Average Rainfall by District", "📍")
rf_dist = df_f.groupby("district")["rainfall"].mean().sort_values().reset_index()
fig = px.bar(
    rf_dist, x="district", y="rainfall", color="rainfall",
    color_continuous_scale="Blues", template="plotly_white",
    labels={"rainfall": "Avg Rainfall (mm)"},
)
fig.update_layout(margin=dict(b=120), coloraxis_showscale=False)
st.plotly_chart(fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — WATER USAGE & AVAILABILITY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.title("🚰 Water Usage & Availability")

u1, u2 = st.columns(2)

with u1:
    fig = px.line(
        df_f.groupby("year")["water_usage"].mean().reset_index(),
        x="year", y="water_usage", markers=True,
        color_discrete_sequence=[RED],
        template="plotly_white",
    )
    fig.update_traces(line=dict(width=3, shape="spline"))
    fig.update_layout(title="Avg Water Usage Over Time", yaxis_title="Water Usage")
    st.plotly_chart(fig, width="stretch")

with u2:
    fig = px.line(
        df_f.groupby("year")["water_availability"].mean().reset_index(),
        x="year", y="water_availability", markers=True,
        color_discrete_sequence=[GREEN],
        template="plotly_white",
    )
    fig.update_traces(line=dict(width=3, shape="spline"))
    fig.update_layout(title="Avg Water Availability Over Time", yaxis_title="Water Availability")
    st.plotly_chart(fig, width="stretch")

u3, u4 = st.columns(2)

with u3:
    fig = px.bar(
        df_f.groupby(["district", "region_type"])["water_usage"].mean().reset_index(),
        x="district", y="water_usage", color="region_type",
        barmode="group",
        template="plotly_white",
        color_discrete_sequence=[PURPLE, TEAL, ORANGE],
    )
    fig.update_layout(title="Water Usage by District & Region Type", xaxis_title="District", margin=dict(b=120))
    st.plotly_chart(fig, width="stretch")

with u4:
    fig = px.bar(
        df_f.groupby(["district", "region_type"])["water_availability"].mean().reset_index(),
        x="district", y="water_availability", color="region_type",
        barmode="group",
        template="plotly_white",
        color_discrete_sequence=[PURPLE, TEAL, ORANGE],
    )
    fig.update_layout(title="Water Availability by District & Region Type", xaxis_title="District", margin=dict(b=120))
    st.plotly_chart(fig, width="stretch")

section_header("Water Usage vs Availability (District Aggregated)", "⚖️")
dist_ua = df_f.groupby("district")[["water_usage","water_availability","storage_capacity"]].mean().reset_index()
dist_ua = dist_ua.sort_values("water_usage", ascending=False)

fig = make_subplots(rows=1, cols=3, subplot_titles=["Avg Water Usage", "Avg Water Availability", "Avg Storage Capacity"])
for i, (col, color, title) in enumerate([
    ("water_usage", RED, "Usage"),
    ("water_availability", GREEN, "Availability"),
    ("storage_capacity", BLUE, "Storage Cap"),
], start=1):
    sub = dist_ua.sort_values(col, ascending=False)
    fig.add_trace(go.Bar(x=sub["district"], y=sub[col], marker_color=color, name=title, showlegend=False), row=1, col=i)
    fig.update_xaxes(tickangle=45, tickfont=dict(size=8), row=1, col=i)

fig.update_layout(title="District Comparison", template="plotly_white", height=400, showlegend=False, margin=dict(b=120))
st.plotly_chart(fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — SEASONAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.title("🌦️ Seasonal Analysis")

s1, s2 = st.columns(2)

with s1:
    seasonal = df_f.groupby("season")[["wsi","water_stress_ratio","groundwater","rainfall","water_usage","water_availability"]].mean().reset_index()
    season_order = ["Winter", "Summer", "Monsoon"]
    present = [s for s in season_order if s in seasonal["season"].values]
    seasonal["season"] = pd.Categorical(seasonal["season"], categories=present, ordered=True)
    seasonal = seasonal.sort_values("season").reset_index(drop=True)
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=["Avg WSI","Avg Stress Ratio","Avg Groundwater","Avg Rainfall","Avg Water Usage","Avg Water Availability"],
        specs=[[{"type":"bar"},{"type":"bar"},{"type":"bar"}],[{"type":"bar"},{"type":"bar"},{"type":"bar"}]],
    )
    colors_season = [BLUE, ORANGE, GREEN]
    for i, (col, color) in enumerate(zip(["wsi","water_stress_ratio","groundwater","rainfall","water_usage","water_availability"], [BLUE,TEAL,ORANGE,GREEN,PURPLE,RED] * 2)):
        row, col_idx = i // 3 + 1, i % 3 + 1
        fig.add_trace(go.Bar(x=seasonal["season"], y=seasonal[col], marker_color=colors_season, showlegend=False), row=row, col=col_idx)
    fig.update_layout(template="plotly_white", title="Seasonal Averages", height=500, showlegend=False, margin=dict(t=60))
    st.plotly_chart(fig, width="stretch")

with s2:
    fig = px.box(
        df_f, x="season", y="wsi", color="season",
        category_orders={"season":["Winter","Summer","Monsoon"]},
        color_discrete_sequence=[BLUE, ORANGE, GREEN],
        template="plotly_white",
        labels={"wsi":"WSI","season":"Season"},
    )
    fig.update_layout(title="WSI Distribution by Season", showlegend=False)
    st.plotly_chart(fig, width="stretch")

section_header("Monthly Patterns", "📅")
monthly = df_f.groupby(["month","season"])[["wsi","water_stress_ratio","rainfall","groundwater"]].mean().reset_index()
fig = px.line(
    monthly, x="month", y="wsi", color="season",
    markers=True, color_discrete_sequence=[BLUE, ORANGE, GREEN],
    template="plotly_white",
    labels={"wsi":"Avg WSI","month":"Month"},
)
fig.update_layout(title="Monthly WSI Pattern by Season", xaxis=dict(tickmode="array", tickvals=list(range(1,13)), ticktext=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]))
st.plotly_chart(fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — URBANIZATION & WATER SOURCE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.title("🏙️ Urbanization & Water Source Impact")

u1, u2 = st.columns(2)

with u1:
    fig = px.box(
        df_f, x="region_type", y="wsi", color="region_type",
        color_discrete_sequence=[PURPLE, TEAL, ORANGE],
        template="plotly_white",
    )
    fig.update_layout(title="WSI Distribution by Region Type", showlegend=False)
    st.plotly_chart(fig, width="stretch")

with u2:
    fig = px.box(
        df_f, x="water_source", y="wsi", color="water_source",
        color_discrete_sequence=[BLUE, GREEN, ORANGE],
        template="plotly_white",
    )
    fig.update_layout(title="WSI Distribution by Water Source", showlegend=False)
    st.plotly_chart(fig, width="stretch")

u3, u4 = st.columns(2)

with u3:
    urban_year = df_f.groupby(["year","region_type"])["urbanization_rate"].mean().reset_index()
    fig = px.line(
        urban_year, x="year", y="urbanization_rate", color="region_type",
        markers=True, color_discrete_sequence=[PURPLE, TEAL, ORANGE],
        template="plotly_white",
        labels={"urbanization_rate":"Urbanization Rate (%)"},
    )
    fig.update_layout(title="Urbanization Rate Over Time")
    st.plotly_chart(fig, width="stretch")

with u4:
    urban_wsi = df_f.groupby(["year","region_type"])["wsi"].mean().reset_index()
    fig = px.line(
        urban_wsi, x="year", y="wsi", color="region_type",
        markers=True, color_discrete_sequence=[PURPLE, TEAL, ORANGE],
        template="plotly_white",
    )
    fig.update_layout(title="WSI Trend by Region Type")
    st.plotly_chart(fig, width="stretch")

section_header("Water Source Mix by District", "💧")
ws_district = df_f.groupby(["district","water_source"]).size().reset_index(name="count")
fig = px.bar(
    ws_district, x="district", y="count", color="water_source",
    barmode="stack",
    color_discrete_sequence=[BLUE, GREEN, ORANGE],
    template="plotly_white",
    labels={"count":"Number of Records"},
)
fig.update_layout(title="Water Source Distribution by District", margin=dict(b=120))
st.plotly_chart(fig, width="stretch")

# Storage capacity vs usage
section_header("Storage Capacity vs Water Usage", "🏗️")
fig = px.scatter(
    df_f.groupby("district")[["storage_capacity","water_usage","urbanization_rate"]].mean().reset_index(),
    x="storage_capacity", y="water_usage", size="urbanization_rate",
    color="urbanization_rate", color_continuous_scale="Purples",
    hover_name="district",
    template="plotly_white",
    labels={"storage_capacity":"Storage Capacity","water_usage":"Water Usage","urbanization_rate":"Urbanization Rate"},
)
fig.update_layout(title="Storage Capacity vs Water Usage (size = urbanization)", height=480)
st.plotly_chart(fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — DISTRICT COMPARATOR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.title("🗺️ District Comparator")

# Select districts to compare
compare_districts = st.multiselect(
    "Select up to 8 districts to compare",
    options=sorted(df_f["district"].unique()),
    default=sorted(df_f["district"].unique())[:5],
    max_selections=8,
)

if compare_districts:
    comp = df_f[df_f["district"].isin(compare_districts)].groupby("district").agg(
        WSI=("wsi","mean"),
        Stress_Ratio=("water_stress_ratio","mean"),
        Groundwater=("groundwater","mean"),
        Rainfall=("rainfall","mean"),
        Water_Usage=("water_usage","mean"),
        Water_Availability=("water_availability","mean"),
        Urbanization=("urbanization_rate","mean"),
        Temperature=("temperature","mean"),
    ).reset_index().round(4)

    st.dataframe(
        comp.set_index("district"),
        width="stretch",
        height=400,
    )

    dc1, dc2 = st.columns(2)

    with dc1:
        fig = px.line_polar(
            comp.melt(id_vars="district", value_vars=["WSI","Stress_Ratio","Groundwater","Rainfall"]),
            r="value", theta="variable", color="district",
            color_discrete_sequence=COLOR_SEQUENCE[:len(compare_districts)],
            template="plotly_white",
        )
        fig.update_layout(title="Multi-metric Radar — Normalized View", polar=dict(radialaxis=dict(visible=True)))
        st.plotly_chart(fig, width="stretch")

    with dc2:
        fig = px.line_polar(
            comp.melt(id_vars="district", value_vars=["Water_Usage","Water_Availability","Urbanization","Temperature"]),
            r="value", theta="variable", color="district",
            color_discrete_sequence=COLOR_SEQUENCE[:len(compare_districts)],
            template="plotly_white",
        )
        fig.update_layout(title="Usage & Availability Radar", polar=dict(radialaxis=dict(visible=True)))
        st.plotly_chart(fig, width="stretch")

    # Side-by-side bar charts
    bar_cols = ["WSI","Groundwater","Rainfall","Water_Usage","Water_Availability"]
    for i in range(0, len(bar_cols), 2):
        bc = st.columns(2)
        for j, col in enumerate(bar_cols[i:i+2]):
            sorted_comp = comp.sort_values(col, ascending=False)
            fig = px.bar(
                sorted_comp, x="district", y=col,
                color=col, color_continuous_scale="Blues" if j==0 else "Greens",
                template="plotly_white",
            )
            fig.update_layout(title=f"Avg {col.replace('_',' ')}", showlegend=False, margin=dict(b=100))
            bc[j].plotly_chart(fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — RAW DATA EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.title("📋 Raw Data Explorer")

st.dataframe(df_f, width="stretch", height=500)

st.markdown(f"**Export filtered data:** {len(df_f):,} rows")

@st.cache_data
def convert_csv(data):
    return data.to_csv(index=False).encode("utf-8")

csv = convert_csv(df_f)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="telangana_water_filtered.csv",
    mime="text/csv",
)
