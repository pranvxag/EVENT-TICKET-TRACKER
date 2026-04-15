# 🎟️ Smart Ticket Sales Tracking & Analytics System

A full-featured, AI-powered ticket sales analytics platform built with **Python**, **Streamlit**, **Plotly**, and **Groq API**. Upload your Excel or CSV file and instantly get interactive dashboards, section-wise breakdowns, channel performance, early-bird discount tracking, and an AI chatbot powered by LLaMA 3.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ticket-analytics.git
cd ticket-analytics
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a `.env` file in the project root (already provided, but **never commit it**):

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [https://console.groq.com](https://console.groq.com).

### 5. Run the application

```bash
streamlit run app.py
```
or
```bash
python -m streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
ticket-analytics/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # API key (not committed to Git)
├── .gitignore              # Prevents sensitive files from being pushed
├── README.md               # This file
└── sample_ticket_data.xlsx # Sample dataset for testing
```

---

## 📊 Features

| Feature | Description |
|---|---|
| **File Upload** | Supports `.xlsx`, `.xls`, and `.csv` ticket data files |
| **Overview Dashboard** | Total revenue, tickets sold, fill rate, avg price |
| **Section Analysis** | Bar + donut charts per section (VIP, Premium, etc.) |
| **Date Trends** | Daily revenue area chart + cumulative growth curve |
| **Channel Breakdown** | Sales by booking channel (Paytm, Online, Agent, etc.) |
| **Day-of-Week Heatmap** | Identifies peak booking days |
| **Top Customers** | Ranked by total spend |
| **Early Bird Discount** | Auto-disabled after 25% of tickets are sold |
| **AI Chatbot** | Groq-powered LLaMA 3 analyst answering natural language queries |
| **Raw Data Explorer** | Search, filter, and download processed data as CSV |

---

## 🐍 Role of Python in This System

Python is the backbone of the entire backend logic and data pipeline:

### Data Ingestion
`pandas.read_excel()` and `pandas.read_csv()` handle multi-format file loading with type inference. The `@st.cache_data` decorator caches parsed DataFrames so re-uploads don't re-process unnecessarily.

### Data Normalization (`process_data`)
A custom function maps messy real-world column names (e.g., `"booking_mode"`, `"date"`, `"status"`) to a standardized schema using string matching. It then coerces types: dates via `pd.to_datetime()`, prices via `pd.to_numeric()`, and boolean sold-status via whitelist matching.

### Analytics Engine (`compute_analytics`)
NumPy and Pandas power all KPI calculations:
- **Revenue aggregation**: `df["Price"].sum()`, `.mean()`, `.median()`
- **Group-by analytics**: `df.groupby("SeatSection").agg(...)` for section stats
- **Time-series derivation**: `.dt.date`, `.dt.day_name()`, `.dt.isocalendar()` for trend data
- **Cumulative metrics**: `.cumsum()` for growth curves
- **Early Bird logic**: threshold = `total_tickets * 0.25`, compared against `total_sold`

### Visualization
Plotly Express and Graph Objects build all interactive charts. Data flows directly from Pandas DataFrames into Plotly figures with no intermediate files.

### AI Context Building (`build_context_summary`)
Python string formatting constructs a compact analytics snapshot that is injected as the system prompt for the Groq LLM, enabling context-aware answers grounded in real data.

---

## 📋 Expected Data Columns

Your Excel/CSV file should include these columns (names are flexible — the app auto-maps common variations):

| Column | Description | Example |
|---|---|---|
| `TicketID` | Unique ticket identifier | TKT-1001 |
| `SeatSection` | Section category | VIP, Premium, General |
| `Row` | Row number | 1, 2, 3 |
| `SeatNumber` | Seat number within row | 5 |
| `Price` | Ticket price in ₹ | 5500 |
| `PurchaseDate` | Date of booking | 2024-11-15 |
| `IsSold` | Whether ticket was sold | Yes / No |
| `Channel` | Booking platform | Online, Paytm, Agent |
| `CustomerName` | Buyer's name | Rahul Sharma |

---

## 🔒 Security

- The Groq API key is loaded from `.env` via `python-dotenv` — it is **never hardcoded**
- `.env` is listed in `.gitignore` — it will not be pushed to GitHub
- Streamlit Secrets (`secrets.toml`) can be used as an alternative on Streamlit Cloud

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit 1.32+ |
| Data Processing | Pandas 2.0, NumPy 1.26 |
| Visualizations | Plotly 5.x |
| AI Chatbot | Groq API (LLaMA 3 8B) |
| Env Management | python-dotenv |
| File Parsing | openpyxl, xlrd |

---

## 🔮 Future Enhancements

- **Forecasting**: ARIMA / Prophet model for revenue prediction
- **Seat map visualization**: Interactive SVG seat map with status overlay
- **Multi-event comparison**: Compare two events side-by-side
- **Export to PDF**: Auto-generate analytics report
- **Streamlit Cloud deployment**: One-click public deployment
- **Email alerts**: Notify when early-bird threshold is crossed

---

## 👤 Author

**Pranav Agale**  
B.Tech CSE · Vishwakarma University, Pune  
[GitHub](https://github.com/prnanvxag) · [Hugging Face](https://huggingface.co/prnanvxag)
