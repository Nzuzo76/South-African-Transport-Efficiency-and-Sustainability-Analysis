# =========================================================
# South African Transport Efficiency & Sustainability
# Professional presentation dashboard — brown / charcoal theme
# Updated: Distinct categorical colors for multi-category charts
# =========================================================

import io
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# Page setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="South African Transport Analysis",
    page_icon="🚍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Theme tokens
# ---------------------------------------------------------
BROWN_DARK   = "#3E2C1F"   # deep espresso
BROWN        = "#5A4030"   # coffee
BROWN_MID    = "#7A5A3F"   # warm oak
TAN          = "#A67B5B"   # soft tan
SAND         = "#D4C4B0"   # light sand
CREAM        = "#F5F1EC"   # page background
CHAR         = "#2E2E2E"   # charcoal text
STONE        = "#6B5B4A"   # muted stone
GOLD         = "#B8860B"   # accent
LINE_GRAY    = "#D8D2CA"

# Curated distinct earthy colors for multi-category charts
CATEGORICAL_COLORS = [
    "#3E2C1F",  # Deep Espresso (Dark Brown)
    "#C05C3E",  # Terracotta (Warm Rust)
    "#4A6D7C",  # Muted Slate Blue (Cool contrast)
    "#D19C3A",  # Golden Ochre (Bright warm)
    "#5C7A4E",  # Olive Green (Natural)
    "#8C7A6B",  # Taupe (Neutral)
    "#7B4463",  # Muted Plum
    "#B87333",  # Copper
    "#2E5B5A",  # Deep Teal
    "#9A3B3B",  # Muted Crimson
]

# For continuous scales (heatmaps)
BROWN_SCALE = [
    [0.00, "#F5F1EC"],
    [0.25, "#D4C4B0"],
    [0.50, "#A67B5B"],
    [0.75, "#5A4030"],
    [1.00, "#3E2C1F"],
]

# ---------------------------------------------------------
# Global CSS — brown / charcoal theme
# ---------------------------------------------------------
st.markdown(f"""
<style>
    /* ---- base ---- */
    html, body, [class*="css"] {{
        font-family: -apple-system, "Segoe UI", "Inter", "Helvetica Neue", sans-serif;
        color: {CHAR};
    }}
    .stApp {{
        background: linear-gradient(180deg, #F8F5F1 0%, #EEE9E2 100%);
    }}

    /* ---- header ---- */
    .main-header {{
        font-size: 2.1rem;
        font-weight: 700;
        color: {BROWN_DARK};
        letter-spacing: -0.02em;
        margin-bottom: 0.1rem;
        line-height: 1.15;
    }}
    .sub-header {{
        color: {STONE};
        font-size: 0.95rem;
        margin-bottom: 1.4rem;
    }}

    /* ---- section titles ---- */
    .section-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {BROWN_DARK};
        margin-top: 1.6rem;
        margin-bottom: 0.9rem;
        padding-bottom: 0.45rem;
        border-bottom: 2px solid {SAND};
        letter-spacing: -0.01em;
    }}

    /* ---- metric cards ---- */
    .metric-card {{
        background: linear-gradient(135deg, #FFFFFF 0%, #F7F3EE 100%);
        border-radius: 10px;
        padding: 1.1rem 1.2rem 1rem 1.2rem;
        border-left: 5px solid {BROWN};
        box-shadow: 0 2px 6px rgba(62, 44, 31, 0.07);
        height: 100%;
    }}
    .metric-label {{
        font-size: 0.72rem;
        color: {STONE};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
    }}
    .metric-value {{
        font-size: 1.55rem;
        font-weight: 700;
        color: {BROWN_DARK};
        margin-top: 0.25rem;
        line-height: 1.1;
    }}
    .metric-sub {{
        font-size: 0.78rem;
        color: {STONE};
        margin-top: 0.2rem;
    }}

    /* ---- insight boxes ---- */
    .insight {{
        background: #FAF6F0;
        border-left: 4px solid {BROWN};
        border-radius: 6px;
        padding: 0.85rem 1.1rem;
        margin: 0.55rem 0;
        font-size: 0.93rem;
        color: #33261B;
        line-height: 1.55;
    }}
    .insight-warn {{
        background: #FDF6E9;
        border-left-color: {GOLD};
    }}
    .insight-note {{
        background: #F0ECE6;
        border-left-color: {STONE};
    }}

    /* ---- sidebar ---- */
    section[data-testid="stSidebar"] {{
        background: #EDE7DF;
        border-right: 1px solid {LINE_GRAY};
    }}
    section[data-testid="stSidebar"] h2 {{
        color: {BROWN_DARK};
        font-size: 1.05rem;
        letter-spacing: 0.02em;
    }}

    /* ---- nav radio ---- */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        padding: 0.45rem 0.6rem;
        border-radius: 6px;
        transition: background 0.15s ease;
        font-size: 0.93rem;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: #E3DBD0;
    }}

    /* ---- buttons ---- */
    .stDownloadButton button, .stButton button {{
        background: {BROWN};
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }}
    .stDownloadButton button:hover, .stButton button:hover {{
        background: {BROWN_DARK};
    }}

    /* ---- dataframe ---- */
    .stDataFrame {{ border-radius: 8px; overflow: hidden; }}

    /* ---- misc ---- */
    .hr-soft {{
        border: none;
        border-top: 1px solid {LINE_GRAY};
        margin: 1.5rem 0;
    }}
    .kicker {{
        display: inline-block;
        background: {SAND};
        color: {BROWN_DARK};
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.18rem 0.55rem;
        border-radius: 4px;
        margin-bottom: 0.4rem;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------
DEFAULT_FILE = "TSDK_South Africa.xlsx"

NOTE_PREF = {"A": 1, "P": 2, "E": 3, "I": 4, "U": 5, "V": 6}
NOTE_LABEL = {
    "A": "A · Observed value",
    "P": "P · Provisional",
    "E": "E · Estimated (modelled)",
    "I": "I · Imputed by reporting agency",
    "U": "U · Low reliability",
    "V": "V · Unvalidated",
}

POP_CODES = {
    "POP_TOT": "Total population",
    "POP_URB": "Urban share (%)",
    "POP_RUR": "Rural share (%)",
    "POP_GRO": "Population growth (%)",
}

GDP_CODES = {
    "GDP_TOT": "Total GDP",
    "GDP_AGR": "Agriculture",
    "GDP_CON": "Construction",
    "GDP_MIN": "Mining",
    "GDP_MAN": "Manufacturing",
    "GDP_SER": "Services",
    "GDP_ENE": "Energy",
    "GDP_GRO": "GDP growth (%)",
}

PASSENGER_MODES = {
    "ROAD_PA_CAR": "Road — Car",
    "ROAD_PA_MINIBU": "Road — Minibus taxi",
    "ROAD_PA_BUS": "Road — Bus",
    "ROAD_PA_MOTORC": "Road — Motorcycle",
    "ROAD_PA_MOV": "Road — Total",
    "RAIL_PA_TOTAL": "Rail — Total",
    "AVIA_PAOC": "Aviation — Total",
}

FREIGHT_MODES = {
    "ROAD_GO_NAT": "Road — Total",
    "ROAD_GO_LDV": "Road — Light duty",
    "ROAD_GO_MDV": "Road — Medium duty",
    "ROAD_GO_HDV": "Road — Heavy duty",
    "RAIL_GO_TOTAL": "Rail — Total",
    "AVIA_GONC": "Aviation — Total",
    "IWW_GO_NAT": "Inland waterways",
}

FLEET_CODES = {
    "ROAD_EQS_TOTAL": "Total fleet",
    "ROAD_EQS_CAR": "Cars",
    "ROAD_EQS_BUS": "Buses",
    "ROAD_EQS_MINIBU": "Minibuses",
    "ROAD_EQS_MOTORC": "Motorcycles",
    "ROAD_EQS_LDV": "Light-duty vehicles",
    "ROAD_EQS_HDV": "Heavy-duty vehicles",
}

ENERGY_INT_PKM = {
    "NRG_EIP_CARELEURB": "Car — Electric",
    "NRG_EIP_CARHYBURB": "Car — Hybrid",
    "NRG_EIP_CARPETURB": "Car — Petrol",
    "NRG_EIP_MINIBUPETURB": "Minibus — Petrol",
}

ENERGY_INT_VKM = {
    "NRG_EIV_MOTORC": "Motorcycle",
    "NRG_EIV_CAR": "Car",
    "NRG_EIV_MINIBU": "Minibus",
    "NRG_EIV_BUS": "Bus",
    "NRG_EIV_LDV": "Light-duty vehicle",
    "NRG_EIV_RAIL": "Rail",
}

LOAD_FACTORS = {
    "NRG_LF_CARURB": "Car (urban)",
    "NRG_LF_CARELEURB": "Car — Electric",
    "NRG_LF_CARHYBURB": "Car — Hybrid",
    "NRG_LF_CARPETURB": "Car — Petrol",
    "NRG_LF_MINIBUURB": "Minibus (urban)",
    "NRG_LF_MINIBUPETURB": "Minibus — Petrol",
    "NRG_LF_BUSDIEURB": "Bus — Diesel",
}

# ---------------------------------------------------------
# Plotly helpers
# ---------------------------------------------------------
def styled(fig, height=380, **layout_kwargs):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family="-apple-system, Segoe UI, sans-serif",
                  color=CHAR, size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor=BROWN,
                        font=dict(color=CHAR)),
        **layout_kwargs,
    )
    fig.update_xaxes(gridcolor=LINE_GRAY, linecolor=LINE_GRAY)
    fig.update_yaxes(gridcolor=LINE_GRAY, linecolor=LINE_GRAY)
    return fig

# ---------------------------------------------------------
# Loaders
# ---------------------------------------------------------
@st.cache_data(show_spinner="Loading Transport Starter Data Kit…")
def load_excel(source):
    if isinstance(source, (bytes, bytearray)):
        df = pd.read_excel(io.BytesIO(source), sheet_name="Data")
    else:
        df = pd.read_excel(source, sheet_name="Data")

    df = df.replace(["..", "...", "N/A", "n/a", "na", ""], np.nan)

    year_cols = []
    for c in df.columns:
        s = str(c).strip()
        if s.isdigit() and 1990 <= int(s) <= 2021:
            year_cols.append(c)
    year_cols = sorted(year_cols, key=lambda x: int(str(x)))

    for y in year_cols:
        df[y] = pd.to_numeric(df[y], errors="coerce")

    return df, [int(str(y)) for y in year_cols], year_cols

@st.cache_data(show_spinner=False)
def melt(df, year_cols):
    id_cols = [c for c in df.columns if c not in year_cols]
    long = df.melt(id_vars=id_cols, value_vars=year_cols,
                   var_name="Year", value_name="Value")
    long["Year"] = long["Year"].apply(lambda v: int(str(v)))
    return long.dropna(subset=["Value"]).reset_index(drop=True)

def get_series(long, data_code):
    sub = long[long["Data code"] == data_code].copy()
    if sub.empty:
        return pd.DataFrame(columns=["Year", "Value", "Notes", "Unit"])
    sub["_pref"] = sub["Notes"].map(NOTE_PREF).fillna(99)
    sub = sub.sort_values(["_pref", "Year"]).drop_duplicates("Year", keep="first")
    return sub.sort_values("Year")[["Year", "Value", "Notes", "Unit"]].reset_index(drop=True)

def latest_value(series):
    if series.empty:
        return None, None
    row = series.iloc[-1]
    return float(row["Value"]), int(row["Year"])

# ---------------------------------------------------------
# Small UI helpers
# ---------------------------------------------------------
def metric_card(label, value, sub=""):
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-sub">{sub}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

def insight(text, kind="default"):
    cls = {"default": "insight",
           "warn": "insight insight-warn",
           "note": "insight insight-note"}.get(kind, "insight")
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)

def section(title, kicker=None):
    if kicker:
        st.markdown(f'<div class="kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    st.markdown('<div class="main-header">South African Transport Analysis</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Efficiency & sustainability insights from the '
        'Climate Compatible Growth <i>Transport Starter Data Kit</i> '
        '&nbsp;·&nbsp; 1990 – 2021</div>',
        unsafe_allow_html=True,
    )

    # ---- Load ----
    df_raw, years_all, year_cols = None, None, None
    if Path(DEFAULT_FILE).exists():
        df_raw, years_all, year_cols = load_excel(DEFAULT_FILE)

    with st.sidebar:
        st.markdown("### Settings")

        if df_raw is None:
            st.warning("Data file not found — please upload the workbook.")
            up = st.file_uploader("Upload TSDK_South Africa.xlsx", type=["xlsx"])
            if up:
                df_raw, years_all, year_cols = load_excel(up.getvalue())
            else:
                st.stop()

        y_min, y_max = min(years_all), max(years_all)
        year_range = st.slider("Year range", y_min, y_max, (y_min, y_max))

        note_choices = [n for n in NOTE_LABEL if n in df_raw["Notes"].unique()]
        note_sel = st.multiselect(
            "Observation status",
            options=note_choices,
            default=[n for n in ["A", "P", "E", "I"] if n in note_choices],
            format_func=lambda n: NOTE_LABEL[n],
            help="A = observed · P = provisional · E = modelled · I = imputed. "
                 "Modelled values are ITF estimates, not national reporting.",
        )

        st.markdown("---")
        st.markdown("### Navigate")
        nav = st.radio(
            "",
            [
                "  Overview",
                "  Data Quality",
                "  Population & GDP",
                "  Passenger Transport",
                "  Freight Transport",
                "  Vehicle Fleet",
                "  Energy & Efficiency",
                "  Correlations",
                "  Key Findings",
                "  About & Sources",
            ],
        )

        st.markdown("---")
        st.caption(
            "Tan et al. (2023) · Transport Starter Data Kit · "
            "climatecompatiblegrowth.com/starter-kits"
        )

    long = melt(df_raw, year_cols)
    long = long[(long["Year"] >= year_range[0]) & (long["Year"] <= year_range[1])]
    if note_sel:
        long = long[long["Notes"].isin(note_sel)]

    pages = {
        "  Overview": view_overview,
        "  Data Quality": view_data_quality,
        "  Population & GDP": view_pop_gdp,
        "  Passenger Transport": view_passenger,
        "  Freight Transport": view_freight,
        "  Vehicle Fleet": view_fleet,
        "  Energy & Efficiency": view_energy,
        "  Correlations": view_correlations,
        "  Key Findings": view_findings,
        "  About & Sources": view_about,
    }
    pages[nav](df_raw, long, years_all)


# ---------------------------------------------------------
# Views
# ---------------------------------------------------------
def view_overview(df_raw, long, years_all):
    section("Overview", "At a glance")

    pop = get_series(long, "POP_TOT")
    gdp = get_series(long, "GDP_TOT")
    pop_v, pop_y = latest_value(pop)
    gdp_v, gdp_y = latest_value(gdp)
    pop0 = float(pop.iloc[0]["Value"]) if not pop.empty else None
    gdp0 = float(gdp.iloc[0]["Value"]) if not gdp.empty else None

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Population",
                    f"{pop_v:.1f} M" if pop_v else "—",
                    f"Latest year: {pop_y}" if pop_y else "")
    with c2:
        metric_card("GDP (constant 2015 US$)",
                    f"{gdp_v/1e6:.2f} T" if gdp_v and gdp_v > 1e6 else f"{gdp_v:,.0f} M",
                    f"Latest year: {gdp_y}" if gdp_y else "")
    with c3:
        g = ((pop_v - pop0) / pop0 * 100) if pop0 else None
        metric_card("Population change",
                    f"{g:+.1f}%" if g is not None else "—",
                    f"{years_all[0]} → {pop_y}" if pop_y else "")
    with c4:
        g = ((gdp_v - gdp0) / gdp0 * 100) if gdp0 else None
        metric_card("GDP change",
                    f"{g:+.1f}%" if g is not None else "—",
                    f"{years_all[0]} → {gdp_y}" if gdp_y else "")

    section("Modal split — passenger and freight", "Snapshot")

    pass_rows = []
    for code, label in PASSENGER_MODES.items():
        s = get_series(long, code)
        v, y = latest_value(s)
        if v:
            pass_rows.append({"Mode": label, "Value": v, "Year": y})
    pass_df = pd.DataFrame(pass_rows).sort_values("Value")

    fr_rows = []
    for code, label in FREIGHT_MODES.items():
        s = get_series(long, code)
        v, y = latest_value(s)
        if v:
            fr_rows.append({"Mode": label, "Value": v, "Year": y})
    fr_df = pd.DataFrame(fr_rows).sort_values("Value")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Passenger activity — latest per mode**")
        if not pass_df.empty:
            fig = px.bar(pass_df, x="Value", y="Mode", orientation="h",
                         text="Year", color="Mode",
                         color_discrete_sequence=CATEGORICAL_COLORS)
            fig.update_traces(textposition="outside",
                              textfont=dict(color=BROWN_DARK, size=11))
            fig.update_layout(showlegend=False)
            st.plotly_chart(styled(fig, 340), use_container_width=True)
        else:
            st.info("No passenger data in the selected filter.")

    with col2:
        st.markdown("**Freight activity — latest per mode**")
        if not fr_df.empty:
            fig = px.bar(fr_df, x="Value", y="Mode", orientation="h",
                         text="Year", color="Mode",
                         color_discrete_sequence=CATEGORICAL_COLORS)
            fig.update_traces(textposition="outside",
                              textfont=dict(color=BROWN_DARK, size=11))
            fig.update_layout(showlegend=False)
            st.plotly_chart(styled(fig, 340), use_container_width=True)
        else:
            st.info("No freight data in the selected filter.")

    insight(
        "Data years are <b>not aligned across modes</b>: UCT's 2006 bottom-up "
        "study underpins most modal splits, while UN DESA's modelled estimates "
        "cover 2018. Each bar carries its year label — read them as snapshots, "
        "not as a single-year total.",
        kind="warn",
    )

def view_data_quality(df_raw, long, years_all):
    section("Observation status (SDMX)", "Provenance")

    counts = long["Notes"].value_counts().rename_axis("Note").reset_index(name="Records")
    counts["Meaning"] = counts["Note"].map(NOTE_LABEL).fillna(counts["Note"])
    st.dataframe(counts, use_container_width=True, hide_index=True)

    section("Coverage heatmap — records per variable per year", "Density")
    year_cols_all = [c for c in df_raw.columns if str(c).strip().isdigit()]
    cov = (df_raw.melt(id_vars=["Variable"], value_vars=year_cols_all,
                       var_name="Year", value_name="Value")
           .dropna(subset=["Value"])
           .groupby(["Variable", "Year"]).size().unstack(fill_value=0))
    if not cov.empty:
        fig = px.imshow(cov, aspect="auto", color_continuous_scale=BROWN_SCALE,
                        labels=dict(x="Year", y="Variable", color="records"))
        fig.update_layout(height=max(300, 40 * len(cov)))
        st.plotly_chart(styled(fig, max(300, 40 * len(cov))),
                        use_container_width=True)
    else:
        st.info("No data available with the current filters.")

    section("Data caveats", "Notes for the reader")
    insight(
        "Construction, Mining and Energy GDP shares are <b>estimated (E)</b>. "
        "After subtracting agriculture, manufacturing and services from 100%, "
        "the residual is split evenly across the three remaining sectors — they "
        "should not be treated as independent observations.",
        kind="warn",
    )
    insight(
        "The vehicle-fleet series contains a <b>definitional break</b> between "
        "UCT (2006) and IRF (2015–2020). The jump from ≈5.7 M to ≈10.3 M "
        "vehicles is a change of scope, not organic growth.",
        kind="warn",
    )
    insight(
        "UN DESA modelled values (Note = I) are ITF model estimates, not "
        "nationally reported. Use the status filter to isolate observed data "
        "when precision matters.",
        kind="note",
    )

def view_pop_gdp(df_raw, long, years_all):
    section("Population", "Demographics")
    pop = get_series(long, "POP_TOT")
    urb = get_series(long, "POP_URB")
    rur = get_series(long, "POP_RUR")

    if not pop.empty:
        fig = px.area(pop, x="Year", y="Value",
                      color_discrete_sequence=[BROWN])
        fig.update_traces(line=dict(width=2.5))
        st.plotly_chart(styled(fig, 320, yaxis_title="Million people"),
                        use_container_width=True)

    if not urb.empty and not rur.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=urb["Year"], y=urb["Value"], mode="lines+markers",
                                 name="Urban %",
                                 line=dict(color=BROWN, width=2.5)))
        fig.add_trace(go.Scatter(x=rur["Year"], y=rur["Value"], mode="lines+markers",
                                 name="Rural %",
                                 line=dict(color=TAN, width=2.5)))
        st.plotly_chart(styled(fig, 300, yaxis_title="Share of population (%)"),
                        use_container_width=True)

    section("GDP", "Economy")
    gdp = get_series(long, "GDP_TOT")
    if not gdp.empty:
        fig = px.area(gdp, x="Year", y="Value",
                      color_discrete_sequence=[BROWN_MID])
        fig.update_traces(line=dict(width=2.5))
        st.plotly_chart(styled(fig, 320, yaxis_title="Million USD (constant 2015)"),
                        use_container_width=True)

    st.markdown("**GDP composition by sector (% of GDP)**")
    rows = []
    for code, label in GDP_CODES.items():
        if code in ("GDP_TOT", "GDP_GRO"):
            continue
        s = get_series(long, code)
        if s.empty:
            continue
        s = s.copy()
        s["Sector"] = label
        rows.append(s)
    if rows:
        df = pd.concat(rows, ignore_index=True)
        fig = px.area(df, x="Year", y="Value", color="Sector",
                      color_discrete_sequence=CATEGORICAL_COLORS)
        st.plotly_chart(styled(fig, 380, yaxis_title="% of GDP"),
                        use_container_width=True)
    else:
        st.info("No sector GDP data in the selection.")

def view_passenger(df_raw, long, years_all):
    section("Passenger activity by mode", "Million passenger-km")

    rows = []
    for code, label in PASSENGER_MODES.items():
        s = get_series(long, code)
        if s.empty:
            continue
        s = s.copy()
        s["Mode"] = label
        rows.append(s)
    df = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    if df.empty:
        st.info("No passenger data under the current filters.")
        return

    fig = px.line(df, x="Year", y="Value", color="Mode", markers=True,
                  color_discrete_sequence=CATEGORICAL_COLORS)
    fig.update_traces(line=dict(width=2.2))
    st.plotly_chart(styled(fig, 420, yaxis_title="Million passenger-km",
                           hovermode="x unified"),
                    use_container_width=True)

    section("Latest snapshot per mode", "Cross-section")
    latest = df.loc[df.groupby("Mode")["Year"].idxmax()].sort_values("Value")
    fig2 = px.bar(latest, x="Value", y="Mode", orientation="h",
                  color="Mode", text="Year",
                  color_discrete_sequence=CATEGORICAL_COLORS)
    fig2.update_traces(textposition="outside",
                       textfont=dict(color=BROWN_DARK, size=11))
    fig2.update_layout(showlegend=False)
    st.plotly_chart(styled(fig2, 340, xaxis_title="Million passenger-km"),
                    use_container_width=True)

    total = latest["Value"].sum()
    if total > 0:
        latest["Share %"] = latest["Value"] / total * 100
        st.dataframe(
            latest[["Mode", "Year", "Value", "Share %", "Notes"]]
            .rename(columns={"Value": "million passenger-km"})
            .round({"million passenger-km": 1, "Share %": 1})
            .sort_values("million passenger-km", ascending=False),
            use_container_width=True, hide_index=True,
        )

    insight(
        "Road dominates passenger activity. Using UCT (2006): minibus taxis "
        "alone move ≈117,400 M passenger-km — nearly as much as private cars "
        "(≈116,100 M) — while making up only about 5% of the vehicle fleet.",
    )

def view_freight(df_raw, long, years_all):
    section("Freight activity by mode", "Million tonne-km")

    rows = []
    for code, label in FREIGHT_MODES.items():
        s = get_series(long, code)
        if s.empty:
            continue
        s = s.copy()
        s["Mode"] = label
        rows.append(s)
    df = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    if df.empty:
        st.info("No freight data under the current filters.")
        return

    fig = px.line(df, x="Year", y="Value", color="Mode", markers=True,
                  color_discrete_sequence=CATEGORICAL_COLORS)
    fig.update_traces(line=dict(width=2.2))
    st.plotly_chart(styled(fig, 420, yaxis_title="Million tonne-km",
                           hovermode="x unified"),
                    use_container_width=True)

    latest = df.loc[df.groupby("Mode")["Year"].idxmax()].sort_values("Value")
    fig2 = px.bar(latest, x="Value", y="Mode", orientation="h",
                  color="Mode", text="Year",
                  color_discrete_sequence=CATEGORICAL_COLORS)
    fig2.update_traces(textposition="outside",
                       textfont=dict(color=BROWN_DARK, size=11))
    fig2.update_layout(showlegend=False)
    st.plotly_chart(styled(fig2, 340, xaxis_title="Million tonne-km"),
                    use_container_width=True)

    road = get_series(long, "ROAD_GO_NAT")
    rail = get_series(long, "RAIL_GO_TOTAL")
    road_v, road_y = latest_value(road)
    rail_v, rail_y = latest_value(rail)

    if road_v and rail_v:
        section("Road vs rail share", "Modal balance")
        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Road freight", f"{road_v:,.0f} M", f"tonne-km · {road_y}")
        with c2:
            metric_card("Rail freight", f"{rail_v:,.0f} M", f"tonne-km · {rail_y}")
        with c3:
            metric_card("Rail share", f"{rail_v / (road_v + rail_v) * 100:.1f}%",
                        "of road + rail total")

        insight(
            "Road freight carries roughly <b>60%</b> of the road+rail total in "
            "the latest year on record — a striking modal imbalance for a "
            "country with an extensive rail network. Rail is the single largest "
            "decarbonisation lever for South African freight.",
        )

def view_fleet(df_raw, long, years_all):
    section("Vehicle stock", "Fleet overview")

    rows = []
    for code, label in FLEET_CODES.items():
        s = get_series(long, code)
        if s.empty:
            continue
        s = s.copy()
        s["Mode"] = label
        rows.append(s)
    df = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    if df.empty:
        st.info("No vehicle stock data under the current filters.")
        return

    fig = px.line(df, x="Year", y="Value", color="Mode", markers=True,
                  color_discrete_sequence=CATEGORICAL_COLORS)
    fig.update_traces(line=dict(width=2.2))
    st.plotly_chart(styled(fig, 420, yaxis_title="Vehicles",
                           hovermode="x unified"),
                    use_container_width=True)

    total = get_series(long, "ROAD_EQS_TOTAL")
    if not total.empty:
        c1, c2 = st.columns(2)
        first, last = total.iloc[0], total.iloc[-1]
        with c1:
            metric_card("Fleet — first year",
                        f"{first['Value']:,.0f}",
                        f"Year {first['Year']}")
        with c2:
            metric_card("Fleet — latest year",
                        f"{last['Value']:,.0f}",
                        f"Year {last['Year']}")

        if abs(last["Value"] / first["Value"] - 1) > 0.5:
            insight(
                f"Fleet size appears to jump from <b>{first['Value']:,.0f}</b> "
                f"to <b>{last['Value']:,.0f}</b>. This is a definitional break "
                "(UCT bottom-up model vs IRF World Road Statistics) — treat the "
                "2006 and 2015+ series as separate observations, not a growth "
                "trend.",
                kind="warn",
            )

    section("Latest fleet composition", "By vehicle type")
    latest = df.loc[df.groupby("Mode")["Year"].idxmax()].sort_values("Value")
    fig2 = px.bar(latest, x="Value", y="Mode", orientation="h",
                  color="Mode", text="Year",
                  color_discrete_sequence=CATEGORICAL_COLORS)
    fig2.update_traces(textposition="outside",
                       textfont=dict(color=BROWN_DARK, size=11))
    fig2.update_layout(showlegend=False)
    st.plotly_chart(styled(fig2, 340, xaxis_title="Vehicles"),
                    use_container_width=True)

def view_energy(df_raw, long, years_all):
    section("Energy intensity", "MJ per passenger-km")

    rows = []
    for code, label in ENERGY_INT_PKM.items():
        s = get_series(long, code)
        if s.empty:
            continue
        s = s.copy()
        s["Vehicle"] = label
        rows.append(s)
    if rows:
        df = pd.concat(rows, ignore_index=True)
        fig = px.bar(df, x="Vehicle", y="Value", color="Vehicle",
                     text="Year", color_discrete_sequence=CATEGORICAL_COLORS,
                     labels={"Value": "MJ / passenger-km"})
        fig.update_traces(textposition="outside",
                          textfont=dict(color=BROWN_DARK, size=11))
        fig.update_layout(showlegend=False)
        st.plotly_chart(styled(fig, 340), use_container_width=True)

        ev = get_series(long, "NRG_EIP_CARELEURB")["Value"].mean()
        pe = get_series(long, "NRG_EIP_CARPETURB")["Value"].mean()
        hy = get_series(long, "NRG_EIP_CARHYBURB")["Value"].mean()
        if pd.notna(ev) and pd.notna(pe) and pe > 0:
            saving = (pe - ev) / pe * 100
            metric_card("EV vs petrol energy saving", f"{saving:.0f}%",
                        f"hybrid sits at {hy:.2f} MJ/pkm")
            insight(
                f"Electric cars use <b>{ev:.2f} MJ/passenger-km</b> vs "
                f"<b>{pe:.2f}</b> for petrol ({hy:.2f} for hybrid). "
                f"Electrification alone cuts car energy intensity by "
                f"≈<b>{saving:.0f}%</b>, before grid decarbonisation.",
            )

    section("Energy intensity — per vehicle-km", "MJ per vehicle-km")
    rows = []
    for code, label in ENERGY_INT_VKM.items():
        s = get_series(long, code)
        if s.empty:
            continue
        s = s.copy()
        s["Vehicle"] = label
        rows.append(s)
    if rows:
        df2 = pd.concat(rows, ignore_index=True)
        fig = px.bar(df2, x="Vehicle", y="Value", color="Vehicle",
                     text="Year", color_discrete_sequence=CATEGORICAL_COLORS,
                     labels={"Value": "MJ / vehicle-km"})
        fig.update_traces(textposition="outside",
                          textfont=dict(color=BROWN_DARK, size=11))
        fig.update_layout(showlegend=False)
        st.plotly_chart(styled(fig, 340), use_container_width=True)

    section("Load factors", "Passengers per vehicle")
    rows = []
    for code, label in LOAD_FACTORS.items():
        s = get_series(long, code)
        if s.empty:
            continue
        s = s.copy()
        s["Vehicle"] = label
        rows.append(s)
    if rows:
        df3 = pd.concat(rows, ignore_index=True)
        fig = px.bar(df3, x="Vehicle", y="Value", color="Vehicle",
                     text="Year", color_discrete_sequence=CATEGORICAL_COLORS,
                     labels={"Value": "passengers / vehicle"})
        fig.update_traces(textposition="outside",
                          textfont=dict(color=BROWN_DARK, size=11))
        fig.update_layout(showlegend=False)
        st.plotly_chart(styled(fig, 340), use_container_width=True)

def view_correlations(df_raw, long, years_all):
    section("GDP and population", "Trend relationship")

    pop = get_series(long, "POP_TOT")[["Year", "Value"]].rename(columns={"Value": "Population"})
    gdp = get_series(long, "GDP_TOT")[["Year", "Value"]].rename(columns={"Value": "GDP"})
    merged = pd.merge(pop, gdp, on="Year", how="inner")

    if len(merged) < 3:
        st.info("Not enough overlapping years to compute correlations.")
        return

    fig = px.scatter(merged, x="Population", y="GDP", color="Year",
                     color_continuous_scale=BROWN_SCALE,
                     trendline="ols",
                     trendline_color_override=BROWN)
    st.plotly_chart(styled(fig, 420), use_container_width=True)

    corr = merged[["GDP", "Population"]].corr().iloc[0, 1]
    metric_card("Pearson correlation (GDP ↔ Population)", f"{corr:.3f}",
                "Both trend upward over 30+ years")

    insight(
        f"A correlation of <b>{corr:.2f}</b> is expected because both variables "
        "trend upward over the period — it does <i>not</i> imply that population "
        "growth caused GDP growth. For causal inference you would need "
        "instrumental variables or panel methods.",
        kind="warn",
    )

    section("Year-on-year GDP change", "Volatility")
    gdp2 = get_series(long, "GDP_TOT").copy()
    gdp2["YoY %"] = gdp2["Value"].pct_change() * 100
    colors = [BROWN if v >= 0 else GOLD for v in gdp2["YoY %"]]
    fig = go.Figure(go.Bar(x=gdp2["Year"], y=gdp2["YoY %"],
                           marker_color=colors))
    st.plotly_chart(styled(fig, 320, yaxis_title="% change"),
                    use_container_width=True)

    section("Correlation matrix", "Available yearly series")
    keys = ["POP_TOT", "GDP_TOT", "ROAD_PA_MOV", "RAIL_PA_TOTAL",
            "ROAD_GO_NAT", "RAIL_GO_TOTAL", "ROAD_EQS_TOTAL"]
    cols = {}
    for k in keys:
        s = get_series(long, k)
        if not s.empty:
            cols[k] = s.set_index("Year")["Value"]
    if len(cols) >= 2:
        mat = pd.DataFrame(cols).corr()
        fig = px.imshow(mat, text_auto=".2f",
                        color_continuous_scale="RdYlBu_r",
                        zmin=-1, zmax=1, aspect="auto")
        st.plotly_chart(styled(fig, 430), use_container_width=True)


def view_findings(df_raw, long, years_all):
    section("Key findings", "Summary of the data")

    pop = get_series(long, "POP_TOT")
    gdp = get_series(long, "GDP_TOT")

    if len(pop) >= 2:
        p0, p1 = pop.iloc[0], pop.iloc[-1]
        insight(
            f"<b>Population</b> grew from <b>{p0['Value']:.1f} M</b> "
            f"({p0['Year']}) to <b>{p1['Value']:.1f} M</b> ({p1['Year']}), "
            f"a change of <b>{(p1['Value'] - p0['Value']) / p0['Value'] * 100:+.1f}%</b>."
        )
    if len(gdp) >= 2:
        g0, g1 = gdp.iloc[0], gdp.iloc[-1]
        insight(
            f"<b>GDP</b> (constant 2015 USD) grew from "
            f"<b>{g0['Value']:,.0f} M</b> ({g0['Year']}) to "
            f"<b>{g1['Value']:,.0f} M</b> ({g1['Year']}), a change of "
            f"<b>{(g1['Value'] - g0['Value']) / g0['Value'] * 100:+.1f}%</b>."
        )

    pass_rows = []
    for code, label in PASSENGER_MODES.items():
        s = get_series(long, code)
        v, y = latest_value(s)
        if v:
            pass_rows.append((label, v, y))
    if pass_rows:
        pass_rows.sort(key=lambda r: r[1], reverse=True)
        top = pass_rows[0]
        insight(
            f"<b>{top[0]}</b> is the largest passenger mode in the dataset "
            f"(<b>{top[1]:,.0f} M passenger-km</b>, {top[2]}). Minibus taxis "
            "carry a large share of passenger-km with a small share of the "
            "fleet — a clear efficiency lever."
        )

    road = get_series(long, "ROAD_GO_NAT")
    rail = get_series(long, "RAIL_GO_TOTAL")
    rv, ry = latest_value(road)
    lv, ly = latest_value(rail)
    if rv and lv:
        insight(
            f"<b>Road freight</b> carries <b>{rv:,.0f} M tonne-km</b> "
            f"(latest year {ry}) while <b>rail</b> carries <b>{lv:,.0f} M</b> "
            f"({ly}). Rail's share of the road+rail total is only "
            f"≈<b>{lv / (rv + lv) * 100:.0f}%</b> — well below what a "
            "1.5 °C-aligned freight strategy would require."
        )

    ev = get_series(long, "NRG_EIP_CARELEURB")
    pe = get_series(long, "NRG_EIP_CARPETURB")
    if not ev.empty and not pe.empty:
        saving = (pe["Value"].iloc[0] - ev["Value"].iloc[0]) / pe["Value"].iloc[0] * 100
        insight(
            f"<b>Electric cars</b> consume <b>{ev['Value'].iloc[0]:.2f} MJ/passenger-km</b> "
            f"vs <b>{pe['Value'].iloc[0]:.2f}</b> for petrol — a "
            f"<b>{saving:.0f}%</b> energy saving before grid decarbonisation."
        )

    section("Recommendations", "Strategic priorities")

    recs = [
        ("Rebalance freight toward rail",
         "Road freight carries the majority of tonne-km on a network with an "
         "extensive rail alternative. Rail's energy intensity per tonne-km is "
         "an order of magnitude lower — expanding its share is the single "
         "biggest decarbonisation lever in the sector."),
        ("Modernise and electrify the minibus fleet",
         "Minibus taxis move a disproportionate share of passengers. "
         "Electrifying this segment, paired with grid decarbonisation, "
         "delivers outsized efficiency gains because of high utilisation and "
         "load factors."),
        ("Accelerate private-vehicle electrification",
         "Electric cars already show roughly a 75% energy-intensity reduction "
         "versus petrol per passenger-km. Purchase incentives and urban "
         "charging roll-out are the two levers that convert this potential."),
        ("Close transport data gaps",
         "The starter kit relies on 2006 UCT and 2018 UN DESA estimates for "
         "most transport indicators. An annual national transport survey would "
         "let decarbonisation scenarios rest on observed, not modelled, "
         "baselines."),
        ("Use observation status in modelling",
         "Observed (A) and modelled (I/E) values are not interchangeable. "
         "Scenario builders should explicitly flag which figures underpin "
         "their baselines."),
    ]
    for i, (title, body) in enumerate(recs, 1):
        st.markdown(
            f"<div class='insight'>"
            f"<b>{i}. {title}.</b> {body}"
            f"</div>",
            unsafe_allow_html=True,
        )


def view_about(df_raw, long, years_all):
    section("About this dashboard", "Overview")
    st.markdown("""
This dashboard provides an interactive view of the **Climate Compatible Growth
Transport Starter Data Kit** for South Africa. It reproduces the accompanying
Jupyter analysis in a shareable, filter-driven interface.

#### Suggested citation
> Tan, N., Ambunda, R., Medimorec, N., Cortez, A., Krapp, A., Maxwell, E.,
> Harrison, J., Howells, M. (2023). *Transport Starter Data Kit*.
> [climatecompatiblegrowth.com/starter-kits](https://climatecompatiblegrowth.com/starter-kits/)

#### Primary data sources
- **World Bank** — World Development Indicators (population, GDP)
- **University of Cape Town** (Merven et al., 2012) — bottom-up transport
  model for 2006 (passenger, freight, fleet, energy intensity, load factors)
- **Stellenbosch University** (Havenga et al., 2016) — Logistics Barometer
  (road / rail freight, 2013–2014; corridor / metro / rural split)
- **UN DESA** (2020) — SDG Indicator 9.1.2 modelled passenger & freight activity
- **UIC** — Rail Information System (Railisa)
- **IRF World Road Statistics** — vehicle fleet, 2015–2020
- **Kane (2016)**, **Venter & Mohammed (2013)** — energy intensity, load factors

#### Observation status
- `A` — observed (national report or authoritative source)
- `P` — provisional
- `E` — estimated (modelled)
- `I` — imputed by reporting agency (e.g. UN DESA model outputs)

#### Limitations
- Sparse coverage: most transport indicators have 1–3 data points.
- Mixed sources and vintages (2006, 2013–2014, 2018, 2020–2021).
- Some values are modelled, not observed.
- Fleet series contains a source discontinuity between 2006 and 2015+.
- Correlation does not establish causation.
""")

    section("Export filtered data", "Download")
    csv = long.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️  Download CSV", data=csv,
                       file_name="sa_transport_filtered.csv",
                       mime="text/csv")


# ---------------------------------------------------------
if __name__ == "__main__":
    main()
