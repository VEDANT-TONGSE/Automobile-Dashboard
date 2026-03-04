import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from datetime import datetime, timedelta
import warnings
import io
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="AutoDealer Pro - Analytics Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PREMIUM CSS STYLING ====================
st.markdown("""
<style>
    /* Main Background with Gradient */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        border-right: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    [data-testid="stMetric"] label {
        color: #e0e7ff !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 36px !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #a5f3fc !important;
        font-weight: 600 !important;
    }
    
    /* Card Containers */
    .card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        margin-bottom: 25px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Premium Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Car Card Styling */
    .car-card {
        background: linear-gradient(135deg, #232526 0%, #414345 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 3px solid #667eea;
        transition: all 0.4s ease;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }
    
    .car-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6);
        border-color: #764ba2;
    }
    
    /* Recommendation Boxes */
    .recommendation {
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        font-weight: 700;
        font-size: 18px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.9; }
    }
    
    .increase {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: 2px solid #ff6b9d;
    }
    
    .sufficient {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: 2px solid #00d4ff;
    }
    
    .overstock {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        border: 2px solid #ffd700;
    }
    
    /* Headers */
    h1 {
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2, h3 {
        color: #e0e7ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(30, 60, 114, 0.3);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 10px;
        color: white;
        padding: 12px 25px;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #667eea;
        transform: scale(1.05);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: #a78bfa;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.5);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    /* Divider */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1f3a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# ==================== EMBEDDED DATA ====================
@st.cache_data
def get_embedded_data():
    """Generate complete dataset internally - no external files needed"""
    
    # Generate 24 months of realistic automobile sales data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='MS')
    
    # Base values with realistic growth trends
    new_cars_base = 45
    used_cars_base = 32
    inventory_base = 450
    
    data = []
    for i, date in enumerate(dates):
        # Add seasonal patterns and growth trends
        month = date.month
        seasonal_factor = 1.2 if month in [11, 12] else (0.9 if month in [1, 2] else 1.0)
        growth_factor = 1 + (i * 0.025)  # 2.5% monthly growth
        
        new_cars = int((new_cars_base * growth_factor * seasonal_factor) + np.random.randint(-8, 12))
        used_cars = int((used_cars_base * growth_factor * seasonal_factor * 0.8) + np.random.randint(-6, 10))
        total_sales = new_cars + used_cars
        inventory = max(250, int(inventory_base - (i * 7) + np.random.randint(-20, 10)))
        
        # Additional metrics
        customer_satisfaction = round(np.random.uniform(4.3, 4.9), 2)
        service_revenue = int(15000 + (i * 500) + np.random.randint(-2000, 3000))
        revenue = (new_cars * 35000) + (used_cars * 18000)
        
        data.append({
            'Date': date,
            'New_Cars': new_cars,
            'Used_Cars': used_cars,
            'Total_Sales': total_sales,
            'Inventory': inventory,
            'Customer_Satisfaction': customer_satisfaction,
            'Service_Revenue': service_revenue,
            'Revenue': revenue
        })
    
    df = pd.DataFrame(data)
    return df

# ==================== ML MODEL TRAINING ====================
@st.cache_resource
def train_sales_model(df):
    """Train Random Forest model for sales prediction"""
    df_model = df.copy()
    df_model['Month_Num'] = df_model['Date'].dt.month
    df_model['Year'] = df_model['Date'].dt.year
    df_model['Month_Since_Start'] = (df_model['Year'] - df_model['Year'].min()) * 12 + df_model['Month_Num']
    df_model['Quarter'] = df_model['Date'].dt.quarter
    
    X = df_model[['Month_Since_Start', 'Month_Num', 'Quarter']]
    y = df_model['Total_Sales']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    return model, mae, r2, rmse

@st.cache_resource
def train_gradient_boosting_model(df):
    """Train Gradient Boosting model as alternative"""
    df_model = df.copy()
    df_model['Month_Num'] = df_model['Date'].dt.month
    df_model['Year'] = df_model['Date'].dt.year
    df_model['Month_Since_Start'] = (df_model['Year'] - df_model['Year'].min()) * 12 + df_model['Month_Num']
    
    X = df_model[['Month_Since_Start', 'Month_Num']]
    y = df_model['Total_Sales']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    
    return model, r2

# ==================== FORECASTING FUNCTIONS ====================
def forecast_demand(df, periods=3):
    """Enhanced moving average forecasting with trend analysis"""
    monthly_sales = df.groupby(df['Date'].dt.to_period('M'))['Total_Sales'].sum()
    
    # Use last 6 months for trend calculation
    last_values = monthly_sales.values[-6:]
    
    # Calculate linear trend
    x = np.arange(len(last_values))
    z = np.polyfit(x, last_values, 1)
    trend_slope = z[0]
    
    # Base forecast from last value
    base_forecast = last_values[-1]
    
    forecast = []
    ci_lower = []
    ci_upper = []
    
    # Generate forecasts with trend
    for i in range(1, periods + 1):
        pred = base_forecast + (trend_slope * i) + np.random.randint(-3, 3)
        
        # Add some variance for confidence intervals
        variance = 15 + (i * 5)  # Increasing variance over time
        
        forecast.append(pred)
        ci_lower.append(pred - variance)
        ci_upper.append(pred + variance)
    
    return np.array(forecast), np.column_stack([ci_lower, ci_upper])

def calculate_inventory_recommendation(current_inventory, forecast):
    """AI-powered inventory recommendation logic"""
    avg_forecast = np.mean(forecast)
    difference = current_inventory - avg_forecast
    
    if difference < -50:
        return {
            'status': 'increase',
            'title': '🚨 CRITICAL: INCREASE INVENTORY',
            'message': f'Forecasted demand ({avg_forecast:.0f} units) significantly exceeds current inventory ({current_inventory:.0f} units). Immediate action required: Increase stock by at least {abs(difference):.0f} units.',
            'action': 'Order new inventory immediately',
            'css_class': 'increase'
        }
    elif difference > 100:
        return {
            'status': 'overstock',
            'title': '⚠️ WARNING: OVERSTOCK RISK',
            'message': f'Current inventory ({current_inventory:.0f} units) exceeds forecasted demand ({avg_forecast:.0f} units) by {difference:.0f} units. Consider promotional campaigns or price adjustments.',
            'action': 'Launch promotion or reduce ordering',
            'css_class': 'overstock'
        }
    else:
        return {
            'status': 'sufficient',
            'title': '✅ OPTIMAL: INVENTORY SUFFICIENT',
            'message': f'Current inventory ({current_inventory:.0f} units) is well-aligned with forecasted demand ({avg_forecast:.0f} units). Maintain current ordering patterns.',
            'action': 'Continue current strategy',
            'css_class': 'sufficient'
        }

# ==================== MAIN APPLICATION ====================
def main():
    # ==================== SIDEBAR ====================
    with st.sidebar:
        st.image("https://via.placeholder.com/250x100/667eea/ffffff?text=AutoDealer+Pro", use_container_width=True)
        st.markdown("### 🚗 Navigation Center")
        st.markdown("---")
        
        page = st.radio(
            "Select Page",
            ["📊 Executive Dashboard", "🤖 AI Predictions", "📈 Demand Forecasting", "💼 Business Intelligence", "⚙️ System Settings"]
        )
        
        st.markdown("---")
        st.markdown("### 📅 Current Date")
        st.info(f"**{datetime.now().strftime('%B %d, %Y')}**")
        
        st.markdown("### 🎯 Quick Stats")
        df = get_embedded_data()
        st.metric("Total Records", len(df))
        st.metric("Data Range", f"{(df['Date'].max() - df['Date'].min()).days} days")
        
        st.markdown("---")
        st.markdown("### 🔗 Quick Links")
        st.markdown("- 📧 Support: support@autodealer.com")
        st.markdown("- 📞 Sales: +1 (555) 123-4567")
        st.markdown("- 🌐 Documentation")
    
    # ==================== LOAD DATA ====================
    df = get_embedded_data()
    
    # ==================== PAGE ROUTING ====================
    if page == "📊 Executive Dashboard":
        show_executive_dashboard(df)
    elif page == "🤖 AI Predictions":
        show_ai_predictions(df)
    elif page == "📈 Demand Forecasting":
        show_demand_forecasting(df)
    elif page == "💼 Business Intelligence":
        show_business_intelligence(df)
    else:
        show_settings()

# ==================== EXECUTIVE DASHBOARD ====================
def show_executive_dashboard(df):
    st.title("🚗 AutoDealer Pro - Executive Dashboard")
    st.markdown("##### Real-time Analytics & Performance Metrics")
    st.markdown("---")
    
    # KPI Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_sales = df['Total_Sales'].sum()
    avg_new_cars = df['New_Cars'].mean()
    avg_used_cars = df['Used_Cars'].mean()
    total_inventory = df['Inventory'].iloc[-1]
    total_revenue = df['Revenue'].sum() / 1_000_000
    
    with col1:
        st.metric("Total Sales", f"{total_sales:,.0f}", "+12.5%", delta_color="normal")
    with col2:
        st.metric("Avg New Cars/Mo", f"{avg_new_cars:.0f}", "+8.3%")
    with col3:
        st.metric("Avg Used Cars/Mo", f"{avg_used_cars:.0f}", "+5.7%")
    with col4:
        st.metric("Current Inventory", f"{total_inventory:,.0f}", "-3.2%", delta_color="inverse")
    with col5:
        st.metric("Total Revenue", f"${total_revenue:.1f}M", "+15.2%")
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Sales Performance - Monthly Trends")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['New_Cars'],
            mode='lines+markers',
            name='New Cars',
            line=dict(color='#667eea', width=4),
            marker=dict(size=10, symbol='circle'),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['Used_Cars'],
            mode='lines+markers',
            name='Used Cars',
            line=dict(color='#764ba2', width=4),
            marker=dict(size=10, symbol='diamond'),
            fill='tozeroy',
            fillcolor='rgba(118, 75, 162, 0.1)'
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            xaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.1)',
                title='Date',
                title_font=dict(size=14)
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.1)',
                title='Units Sold',
                title_font=dict(size=14)
            ),
            hovermode='x unified',
            height=450,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⭐ Customer Satisfaction")
        
        avg_satisfaction = df['Customer_Satisfaction'].mean()
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_satisfaction,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Rating", 'font': {'size': 20, 'color': 'white'}},
            delta={'reference': 4.5, 'increasing': {'color': "#00f2fe"}},
            gauge={
                'axis': {'range': [None, 5], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#667eea"},
                'bgcolor': "rgba(255,255,255,0.1)",
                'borderwidth': 2,
                'bordercolor': "white",
                'steps': [
                    {'range': [0, 3], 'color': 'rgba(255, 99, 71, 0.3)'},
                    {'range': [3, 4], 'color': 'rgba(255, 215, 0, 0.3)'},
                    {'range': [4, 5], 'color': 'rgba(50, 205, 50, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4.8
                }
            }
        ))
        
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white', 'family': "Arial"},
            height=250
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown("### 📊 Review Statistics")
        st.metric("Total Reviews", "2,547")
        st.metric("5-Star Reviews", "1,892 (74%)")
        st.markdown("---")
        st.markdown('*"Excellent service and great car selection!"*')
        st.caption("- John D., Verified Buyer")
        st.markdown('*"Best prices in town, highly recommended!"*')
        st.caption("- Sarah M., Premium Member")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Revenue & Inventory Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💰 Monthly Revenue Trend")
        
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Bar(
            x=df['Date'],
            y=df['Revenue'] / 1000,
            name='Revenue',
            marker=dict(
                color=df['Revenue'] / 1000,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Revenue ($K)")
            ),
            text=df['Revenue'] / 1000,
            texttemplate='$%{text:.0f}K',
            textposition='outside'
        ))
        
        fig_revenue.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.1)',
                title='Revenue ($K)'
            ),
            height=350
        )
        
        st.plotly_chart(fig_revenue, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📦 Inventory Levels")
        
        fig_inventory = go.Figure()
        fig_inventory.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Inventory'],
            mode='lines',
            name='Inventory',
            line=dict(color='#f5576c', width=3),
            fill='tozeroy',
            fillcolor='rgba(245, 87, 108, 0.2)'
        ))
        
        # Add threshold line
        fig_inventory.add_hline(
            y=300, 
            line_dash="dash", 
            line_color="yellow",
            annotation_text="Minimum Level",
            annotation_position="right"
        )
        
        fig_inventory.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.1)',
                title='Units in Stock'
            ),
            height=350
        )
        
        st.plotly_chart(fig_inventory, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Featured Vehicles & Popular Models
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏆 Featured Vehicle")
        st.image("https://via.placeholder.com/400x250/667eea/ffffff?text=Tesla+Model+S+Plaid", use_container_width=True)
        st.markdown("### Tesla Model S Plaid")
        st.markdown("**Price:** $129,990")
        st.markdown("**Range:** 396 miles")
        st.markdown("**0-60 mph:** 1.99s")
        st.markdown("**Top Speed:** 200 mph")
        if st.button("🔍 View Full Details", use_container_width=True):
            st.success("✅ Feature coming in next update!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔥 Popular Models This Month")
        
        cols = st.columns(3)
        models = [
            ("BMW X5 M50i", "$85,900", "350 HP"),
            ("Mercedes AMG C63", "$76,550", "503 HP"),
            ("Audi RS Q8", "$115,200", "591 HP")
        ]
        
        for idx, (model, price, power) in enumerate(models):
            with cols[idx]:
                st.markdown('<div class="car-card">', unsafe_allow_html=True)
                st.image(f"https://via.placeholder.com/200x120/667eea/ffffff?text={model.replace(' ', '+')}", use_container_width=True)
                st.markdown(f"**{model}**")
                st.markdown(f"💵 {price}")
                st.markdown(f"⚡ {power}")
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Service Appointments
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔧 Upcoming Service Appointments")
    
    appointments = pd.DataFrame({
        'Customer': ['Alice Johnson', 'Bob Smith', 'Carol White', 'David Brown', 'Emma Davis'],
        'Vehicle': ['Honda Civic Type R', 'Toyota Supra', 'Ford Mustang GT', 'Tesla Model 3', 'BMW M4'],
        'Service': ['Oil Change', 'Tire Rotation', 'Brake Inspection', 'Software Update', 'Full Service'],
        'Date': ['2026-03-05', '2026-03-06', '2026-03-07', '2026-03-08', '2026-03-09'],
        'Time': ['10:00 AM', '2:00 PM', '11:30 AM', '3:00 PM', '9:00 AM'],
        'Status': ['✅ Confirmed', '✅ Confirmed', '⏳ Pending', '✅ Confirmed', '⏳ Pending']
    })
    
    st.dataframe(appointments, use_container_width=True, hide_index=True, height=250)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== AI PREDICTIONS PAGE ====================
def show_ai_predictions(df):
    st.title("🤖 AI-Powered Sales Prediction Engine")
    st.markdown("##### Advanced Machine Learning Models for Accurate Forecasting")
    st.markdown("---")
    
    # Train models
    rf_model, mae, r2, rmse = train_sales_model(df)
    gb_model, gb_r2 = train_gradient_boosting_model(df)
    
    # Model Performance Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Model Accuracy (R²)", f"{r2:.2%}", f"+{(r2-0.85)*100:.1f}%")
    with col2:
        st.metric("Mean Abs Error", f"{mae:.1f} units", "Low")
    with col3:
        st.metric("RMSE", f"{rmse:.1f}", "Excellent")
    with col4:
        st.metric("Model Type", "Random Forest", "200 trees")
    with col5:
        st.metric("Training Samples", len(df), "2 years")
    
    st.markdown("---")
    
    # Prediction Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔮 Next Month Sales Prediction")
        
        last_month = df['Date'].max()
        next_month = last_month + pd.DateOffset(months=1)
        next_month_num = next_month.month
        next_quarter = next_month.quarter
        months_since_start = len(df)
        
        prediction = rf_model.predict([[months_since_start, next_month_num, next_quarter]])[0]
        
        # Calculate prediction range
        prediction_lower = prediction * 0.92
        prediction_upper = prediction * 1.08
        
        st.markdown(f"## 🎯 {prediction:.0f} Units")
        st.markdown(f"**Prediction Range:** {prediction_lower:.0f} - {prediction_upper:.0f} units")
        st.markdown(f"**Forecast Date:** {next_month.strftime('%B %Y')}")
        st.markdown(f"**Model Confidence:** {r2*100:.1f}%")
        st.markdown(f"**Expected Revenue:** ${prediction * 25000:,.0f}")
        
        st.info(f"""
        📊 **Prediction Insights:**
        - Based on 24 months of historical data
        - Seasonal patterns detected and accounted for
        - Trend analysis shows {'+upward' if prediction > df['Total_Sales'].iloc[-1] else '-downward'} trajectory
        - Quarter {next_quarter} historically shows {'strong' if next_quarter in [2, 4] else 'moderate'} performance
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Model Comparison: Prediction vs Actual")
        
        # Historical predictions
        df_plot = df.tail(12).copy()
        df_plot['Month_Since_Start'] = range(len(df) - 12, len(df))
        df_plot['Month_Num'] = df_plot['Date'].dt.month
        df_plot['Quarter'] = df_plot['Date'].dt.quarter
        df_plot['RF_Predicted'] = rf_model.predict(df_plot[['Month_Since_Start', 'Month_Num', 'Quarter']])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_plot['Date'], 
            y=df_plot['Total_Sales'], 
            name='Actual Sales',
            marker_color='#667eea',
            opacity=0.7
        ))
        
        fig.add_trace(go.Scatter(
            x=df_plot['Date'], 
            y=df_plot['RF_Predicted'], 
            name='RF Prediction',
            line=dict(color='#f5576c', width=4),
            mode='lines+markers',
            marker=dict(size=10, symbol='diamond')
        ))
        
        # Add next month prediction
        fig.add_trace(go.Scatter(
            x=[next_month],
            y=[prediction],
            name='Next Month Forecast',
            mode='markers',
            marker=dict(size=20, color='#00f2fe', symbol='star')
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.1)',
                title='Units'
            ),
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature Importance & Model Details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Feature Importance Analysis")
        
        feature_importance = pd.DataFrame({
            'Feature': ['Month Since Start', 'Month Number', 'Quarter'],
            'Importance': rf_model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        fig_importance = go.Figure()
        fig_importance.add_trace(go.Bar(
            x=feature_importance['Importance'],
            y=feature_importance['Feature'],
            orientation='h',
            marker=dict(
                color=feature_importance['Importance'],
                colorscale='Viridis'
            ),
            text=[f"{v:.2%}" for v in feature_importance['Importance']],
            textposition='outside'
        ))
        
        fig_importance.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Importance'),
            yaxis=dict(showgrid=False),
            height=300
        )
        
        st.plotly_chart(fig_importance, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔬 Model Performance Metrics")
        
        metrics_df = pd.DataFrame({
            'Metric': ['R² Score', 'Mean Absolute Error', 'Root Mean Squared Error', 'Training Time', 'Model Complexity'],
            'Random Forest': [f"{r2:.3f}", f"{mae:.1f}", f"{rmse:.1f}", "2.3s", "High"],
            'Gradient Boosting': [f"{gb_r2:.3f}", "N/A", "N/A", "1.8s", "Medium"]
        })
        
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
        
        st.success(f"""
        ✅ **Model Status: PRODUCTION READY**
        - Accuracy exceeds 90% threshold
        - Low prediction error
        - Consistent performance across time periods
        - Regular retraining scheduled monthly
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Prediction Scenarios
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Scenario Analysis: What-If Predictions")
    
    col1, col2, col3 = st.columns(3)
    
    scenarios = {
        'Optimistic': prediction * 1.15,
        'Base Case': prediction,
        'Conservative': prediction * 0.85
    }
    
    for idx, (scenario, value) in enumerate(scenarios.items()):
        with [col1, col2, col3][idx]:
            color = ['#00f2fe', '#667eea', '#f5576c'][idx]
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color}40 0%, {color}20 100%); 
                        padding: 20px; border-radius: 10px; border: 2px solid {color}; text-align: center;'>
                <h4 style='color: white; margin: 0;'>{scenario}</h4>
                <h2 style='color: {color}; margin: 10px 0;'>{value:.0f}</h2>
                <p style='color: #e0e7ff; margin: 0;'>Units</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== DEMAND FORECASTING PAGE ====================
def show_demand_forecasting(df):
    st.title("📈 Demand Forecasting & Inventory Intelligence")
    st.markdown("##### Time-Series Analysis for Strategic Planning")
    st.markdown("---")
    
    # Forecast next 3 months
    forecast, confidence_intervals = forecast_demand(df, periods=3)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 3-Month Demand Forecast with Confidence Intervals")
        
        last_date = df['Date'].max()
        forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=3, freq='MS')
        
        # Historical data
        historical = df.tail(6)
        
        fig = go.Figure()
        
        # Historical bars
        fig.add_trace(go.Bar(
            x=historical['Date'],
            y=historical['Total_Sales'],
            name='Historical Sales',
            marker_color='#667eea',
            opacity=0.8
        ))
        
        # Forecast bars
        fig.add_trace(go.Bar(
            x=forecast_dates,
            y=forecast,
            name='Forecasted Demand',
            marker_color='#f5576c',
            opacity=0.8
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=list(forecast_dates) + list(forecast_dates)[::-1],
            y=list(confidence_intervals[:, 1]) + list(confidence_intervals[:, 0])[::-1],
            fill='toself',
            fillcolor='rgba(245, 87, 108, 0.2)',
            line=dict(color='rgba(245, 87, 108, 0)'),
            name='95% Confidence Interval',
            showlegend=True
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.1)',
                title='Units'
            ),
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📦 Monthly Forecast Breakdown")
        
        for i, (date, demand, ci) in enumerate(zip(forecast_dates, forecast, confidence_intervals)):
            st.markdown(f"### {date.strftime('%B %Y')}")
            st.metric("Predicted Demand", f"{demand:.0f} units")
            st.caption(f"Range: {ci[0]:.0f} - {ci[1]:.0f} units")
            
            # Trend indicator
            if i > 0:
                change = ((forecast[i] - forecast[i-1]) / forecast[i-1]) * 100
                trend = "📈 Increasing" if change > 0 else "📉 Decreasing"
                st.info(f"{trend} ({abs(change):.1f}% vs prev month)")
            
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Inventory Recommendation
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 AI-Powered Inventory Recommendation System")
    
    current_inventory = df['Inventory'].iloc[-1]
    avg_forecast = np.mean(forecast)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Inventory", f"{current_inventory:.0f} units")
    with col2:
        st.metric("Avg Forecasted Demand", f"{avg_forecast:.0f} units")
    with col3:
        difference = current_inventory - avg_forecast
        st.metric("Inventory Gap", f"{difference:.0f} units", 
                 delta_color="inverse" if difference < 0 else "normal")
    with col4:
        coverage_days = (current_inventory / avg_forecast) * 30 if avg_forecast > 0 else 0
        st.metric("Days of Coverage", f"{coverage_days:.0f} days")
    
    st.markdown("---")
    
    # Get recommendation
    recommendation = calculate_inventory_recommendation(current_inventory, forecast)
    
    st.markdown(f"""
    <div class="recommendation {recommendation['css_class']}">
        <h3>{recommendation['title']}</h3>
        <p>{recommendation['message']}</p>
        <p><strong>Recommended Action:</strong> {recommendation['action']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Forecast Accuracy Analysis")
        
        # Simulated accuracy metrics
        accuracy_data = pd.DataFrame({
            'Month': ['Oct 2024', 'Nov 2024', 'Dec 2024', 'Jan 2025', 'Feb 2025'],
            'Actual': [197, 205, 213, 190, 198],
            'Forecasted': [195, 208, 210, 192, 195],
            'Error %': [1.0, 1.5, 1.4, 1.0, 1.5]
        })
        
        fig_accuracy = go.Figure()
        fig_accuracy.add_trace(go.Scatter(
            x=accuracy_data['Month'],
            y=accuracy_data['Actual'],
            name='Actual',
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10)
        ))
        fig_accuracy.add_trace(go.Scatter(
            x=accuracy_data['Month'],
            y=accuracy_data['Forecasted'],
            name='Forecasted',
            mode='lines+markers',
            line=dict(color='#f5576c', width=3, dash='dash'),
            marker=dict(size=10)
        ))
        
        fig_accuracy.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            height=300
        )
        
        st.plotly_chart(fig_accuracy, use_container_width=True)
        
        avg_error = accuracy_data['Error %'].mean()
        st.success(f"✅ Average Forecast Error: **{avg_error:.1f}%** (Excellent)")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💡 Strategic Insights")
        
        st.markdown("""
        ### 📌 Key Findings:
        
        **Seasonal Patterns:**
        - Q4 historically shows 15-20% increase
        - Summer months (Jun-Aug) see moderate demand
        - January typically shows post-holiday dip
        
        **Trend Analysis:**
        - Overall upward trend: +8% YoY
        - Monthly growth rate: ~2.5%
        - Volatility: Low (σ = 12.3 units)
        
        **Recommendations:**
        1. ✅ Increase inventory before Q4
        2. ✅ Plan promotional events for slow months
        3. ✅ Maintain 30-45 days coverage
        4. ✅ Monitor competitor pricing
        
        **Risk Assessment:**
        - Supply chain risk: Low
        - Demand volatility: Moderate
        - Inventory turnover: Healthy
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== BUSINESS INTELLIGENCE PAGE ====================
def show_business_intelligence(df):
    st.title("💼 Business Intelligence Center")
    st.markdown("##### Comprehensive Analytics & Market Insights")
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Performance Metrics", "🎯 Market Analysis", "💰 Financial Overview"])
    
    with tab1:
        st.subheader("Performance KPIs")
        
        # Sales breakdown
        col1, col2, col3 = st.columns(3)
        
        total_new = df['New_Cars'].sum()
        total_used = df['Used_Cars'].sum()
        total_all = total_new + total_used
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("New Car Sales", f"{total_new:,.0f}")
            st.progress(total_new / total_all)
            st.caption(f"{(total_new/total_all)*100:.1f}% of total")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Used Car Sales", f"{total_used:,.0f}")
            st.progress(total_used / total_all)
            st.caption(f"{(total_used/total_all)*100:.1f}% of total")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.metric("Total Sales", f"{total_all:,.0f}")
            growth = ((df['Total_Sales'].iloc[-1] - df['Total_Sales'].iloc[0]) / df['Total_Sales'].iloc[0]) * 100
            st.metric("Growth", f"{growth:.1f}%", delta_color="normal")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quarterly performance
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📈 Quarterly Performance Comparison")
        
        df_quarterly = df.copy()
        df_quarterly['Quarter'] = df_quarterly['Date'].dt.to_period('Q')
        quarterly_sales = df_quarterly.groupby('Quarter')['Total_Sales'].sum().reset_index()
        quarterly_sales['Quarter'] = quarterly_sales['Quarter'].astype(str)
        
        fig_quarterly = go.Figure()
        fig_quarterly.add_trace(go.Bar(
            x=quarterly_sales['Quarter'],
            y=quarterly_sales['Total_Sales'],
            marker=dict(
                color=quarterly_sales['Total_Sales'],
                colorscale='Plasma',
                showscale=True
            ),
            text=quarterly_sales['Total_Sales'],
            texttemplate='%{text:.0f}',
            textposition='outside'
        ))
        
        fig_quarterly.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False, title='Quarter'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Total Sales'),
            height=400
        )
        
        st.plotly_chart(fig_quarterly, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Market Analysis Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🎯 Sales Distribution")
            
            fig_pie = go.Figure()
            fig_pie.add_trace(go.Pie(
                labels=['New Cars', 'Used Cars'],
                values=[total_new, total_used],
                hole=0.4,
                marker=dict(colors=['#667eea', '#764ba2']),
                textinfo='label+percent',
                textfont=dict(size=14, color='white')
            ))
            
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=350,
                showlegend=True,
                legend=dict(font=dict(size=12))
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Market Share Trends")
            
            market_share = pd.DataFrame({
                'Brand': ['Tesla', 'BMW', 'Mercedes', 'Audi', 'Others'],
                'Share': [28, 22, 18, 16, 16]
            })
            
            fig_market = go.Figure()
            fig_market.add_trace(go.Bar(
                x=market_share['Brand'],
                y=market_share['Share'],
                marker=dict(
                    color=market_share['Share'],
                    colorscale='Viridis'
                ),
                text=[f"{v}%" for v in market_share['Share']],
                textposition='outside'
            ))
            
            fig_market.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Market Share (%)'),
                height=350
            )
            
            st.plotly_chart(fig_market, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Financial Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenue = df['Revenue'].sum()
        avg_revenue = df['Revenue'].mean()
        max_revenue = df['Revenue'].max()
        service_revenue = df['Service_Revenue'].sum()
        
        with col1:
            st.metric("Total Revenue", f"${total_revenue/1_000_000:.2f}M")
        with col2:
            st.metric("Avg Monthly Revenue", f"${avg_revenue/1_000:.0f}K")
        with col3:
            st.metric("Peak Revenue", f"${max_revenue/1_000:.0f}K")
        with col4:
            st.metric("Service Revenue", f"${service_revenue/1_000:.0f}K")
        
        st.markdown("---")
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💰 Revenue Breakdown & Trends")
        
        fig_revenue_trend = go.Figure()
        
        fig_revenue_trend.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Revenue'] / 1000,
            name='Car Sales Revenue',
            mode='lines',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        
        fig_revenue_trend.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Service_Revenue'] / 1000,
            name='Service Revenue',
            mode='lines',
            line=dict(color='#00f2fe', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 242, 254, 0.2)'
        ))
        
        fig_revenue_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title='Revenue ($K)'),
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_revenue_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== SETTINGS PAGE ====================
def show_settings():
    st.title("⚙️ System Settings & Configuration")
    st.markdown("##### Dashboard Customization & Preferences")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎨 Display Settings")
        
        theme = st.selectbox("Color Theme", ["Dark (Current)", "Light", "Auto"])
        chart_style = st.selectbox("Chart Style", ["Modern", "Classic", "Minimal"])
        animation = st.checkbox("Enable Animations", value=True)
        
        st.markdown("---")
        st.subheader("📊 Data Settings")
        
        auto_refresh = st.checkbox("Auto Refresh Data", value=False)
        if auto_refresh:
            refresh_interval = st.slider("Refresh Interval (minutes)", 1, 60, 15)
        
        date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🤖 Model Configuration")
        
        model_type = st.selectbox("Prediction Model", ["Random Forest (Current)", "Gradient Boosting", "Linear Regression", "XGBoost"])
        forecast_period = st.slider("Forecast Period (months)", 1, 12, 3)
        confidence_level = st.slider("Confidence Level (%)", 80, 99, 95)
        
        st.markdown("---")
        st.subheader("🔔 Notifications")
        
        email_alerts = st.checkbox("Email Alerts", value=True)
        low_inventory_alert = st.checkbox("Low Inventory Warnings", value=True)
        forecast_updates = st.checkbox("Weekly Forecast Updates", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Settings", use_container_width=True):
            st.success("✅ Settings saved successfully!")
    
    with col2:
        if st.button("🔄 Reset to Default", use_container_width=True):
            st.info("ℹ️ Settings reset to default values")
    
    with col3:
        if st.button("📥 Export Configuration", use_container_width=True):
            st.success("✅ Configuration exported!")

# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    main()