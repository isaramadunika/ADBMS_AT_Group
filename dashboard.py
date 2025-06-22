import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pyodbc
from datetime import datetime, timedelta
import numpy as np

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Vehicle Management System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database connection configuration
def connect_to_sql_server():
    try:
        connection_string = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=your_server_name;"
            "Database=your_database_name;"
            "UID=your_username;"
            "PWD=your_password;"
        )
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def load_data_from_sql():
    conn = connect_to_sql_server()
    if conn:
        query = "SELECT * FROM vehicle_sales"  # Replace with your table name
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    return None

# Sample data creation (replace with SQL data loading)
@st.cache_data
def load_sample_data():
    # Vehicle models
    bike_models = ['Dio', 'Pulsar', 'Fz', 'Ct100', 'Platina']
    three_wheel_models = ['Auto Rickshaw', 'Three Wheeler']
    
    # Sri Lankan names database
    sri_lankan_first_names = [
        'Kamal', 'Nimal', 'Sunil', 'Rohan', 'Ajith', 'Chaminda', 'Pradeep', 'Nuwan', 'Dinesh', 'Mahesh',
        'Saman', 'Ruwan', 'Gayan', 'Chathura', 'Thilina', 'Kasun', 'Lahiru', 'Dilan', 'Buddhika', 'Sampath',
        'Kumara', 'Thushara', 'Indika', 'Chandana', 'Tharaka', 'Sandun', 'Prasad', 'Udaya', 'Janaka', 'Dilshan',
        'Sachith', 'Ranjan', 'Lakmal', 'Nalin', 'Dileepa', 'Charith', 'Ashan', 'Ranil', 'Asanka', 'Chamara',
        'Raveena', 'Sewwandi', 'Nimali', 'Rashika', 'Sandani', 'Thanuja', 'Kavisha', 'Dilrukshi', 'Chathurika', 'Dinusha',
        'Gayani', 'Malani', 'Anusha', 'Shamali', 'Nadeeka', 'Priyanka', 'Charuni', 'Manisha', 'Randika', 'Tharushi',
        'Hiruni', 'Sachini', 'Buddhini', 'Nayana', 'Ishara', 'Amila', 'Suranga', 'Darshana', 'Isuru', 'Shanka'
    ]
    
    sri_lankan_last_names = [
        'Silva', 'Perera', 'Fernando', 'Jayawardena', 'Gunasekara', 'Wijesinghe', 'Rajapaksa', 'Wickramasinghe',
        'Mendis', 'Bandara', 'Rathnayaka', 'Dissanayaka', 'Gunawardena', 'Senaratne', 'Wijerathne', 'Peiris',
        'Kumara', 'Weerasinghe', 'Jayasuriya', 'Ranasinghe', 'Gamage', 'Amarasinghe', 'Liyanage', 'Abeywardena',
        'Abeysinghe', 'Wickremaratne', 'Ratnayake', 'Kumarasinghe', 'Priyantha', 'Samaraweera', 'Herath', 'Karunaratne',
        'Jayaratne', 'Weerasekara', 'Kodikara', 'Senanayake', 'Wickramage', 'Dharmasena', 'Pathirana', 'Madusanka'
    ]
    
    # Sri Lankan cities and areas
    sri_lankan_addresses = [
        'Colombo 01', 'Colombo 02', 'Colombo 03', 'Colombo 04', 'Colombo 05', 'Colombo 06', 'Colombo 07',
        'Dehiwala', 'Mount Lavinia', 'Moratuwa', 'Panadura', 'Kalutara', 'Beruwala', 'Bentota', 'Galle',
        'Matara', 'Tangalle', 'Hambantota', 'Ratnapura', 'Embilipitiya', 'Balangoda', 'Kandy', 'Peradeniya',
        'Gampola', 'Nawalapitiya', 'Hatton', 'Nuwara Eliya', 'Bandarawela', 'Badulla', 'Monaragala', 'Wellawaya',
        'Kurunegala', 'Puttalam', 'Chilaw', 'Negombo', 'Wattala', 'Ja-Ela', 'Gampaha', 'Kadawatha', 'Ragama',
        'Kelaniya', 'Maharagama', 'Kottawa', 'Piliyandala', 'Homagama', 'Avissawella', 'Malabe', 'Battaramulla',
        'Anuradhapura', 'Polonnaruwa', 'Dambulla', 'Sigiriya', 'Matale', 'Akurana', 'Trincomalee', 'Batticaloa',
        'Ampara', 'Kalmunai', 'Jaffna', 'Vavuniya', 'Mannar', 'Kilinochchi', 'Mullativu'
    ]
    
    # Sri Lankan vehicle number prefixes (actual format)
    vehicle_prefixes = ['WP', 'CP', 'SP', 'EP', 'NP', 'NC', 'UP', 'SG', 'NW']
    
    # Generate sample data with proper 12-month distribution
    data = []
    current_year = datetime.now().year
    
    for i in range(1, 201):  # Increased sample size for better distribution
        vehicle_type = np.random.choice(['Bike', 'Three Wheeler'], p=[0.7, 0.3])
        if vehicle_type == 'Bike':
            model = np.random.choice(bike_models)
            price_range = (400000, 600000)
        else:
            model = np.random.choice(three_wheel_models)
            price_range = (800000, 1000000)
        
        # Generate dates across all 12 months of current year
        random_month = np.random.randint(1, 13)
        random_day = np.random.randint(1, 29)  # Safe day range for all months
        purchase_date = datetime(current_year, random_month, random_day)
        
        # Generate Sri Lankan customer details
        first_name = np.random.choice(sri_lankan_first_names)
        last_name = np.random.choice(sri_lankan_last_names)
        customer_name = f"{first_name} {last_name}"
        
        # Generate Sri Lankan style address
        house_no = np.random.randint(1, 999)
        street_names = ['Galle Road', 'Kandy Road', 'Negombo Road', 'Main Street', 'Temple Road', 
                       'School Lane', 'Church Street', 'Station Road', 'Lake Road', 'Hill Street']
        street = np.random.choice(street_names)
        city = np.random.choice(sri_lankan_addresses)
        address = f"{house_no}/{np.random.randint(1, 20)}, {street}, {city}"
        
        # Generate Sri Lankan NIC number (format: YYMMDDXXXV or new format)
        birth_year = np.random.randint(70, 99)  # 1970-1999
        if np.random.random() > 0.5:  # Old format
            nic = f"{birth_year:02d}{np.random.randint(100, 365):03d}{np.random.randint(1000, 9999):04d}V"
        else:  # New format
            nic = f"{1900 + birth_year}{np.random.randint(100, 365):03d}{np.random.randint(10000, 99999):05d}"
        
        # Generate phone number (Sri Lankan format)
        phone = f"0{np.random.choice([70, 71, 72, 75, 76, 77, 78])}{np.random.randint(1000000, 9999999)}"
        
        # Generate vehicle number (Sri Lankan format)
        prefix = np.random.choice(vehicle_prefixes)
        if vehicle_type == 'Bike':
            vehicle_number = f"{prefix} {np.random.choice(['CAA', 'CAB', 'CAC', 'CAD', 'CAE'])} {np.random.randint(1000, 9999)}"
        else:
            vehicle_number = f"{prefix} {np.random.choice(['PA', 'PB', 'PC', 'PD', 'PE'])} {np.random.randint(1000, 9999)}"
        
        data.append({
            'VehicleNumber': vehicle_number,
            'CustomerId': i,
            'CustomerName': customer_name,
            'Address': address,
            'NIC': nic,
            'Phone': phone,
            'VehicleType': vehicle_type,
            'Model': model,
            'PurchaseDate': purchase_date,
            'Payment': np.random.randint(*price_range),
            'PaymentMethod': np.random.choice(['Cash', 'Credit Card', 'Bank Transfer', 'Cheque']),
            'EmployeeId': np.random.randint(1, 100),
            'Status': np.random.choice(['Sold', 'Available', 'Under Repair']),
            'RepairCost': np.random.randint(5000, 50000) if np.random.random() > 0.7 else 0,
            'RepairStatus': np.random.choice(['Completed', 'In Progress', 'Pending']) if np.random.random() > 0.7 else 'None'
        })
    
    return pd.DataFrame(data)

# Enhanced CSS with top navigation
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 0 0 15px 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    /* Top navigation */
    .top-nav {
        background: black;
        padding: 0.4rem 0.4rem;
        border-radius: 10px;
        margin-bottom: 0.4rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Navigation buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.2rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    
    /* Chart containers */
    .chart-container {
        background: black;
        padding: 0.4rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* Hide sidebar completely */
    .css-1d391kg {
        display: none;
    }
    
    /* Page content styling */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
df = load_sample_data()

# Header
st.markdown("""
<div class="main-header">
    <h1>CM Vehicle Management System</h1>
</div>
""", unsafe_allow_html=True)

# Top Navigation
st.markdown('<div class="top-nav">', unsafe_allow_html=True)
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)

with nav_col1:
    dashboard_btn = st.button("🏠 Dashboard", use_container_width=True)
with nav_col2:
    vehicle_btn = st.button("🚗 Vehicle Management", use_container_width=True)
with nav_col3:
    customer_btn = st.button("👥 Customer Management", use_container_width=True)
with nav_col4:
    repair_btn = st.button("🔧 Repair Management", use_container_width=True)
with nav_col5:
    supplier_btn = st.button("🏪 Supplier Management", use_container_width=True)
with nav_col6:
    reports_btn = st.button("💰 Sales Reports", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Page state management
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

if dashboard_btn:
    st.session_state.current_page = 'dashboard'
elif vehicle_btn:
    st.session_state.current_page = 'vehicle_management'
elif customer_btn:
    st.session_state.current_page = 'customer_management'
elif repair_btn:
    st.session_state.current_page = 'repair_management'
elif supplier_btn:
    st.session_state.current_page = 'supplier_management'
elif reports_btn:
    st.session_state.current_page = 'sales_reports'

# Dashboard Page
if st.session_state.current_page == 'dashboard':
    st.markdown('<h1 style="text-align: center; color: #1f77b4; margin-bottom: 2rem;">Admin Dashboard</h1>', unsafe_allow_html=True)
    
    # June-only focus
    st.markdown(f'<h2 style="text-align: center; color: #2c3e50; margin-bottom: 1rem;">📅 June 2025 Performance Dashboard</h2>', unsafe_allow_html=True)
    
    # Filter data for June only (month 6)
    june_data = df[df['PurchaseDate'].dt.month == 6]
    
    # Key Metrics Row - June Only
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        june_sales = len(june_data[june_data['Status'] == 'Sold'])
        st.metric("June Sales", june_sales, delta=f"+{np.random.randint(3, 8)} from May")
    
    with col2:
        june_revenue = june_data[june_data['Status'] == 'Sold']['Payment'].sum()
        st.metric("June Revenue", f"Rs.{june_revenue/1000000:.1f}M", delta="+15% from May")
    
    with col3:
        if june_sales > 0:
            june_avg_sale = june_revenue / june_sales
        else:
            june_avg_sale = 0
        st.metric("June Avg Sale", f"Rs.{june_avg_sale/1000:.0f}k", delta="+8%")
    
    with col4:
        june_repairs = len(june_data[june_data['Status'] == 'Under Repair'])
        st.metric("June Repairs", june_repairs, delta="-2 from May")
    
    # June-only Time Series Charts
    st.markdown('<h3 style="color: #34495e; margin: 2rem 0 1rem 0;">📈 June 2025 Daily Analysis</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 June Daily Sales Performance")
        
        # Daily sales for June only
        june_daily = june_data[june_data['Status'] == 'Sold'].groupby(
            june_data['PurchaseDate'].dt.day
        )['Payment'].sum().reset_index()
        june_daily.columns = ['Day', 'Sales']
        
        # Create complete June day range (1-30)
        june_days = pd.DataFrame({'Day': range(1, 31)})
        complete_june_daily = june_days.merge(june_daily, on='Day', how='left')
        complete_june_daily['Sales'] = complete_june_daily['Sales'].fillna(0)
        
        fig = px.line(complete_june_daily, x='Day', y='Sales', 
                     title="June 2025 - Daily Sales Trend",
                     color_discrete_sequence=['#e74c3c'])
        fig.update_traces(mode='lines+markers', marker=dict(size=8))
        fig.update_layout(
            showlegend=False, 
            height=400,
            xaxis_title="June Days",
            yaxis_title="Daily Sales (Rs.)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🚗 June Vehicle Sales Count")
        
        # Daily vehicle count for June
        june_count_daily = june_data[june_data['Status'] == 'Sold'].groupby(
            june_data['PurchaseDate'].dt.day
        ).size().reset_index()
        june_count_daily.columns = ['Day', 'Count']
        
        # Merge with complete June days
        complete_june_count = june_days.merge(june_count_daily, on='Day', how='left')
        complete_june_count['Count'] = complete_june_count['Count'].fillna(0)
        
        fig = px.bar(complete_june_count, x='Day', y='Count', 
                    title="June 2025 - Daily Vehicle Sales",
                    color_discrete_sequence=['#3498db'])
        fig.update_layout(
            showlegend=False, 
            height=400,
            xaxis_title="June Days",
            yaxis_title="Vehicles Sold"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # June Weekly Analysis
    st.markdown('<h3 style="color: #34495e; margin: 2rem 0 1rem 0;">📅 June Weekly Breakdown</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("June Sales by Week")
        
        # Create June weeks (Week 1: 1-7, Week 2: 8-14, Week 3: 15-21, Week 4: 22-30)
        june_weeks = june_data[june_data['Status'] == 'Sold'].copy()
        june_weeks['Week'] = pd.cut(june_weeks['PurchaseDate'].dt.day, 
                                   bins=[0, 7, 14, 21, 31], 
                                   labels=['Week 1', 'Week 2', 'Week 3', 'Week 4'])
        
        weekly_sales = june_weeks.groupby('Week')['Payment'].sum().reset_index()
        
        fig = go.Figure()
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        for i, (week, sales) in enumerate(weekly_sales.values):
            fig.add_trace(go.Bar(
                x=[week],
                y=[sales],
                name=week,
                marker_color=colors[i % 4],
                text=[f"Rs.{sales/1000000:.1f}M"],
                textposition='auto'
            ))
        
        fig.update_layout(
            showlegend=False,
            height=400,
            title="June Weekly Revenue",
            xaxis_title="June Weeks",
            yaxis_title="Revenue (Rs.)"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("June Vehicle Types")
        june_vehicle_sales = june_data[june_data['Status'] == 'Sold']['VehicleType'].value_counts()
        
        if len(june_vehicle_sales) > 0:
            fig = px.pie(values=june_vehicle_sales.values, names=june_vehicle_sales.index,
                        title="June Sales by Vehicle Type",
                        color_discrete_sequence=['#ff9999', '#66b3ff'])
            fig.update_traces(textposition='inside', textinfo='value+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No June sales data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("June Summary Stats")
        
        june_sold = june_data[june_data['Status'] == 'Sold']
        
        if len(june_sold) > 0:
            total_june_revenue = june_sold['Payment'].sum()
            total_june_vehicles = len(june_sold)
            avg_june_sale = total_june_revenue / total_june_vehicles if total_june_vehicles > 0 else 0
            top_june_model = june_sold['Model'].mode().iloc[0] if len(june_sold) > 0 else "N/A"
            
            st.metric("Total June Revenue", f"Rs.{total_june_revenue/1000000:.2f}M")
            st.metric("Total Vehicles Sold", total_june_vehicles)
            st.metric("Average Sale Value", f"Rs.{avg_june_sale/1000:.0f}k")
            st.write(f"**Top Model in June:** {top_june_model}")
            st.write(f"**June Performance:** {'🟢 Excellent' if total_june_vehicles > 15 else '🟡 Good' if total_june_vehicles > 10 else '🔴 Needs Improvement'}")
        else:
            st.info("No June sales data to display")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Row 2
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Sales Breakdown by Vehicle Type")
        vehicle_sales = df[df['Status'] == 'Sold']['VehicleType'].value_counts()
        
        fig = go.Figure()
        for i, (vehicle_type, count) in enumerate(vehicle_sales.items()):
            fig.add_trace(go.Bar(
                x=[vehicle_type],
                y=[count],
                name=vehicle_type,
                marker_color=['#1f77b4', '#ff7f0e'][i % 2],
                text=[count],
                textposition='auto'
            ))
        
        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Vehicle Type",
            yaxis_title="Sales Count"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Repair Cost Analytics")
        repair_data = df[df['RepairCost'] > 0]
        total_repair_cost = repair_data['RepairCost'].sum()
        avg_repair_time = "23m"  # Sample data
        
        st.write(f"**Total Repair Cost:** Rs.{total_repair_cost/1000:.1f}k")
        st.write(f"**Avg. Repair Time:** {avg_repair_time}")
        st.write(f"**Days:** 1")
        st.write(f"**No. of Vehicles Under Repair:** {vehicles_under_repair}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("Inventory Status")
        status_counts = df['Status'].value_counts()
        
        # Create custom labels with count values
        labels = []
        values = []
        for status, count in status_counts.items():
            labels.append(f"{status}")
            values.append(count)
        
        fig = px.pie(
            values=values, 
            names=labels,
            color_discrete_sequence=['#ff9999', '#66b3ff', '#99ff99'],
            title="Inventory Distribution"
        )
        
        # Update traces to show count values instead of percentages
        fig.update_traces(
            textposition='inside', 
            textinfo='value+label',
            textfont_size=12,
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        
        fig.update_layout(
            height=400, 
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.01
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Vehicle Management Page
elif st.session_state.current_page == 'vehicle_management':
    st.title("Vehicle Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["All Vehicles", "Add Vehicle", "Update Vehicle", "Vehicle Actions"])
    
    with tab1:
        st.subheader("All Vehicles")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            vehicle_type_filter = st.selectbox("Filter by Type", ["All"] + list(df['VehicleType'].unique()))
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All"] + list(df['Status'].unique()))
        with col3:
            model_filter = st.selectbox("Filter by Model", ["All"] + list(df['Model'].unique()))
        
        # Apply filters
        filtered_df = df.copy()
        if vehicle_type_filter != "All":
            filtered_df = filtered_df[filtered_df['VehicleType'] == vehicle_type_filter]
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['Status'] == status_filter]
        if model_filter != "All":
            filtered_df = filtered_df[filtered_df['Model'] == model_filter]
        
        st.dataframe(filtered_df, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Vehicle")
        
        col1, col2 = st.columns(2)
        with col1:
            vehicle_number = st.text_input("Vehicle Number", placeholder="e.g., ABC 1234")
            vehicle_type = st.selectbox("Vehicle Type", ["Bike", "Three Wheeler"])
            
            if vehicle_type == "Bike":
                model = st.selectbox("Model", ['Dio', 'Pulsar', 'Fz', 'Ct100', 'Platina'])
            else:
                model = st.selectbox("Model", ['Auto Rickshaw', 'Three Wheeler'])
            
            purchase_price = st.number_input("Purchase Price (Rs.)", min_value=0, step=1000)
        
        with col2:
            customer_id = st.number_input("Customer ID", min_value=1, step=1)
            employee_id = st.number_input("Employee ID", min_value=1, step=1)
            payment_method = st.selectbox("Payment Method", ['Cash', 'Credit Card', 'Bank Transfer', 'Cheque'])
            status = st.selectbox("Status", ['Available', 'Sold', 'Under Repair'])
        
        if st.button("Add Vehicle", type="primary"):
            # Here you would insert into database
            st.success("Vehicle added successfully!")
    
    with tab3:
        st.subheader("Update Vehicle")
        
        vehicle_to_update = st.selectbox("Select Vehicle to Update", df['VehicleNumber'].tolist())
        
        if vehicle_to_update:
            selected_vehicle = df[df['VehicleNumber'] == vehicle_to_update].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                new_status = st.selectbox("Status", ['Available', 'Sold', 'Under Repair'], 
                                        index=['Available', 'Sold', 'Under Repair'].index(selected_vehicle['Status']))
                new_price = st.number_input("Price", value=int(selected_vehicle['Payment']))
            
            with col2:
                new_customer = st.number_input("Customer ID", value=int(selected_vehicle['CustomerId']))
                new_employee = st.number_input("Employee ID", value=int(selected_vehicle['EmployeeId']))
            
            if st.button("Update Vehicle", type="primary"):
                st.success("Vehicle updated successfully!")
    
    with tab4:
        st.subheader("Vehicle Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Repair Vehicle")
            repair_vehicle = st.selectbox("Select Vehicle for Repair", df['VehicleNumber'].tolist())
            repair_details = st.text_area("Repair Details")
            repair_cost = st.number_input("Repair Cost (Rs.)", min_value=0, step=100)
            
            if st.button("Submit for Repair"):
                st.success("Vehicle submitted for repair!")
        
        with col2:
            st.subheader("Sell Vehicle")
            available_vehicles = df[df['Status'] == 'Available']['VehicleNumber'].tolist()
            if available_vehicles:
                sell_vehicle = st.selectbox("Select Vehicle to Sell", available_vehicles)
                if st.button("Mark as Sold"):
                    st.success("Vehicle marked as sold!")
            else:
                st.info("No vehicles available for sale")

# Customer Management Page
elif st.session_state.current_page == 'customer_management':
    st.title("Customer Management")
    
    tab1, tab2, tab3 = st.tabs(["All Customers", "Add Customer", "Update Customer"])
    
    with tab1:
        # Display customer data with Sri Lankan details
        customers = df[['CustomerId', 'CustomerName', 'Address', 'NIC', 'Phone']].drop_duplicates()
        st.dataframe(customers, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Customer")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            address = st.text_area("Address")
            nic_number = st.text_input("NIC Number")
        
        with col2:
            last_name = st.text_input("Last Name")
            phone_number = st.text_input("Phone Number")
        
        if st.button("Add Customer", type="primary"):
            st.success("Customer added successfully!")
    
    with tab3:
        st.subheader("Update Customer")
        customers = df[['CustomerId', 'CustomerName', 'Address', 'NIC', 'Phone']].drop_duplicates()
        customer_to_update = st.selectbox("Select Customer", customers['CustomerName'].tolist())
        
        if customer_to_update:
            selected_customer = customers[customers['CustomerName'] == customer_to_update].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                current_name_parts = selected_customer['CustomerName'].split(' ')
                first_name = current_name_parts[0] if len(current_name_parts) > 0 else ""
                st.text_input("First Name", value=first_name, key="update_fname")
                st.text_area("Address", value=selected_customer['Address'], key="update_address")
                st.text_input("NIC Number", value=selected_customer['NIC'], key="update_nic")
            
            with col2:
                last_name = " ".join(current_name_parts[1:]) if len(current_name_parts) > 1 else ""
                st.text_input("Last Name", value=last_name, key="update_lname")
                st.text_input("Phone Number", value=selected_customer['Phone'], key="update_phone")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Customer", type="secondary"):
                    st.warning("Customer deleted!")
            with col2:
                if st.button("Save Changes", type="primary"):
                    st.success("Customer updated successfully!")

# Repair Management Page
elif st.session_state.current_page == 'repair_management':
    st.title("Repair Management")
    
    tab1, tab2, tab3 = st.tabs(["Active Repairs", "Add Repair", "Repair History"])
    
    with tab1:
        st.subheader("Active Repairs")
        repair_data = df[df['Status'] == 'Under Repair']
        st.dataframe(repair_data[['VehicleNumber', 'Model', 'RepairCost', 'RepairStatus']], use_container_width=True)
    
    with tab2:
        st.subheader("Add New Repair")
        
        col1, col2 = st.columns(2)
        with col1:
            repair_vehicle = st.selectbox("Vehicle Number", df['VehicleNumber'].tolist())
            repair_start_date = st.date_input("Repair Start Date")
            repair_details = st.text_area("Repair Details")
            repair_location = st.text_input("Location")
        
        with col2:
            repair_end_date = st.date_input("Repair End Date")
            repair_amount = st.number_input("Repair Amount (Rs.)", min_value=0, step=100)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear"):
                st.rerun()
        with col2:
            if st.button("Save", type="primary"):
                st.success("Repair record saved!")
    
    with tab3:
        st.subheader("Repair History")
        # Sample repair history
        repair_history = df[df['RepairCost'] > 0][['VehicleNumber', 'Model', 'RepairCost', 'RepairStatus']]
        st.dataframe(repair_history, use_container_width=True)

# Supplier Management Page
elif st.session_state.current_page == 'supplier_management':
    st.title("Supplier Management")
    
    tab1, tab2, tab3 = st.tabs(["All Suppliers", "Add Supplier", "Update Supplier"])
    
    with tab1:
        # Generate realistic Sri Lankan supplier data
        sri_lankan_supplier_companies = [
            'Abans PLC', 'Singer (Sri Lanka) PLC', 'Softlogic Holdings PLC', 'Hemas Holdings PLC',
            'John Keells Holdings PLC', 'Cargills (Ceylon) PLC', 'Commercial Bank of Ceylon PLC',
            'Dialog Axiata PLC', 'Ceylon Tobacco Company PLC', 'Lanka IOC PLC',
            'Dimo Motors', 'United Motors Lanka (UML)', 'AMW Group', 'David Pieris Motor Company',
            'Ideal Motors', 'Micro Cars (Pvt) Ltd', 'Stafford Motor Company', 'Prestige Automobile',
            'Asia Motor Works', 'Central Finance Company PLC'
        ]
        
        supplier_types = ['Vehicle Importer', 'Parts Supplier', 'Service Provider', 'Finance Partner', 'Insurance Provider']
        
        suppliers = pd.DataFrame({
            'SupplierID': [f"SUP{str(i).zfill(3)}" for i in range(1, 21)],
            'CompanyName': np.random.choice(sri_lankan_supplier_companies, 20, replace=False),
            'ContactPerson': [f"{np.random.choice(['Kamal', 'Nimal', 'Sunil', 'Rohan', 'Ajith', 'Chaminda', 'Pradeep', 'Nuwan', 'Dinesh', 'Mahesh', 'Saman', 'Ruwan', 'Gayan', 'Chathura', 'Thilina'])} {np.random.choice(['Silva', 'Perera', 'Fernando', 'Jayawardena', 'Gunasekara', 'Wijesinghe', 'Rajapaksa', 'Wickramasinghe', 'Mendis', 'Bandara'])}" for _ in range(20)],
            'SupplierType': np.random.choice(supplier_types, 20),
            'Address': [f"{np.random.randint(100, 999)}, {np.random.choice(['Galle Road', 'Kandy Road', 'Negombo Road', 'Baseline Road', 'Duplication Road'])}, {np.random.choice(['Colombo 03', 'Colombo 04', 'Dehiwala', 'Mount Lavinia', 'Moratuwa', 'Kandy', 'Galle', 'Negombo'])}" for _ in range(20)],
            'Phone': [f"011{np.random.randint(2000000, 2999999)}" for _ in range(20)],
            'Email': [f"{company.lower().replace(' ', '').replace('(', '').replace(')', '').replace('pvt', '').replace('plc', '').replace('ltd', '')}@gmail.com" for company in np.random.choice(sri_lankan_supplier_companies, 20, replace=False)],
            'Rating': np.random.choice([3.5, 4.0, 4.2, 4.5, 4.7, 4.8, 4.9, 5.0], 20),
            'LastDelivery': pd.date_range(start='2024-01-01', end='2025-06-01', periods=20).strftime('%Y-%m-%d'),
            'TotalOrders': np.random.randint(5, 150, 20),
            'Status': np.random.choice(['Active', 'Pending', 'Suspended'], 20, p=[0.8, 0.15, 0.05])
        })
        
        st.dataframe(suppliers, use_container_width=True)
    
    with tab2:
        st.subheader("Add New Supplier")
        
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            contact_person = st.text_input("Contact Person")
            supplier_type = st.selectbox("Supplier Type", ['Vehicle Importer', 'Parts Supplier', 'Service Provider', 'Finance Partner', 'Insurance Provider'])
            supplier_address = st.text_area("Address")
        
        with col2:
            phone_number = st.text_input("Phone Number")
            email_address = st.text_input("Email Address")
            rating = st.selectbox("Rating", [5.0, 4.9, 4.8, 4.7, 4.5, 4.2, 4.0, 3.5])
            status = st.selectbox("Status", ['Active', 'Pending', 'Suspended'])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear"):
                st.rerun()
        with col2:
            if st.button("Submit", type="primary"):
                st.success("Supplier added successfully!")
    
    with tab3:
        st.subheader("Update Supplier")
        
        # Use realistic supplier data for update
        sri_lankan_supplier_companies = [
            'Abans PLC', 'Singer (Sri Lanka) PLC', 'Softlogic Holdings PLC', 'Hemas Holdings PLC',
            'John Keells Holdings PLC', 'Cargills (Ceylon) PLC', 'Commercial Bank of Ceylon PLC',
            'Dialog Axiata PLC', 'Ceylon Tobacco Company PLC', 'Lanka IOC PLC'
        ]
        
        supplier_to_update = st.selectbox("Select Supplier", sri_lankan_supplier_companies)
        
        if supplier_to_update:
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Company Name", value=supplier_to_update, key="update_sup_company")
                st.text_input("Contact Person", value="Kamal Silva", key="update_sup_contact")
                st.selectbox("Supplier Type", ['Vehicle Importer', 'Parts Supplier', 'Service Provider'], key="update_sup_type")
                st.text_area("Address", value="123, Galle Road, Colombo 03", key="update_sup_address")
            
            with col2:
                st.text_input("Phone Number", value="0112345678", key="update_sup_phone")
                st.text_input("Email", value="info@company.lk", key="update_sup_email")
                st.selectbox("Rating", [5.0, 4.9, 4.8, 4.7, 4.5], key="update_sup_rating")
                st.selectbox("Status", ['Active', 'Pending', 'Suspended'], key="update_sup_status")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Delete Supplier", type="secondary"):
                    st.warning("Supplier deleted!")
            with col2:
                if st.button("Save Changes", type="primary"):
                    st.success("Supplier updated successfully!")

# Sales Reports Page
elif st.session_state.current_page == 'sales_reports':
    st.title("Sales Reports & Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=365))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Filter data by date range
    filtered_sales = df[(df['PurchaseDate'].dt.date >= start_date) & 
                       (df['PurchaseDate'].dt.date <= end_date) & 
                       (df['Status'] == 'Sold')]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", len(filtered_sales))
    with col2:
        st.metric("Total Revenue", f"Rs.{filtered_sales['Payment'].sum()/1000000:.2f}M")
    with col3:
        st.metric("Average Sale", f"Rs.{filtered_sales['Payment'].mean():.0f}")
    with col4:
        st.metric("Top Model", filtered_sales['Model'].mode().iloc[0] if len(filtered_sales) > 0 else "N/A")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by Model
        st.subheader("Sales by Model")
        model_sales = filtered_sales['Model'].value_counts()
        fig = px.pie(values=model_sales.values, names=model_sales.index, 
                    title="Sales Distribution by Model")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales by Payment Method
        st.subheader("Sales by Payment Method")
        payment_sales = filtered_sales['PaymentMethod'].value_counts()
        fig = px.bar(x=payment_sales.index, y=payment_sales.values,
                    title="Sales by Payment Method")
        st.plotly_chart(fig, use_container_width=True)
    
    # Monthly sales trend with proper 12-month display
    st.subheader("Monthly Sales Trend")
    
    # Create complete 12-month framework
    all_months_df = pd.DataFrame({
        'Month': range(1, 13),
        'MonthName': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    })
    
    # Get actual monthly sales data
    monthly_sales = filtered_sales.groupby(filtered_sales['PurchaseDate'].dt.month).agg({
        'Payment': 'sum',
        'VehicleNumber': 'count'
    }).reset_index()
    monthly_sales.columns = ['Month', 'Revenue', 'Count']
    
    # Merge with complete 12-month data
    complete_monthly_sales = all_months_df.merge(monthly_sales, on='Month', how='left')
    complete_monthly_sales['Revenue'] = complete_monthly_sales['Revenue'].fillna(0)
    complete_monthly_sales['Count'] = complete_monthly_sales['Count'].fillna(0)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=complete_monthly_sales['MonthName'], y=complete_monthly_sales['Revenue'], 
               name="Revenue", marker_color='lightblue'),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=complete_monthly_sales['MonthName'], y=complete_monthly_sales['Count'], 
                  name="Count", mode='lines+markers', marker_color='red'),
        secondary_y=True,
    )
    fig.update_yaxes(title_text="Revenue (Rs.)", secondary_y=False)
    fig.update_yaxes(title_text="Number of Sales", secondary_y=True)
    fig.update_layout(title_text="Monthly Sales Revenue and Count - Full Year")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed sales table
    st.subheader("Detailed Sales Data")
    st.dataframe(filtered_sales, use_container_width=True)

st.markdown("""
<div style="text-align: center; color: #ecf0f1; padding: 2rem; background: linear-gradient(to bottom, #0d0f14, #000000); border-radius: 15px; margin: 2rem 0;">
    <h3> CM Vehicle Management System</h3>
    <p><strong>Vehicle Sales & Management Dashboard</strong></p>
    <p>Built with Group AT | © 2025 CM Vehicle Management. All rights reserved.</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        📧 Email: chamod@cmvehicles.com | 📞 Phone: +94 70 520 6400 
    </p>
</div>
""", unsafe_allow_html=True)
