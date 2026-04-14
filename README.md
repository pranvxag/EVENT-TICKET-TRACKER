# Nova Fest 2025 — Ticket System

## Files
```
novafest/
├── ticket_store.html           ← Ticket buying page
├── ticket_tracker_dashboard.html  ← Tracker + Date-wise Sales
├── server.py                   ← Python calculation server
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Python server
```bash
python server.py
```
Server runs at http://localhost:5050

### 3. Open the HTML files
Open both in your browser (same window, different tabs):
- `ticket_store.html`
- `ticket_tracker_dashboard.html`

They share data via **localStorage** and send calculations to the **Python server**.

---

## Architecture

```
ticket_store.html  ←──localStorage──→  ticket_tracker_dashboard.html
       ↕                                           ↕
       └──────────── Python server ────────────────┘
                     localhost:5050
                     /stats  /search  /date-graph
```

### Python API Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Server liveness check |
| `/stats` | POST | Full stats: revenue, section breakdown, date series |
| `/search` | POST | Filter + sort tickets |
| `/date-graph` | POST | Date-wise sales series for charts |

> **Note:** If the Python server is offline, both pages fall back to JavaScript calculations automatically. The UI always works.

---

## Tracker Dashboard Pages
| Page | Nav Button | Description |
|---|---|---|
| Dashboard | 📊 Dashboard | Original live tracker (unchanged) |
| Date-wise Sales | 📈 Date-wise Sales | Bar/line/cumulative chart + section comparison + heatmap |

More pages coming soon!
