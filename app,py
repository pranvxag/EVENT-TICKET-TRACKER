import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Event Ticket Sales Tracker",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
    }
    
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    }
    
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin: 10px 0;
        border: none;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
        font-weight: 500;
    }
    
    .ticket-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .ticket-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .sold-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .available-badge {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .progress-bar {
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Initialize session state for tickets
if 'tickets' not in st.session_state:
    st.session_state.tickets = []
    
    # Generate 5000 tickets across different sections
    sections = {
        'VIP': {'price': 500, 'seats': 200},
        'Premium': {'price': 300, 'seats': 800},
        'General A': {'price': 150, 'seats': 1500},
        'General B': {'price': 100, 'seats': 1500},
        'Economy': {'price': 50, 'seats': 1000}
    }
    
    ticket_id = 1
    # Generate tickets with some already sold
    for section, info in sections.items():
        for seat in range(1, info['seats'] + 1):
            # Randomly mark some tickets as sold (about 60% sold)
            is_sold = random.random() < 0.6
            purchase_date = None
            if is_sold:
                # Random purchase date within last 30 days
                days_ago = random.randint(0, 30)
                purchase_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            ticket = {
                'TicketID': f'T{ticket_id:05d}',
                'SeatSection': section,
                'SeatNumber': seat,
                'Price': info['price'],
                'IsSold': is_sold,
                'PurchaseDate': purchase_date
            }
            st.session_state.tickets.append(ticket)
            ticket_id += 1

# Convert to DataFrame for easy handling
def get_tickets_df():
    return pd.DataFrame(st.session_state.tickets)

# Header
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1>🎵 Event Ticket Sales Tracker 🎫</h1>
    <p style="color: rgba(255,255,255,0.8); font-size: 18px;">
        Concert Venue Management System | 5000 Capacity
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h2 style="color: white;">🎸 Control Panel</h2>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("", ["📊 Dashboard", "🔍 Find Tickets", "💰 Revenue", "⏰ Early Bird Check"])

df = get_tickets_df()

# ========== DASHBOARD PAGE ==========
if page == "📊 Dashboard":
    st.markdown("<h2 style='text-align: center; color: white;'>Live Sales Dashboard</h2>", unsafe_allow_html=True)
    
    # Calculate metrics
    total_tickets = len(df)
    sold_tickets = len(df[df['IsSold'] == True])
    available_tickets = total_tickets - sold_tickets
    total_revenue = df[df['IsSold'] == True]['Price'].sum()
    sold_percentage = (sold_tickets / total_tickets) * 100
    
    # Metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_tickets}</div>
            <div class="metric-label">Total Tickets</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f5576c;">{sold_tickets}</div>
            <div class="metric-label">Tickets Sold</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #00f2fe;">{available_tickets}</div>
            <div class="metric-label">Available</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #764ba2;">${total_revenue:,}</div>
            <div class="metric-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.9); padding: 20px; border-radius: 15px;">
        <h3 style="color: #333; margin-bottom: 10px;">Sales Progress: {sold_percentage:.1f}%</h3>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {sold_percentage}%"></div>
        </div>
        <p style="color: #666; margin-top: 10px;">Target: 75% for Early Bird Promotion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Section breakdown
    st.markdown("<br><h3 style='color: white; text-align: center;'>Sales by Section</h3>", unsafe_allow_html=True)
    
    section_stats = df.groupby('SeatSection').agg({
        'IsSold': ['sum', 'count'],
        'Price': 'first'
    }).reset_index()
    section_stats.columns = ['Section', 'Sold', 'Total', 'Price']
    section_stats['Available'] = section_stats['Total'] - section_stats['Sold']
    section_stats['Revenue'] = section_stats['Sold'] * section_stats['Price']
    
    cols = st.columns(len(section_stats))
    for idx, row in section_stats.iterrows():
        with cols[idx]:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <h4 style="color: #667eea; margin: 0;">{row['Section']}</h4>
                <p style="font-size: 24px; font-weight: 700; color: #333; margin: 10px 0;">
                    {row['Sold']}/{row['Total']}
                </p>
                <p style="color: #666; font-size: 12px;">${row['Price']} per ticket</p>
                <p style="color: #764ba2; font-weight: 600;">${row['Revenue']:,} revenue</p>
            </div>
            """, unsafe_allow_html=True)

# ========== FIND TICKETS PAGE ==========
elif page == "🔍 Find Tickets":
    st.markdown("<h2 style='text-align: center; color: white;'>Find Available Tickets</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px;">
            <h3 style="color: #333;">Filter by Section</h3>
        </div>
        """, unsafe_allow_html=True)
        selected_section = st.selectbox("Choose Section", ['All'] + list(df['SeatSection'].unique()))
    
    with col2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px;">
            <h3 style="color: #333;">Budget Filter</h3>
        </div>
        """, unsafe_allow_html=True)
        max_price = st.slider("Maximum Price ($)", 0, 500, 500, 50)
    
    # Filter tickets
    filtered_df = df.copy()
    
    if selected_section != 'All':
        filtered_df = filtered_df[filtered_df['SeatSection'] == selected_section]
    
    filtered_df = filtered_df[filtered_df['Price'] <= max_price]
    
    # Show available tickets
    available = filtered_df[filtered_df['IsSold'] == False].sort_values('Price')
    
    st.markdown(f"<br><h3 style='color: white;'>Found {len(available)} Available Tickets</h3>", unsafe_allow_html=True)
    
    if len(available) > 0:
        # Show tickets in a grid
        ticket_cols = st.columns(3)
        for idx, (_, ticket) in enumerate(available.head(12).iterrows()):
            with ticket_cols[idx % 3]:
                st.markdown(f"""
                <div class="ticket-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 20px; font-weight: 700; color: #667eea;">
                            {ticket['SeatSection']}
                        </span>
                        <span class="available-badge">AVAILABLE</span>
                    </div>
                    <p style="color: #666; margin: 10px 0;">Seat #{ticket['SeatNumber']}</p>
                    <p style="font-size: 28px; font-weight: 700; color: #764ba2; margin: 10px 0;">
                        ${ticket['Price']}
                    </p>
                    <p style="color: #999; font-size: 12px;">ID: {ticket['TicketID']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Sort option
        st.markdown("<br>", unsafe_allow_html=True)
        sort_order = st.radio("Sort by Price:", ["Low to High", "High to Low"], horizontal=True)
        
        if sort_order == "High to Low":
            available = available.sort_values('Price', ascending=False)
        
        # Show as table too
        st.markdown("""
        <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-top: 20px;">
            <h3 style="color: #333;">Detailed List</h3>
        </div>
        """, unsafe_allow_html=True)
        
        display_df = available[['TicketID', 'SeatSection', 'SeatNumber', 'Price']].copy()
        display_df.columns = ['Ticket ID', 'Section', 'Seat #', 'Price ($)']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No tickets available matching your criteria!")

# ========== REVENUE PAGE ==========
elif page == "💰 Revenue":
    st.markdown("<h2 style='text-align: center; color: white;'>Revenue Analysis</h2>", unsafe_allow_html=True)
    
    sold_df = df[df['IsSold'] == True].copy()
    
    # Calculate revenue by section
    revenue_by_section = sold_df.groupby('SeatSection').agg({
        'Price': ['sum', 'count', 'mean']
    }).reset_index()
    revenue_by_section.columns = ['Section', 'Total Revenue', 'Tickets Sold', 'Avg Price']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #667eea; margin-bottom: 20px;">Revenue by Section</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for _, row in revenue_by_section.iterrows():
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #333;">{row['Section']}</span>
                    <span style="font-size: 20px; font-weight: 700; color: #764ba2;">${row['Total Revenue']:,.0f}</span>
                </div>
                <p style="color: #666; font-size: 12px; margin: 5px 0 0 0;">
                    {row['Tickets Sold']} tickets @ ${row['Avg Price']:.0f} avg
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #667eea; margin-bottom: 20px;">Sales Summary</h3>
        </div>
        """, unsafe_allow_html=True)
        
        total_rev = sold_df['Price'].sum()
        total_sold = len(sold_df)
        avg_ticket = sold_df['Price'].mean()
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <p style="font-size: 48px; font-weight: 700; color: #667eea; margin: 0;">${total_rev:,}</p>
            <p style="color: #666;">Total Revenue</p>
        </div>
        <hr style="border: 1px solid #eee;">
        <div style="display: flex; justify-content: space-around; padding: 20px 0;">
            <div style="text-align: center;">
                <p style="font-size: 28px; font-weight: 700; color: #f5576c; margin: 0;">{total_sold}</p>
                <p style="color: #666; font-size: 12px;">Tickets Sold</p>
            </div>
            <div style="text-align: center;">
                <p style="font-size: 28px; font-weight: 700; color: #00f2fe; margin: 0;">${avg_ticket:.0f}</p>
                <p style="color: #666; font-size: 12px;">Average Price</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Daily sales trend (simulated)
    st.markdown("<br><h3 style='color: white; text-align: center;'>Daily Sales Trend</h3>", unsafe_allow_html=True)
    
    # Create sample daily data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    daily_sales = []
    cumulative = 0
    
    for date in dates:
        # Simulate daily sales
        daily = random.randint(50, 150)
        cumulative += daily
        daily_sales.append({
            'Date': date.strftime('%m/%d'),
            'Daily Sales': daily,
            'Cumulative': cumulative
        })
    
    trend_df = pd.DataFrame(daily_sales)
    
    st.markdown("""
    <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px;">
    """, unsafe_allow_html=True)
    st.line_chart(trend_df.set_index('Date')[['Daily Sales', 'Cumulative']])
    st.markdown("</div>", unsafe_allow_html=True)

# ========== EARLY BIRD PAGE ==========
elif page == "⏰ Early Bird Check":
    st.markdown("<h2 style='text-align: center; color: white;'>Early Bird Promotion Tracker</h2>", unsafe_allow_html=True)
    
    total_tickets = len(df)
    sold_tickets = len(df[df['IsSold'] == True])
    sold_percentage = (sold_tickets / total_tickets) * 100
    target_percentage = 75
    remaining_to_target = (target_percentage / 100 * total_tickets) - sold_tickets
    
    # Main status card
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.95); padding: 30px; border-radius: 20px; text-align: center; margin: 20px 0;">
        <h2 style="color: #667eea; margin-bottom: 20px;">Early Bird Target: 75% Sales</h2>
        <div style="display: flex; justify-content: center; align-items: center; gap: 30px; flex-wrap: wrap;">
            <div>
                <p style="font-size: 64px; font-weight: 700; color: {'#00d26a' if sold_percentage >= 75 else '#f5576c'}; margin: 0;">
                    {sold_percentage:.1f}%
                </p>
                <p style="color: #666;">Current Sales</p>
            </div>
            <div style="font-size: 48px; color: #ddd;">→</div>
            <div>
                <p style="font-size: 64px; font-weight: 700; color: #667eea; margin: 0;">75%</p>
                <p style="color: #666;">Target</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if sold_percentage >= 75:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00d26a 0%, #00b894 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; margin: 20px 0;">
            <h2 style="color: white; margin: 0;">🎉 TARGET ACHIEVED! 🎉</h2>
            <p style="color: rgba(255,255,255,0.9); font-size: 18px; margin: 10px 0 0 0;">
                Early Bird promotion can now be closed!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%); 
                    padding: 25px; border-radius: 15px; text-align: center; margin: 20px 0;">
            <h2 style="color: white; margin: 0;">⏳ TARGET NOT YET REACHED</h2>
            <p style="color: rgba(255,255,255,0.9); font-size: 18px; margin: 10px 0 0 0;">
                Need {remaining_to_target:.0f} more sales to reach 75%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Section-wise progress
    st.markdown("<br><h3 style='color: white; text-align: center;'>Progress by Section</h3>", unsafe_allow_html=True)
    
    section_progress = df.groupby('SeatSection').agg({
        'IsSold': ['sum', 'count']
    }).reset_index()
    section_progress.columns = ['Section', 'Sold', 'Total']
    section_progress['Percentage'] = (section_progress['Sold'] / section_progress['Total']) * 100
    
    for _, row in section_progress.iterrows():
        pct = row['Percentage']
        color = '#00d26a' if pct >= 75 else '#f5576c'
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #333; font-size: 18px;">{row['Section']}</span>
                <span style="font-weight: 700; color: {color}; font-size: 20px;">{pct:.1f}%</span>
            </div>
            <div style="background: #f0f0f0; border-radius: 10px; height: 15px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                            width: {pct}%; height: 100%; border-radius: 10px;"></div>
            </div>
            <p style="color: #666; font-size: 12px; margin: 8px 0 0 0;">
                {row['Sold']} of {row['Total']} tickets sold
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Promotion cutoff date estimation
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(255,255,255,0.95); padding: 25px; border-radius: 15px;">
        <h3 style="color: #667eea; margin-bottom: 15px;">📅 Promotion Strategy</h3>
        <p style="color: #555; line-height: 1.6;">
            <strong>Current Status:</strong> The early bird promotion offers discounted prices to incentivize 
            early purchases. Once 75% of tickets are sold, the promotion ends and regular pricing applies.
        </p>
        <p style="color: #555; line-height: 1.6;">
            <strong>Recommendation:</strong> Monitor sales daily. If the target is not reached within 
            the promotional period, consider extending the deadline or increasing marketing efforts.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 30px; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.2);">
    <p style="color: rgba(255,255,255,0.6);">
        🎫 Event Ticket Sales Tracker | Python Course Project<br>
        Built with ❤️ using Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
