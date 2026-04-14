# 🎟️ Smart Ticket Sales Tracking & Analytics System

A full-featured ticket sales analytics dashboard built with Python, Streamlit, and Groq AI.

## Features

- **Data Upload** — Upload `.xlsx` or `.csv` ticket data files
- **Live Analytics** — Total revenue, tickets sold, available seats, section-wise breakdown
- **Interactive Charts** — Daily trends, revenue share, booking mode comparison (Plotly)
- **Visual Seat Map** — Color-coded grid showing sold vs. available seats by section
- **Early Bird Discount** — Automatically disabled once 25% of tickets are sold
- **AI Chatbot** — Powered by Groq API (LLaMA 3.3 70B) for intelligent sales insights
- **Ticket Registry** — Searchable and filterable ticket list

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd ticket-tracker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Groq API key

Create a `.env` file in the `ticket-tracker/` directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at [console.groq.com](https://console.groq.com).

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:5000`.

## Sample Data Format

Your Excel/CSV file should include these columns:

| Column | Description | Example |
|---|---|---|
| `ticket_id` | Unique ticket identifier | T001 |
| `seat_number` | Seat label | A1 |
| `section` | Zone name | VIP, Premium, General, Balcony |
| `price` | Ticket price (₹) | 5000 |
| `date` | Sale date (YYYY-MM-DD) | 2024-12-01 |
| `booking_mode` | online / offline | online |
| `is_sold` | Boolean (True/False) | True |

A sample file `sample_data.csv` is included for testing.

## Python Libraries Used

| Library | Role |
|---|---|
| **Pandas** | Data loading, cleaning, grouping, filtering, and transformation |
| **NumPy** | Numerical computations — `np.sum()`, `np.cumsum()`, array operations |
| **Streamlit** | Web UI framework — renders the dashboard in the browser |
| **Plotly** | Interactive charts — bar charts, pie/donut charts, line overlays |
| **Groq** | AI chatbot integration using LLaMA 3.3 70B model |
| **openpyxl** | Reading `.xlsx` Excel files with pandas |
| **python-dotenv** | Loading `GROQ_API_KEY` from a local `.env` file |

## Python's Role in This System

Python powers the entire backend logic of this application:

- **Data Processing**: `pandas.read_csv()` / `read_excel()` loads raw files into DataFrames. Column normalization, type coercion, and boolean parsing are all done with pandas operations.
- **Analysis**: NumPy arrays compute aggregate metrics — `np.sum()` calculates total revenue from sold ticket prices; `np.cumsum()` generates the cumulative trend line.
- **Filtering**: Boolean indexing (`df[df['is_sold'] == True]`) isolates sold tickets; `.groupby('section')` aggregates per-zone stats.
- **Early Bird Logic**: A threshold check (`sold / total < 0.25`) auto-disables early bird pricing once 25% capacity is reached.
- **AI Context**: Python builds a structured natural-language context string from computed stats, which is sent to the Groq API alongside the user's question.
- **Seat Map**: Python iterates over DataFrame rows to generate color-coded HTML seat cells dynamically.

## Project Structure

```
ticket-tracker/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── sample_data.csv     # Sample dataset for testing
├── README.md           # This file
├── .env                # Groq API key (not committed)
├── .gitignore          # Excludes .env, __pycache__, etc.
└── .streamlit/
    └── config.toml     # Streamlit server configuration
```
