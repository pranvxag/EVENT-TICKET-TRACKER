"""
Smart Ticket Sales Tracking and Analytics System
Author: Pranav Agale
Stack: Python · Pandas · NumPy · Streamlit · Plotly · Groq API
"""

import os
import io
import json
import traceback
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ─── ENV ─────────────────────────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎟️ Smart Ticket Analytics",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── THEME / CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark background */
.stApp {
    background: #08080f;
    color: #e8e8f0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
section[data-testid="stSidebar"] * { color: #e8e8f0 !important; }

/* Metric cards */
[data-testid="stMetric"] {
    background: #141424;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 22px !important;
}
[data-testid="stMetricLabel"] { color: #6a6a8a !important; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; }
[data-testid="stMetricValue"] { color: #c8f53d !important; font-family: 'Space Mono', monospace; font-size: 26px; }
[data-testid="stMetricDelta"] { color: #38e8c8 !important; }

/* Headings */
h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 2px;
    color: #e8e8f0;
}
h1 { font-size: 3rem; }
h2 { font-size: 1.8rem; color: #c8f53d; }

/* Pill badges */
.pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 100px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    font-weight: 700;
}
.pill-neon  { background: rgba(200,245,61,0.12);  border:1px solid rgba(200,245,61,0.35);  color:#c8f53d; }
.pill-cyan  { background: rgba(56,232,200,0.12);  border:1px solid rgba(56,232,200,0.35);  color:#38e8c8; }
.pill-purple{ background: rgba(168,85,247,0.12);  border:1px solid rgba(168,85,247,0.35);  color:#a855f7; }
.pill-pink  { background: rgba(245,61,143,0.12);  border:1px solid rgba(245,61,143,0.35);  color:#f53d8f; }
.pill-yellow{ background: rgba(245,200,66,0.12);  border:1px solid rgba(245,200,66,0.35);  color:#f5c842; }

/* Card wrapper */
.card {
    background: #141424;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 18px;
}

/* Section divider */
.sec-divider {
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 28px 0 20px;
}

/* Chat bubbles */
.chat-user {
    background: rgba(200,245,61,0.08);
    border: 1px solid rgba(200,245,61,0.2);
    border-radius: 12px 12px 2px 12px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #e8e8f0;
    font-size: 14px;
}
.chat-bot {
    background: rgba(168,85,247,0.08);
    border: 1px solid rgba(168,85,247,0.2);
    border-radius: 12px 12px 12px 2px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #e8e8f0;
    font-size: 14px;
}
.chat-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

/* Status banner */
.banner-success {
    background: rgba(56,232,200,0.1);
    border: 1px solid rgba(56,232,200,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    color: #38e8c8;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
}
.banner-warning {
    background: rgba(245,200,66,0.1);
    border: 1px solid rgba(245,200,66,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    color: #f5c842;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
}
.banner-info {
    background: rgba(168,85,247,0.1);
    border: 1px solid rgba(168,85,247,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    color: #a855f7;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
}

/* Plotly chart backgrounds */
.js-plotly-plot, .plot-container {
    background: transparent !important;
}

/* Buttons */
.stButton > button {
    background: rgba(200,245,61,0.1) !important;
    border: 1px solid rgba(200,245,61,0.4) !important;
    color: #c8f53d !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(200,245,61,0.2) !important;
    border-color: #c8f53d !important;
}

/* File uploader */
[data-testid="stFileUploadDropzone"] {
    background: #141424 !important;
    border: 1.5px dashed rgba(200,245,61,0.3) !important;
    border-radius: 12px !important;
    color: #6a6a8a !important;
}

/* Input fields */
.stTextInput > div > input, .stTextArea > div > textarea {
    background: #141424 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
}

/* Slider */
.stSlider > div > div { color: #c8f53d !important; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ─────────────────────────────────────────────────────────────────
SECTION_COLORS = {
    "VIP":     "#f5c842",
    "Gold":    "#f5a842",
    "Premium": "#a855f7",
    "Silver":  "#a0aec0",
    "Bronze":  "#cd7f32",
    "General": "#38e8c8",
    "Balcony": "#f53d8f",
    "Lawn":    "#c8f53d",
}
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e8e8f0",
    font_family="DM Sans",
    margin=dict(l=16, r=16, t=32, b=16),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)


def color_for_section(section: str) -> str:
    return SECTION_COLORS.get(section, "#38e8c8")


# ─── DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    if file_name.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        df = pd.read_excel(io.BytesIO(file_bytes))
    return df


# ─── DATA PROCESSING ─────────────────────────────────────────────────────────
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and types; derive useful computed columns."""
    # ── Normalise column names
    col_map = {}
    for c in df.columns:
        lower = c.lower().replace(" ", "").replace("_", "")
        if lower in ("issold", "sold", "status"):
            col_map[c] = "IsSold"
        elif lower in ("purchasedate", "date", "saledate", "bookingdate"):
            col_map[c] = "PurchaseDate"
        elif lower in ("price", "ticketprice", "amount"):
            col_map[c] = "Price"
        elif lower in ("seatsection", "section", "category"):
            col_map[c] = "SeatSection"
        elif lower in ("channel", "bookingmode", "mode"):
            col_map[c] = "Channel"
        elif lower in ("ticketid", "id"):
            col_map[c] = "TicketID"
        elif lower in ("seatnumber", "seat"):
            col_map[c] = "SeatNumber"
        elif lower in ("row", "rowno", "rownumber"):
            col_map[c] = "Row"
        elif lower in ("customername", "customer", "name"):
            col_map[c] = "CustomerName"
    df = df.rename(columns=col_map)

    # ── IsSold → boolean
    if "IsSold" in df.columns:
        df["IsSold"] = df["IsSold"].astype(str).str.strip().str.lower().isin(
            ["yes", "true", "1", "sold", "y"]
        )
    else:
        df["IsSold"] = True  # assume all are sold if column missing

    # ── PurchaseDate → datetime
    if "PurchaseDate" in df.columns:
        df["PurchaseDate"] = pd.to_datetime(df["PurchaseDate"], errors="coerce")
        df["PurchaseMonth"] = df["PurchaseDate"].dt.to_period("M").astype(str)
        df["PurchaseWeek"]  = df["PurchaseDate"].dt.isocalendar().week.astype("Int64")
        df["DayOfWeek"]     = df["PurchaseDate"].dt.day_name()

    # ── Price → numeric
    if "Price" in df.columns:
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0)

    # ── Channel grouping
    if "Channel" in df.columns:
        df["ChannelGroup"] = df["Channel"].apply(
            lambda x: "Online" if isinstance(x, str) and x.lower() not in
            ("agent", "offline counter", "offline", "counter", "walk-in") else "Offline"
        )

    return df


# ─── ANALYTICS ───────────────────────────────────────────────────────────────
def compute_analytics(df: pd.DataFrame, discount_pct: float = 10.0) -> dict:
    """Return a dict of all computed KPIs and sub-dataframes."""
    sold = df[df["IsSold"] == True].copy()
    total_tickets   = len(df)
    total_sold      = len(sold)
    total_unsold    = total_tickets - total_sold
    sold_pct        = (total_sold / total_tickets * 100) if total_tickets else 0
    total_revenue   = float(sold["Price"].sum()) if "Price" in sold.columns else 0.0
    avg_ticket_price= float(sold["Price"].mean()) if "Price" in sold.columns and len(sold) else 0.0
    median_price    = float(sold["Price"].median()) if "Price" in sold.columns and len(sold) else 0.0

    # Early bird: active until 25% of total tickets are sold
    early_bird_threshold = total_tickets * 0.25
    early_bird_active    = total_sold < early_bird_threshold
    early_bird_remaining = max(0, early_bird_threshold - total_sold)
    discounted_revenue   = total_revenue * (1 - discount_pct / 100) if early_bird_active else total_revenue

    # Section-wise
    section_stats = pd.DataFrame()
    if "SeatSection" in sold.columns and "Price" in sold.columns:
        section_stats = (
            sold.groupby("SeatSection")
            .agg(
                Tickets=("SeatSection", "count"),
                Revenue=("Price", "sum"),
                AvgPrice=("Price", "mean"),
            )
            .reset_index()
            .sort_values("Revenue", ascending=False)
        )
        section_stats["RevenueShare"] = (
            section_stats["Revenue"] / section_stats["Revenue"].sum() * 100
        ).round(1)

    # Date-wise
    daily_stats = pd.DataFrame()
    if "PurchaseDate" in sold.columns:
        daily_stats = (
            sold.dropna(subset=["PurchaseDate"])
            .groupby(sold["PurchaseDate"].dt.date)
            .agg(Tickets=("IsSold", "count"), Revenue=("Price", "sum"))
            .reset_index()
            .rename(columns={"PurchaseDate": "Date"})
        )
        daily_stats["CumRevenue"] = daily_stats["Revenue"].cumsum()
        daily_stats["CumTickets"] = daily_stats["Tickets"].cumsum()

    # Channel-wise
    channel_stats = pd.DataFrame()
    if "Channel" in sold.columns:
        channel_stats = (
            sold.groupby("Channel")
            .agg(Tickets=("Channel", "count"), Revenue=("Price", "sum"))
            .reset_index()
            .sort_values("Tickets", ascending=False)
        )

    # Top customers
    top_customers = pd.DataFrame()
    if "CustomerName" in sold.columns:
        top_customers = (
            sold.groupby("CustomerName")
            .agg(Tickets=("CustomerName", "count"), Spent=("Price", "sum"))
            .reset_index()
            .sort_values("Spent", ascending=False)
            .head(10)
        )

    # Day-of-week
    dow_stats = pd.DataFrame()
    if "DayOfWeek" in sold.columns:
        order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dow_stats = (
            sold.groupby("DayOfWeek")
            .agg(Tickets=("DayOfWeek","count"), Revenue=("Price","sum"))
            .reindex(order).fillna(0).reset_index()
        )

    return dict(
        total_tickets=total_tickets,
        total_sold=total_sold,
        total_unsold=total_unsold,
        sold_pct=sold_pct,
        total_revenue=total_revenue,
        avg_ticket_price=avg_ticket_price,
        median_price=median_price,
        early_bird_active=early_bird_active,
        early_bird_threshold=early_bird_threshold,
        early_bird_remaining=early_bird_remaining,
        discounted_revenue=discounted_revenue,
        discount_pct=discount_pct,
        section_stats=section_stats,
        daily_stats=daily_stats,
        channel_stats=channel_stats,
        top_customers=top_customers,
        dow_stats=dow_stats,
    )


# ─── CHART BUILDERS ──────────────────────────────────────────────────────────
def chart_section_revenue(section_stats: pd.DataFrame):
    colors = [color_for_section(s) for s in section_stats["SeatSection"]]
    fig = go.Figure(go.Bar(
        x=section_stats["SeatSection"],
        y=section_stats["Revenue"],
        marker_color=colors,
        text=section_stats["Revenue"].apply(lambda x: f"₹{x:,.0f}"),
        textposition="outside",
        textfont_color="#e8e8f0",
    ))
    fig.update_layout(title="Section-wise Revenue", **PLOTLY_LAYOUT)
    return fig


def chart_section_donut(section_stats: pd.DataFrame):
    fig = go.Figure(go.Pie(
        labels=section_stats["SeatSection"],
        values=section_stats["Revenue"],
        hole=0.6,
        marker_colors=[color_for_section(s) for s in section_stats["SeatSection"]],
        textfont_color="#e8e8f0",
    ))
    fig.update_layout(title="Revenue Share by Section", **PLOTLY_LAYOUT)
    return fig


def chart_daily_sales(daily_stats: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_stats["Date"], y=daily_stats["Revenue"],
        fill="tozeroy", name="Daily Revenue",
        line=dict(color="#c8f53d", width=2),
        fillcolor="rgba(200,245,61,0.08)",
    ))
    fig.update_layout(title="Daily Revenue Trend", **PLOTLY_LAYOUT)
    return fig


def chart_cumulative(daily_stats: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_stats["Date"], y=daily_stats["CumRevenue"],
        name="Cumulative Revenue",
        line=dict(color="#a855f7", width=2.5),
        fill="tozeroy", fillcolor="rgba(168,85,247,0.07)",
    ))
    fig.add_trace(go.Scatter(
        x=daily_stats["Date"], y=daily_stats["CumTickets"] * (daily_stats["CumRevenue"].max() / daily_stats["CumTickets"].max()),
        name="Cumulative Tickets (scaled)",
        line=dict(color="#38e8c8", width=1.5, dash="dot"),
    ))
    fig.update_layout(title="Cumulative Revenue & Tickets", **PLOTLY_LAYOUT)
    return fig


def chart_channel(channel_stats: pd.DataFrame):
    fig = go.Figure(go.Bar(
        x=channel_stats["Tickets"],
        y=channel_stats["Channel"],
        orientation="h",
        marker_color="#38e8c8",
        text=channel_stats["Tickets"],
        textposition="outside",
        textfont_color="#e8e8f0",
    ))
    fig.update_layout(title="Tickets by Channel", height=350, **PLOTLY_LAYOUT)
    return fig


def chart_dow(dow_stats: pd.DataFrame):
    fig = go.Figure(go.Bar(
        x=dow_stats["DayOfWeek"],
        y=dow_stats["Tickets"],
        marker_color="#f53d8f",
        text=dow_stats["Tickets"].astype(int),
        textposition="outside",
        textfont_color="#e8e8f0",
    ))
    fig.update_layout(title="Sales by Day of Week", **PLOTLY_LAYOUT)
    return fig


# ─── GROQ CHATBOT ────────────────────────────────────────────────────────────
def build_context_summary(analytics: dict, df: pd.DataFrame) -> str:
    """Create a compact text summary of the dataset for the LLM."""
    s = analytics
    lines = [
        f"Event Ticket Sales Analytics Context:",
        f"- Total Tickets: {s['total_tickets']} | Sold: {s['total_sold']} ({s['sold_pct']:.1f}%) | Unsold: {s['total_unsold']}",
        f"- Total Revenue: ₹{s['total_revenue']:,.2f}",
        f"- Avg Price: ₹{s['avg_ticket_price']:,.2f} | Median Price: ₹{s['median_price']:,.2f}",
        f"- Early Bird Discount ({s['discount_pct']}%): {'ACTIVE' if s['early_bird_active'] else 'DISABLED (25% threshold crossed)'}",
    ]
    if not s["section_stats"].empty:
        lines.append("- Section Performance:")
        for _, row in s["section_stats"].iterrows():
            lines.append(f"  • {row['SeatSection']}: {row['Tickets']} tickets, ₹{row['Revenue']:,.0f} revenue ({row['RevenueShare']}%)")
    if not s["channel_stats"].empty:
        top_ch = s["channel_stats"].iloc[0]
        lines.append(f"- Top Channel: {top_ch['Channel']} with {top_ch['Tickets']} tickets")
    if not s["daily_stats"].empty:
        peak = s["daily_stats"].loc[s["daily_stats"]["Revenue"].idxmax()]
        lines.append(f"- Peak Sales Day: {peak['Date']} (₹{peak['Revenue']:,.0f}, {peak['Tickets']} tickets)")
    return "\n".join(lines)


def ask_groq(user_message: str, context_summary: str, chat_history: list) -> str:
    if not GROQ_API_KEY:
        return "⚠️ Groq API key not found. Please set GROQ_API_KEY in your .env file."
    try:
        client = Groq(api_key=GROQ_API_KEY)
        system_prompt = f"""You are an expert ticket sales analyst AI assistant for an event management system.
You have access to the following real-time analytics data:

{context_summary}

Your role:
- Answer questions about ticket sales, revenue, trends, and performance
- Provide actionable business insights and strategic recommendations
- Interpret patterns in the data (pricing, channels, sections, dates)
- Be concise, data-driven, and professional
- Use ₹ symbol for Indian Rupee amounts
- Highlight important numbers and key takeaways
- If asked something outside the data scope, politely redirect
"""
        messages = [{"role": "system", "content": system_prompt}]
        # Include last 6 messages for context
        for msg in chat_history[-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=600,
            temperature=0.4,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Groq API error: {str(e)}"


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
def render_sidebar(analytics: dict | None):
    with st.sidebar:
        st.markdown("""
        <div style='padding:10px 0 24px'>
            <div style='font-family:Space Mono,monospace; font-size:10px; letter-spacing:2px; color:#6a6a8a; margin-bottom:6px;'>● LIVE SYSTEM</div>
            <div style='font-family:Bebas Neue,sans-serif; font-size:28px; letter-spacing:3px; color:#c8f53d;'>TICKET<br>ANALYTICS</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📂 Upload Data")
        uploaded = st.file_uploader(
            "Drop your .xlsx or .csv file",
            type=["xlsx", "xls", "csv"],
            help="Columns expected: TicketID, SeatSection, Price, PurchaseDate, IsSold, Channel",
        )

        discount_pct = 10.0
        if analytics:
            st.markdown("---")
            st.markdown("### ⚙️ Settings")
            discount_pct = st.slider(
                "Early Bird Discount %",
                min_value=1, max_value=50, value=10, step=1,
                help="Applied while sold tickets < 25% of total"
            )

            st.markdown("---")
            st.markdown("### 📊 Quick Stats")
            st.markdown(f"""
            <div style='font-family:Space Mono,monospace; font-size:12px; line-height:2;'>
                <div>🎟️ Sold: <span style='color:#c8f53d'>{analytics['total_sold']}/{analytics['total_tickets']}</span></div>
                <div>💰 Revenue: <span style='color:#38e8c8'>₹{analytics['total_revenue']:,.0f}</span></div>
                <div>📈 Fill Rate: <span style='color:#a855f7'>{analytics['sold_pct']:.1f}%</span></div>
                <div>🏷️ Early Bird: <span style='color:{"#c8f53d" if analytics["early_bird_active"] else "#f53d8f"}'>{"ACTIVE" if analytics["early_bird_active"] else "CLOSED"}</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style='font-family:Space Mono,monospace; font-size:10px; color:#6a6a8a; line-height:1.8;'>
            Built by Pranav Agale<br>
            Stack: Python · Streamlit<br>
            AI: Groq · LLaMA3
        </div>
        """, unsafe_allow_html=True)

    return uploaded, discount_pct


# ─── TABS ─────────────────────────────────────────────────────────────────────
def render_overview(analytics: dict):
    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📊 OVERVIEW")
    a = analytics

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Tickets", f"{a['total_tickets']:,}")
    c2.metric("Tickets Sold", f"{a['total_sold']:,}", f"{a['sold_pct']:.1f}% fill rate")
    c3.metric("Total Revenue", f"₹{a['total_revenue']:,.0f}")
    c4.metric("Avg Ticket Price", f"₹{a['avg_ticket_price']:,.0f}")
    c5.metric("Unsold Seats", f"{a['total_unsold']:,}", f"-{100-a['sold_pct']:.1f}%")

    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)

    # Early Bird Banner
    if a["early_bird_active"]:
        st.markdown(f"""
        <div class="banner-success">
            🏷️ EARLY BIRD DISCOUNT ACTIVE — {a['discount_pct']}% off applied
            &nbsp;|&nbsp; {int(a['early_bird_remaining'])} more tickets to sell before threshold
            &nbsp;|&nbsp; Discounted Revenue: ₹{a['discounted_revenue']:,.0f}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="banner-warning">
            ⚡ EARLY BIRD DISCOUNT CLOSED — 25% threshold ({int(a['early_bird_threshold'])} tickets) crossed.
            Full pricing is now active.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Revenue + Date trend
    if not a["daily_stats"].empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(chart_daily_sales(a["daily_stats"]), use_container_width=True)
        with col2:
            st.plotly_chart(chart_cumulative(a["daily_stats"]), use_container_width=True)


def render_sections(analytics: dict):
    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🏟️ SECTION PERFORMANCE")
    a = analytics

    if a["section_stats"].empty:
        st.info("No section data available.")
        return

    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(chart_section_revenue(a["section_stats"]), use_container_width=True)
    with col2:
        st.plotly_chart(chart_section_donut(a["section_stats"]), use_container_width=True)

    # Section cards
    cols = st.columns(len(a["section_stats"]))
    for i, (_, row) in enumerate(a["section_stats"].iterrows()):
        color = color_for_section(row["SeatSection"])
        with cols[i]:
            st.markdown(f"""
            <div class="card" style="border-color:{color}30">
                <div style="font-family:Space Mono,monospace;font-size:10px;color:{color};letter-spacing:1px;margin-bottom:8px;">
                    {row['SeatSection'].upper()}
                </div>
                <div style="font-size:22px;font-family:Space Mono,monospace;color:#e8e8f0;">
                    ₹{row['Revenue']:,.0f}
                </div>
                <div style="font-size:12px;color:#6a6a8a;margin-top:4px;">
                    {row['Tickets']} tickets · ₹{row['AvgPrice']:,.0f} avg
                </div>
                <div style="margin-top:8px;font-size:11px;color:{color};">
                    {row['RevenueShare']}% revenue share
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_channels(analytics: dict):
    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📡 CHANNEL & BOOKING ANALYSIS")
    a = analytics

    col1, col2 = st.columns([2, 1])
    with col1:
        if not a["channel_stats"].empty:
            st.plotly_chart(chart_channel(a["channel_stats"]), use_container_width=True)
    with col2:
        if not a["dow_stats"].empty:
            st.plotly_chart(chart_dow(a["dow_stats"]), use_container_width=True)

    if not a["channel_stats"].empty:
        st.markdown("### Channel Breakdown Table")
        display_ch = a["channel_stats"].copy()
        display_ch["Revenue"] = display_ch["Revenue"].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(
            display_ch,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Channel":  st.column_config.TextColumn("Channel"),
                "Tickets":  st.column_config.NumberColumn("Tickets Sold"),
                "Revenue":  st.column_config.TextColumn("Revenue"),
            }
        )


def render_customers(analytics: dict):
    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 👥 TOP CUSTOMERS")
    a = analytics

    if a["top_customers"].empty:
        st.info("No customer data available.")
        return

    col1, col2 = st.columns([2, 1])
    with col1:
        fig = go.Figure(go.Bar(
            x=a["top_customers"]["Spent"],
            y=a["top_customers"]["CustomerName"],
            orientation="h",
            marker_color="#a855f7",
            text=a["top_customers"]["Spent"].apply(lambda x: f"₹{x:,.0f}"),
            textposition="outside",
            textfont_color="#e8e8f0",
        ))
        fig.update_layout(title="Top 10 Customers by Spend", height=380, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        display = a["top_customers"].copy()
        display["Spent"] = display["Spent"].apply(lambda x: f"₹{x:,.0f}")
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "CustomerName": st.column_config.TextColumn("Customer"),
                "Tickets":      st.column_config.NumberColumn("Tickets"),
                "Spent":        st.column_config.TextColumn("Total Spent"),
            }
        )


def render_raw_data(df: pd.DataFrame):
    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🗃️ RAW DATA")

    search_term = st.text_input("🔍 Search in data", placeholder="Filter by name, section, channel…")
    if search_term:
        mask = df.astype(str).apply(lambda col: col.str.contains(search_term, case=False, na=False)).any(axis=1)
        df_show = df[mask]
    else:
        df_show = df

    st.markdown(f"<small style='color:#6a6a8a;'>Showing {len(df_show):,} / {len(df):,} rows</small>", unsafe_allow_html=True)
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    # Download
    csv_bytes = df.to_csv(index=False).encode()
    st.download_button(
        label="⬇ Download as CSV",
        data=csv_bytes,
        file_name="ticket_data_export.csv",
        mime="text/csv",
    )


def render_chatbot(analytics: dict, df: pd.DataFrame):
    st.markdown('<div class="sec-divider"></div>', unsafe_allow_html=True)
    st.markdown("## 🤖 AI INSIGHTS CHATBOT")

    if not GROQ_API_KEY:
        st.markdown("""
        <div class="banner-warning">
            ⚠️ Groq API key not configured.<br>
            Add <code>GROQ_API_KEY=your_key</code> to your <code>.env</code> file and restart the app.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="banner-info" style='margin-bottom:20px;'>
        💡 Ask me anything about your ticket sales — trends, recommendations, anomalies, revenue forecasts, and more.
    </div>
    """, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    context_summary = build_context_summary(analytics, df)

    # Render chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-user">
                <div class="chat-label" style="color:#c8f53d;">YOU</div>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bot">
                <div class="chat-label" style="color:#a855f7;">AI ANALYST</div>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)

    # Suggested queries
    if not st.session_state.chat_history:
        st.markdown("**💬 Try asking:**")
        suggestions = [
            "What is the best-performing section?",
            "Which booking channel drives the most revenue?",
            "When was the peak sales day?",
            "Is the early bird discount helping sales?",
            "Give me a revenue summary",
        ]
        cols = st.columns(len(suggestions))
        for i, s in enumerate(suggestions):
            if cols[i].button(s, key=f"sug_{i}"):
                with st.spinner("Thinking…"):
                    reply = ask_groq(s, context_summary, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "user", "content": s})
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    # Input
    col_input, col_btn, col_clear = st.columns([6, 1, 1])
    with col_input:
        user_input = st.text_input("Your question…", key="chat_input", label_visibility="collapsed", placeholder="Ask about sales, revenue, trends…")
    with col_btn:
        send = st.button("Send ➤")
    with col_clear:
        if st.button("Clear"):
            st.session_state.chat_history = []
            st.rerun()

    if send and user_input.strip():
        with st.spinner("Analyzing…"):
            reply = ask_groq(user_input.strip(), context_summary, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()


# ─── LANDING PAGE ─────────────────────────────────────────────────────────────
def render_landing():
    st.markdown("""
    <div style='text-align:center; padding: 60px 0 40px;'>
        <div style='font-family:Space Mono,monospace; font-size:11px; letter-spacing:3px; color:#6a6a8a; margin-bottom:14px;'>
            ● SMART ANALYTICS PLATFORM
        </div>
        <div style='font-family:Bebas Neue,sans-serif; font-size:72px; letter-spacing:4px; line-height:0.9; color:#e8e8f0;'>
            TICKET SALES<br><span style='color:#c8f53d;'>ANALYTICS</span>
        </div>
        <div style='color:#6a6a8a; margin-top:18px; font-size:15px; max-width:520px; margin-left:auto; margin-right:auto;'>
            Upload your Excel or CSV file to unlock real-time insights, interactive charts,
            section performance, channel analysis, and AI-powered recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, title, desc in [
        (c1, "📈", "Revenue Analysis", "Total, avg & trend breakdowns"),
        (c2, "🏟️", "Section Insights", "VIP, Premium, General, Balcony"),
        (c3, "📡", "Channel Tracking", "Online vs Offline performance"),
        (c4, "🤖", "AI Chatbot", "Ask questions, get insights"),
    ]:
        col.markdown(f"""
        <div class="card" style='text-align:center;'>
            <div style='font-size:28px; margin-bottom:8px;'>{icon}</div>
            <div style='font-family:Bebas Neue,sans-serif; font-size:16px; letter-spacing:1px; color:#c8f53d;'>{title}</div>
            <div style='font-size:12px; color:#6a6a8a; margin-top:4px;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-top:28px; color:#6a6a8a; font-size:13px;'>
        ← Upload your file from the sidebar to get started
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown("""
    <div style='display:flex; align-items:center; gap:14px; margin-bottom:4px;'>
        <div style='font-size:32px;'>🎟️</div>
        <div>
            <span style='font-family:Space Mono,monospace; font-size:10px; letter-spacing:2px; color:#6a6a8a;'>
                SMART ANALYTICS PLATFORM
            </span><br>
            <span style='font-family:Bebas Neue,sans-serif; font-size:36px; letter-spacing:3px; color:#e8e8f0;'>
                TICKET SALES TRACKER
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "df" not in st.session_state:
        st.session_state.df = None
        st.session_state.analytics = None

    # Sidebar - ALWAYS render first
    with st.sidebar:
        st.markdown("""
        <div style='padding:10px 0 24px'>
            <div style='font-family:Space Mono,monospace; font-size:10px; letter-spacing:2px; color:#6a6a8a; margin-bottom:6px;'>● LIVE SYSTEM</div>
            <div style='font-family:Bebas Neue,sans-serif; font-size:28px; letter-spacing:3px; color:#c8f53d;'>TICKET<br>ANALYTICS</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📂 Upload Data")
        uploaded = st.file_uploader(
            "Drop your .xlsx or .csv file",
            type=["xlsx", "xls", "csv"],
            help="Columns expected: TicketID, SeatSection, Price, PurchaseDate, IsSold, Channel",
        )

        discount_pct = 10.0
        
        # Show settings and stats if data is loaded
        if st.session_state.analytics:
            st.markdown("---")
            st.markdown("### ⚙️ Settings")
            discount_pct = st.slider(
                "Early Bird Discount %",
                min_value=1, max_value=50, value=10, step=1,
                help="Applied while sold tickets < 25% of total"
            )
            # Recompute with new discount if changed
            if discount_pct != st.session_state.analytics.get('discount_pct', 10):
                st.session_state.analytics = compute_analytics(st.session_state.df, discount_pct)

            st.markdown("---")
            st.markdown("### 📊 Quick Stats")
            a = st.session_state.analytics
            st.markdown(f"""
            <div style='font-family:Space Mono,monospace; font-size:12px; line-height:2;'>
                <div>🎟️ Sold: <span style='color:#c8f53d'>{a['total_sold']}/{a['total_tickets']}</span></div>
                <div>💰 Revenue: <span style='color:#38e8c8'>₹{a['total_revenue']:,.0f}</span></div>
                <div>📈 Fill Rate: <span style='color:#a855f7'>{a['sold_pct']:.1f}%</span></div>
                <div>🏷️ Early Bird: <span style='color:{"#c8f53d" if a["early_bird_active"] else "#f53d8f"}'>{"ACTIVE" if a["early_bird_active"] else "CLOSED"}</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style='font-family:Space Mono,monospace; font-size:10px; color:#6a6a8a; line-height:1.8;'>
            Built by Pranav Agale<br>
            Stack: Python · Streamlit<br>
            AI: Groq · LLaMA3
        </div>
        """, unsafe_allow_html=True)

    # Handle file upload
    if uploaded is not None:
        try:
            raw_bytes = uploaded.read()
            df = load_data(raw_bytes, uploaded.name)
            df = process_data(df)
            st.session_state.df = df
            st.session_state.analytics = compute_analytics(df, discount_pct)
        except Exception as e:
            st.error(f"❌ Failed to load file: {e}")
            return

    # Show landing page if no data
    if st.session_state.df is None:
        render_landing()
        return

    # Render tabs with loaded data
    analytics = st.session_state.analytics
    
    tab_overview, tab_sections, tab_channels, tab_customers, tab_raw, tab_chat = st.tabs([
        "📊 Overview",
        "🏟️ Sections",
        "📡 Channels",
        "👥 Customers",
        "🗃️ Raw Data",
        "🤖 AI Chat",
    ])

    with tab_overview:
        render_overview(analytics)

    with tab_sections:
        render_sections(analytics)

    with tab_channels:
        render_channels(analytics)

    with tab_customers:
        render_customers(analytics)

    with tab_raw:
        render_raw_data(st.session_state.df)

    with tab_chat:
        render_chatbot(analytics, st.session_state.df)


if __name__ == "__main__":
    main()