import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import io
import math
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Event Ticket Tracker",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS (matches HTML design) ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg: #08080f;
    --surface: #0f0f1a;
    --card: #141424;
    --border: rgba(255,255,255,0.07);
    --neon: #c8f53d;
    --cyan: #38e8c8;
    --purple: #a855f7;
    --pink: #f53d8f;
    --text: #e8e8f0;
    --muted: #6a6a8a;
    --vip: #f5c842;
    --premium: #a855f7;
    --general: #38e8c8;
    --balcony: #f53d8f;
}

html, body, .stApp {
    background-color: #08080f !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0f0f1a !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] * { color: #e8e8f0 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput > div > div > input,
[data-testid="stSidebar"] .stTextArea > div > div > textarea {
    background-color: #141424 !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #e8e8f0 !important;
}

/* Main area */
[data-testid="stMain"] {
    background-color: #08080f !important;
}
.block-container {
    padding: 2rem 2rem 4rem !important;
    max-width: 1200px !important;
}

/* Header */
.tracker-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.label-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(200,245,61,0.1);
    border: 1px solid rgba(200,245,61,0.3);
    color: #c8f53d;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 14px;
    letter-spacing: 1px;
}
.tracker-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(42px, 5vw, 64px);
    line-height: 0.9;
    letter-spacing: 2px;
    color: #e8e8f0;
    margin: 0;
}
.tracker-title span { color: #c8f53d; }
.tracker-sub {
    color: #6a6a8a;
    font-size: 13px;
    margin-top: 10px;
    font-weight: 300;
}
.header-right {
    text-align: right;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #6a6a8a;
    line-height: 2;
}
.header-right strong { color: #c8f53d; display: block; font-size: 13px; }

/* Stat Cards */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 14px;
    margin-bottom: 24px;
}
@media(max-width:800px){ .stats-row{ grid-template-columns: repeat(2,1fr); } }
.stat-card {
    background: #141424;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 22px 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.25s, border-color 0.25s;
}
.stat-card:hover { transform: translateY(-3px); border-color: rgba(255,255,255,0.15); }
.stat-card::before {
    content:'';
    position:absolute;
    top:0;left:0;right:0;
    height:2px;
}
.stat-card.c-neon::before { background:#c8f53d; }
.stat-card.c-pink::before { background:#f53d8f; }
.stat-card.c-cyan::before { background:#38e8c8; }
.stat-card.c-purple::before { background:#a855f7; }
.stat-icon { font-size: 22px; margin-bottom: 10px; }
.stat-label { font-size: 10px; color: #6a6a8a; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 6px; font-family: 'Space Mono', monospace; }
.stat-value { font-family: 'Bebas Neue', sans-serif; font-size: 38px; line-height: 1; }
.stat-card.c-neon .stat-value { color: #c8f53d; }
.stat-card.c-pink .stat-value { color: #f53d8f; }
.stat-card.c-cyan .stat-value { color: #38e8c8; }
.stat-card.c-purple .stat-value { color: #a855f7; }
.stat-sub { font-size: 10px; color: #6a6a8a; margin-top: 5px; font-family: 'Space Mono', monospace; }

/* Early Bird Banner */
.eb-banner {
    background: linear-gradient(135deg, rgba(200,245,61,0.08), rgba(56,232,200,0.08));
    border: 1px solid rgba(200,245,61,0.2);
    border-radius: 14px;
    padding: 18px 24px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
}
.eb-active { border-color: rgba(200,245,61,0.35); }
.eb-disabled {
    background: linear-gradient(135deg, rgba(245,61,143,0.08), rgba(168,85,247,0.08)) !important;
    border-color: rgba(245,61,143,0.3) !important;
}
.eb-text { font-size: 13px; color: #e8e8f0; }
.eb-text strong { color: #c8f53d; font-family: 'Space Mono', monospace; }
.eb-disabled .eb-text strong { color: #f53d8f; }
.eb-badge-active {
    display: inline-block;
    background: rgba(200,245,61,0.15);
    color: #c8f53d;
    border: 1px solid rgba(200,245,61,0.4);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 10px;
    font-family: 'Space Mono', monospace;
    letter-spacing: 1px;
}
.eb-badge-disabled {
    display: inline-block;
    background: rgba(245,61,143,0.12);
    color: #f53d8f;
    border: 1px solid rgba(245,61,143,0.35);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 10px;
    font-family: 'Space Mono', monospace;
    letter-spacing: 1px;
}
.eb-progress-wrap { flex: 1; min-width: 220px; max-width: 320px; }
.eb-progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 9px;
    color: #6a6a8a;
    font-family: 'Space Mono', monospace;
    margin-bottom: 6px;
}
.eb-bar-track {
    height: 8px;
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    overflow: hidden;
}
.eb-bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #c8f53d, #38e8c8);
    transition: width 0.8s ease;
}
.eb-bar-fill-exceeded {
    background: linear-gradient(90deg, #f53d8f, #a855f7);
}

/* Panel */
.panel {
    background: #141424;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 20px;
}
.panel-title {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #6a6a8a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-title::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #c8f53d;
    display: inline-block;
    flex-shrink: 0;
}

/* Section bars */
.section-item { margin-bottom: 16px; }
.section-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 7px; }
.section-name { font-size: 13px; font-weight: 500; display: flex; align-items: center; gap: 7px; }
.section-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.section-stats { font-size: 11px; color: #6a6a8a; font-family: 'Space Mono', monospace; }
.bar-track { height: 6px; background: rgba(255,255,255,0.06); border-radius: 10px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 10px; }

/* Revenue cards */
.rev-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-top: 4px;
}
@media(max-width:700px){ .rev-grid{ grid-template-columns: repeat(2,1fr); } }
.rev-card {
    background: #0f0f1a;
    border-radius: 12px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.07);
    transition: transform 0.2s;
}
.rev-card:hover { transform: translateY(-2px); }
.rev-section-name {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: 'Space Mono', monospace;
    color: #6a6a8a;
}
.rev-amount { font-family: 'Bebas Neue', sans-serif; font-size: 28px; margin-bottom: 4px; }
.rev-meta { font-size: 10px; color: #6a6a8a; font-family: 'Space Mono', monospace; }
.rev-total-row {
    margin-top: 18px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.07);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}
.rev-total-label { font-family: 'Space Mono', monospace; font-size: 11px; color: #6a6a8a; }
.rev-total-val { font-family: 'Bebas Neue', sans-serif; font-size: 44px; color: #c8f53d; line-height: 1; }

/* Seat map */
.seat-map-wrap {
    overflow-x: auto;
    padding: 10px 0;
}
.seat-grid {
    display: flex;
    flex-direction: column;
    gap: 4px;
    width: max-content;
    margin: 0 auto;
}
.seat-row { display: flex; gap: 4px; align-items: center; }
.seat-row-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #6a6a8a;
    width: 30px;
    flex-shrink: 0;
    text-align: right;
    margin-right: 4px;
}
.seat {
    width: 18px;
    height: 18px;
    border-radius: 3px;
    display: inline-block;
    border: 1px solid rgba(255,255,255,0.05);
    transition: transform 0.15s;
    cursor: default;
}
.seat:hover { transform: scale(1.3); z-index: 2; position: relative; }
.seat-legend {
    display: flex;
    gap: 20px;
    margin-top: 14px;
    flex-wrap: wrap;
}
.seat-legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-family: 'Space Mono', monospace;
    color: #6a6a8a;
}
.seat-legend-dot {
    width: 12px;
    height: 12px;
    border-radius: 2px;
    display: inline-block;
}

/* Ticket table */
.ticket-row-html {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border-radius: 10px;
    margin-bottom: 5px;
    border: 1px solid transparent;
    transition: all 0.15s;
    cursor: default;
}
.ticket-row-html:hover { background: rgba(255,255,255,0.02); border-color: rgba(255,255,255,0.07); }
.t-id { font-family: 'Space Mono', monospace; font-size: 11px; color: #6a6a8a; width: 42px; flex-shrink:0; }
.t-sect { font-size: 12px; font-weight: 500; flex:1; display: flex; align-items: center; gap: 6px; }
.t-price { font-family: 'Space Mono', monospace; font-size: 12px; color: #c8f53d; }
.t-mode { font-size: 10px; color: #6a6a8a; font-family: 'Space Mono', monospace; }
.badge-sold {
    display: inline-block;
    background: rgba(245,61,143,0.12);
    color: #f53d8f;
    border: 1px solid rgba(245,61,143,0.3);
    border-radius: 100px;
    padding: 3px 9px;
    font-size: 9px;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
}
.badge-avail {
    display: inline-block;
    background: rgba(56,232,200,0.1);
    color: #38e8c8;
    border: 1px solid rgba(56,232,200,0.3);
    border-radius: 100px;
    padding: 3px 9px;
    font-size: 9px;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
}

/* Python concepts strip */
.py-strip {
    background: #0f0f1a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 24px;
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.py-concept { flex: 1; min-width: 150px; }
.py-label {
    font-size: 9px;
    color: #6a6a8a;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
    font-family: 'Space Mono', monospace;
}
.py-value { font-size: 13px; color: #e8e8f0; font-weight: 500; }
.py-code {
    background: rgba(200,245,61,0.1);
    color: #c8f53d;
    padding: 2px 7px;
    border-radius: 5px;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
}

/* Chat messages */
.chat-msg {
    margin-bottom: 12px;
    display: flex;
    gap: 10px;
    align-items: flex-start;
}
.chat-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}
.chat-avatar-user { background: rgba(200,245,61,0.15); }
.chat-avatar-bot { background: rgba(56,232,200,0.12); }
.chat-bubble {
    background: #141424;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 13px;
    color: #e8e8f0;
    line-height: 1.6;
    max-width: 100%;
}
.chat-bubble-user { background: rgba(200,245,61,0.08); border-color: rgba(200,245,61,0.15); }

/* Divider */
.neon-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(200,245,61,0.2), transparent);
    margin: 24px 0;
}

/* Streamlit overrides */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(200,245,61,0.4) !important;
    color: #c8f53d !important;
    border-radius: 100px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    padding: 6px 18px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(200,245,61,0.1) !important;
    border-color: #c8f53d !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #141424 !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #e8e8f0 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(200,245,61,0.4) !important;
    box-shadow: 0 0 0 1px rgba(200,245,61,0.15) !important;
}
.stSelectbox > div > div {
    background: #141424 !important;
    border-color: rgba(255,255,255,0.1) !important;
    color: #e8e8f0 !important;
    border-radius: 10px !important;
}
.stFileUploader {
    background: #141424 !important;
    border-color: rgba(200,245,61,0.2) !important;
    border-radius: 12px !important;
}
.stFileUploader label { color: #e8e8f0 !important; }
.stAlert { border-radius: 12px !important; }
[data-testid="stMetricValue"] { color: #c8f53d !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 32px !important; }
div[data-testid="stHorizontalBlock"] { gap: 14px !important; }
.stPlotlyChart { border-radius: 12px !important; overflow: hidden; }
.stDataFrame { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ── SECTION COLORS ─────────────────────────────────────────────────────────────
SECTION_COLORS = {
    "VIP": "#f5c842",
    "Premium": "#a855f7",
    "General": "#38e8c8",
    "Balcony": "#f53d8f",
}
SECTION_PRICES = {"VIP": 5000, "Premium": 2500, "General": 1000, "Balcony": 500}
EARLY_BIRD_THRESHOLD = 0.25


# ── LOAD DATA ──────────────────────────────────────────────────────────────────
def load_data(file_obj=None):
    if file_obj is not None:
        name = file_obj.name.lower()
        if name.endswith(".csv"):
            df = pd.read_csv(file_obj)
        else:
            df = pd.read_excel(file_obj)
    else:
        sample_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
        df = pd.read_csv(sample_path)

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    col_map = {
        "ticket_id": ["ticket_id", "id", "ticketid"],
        "seat_number": ["seat_number", "seat", "seat_no"],
        "section": ["section", "zone", "area", "category"],
        "price": ["price", "amount", "cost", "ticket_price"],
        "date": ["date", "sale_date", "booking_date", "purchase_date"],
        "booking_mode": ["booking_mode", "mode", "channel", "type"],
        "is_sold": ["is_sold", "sold", "status", "issold"],
    }
    for standard, variants in col_map.items():
        if standard not in df.columns:
            for v in variants:
                if v in df.columns:
                    df.rename(columns={v: standard}, inplace=True)
                    break

    if "is_sold" in df.columns:
        df["is_sold"] = df["is_sold"].astype(str).str.strip().str.lower().isin(
            ["true", "1", "yes", "sold"]
        )
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

    if "ticket_id" not in df.columns:
        df.insert(0, "ticket_id", [f"T{str(i+1).zfill(3)}" for i in range(len(df))])

    return df


# ── ANALYTICS ─────────────────────────────────────────────────────────────────
def compute_stats(df):
    total = len(df)
    sold_df = df[df["is_sold"] == True] if "is_sold" in df.columns else df.iloc[0:0]
    sold = len(sold_df)
    available = total - sold

    prices = np.array(sold_df["price"].values if "price" in df.columns else [])
    total_revenue = int(np.sum(prices))

    pct_sold = sold / total if total > 0 else 0
    early_bird_active = pct_sold < EARLY_BIRD_THRESHOLD

    section_stats = {}
    if "section" in df.columns:
        for sect in df["section"].unique():
            s_df = df[df["section"] == sect]
            s_sold = s_df[s_df["is_sold"] == True] if "is_sold" in df.columns else s_df.iloc[0:0]
            s_revenue = int(np.sum(np.array(s_sold["price"].values if "price" in s_df.columns else [])))
            section_stats[sect] = {
                "total": len(s_df),
                "sold": len(s_sold),
                "available": len(s_df) - len(s_sold),
                "revenue": s_revenue,
                "pct": len(s_sold) / len(s_df) * 100 if len(s_df) > 0 else 0,
                "price": int(s_df["price"].median()) if "price" in s_df.columns else 0,
            }

    daily_revenue = {}
    if "date" in df.columns and "price" in df.columns:
        sold_with_date = sold_df.dropna(subset=["date"])
        daily_revenue = (
            sold_with_date.groupby(sold_with_date["date"].dt.date)["price"]
            .sum()
            .to_dict()
        )

    mode_stats = {}
    if "booking_mode" in df.columns:
        for mode, grp in sold_df.groupby("booking_mode"):
            mode_stats[str(mode)] = {
                "count": len(grp),
                "revenue": int(np.sum(grp["price"].values)) if "price" in grp.columns else 0,
            }

    return {
        "total": total,
        "sold": sold,
        "available": available,
        "total_revenue": total_revenue,
        "pct_sold": pct_sold,
        "early_bird_active": early_bird_active,
        "section_stats": section_stats,
        "daily_revenue": daily_revenue,
        "mode_stats": mode_stats,
        "sold_df": sold_df,
    }


# ── SEAT MAP ──────────────────────────────────────────────────────────────────
def render_seat_map(df, max_cols=20, max_rows=15):
    if "is_sold" not in df.columns or "section" not in df.columns:
        st.info("Seat map requires 'is_sold' and 'section' columns.")
        return

    display_df = df.head(max_cols * max_rows).reset_index(drop=True)
    n = len(display_df)
    cols = min(max_cols, n)
    rows = math.ceil(n / cols)

    rows_html = []
    for r in range(rows):
        row_seats = []
        for c in range(cols):
            idx = r * cols + c
            if idx >= n:
                row_seats.append('<div class="seat" style="background:transparent;border:none;"></div>')
                continue
            row = display_df.iloc[idx]
            sold = row.get("is_sold", False)
            section = str(row.get("section", ""))
            seat_id = str(row.get("seat_number", row.get("ticket_id", idx)))
            price = int(row.get("price", 0))
            if sold:
                color = SECTION_COLORS.get(section, "#555")
                opacity = "cc"
                tip = f"{seat_id} · {section} · ₹{price:,} · SOLD"
            else:
                color = "#1e1e30"
                opacity = ""
                tip = f"{seat_id} · AVAILABLE"
            rows_html.append(
                f'<div class="seat" style="background:{color}{opacity};" title="{tip}"></div>'
            )

        label = f'<div class="seat-row-label">R{r+1}</div>'
        row_str = f'<div class="seat-row">{label}{"".join(rows_html)}</div>'
        rows_html_final = row_str if r == 0 else rows_html_final + row_str  # noqa: F821
    # rebuild correctly
    all_rows = []
    for r in range(rows):
        row_seats = []
        for c in range(cols):
            idx = r * cols + c
            if idx >= n:
                row_seats.append('<div class="seat" style="background:transparent;border:none;width:18px;height:18px;"></div>')
                continue
            row_data = display_df.iloc[idx]
            sold = row_data.get("is_sold", False)
            section = str(row_data.get("section", ""))
            seat_id = str(row_data.get("seat_number", row_data.get("ticket_id", idx)))
            price = int(row_data.get("price", 0))
            if sold:
                color = SECTION_COLORS.get(section, "#555")
                tip = f"{seat_id} · {section} · ₹{price:,} · SOLD"
                seat_style = f"background:{color}cc;"
            else:
                tip = f"{seat_id} · AVAILABLE"
                seat_style = "background:#1e1e30;"
            row_seats.append(f'<div class="seat" style="{seat_style}" title="{tip}"></div>')
        label = f'<div class="seat-row-label">R{r+1}</div>'
        all_rows.append(f'<div class="seat-row">{label}{"".join(row_seats)}</div>')

    legend_items = ""
    for sect, color in SECTION_COLORS.items():
        legend_items += f'<div class="seat-legend-item"><div class="seat-legend-dot" style="background:{color}cc;"></div>{sect} — Sold</div>'
    legend_items += '<div class="seat-legend-item"><div class="seat-legend-dot" style="background:#1e1e30;border:1px solid rgba(255,255,255,0.1);"></div>Available</div>'

    html = f"""
    <div class="panel">
        <div class="panel-title">Seat Map · Showing {n} Seats</div>
        <div class="seat-map-wrap">
            <div class="seat-grid">
                {"".join(all_rows)}
            </div>
        </div>
        <div class="seat-legend">{legend_items}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ── CHATBOT ───────────────────────────────────────────────────────────────────
def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def build_context(stats, df):
    section_lines = []
    for sect, s in stats["section_stats"].items():
        section_lines.append(
            f"  - {sect}: {s['sold']}/{s['total']} sold, ₹{s['revenue']:,} revenue ({s['pct']:.1f}%)"
        )
    sections_text = "\n".join(section_lines) if section_lines else "  No section data."

    top_day = ""
    if stats["daily_revenue"]:
        top_d = max(stats["daily_revenue"], key=stats["daily_revenue"].get)
        top_day = f"Best sales day: {top_d} with ₹{stats['daily_revenue'][top_d]:,}"

    mode_text = ""
    for mode, m in stats["mode_stats"].items():
        mode_text += f"{mode}: {m['count']} tickets, ₹{m['revenue']:,}. "

    return f"""You are an intelligent ticket sales analytics assistant for an event management system.

Current Dataset Summary:
- Total tickets: {stats['total']}
- Tickets sold: {stats['sold']} ({stats['pct_sold']*100:.1f}% of total)
- Available tickets: {stats['available']}
- Total revenue collected: ₹{stats['total_revenue']:,}
- Early bird discount: {"ACTIVE" if stats['early_bird_active'] else "DISABLED (25% threshold exceeded)"}

Section Performance:
{sections_text}

Booking Mode Breakdown:
{mode_text if mode_text else "No booking mode data."}

{top_day}

The early bird discount is automatically disabled once 25% of tickets are sold.
Currency is Indian Rupees (₹). Answer concisely, accurately, and with actionable insights.
If asked about Python or data processing, explain how pandas/numpy are used in this system."""


def chat_with_groq(user_message, history, stats, df):
    client = get_groq_client()
    if client is None:
        return "⚠️ Groq API key not configured. Please set GROQ_API_KEY in your environment."

    system_prompt = build_context(stats, df)
    messages = [{"role": "system", "content": system_prompt}]
    for h in history[-8:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error connecting to AI: {str(e)}"


# ── PLOTLY THEME ───────────────────────────────────────────────────────────────
PLOT_BG = "#141424"
PAPER_BG = "#141424"
GRID_COLOR = "rgba(255,255,255,0.05)"
FONT_COLOR = "#6a6a8a"


def dark_layout(fig, title=""):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_COLOR, family="Space Mono"),
        title=dict(text=title, font=dict(color="#e8e8f0", size=12), x=0),
        margin=dict(l=10, r=10, t=36 if title else 10, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.07)",
            borderwidth=1,
            font=dict(color="#6a6a8a", size=10),
        ),
    )
    fig.update_xaxes(gridcolor=GRID_COLOR, linecolor="rgba(255,255,255,0.05)", tickfont=dict(size=10))
    fig.update_yaxes(gridcolor=GRID_COLOR, linecolor="rgba(255,255,255,0.05)", tickfont=dict(size=10))
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 0 24px;">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:28px;color:#c8f53d;letter-spacing:2px;">🎟️ TICKET<br>TRACKER</div>
        <div style="font-family:'Space Mono',monospace;font-size:10px;color:#6a6a8a;margin-top:4px;">SMART ANALYTICS SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-family:Space Mono,monospace;font-size:10px;color:#6a6a8a;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">📂 Upload Data</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload Excel or CSV",
        type=["xlsx", "csv"],
        help="Upload your ticket data file (.xlsx or .csv)",
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")
    else:
        st.markdown("""
        <div style="background:rgba(200,245,61,0.05);border:1px dashed rgba(200,245,61,0.2);border-radius:10px;padding:10px 14px;font-size:11px;color:#6a6a8a;font-family:'Space Mono',monospace;line-height:1.7;">
        Using <strong style="color:#c8f53d;">sample_data.csv</strong><br>
        Upload your own file above
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="neon-divider" style="margin:20px 0;"></div>', unsafe_allow_html=True)

    st.markdown('<div style="font-family:Space Mono,monospace;font-size:10px;color:#6a6a8a;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:14px;">🤖 AI Assistant</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history[-6:]:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-msg">
                    <div class="chat-avatar chat-avatar-user">👤</div>
                    <div class="chat-bubble chat-bubble-user">{msg['content']}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-msg">
                    <div class="chat-avatar chat-avatar-bot">🤖</div>
                    <div class="chat-bubble">{msg['content']}</div>
                </div>""", unsafe_allow_html=True)

    user_input = st.text_input(
        "Ask about your ticket data...",
        placeholder="e.g. Which section has highest revenue?",
        label_visibility="collapsed",
        key="chat_input",
    )

    col_send, col_clear = st.columns([3, 1])
    with col_send:
        send = st.button("Send →", use_container_width=True)
    with col_clear:
        clear = st.button("Clear", use_container_width=True)

    if clear:
        st.session_state.chat_history = []
        st.rerun()

    # Quick prompts
    st.markdown('<div style="font-family:Space Mono,monospace;font-size:9px;color:#6a6a8a;text-transform:uppercase;letter-spacing:1px;margin:14px 0 8px;">Quick Prompts</div>', unsafe_allow_html=True)
    quick_prompts = [
        "What is the total revenue?",
        "Which section sells best?",
        "Is early bird active?",
        "Online vs offline sales?",
    ]
    for qp in quick_prompts:
        if st.button(qp, key=f"qp_{qp}", use_container_width=True):
            st.session_state["_quick_prompt"] = qp
            st.rerun()

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
try:
    df = load_data(uploaded_file)
    stats = compute_stats(df)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Process chatbot send (after data is loaded)
prompt_to_send = None
if send and user_input.strip():
    prompt_to_send = user_input.strip()
elif "_quick_prompt" in st.session_state:
    prompt_to_send = st.session_state.pop("_quick_prompt")

if prompt_to_send:
    st.session_state.chat_history.append({"role": "user", "content": prompt_to_send})
    with st.sidebar:
        with st.spinner("Thinking..."):
            reply = chat_with_groq(prompt_to_send, st.session_state.chat_history, stats, df)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="tracker-header">
    <div>
        <div class="label-pill">● LIVE · PROJECT 96</div>
        <div class="tracker-title">EVENT<br><span>TICKET</span><br>TRACKER</div>
        <div class="tracker-sub">Concert venue analytics · 4 price tiers · AI-powered insights</div>
    </div>
    <div class="header-right">
        <strong>Vishwakarma University</strong>
        Python Programming<br>
        First Year · CSE<br>
        <br>
        Real-world apps:<br>
        Ticketmaster · Eventbrite<br>
        StubHub
    </div>
</div>
""", unsafe_allow_html=True)

# ── STAT CARDS ────────────────────────────────────────────────────────────────
revenue_str = f"₹{stats['total_revenue']//1000}K" if stats['total_revenue'] >= 1000 else f"₹{stats['total_revenue']}"
pct_str = f"{stats['pct_sold']*100:.1f}%"

st.markdown(f"""
<div class="stats-row">
    <div class="stat-card c-neon">
        <div class="stat-icon">🎟️</div>
        <div class="stat-label">Total Tickets</div>
        <div class="stat-value">{stats['total']}</div>
        <div class="stat-sub">Dataset loaded</div>
    </div>
    <div class="stat-card c-pink">
        <div class="stat-icon">✅</div>
        <div class="stat-label">Tickets Sold</div>
        <div class="stat-value">{stats['sold']}</div>
        <div class="stat-sub">IsSold = True</div>
    </div>
    <div class="stat-card c-cyan">
        <div class="stat-icon">🟢</div>
        <div class="stat-label">Available</div>
        <div class="stat-value">{stats['available']}</div>
        <div class="stat-sub">IsSold = False</div>
    </div>
    <div class="stat-card c-purple">
        <div class="stat-icon">💰</div>
        <div class="stat-label">Total Revenue</div>
        <div class="stat-value">{revenue_str}</div>
        <div class="stat-sub">np.sum(prices)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── EARLY BIRD BANNER ─────────────────────────────────────────────────────────
eb = stats["early_bird_active"]
pct_val = min(stats["pct_sold"] * 100, 100)
fill_pct = min(stats["pct_sold"] / EARLY_BIRD_THRESHOLD * 100, 100) if eb else 100
fill_class = "" if eb else "eb-bar-fill-exceeded"
banner_class = "eb-active" if eb else "eb-disabled"
badge_html = '<span class="eb-badge-active">✓ ACTIVE</span>' if eb else '<span class="eb-badge-disabled">✗ DISABLED</span>'
cutoff_label = "25% CUTOFF" if eb else "THRESHOLD PASSED"
eb_text = (
    f'🔔 Early-bird discount is <strong>ACTIVE</strong> · {badge_html}'
    if eb else
    f'🚫 Early-bird discount <strong>DISABLED</strong> · 25% threshold exceeded · {badge_html}'
)

st.markdown(f"""
<div class="eb-banner {banner_class}">
    <div class="eb-text">
        {eb_text}<br>
        <span style="font-size:12px;color:#6a6a8a;font-family:'Space Mono',monospace;margin-top:4px;display:block;">
        Sold <strong style="color:#e8e8f0;">{stats['sold']}</strong> of {stats['total']} tickets ({pct_str})
        </span>
    </div>
    <div class="eb-progress-wrap">
        <div class="eb-progress-label">
            <span>0%</span><span>{cutoff_label}</span><span>100%</span>
        </div>
        <div class="eb-bar-track">
            <div class="eb-bar-fill {fill_class}" style="width:{fill_pct:.1f}%;"></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SECTION SALES + DATE TREND ────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    if stats["section_stats"]:
        bars_html = []
        for sect in ["VIP", "Premium", "General", "Balcony"]:
            s = stats["section_stats"].get(sect)
            if not s:
                continue
            color = SECTION_COLORS.get(sect, "#888")
            pct = s["pct"]
            price_k = f"₹{s['price']//1000}K" if s['price'] >= 1000 else f"₹{s['price']}"
            bars_html.append(f"""
            <div class="section-item">
                <div class="section-row">
                    <div class="section-name">
                        <span class="section-dot" style="background:{color};"></span>
                        {sect}
                    </div>
                    <div class="section-stats">{s['sold']} sold / {s['total']} total · {price_k} each</div>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="background:{color};width:{pct:.1f}%;opacity:0.85;"></div>
                </div>
            </div>
            """)

        sections_inner = "".join(bars_html)
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">Sales by Section</div>
            {sections_inner}
        </div>
        """, unsafe_allow_html=True)

        # Revenue share chart
        sect_names = list(stats["section_stats"].keys())
        sect_revs = [stats["section_stats"][s]["revenue"] for s in sect_names]
        colors = [SECTION_COLORS.get(s, "#888") for s in sect_names]

        fig_pie = go.Figure(go.Pie(
            labels=sect_names,
            values=sect_revs,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#08080f", width=2)),
            textfont=dict(family="Space Mono", size=10, color="#e8e8f0"),
            textposition="outside",
        ))
        fig_pie = dark_layout(fig_pie, "Revenue Share")
        fig_pie.update_layout(height=240, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

with col_right:
    if stats["daily_revenue"]:
        days = sorted(stats["daily_revenue"].keys())
        revenues = [stats["daily_revenue"][d] for d in days]
        cumulative = np.cumsum(revenues).tolist()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=[str(d) for d in days],
            y=revenues,
            name="Daily Revenue",
            marker_color="#c8f53d",
            marker_opacity=0.7,
            hovertemplate="<b>%{x}</b><br>₹%{y:,}<extra></extra>",
        ))
        fig_trend.add_trace(go.Scatter(
            x=[str(d) for d in days],
            y=cumulative,
            name="Cumulative",
            line=dict(color="#38e8c8", width=2, dash="dot"),
            mode="lines+markers",
            marker=dict(size=5),
            hovertemplate="<b>%{x}</b><br>Cumulative: ₹%{y:,}<extra></extra>",
            yaxis="y2",
        ))
        fig_trend.update_layout(
            yaxis2=dict(overlaying="y", side="right", gridcolor="rgba(0,0,0,0)", tickfont=dict(size=9, color="#38e8c8")),
            yaxis=dict(tickprefix="₹", tickformat=","),
        )
        fig_trend = dark_layout(fig_trend, "Daily Sales Trend")
        fig_trend.update_layout(height=260, legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown("""
        <div class="panel" style="text-align:center;padding:48px 24px;">
            <div style="font-size:32px;margin-bottom:12px;">📅</div>
            <div style="color:#6a6a8a;font-family:'Space Mono',monospace;font-size:11px;">
            No date data available in dataset
            </div>
        </div>
        """, unsafe_allow_html=True)

    if stats["mode_stats"]:
        modes = list(stats["mode_stats"].keys())
        mode_counts = [stats["mode_stats"][m]["count"] for m in modes]
        mode_colors = ["#c8f53d", "#38e8c8", "#a855f7", "#f53d8f"]

        fig_mode = go.Figure(go.Bar(
            x=modes,
            y=mode_counts,
            marker_color=mode_colors[:len(modes)],
            marker_opacity=0.8,
            hovertemplate="<b>%{x}</b><br>%{y} tickets<extra></extra>",
        ))
        fig_mode = dark_layout(fig_mode, "Booking Mode")
        fig_mode.update_layout(height=200, showlegend=False)
        st.plotly_chart(fig_mode, use_container_width=True, config={"displayModeBar": False})

# ── REVENUE BREAKDOWN ─────────────────────────────────────────────────────────
if stats["section_stats"]:
    rev_cards = ""
    for sect in ["VIP", "Premium", "General", "Balcony"]:
        s = stats["section_stats"].get(sect)
        if not s:
            continue
        color = SECTION_COLORS.get(sect, "#888")
        price_fmt = f"₹{s['price']:,}"
        rev_fmt = f"₹{s['revenue']:,}"
        rev_cards += f"""
        <div class="rev-card">
            <div class="rev-section-name"><span style="color:{color};font-size:14px;">●</span>{sect}</div>
            <div class="rev-amount" style="color:{color};">{rev_fmt}</div>
            <div class="rev-meta">{s['sold']} sold × {price_fmt}</div>
        </div>
        """

    total_str = f"₹{stats['total_revenue']:,}"
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Revenue Breakdown · NumPy Calculation</div>
        <div class="rev-grid">{rev_cards}</div>
        <div class="rev-total-row">
            <div class="rev-total-label">np.array([revenues]) → np.sum() =</div>
            <div class="rev-total-val">{total_str}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── SEAT MAP ──────────────────────────────────────────────────────────────────
render_seat_map(df)

# ── TICKET REGISTRY ────────────────────────────────────────────────────────────
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Ticket Registry & Search</div>', unsafe_allow_html=True)

search_col, filter_col = st.columns([3, 2])
with search_col:
    search_query = st.text_input("Search", placeholder="Search by ticket ID, section, or mode...", label_visibility="collapsed")
with filter_col:
    filter_opt = st.selectbox("Filter", ["All", "Sold", "Available"], label_visibility="collapsed")

display_df = df.copy()
if search_query:
    mask = pd.Series([False] * len(display_df))
    for col in ["ticket_id", "section", "booking_mode", "seat_number"]:
        if col in display_df.columns:
            mask |= display_df[col].astype(str).str.lower().str.contains(search_query.lower(), na=False)
    display_df = display_df[mask]

if filter_opt == "Sold" and "is_sold" in display_df.columns:
    display_df = display_df[display_df["is_sold"] == True]
elif filter_opt == "Available" and "is_sold" in display_df.columns:
    display_df = display_df[display_df["is_sold"] == False]

st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:10px;color:#6a6a8a;margin-bottom:10px;">Showing {len(display_df)} tickets</div>', unsafe_allow_html=True)

ticket_rows_html = []
for _, row in display_df.head(50).iterrows():
    tid = str(row.get("ticket_id", ""))
    sect = str(row.get("section", "—"))
    price = int(row.get("price", 0)) if "price" in row.index else 0
    sold = row.get("is_sold", False)
    mode = str(row.get("booking_mode", "—")).title() if "booking_mode" in row.index else "—"
    color = SECTION_COLORS.get(sect, "#888")
    badge = '<span class="badge-sold">SOLD</span>' if sold else '<span class="badge-avail">AVAILABLE</span>'
    ticket_rows_html.append(f"""
    <div class="ticket-row-html">
        <div class="t-id">{tid}</div>
        <div class="t-sect"><span style="width:8px;height:8px;border-radius:50%;background:{color};flex-shrink:0;display:inline-block;"></span>{sect}</div>
        <div class="t-price">₹{price:,}</div>
        <div class="t-mode">{mode}</div>
        {badge}
    </div>
    """)

if ticket_rows_html:
    st.markdown(
        f'<div style="max-height:320px;overflow-y:auto;padding-right:4px;">{"".join(ticket_rows_html)}</div>',
        unsafe_allow_html=True,
    )
    if len(display_df) > 50:
        st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:10px;color:#6a6a8a;text-align:center;margin-top:8px;">... and {len(display_df)-50} more rows</div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="color:#6a6a8a;font-family:Space Mono,monospace;font-size:12px;padding:24px;text-align:center;">No tickets match your search.</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── PYTHON CONCEPTS STRIP ─────────────────────────────────────────────────────
st.markdown("""
<div class="py-strip">
    <div class="py-concept">
        <div class="py-label">Data Structure</div>
        <div class="py-value"><code class="py-code">DataFrame</code> — Ticket records</div>
    </div>
    <div class="py-concept">
        <div class="py-label">Aggregation</div>
        <div class="py-value"><code class="py-code">np.sum(array)</code></div>
    </div>
    <div class="py-concept">
        <div class="py-label">Filtering</div>
        <div class="py-value"><code class="py-code">df[df.is_sold]</code></div>
    </div>
    <div class="py-concept">
        <div class="py-label">Grouping</div>
        <div class="py-value"><code class="py-code">groupby("section")</code></div>
    </div>
    <div class="py-concept">
        <div class="py-label">Early Bird Logic</div>
        <div class="py-value">25% cutoff auto-disable</div>
    </div>
    <div class="py-concept">
        <div class="py-label">AI Insights</div>
        <div class="py-value"><code class="py-code">Groq API</code> · LLaMA 3.3</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:24px 0 8px;border-top:1px solid rgba(255,255,255,0.05);margin-top:8px;">
    <div style="font-family:'Space Mono',monospace;font-size:10px;color:#6a6a8a;">
        🎟️ Event Ticket Tracker · Built with Python, Streamlit, Pandas, NumPy, Plotly & Groq AI
    </div>
</div>
""", unsafe_allow_html=True)
