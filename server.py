"""
Nova Fest — Ticket Calculation Server
Run: python server.py
All heavy maths live here; HTML files call this via fetch().
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json, datetime, collections

app = Flask(__name__)
CORS(app)   # allow same-machine cross-origin calls from file:// or localhost

# ──────────────────────────────────────────
#  Helper: derive stats from raw ticket list
# ──────────────────────────────────────────
def compute_stats(tickets: list) -> dict:
    CAPACITY = 5000

    sold   = [t for t in tickets if t.get("sold")]
    avail  = [t for t in tickets if not t.get("sold")]

    # --- Revenue per section (Python dict comprehension) ---
    sections = ["VIP", "Premium", "General", "Balcony"]
    rev_by_section = {}
    sold_by_section = {}
    avail_by_section = {}
    total_by_section = {}

    for sec in sections:
        sec_tickets = [t for t in tickets if t["section"] == sec]
        sec_sold    = [t for t in sec_tickets if t.get("sold")]
        rev_by_section[sec]   = sum(t["price"] for t in sec_sold)
        sold_by_section[sec]  = len(sec_sold)
        avail_by_section[sec] = len([t for t in sec_tickets if not t.get("sold")])
        total_by_section[sec] = len(sec_tickets)

    total_revenue = sum(t["price"] for t in sold)
    pct_sold      = round((len(sold) / CAPACITY) * 100, 2)

    # --- Date-wise sales (last 30 days, sorted) ---
    date_counts: dict = collections.defaultdict(lambda: {"count": 0, "revenue": 0})
    for t in sold:
        d = t.get("date")
        if d:
            date_counts[d]["count"]   += 1
            date_counts[d]["revenue"] += t["price"]

    date_series = [
        {"date": k, "count": v["count"], "revenue": v["revenue"]}
        for k, v in sorted(date_counts.items())
    ]

    # --- Cumulative sold series ---
    cumulative = 0
    for entry in date_series:
        cumulative += entry["count"]
        entry["cumulative"] = cumulative

    # --- Section breakdown for pie-ish chart ---
    section_breakdown = [
        {
            "section": sec,
            "sold":    sold_by_section[sec],
            "avail":   avail_by_section[sec],
            "total":   total_by_section[sec],
            "revenue": rev_by_section[sec],
            "price":   next((t["price"] for t in tickets if t["section"] == sec), 0),
            "pct_sold": round(
                sold_by_section[sec] / total_by_section[sec] * 100
                if total_by_section[sec] else 0, 1
            )
        }
        for sec in sections
    ]

    # --- 75% early-bird flag ---
    early_bird_hit = pct_sold >= 75.0

    # --- Top buyers (leaderboard) ---
    buyer_spend: dict = collections.defaultdict(int)
    for t in sold:
        if t.get("buyer"):
            buyer_spend[t["buyer"]] += t["price"]
    top_buyers = sorted(
        [{"buyer": k, "total": v} for k, v in buyer_spend.items()],
        key=lambda x: x["total"], reverse=True
    )[:5]

    return {
        "total_tickets":     len(tickets),
        "sold_count":        len(sold),
        "avail_count":       len(avail),
        "total_revenue":     total_revenue,
        "pct_sold":          pct_sold,
        "capacity":          CAPACITY,
        "early_bird_hit":    early_bird_hit,
        "rev_by_section":    rev_by_section,
        "section_breakdown": section_breakdown,
        "date_series":       date_series,
        "top_buyers":        top_buyers,
    }


# ──────────────────────────────────────────
#  Routes
# ──────────────────────────────────────────

@app.route("/stats", methods=["POST"])
def stats():
    """POST { tickets: [...] }  →  full stats JSON"""
    body    = request.get_json(force=True)
    tickets = body.get("tickets", [])
    return jsonify(compute_stats(tickets))


@app.route("/search", methods=["POST"])
def search():
    """POST { tickets, query, filter, sort_by, sort_dir }
       Returns filtered + sorted ticket list."""
    body    = request.get_json(force=True)
    tickets = body.get("tickets", [])
    query   = body.get("query",  "").lower()
    filt    = body.get("filter", "all")      # all | sold | available
    sort_by = body.get("sort_by", "id")      # id | price | date | section
    sort_dir= body.get("sort_dir", "asc")

    # Filter
    if filt == "sold":      tickets = [t for t in tickets if t.get("sold")]
    if filt == "available": tickets = [t for t in tickets if not t.get("sold")]
    if query:
        tickets = [
            t for t in tickets
            if query in t["id"].lower()
            or query in t["section"].lower()
            or query in (t.get("buyer") or "").lower()
        ]

    # Sort
    reverse = sort_dir == "desc"
    key_map = {
        "id":      lambda t: t["id"],
        "price":   lambda t: t["price"],
        "date":    lambda t: t.get("date") or "",
        "section": lambda t: t["section"],
    }
    tickets = sorted(tickets, key=key_map.get(sort_by, key_map["id"]), reverse=reverse)

    return jsonify({"tickets": tickets, "count": len(tickets)})


@app.route("/date-graph", methods=["POST"])
def date_graph():
    """POST { tickets }  →  date-series for chart rendering"""
    body    = request.get_json(force=True)
    tickets = body.get("tickets", [])
    stats   = compute_stats(tickets)
    return jsonify({
        "date_series":       stats["date_series"],
        "section_breakdown": stats["section_breakdown"],
        "total_revenue":     stats["total_revenue"],
        "sold_count":        stats["sold_count"],
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": datetime.datetime.now().isoformat()})


if __name__ == "__main__":
    print("\n  Nova Fest Python Server")
    print("  ========================")
    print("  Running on  http://localhost:5050")
    print("  Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=5050, debug=True)
