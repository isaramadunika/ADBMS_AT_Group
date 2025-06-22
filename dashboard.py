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

# Load data and initialize session state
df = load_sample_data()

# Initialize session state for real-time updates
if 'vehicles_data' not in st.session_state:
    st.session_state.vehicles_data = df.copy()

if 'customers_data' not in st.session_state:
    customers_base = st.session_state.vehicles_data[['CustomerId', 'CustomerName', 'Address', 'NIC', 'Phone']].drop_duplicates()
    st.session_state.customers_data = customers_base.copy()

if 'suppliers_data' not in st.session_state:
    # Initialize supplier data
    sri_lankan_supplier_companies = [
        'Abans PLC', 'Singer (Sri Lanka) PLC', 'Softlogic Holdings PLC', 'Hemas Holdings PLC',
        'John Keells Holdings PLC', 'Cargills (Ceylon) PLC', 'Commercial Bank of Ceylon PLC',
        'Dialog Axiata PLC', 'Ceylon Tobacco Company PLC', 'Lanka IOC PLC',
        'Dimo Motors', 'United Motors Lanka (UML)', 'AMW Group', 'David Pieris Motor Company',
        'Ideal Motors', 'Micro Cars (Pvt) Ltd', 'Stafford Motor Company', 'Prestige Automobile',
        'Asia Motor Works', 'Central Finance Company PLC'
    ]
    
    supplier_types = ['Vehicle Importer', 'Parts Supplier', 'Service Provider', 'Finance Partner', 'Insurance Provider']
    
    initial_suppliers = pd.DataFrame({
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
    st.session_state.suppliers_data = initial_suppliers.copy()

if 'repairs_data' not in st.session_state:
    # Initialize repair data
    repair_vehicles = st.session_state.vehicles_data[st.session_state.vehicles_data['Status'] == 'Under Repair']
    if len(repair_vehicles) > 0:
        initial_repairs = pd.DataFrame({
            'RepairID': [f"REP{str(i).zfill(3)}" for i in range(1, len(repair_vehicles) + 1)],
            'VehicleNumber': repair_vehicles['VehicleNumber'].values,
            'StartDate': pd.date_range(start='2025-05-01', end='2025-06-20', periods=len(repair_vehicles)).strftime('%Y-%m-%d'),
            'EndDate': pd.date_range(start='2025-06-01', end='2025-06-30', periods=len(repair_vehicles)).strftime('%Y-%m-%d'),
            'RepairDetails': [f"Repair work for {vehicle}" for vehicle in repair_vehicles['VehicleNumber'].values],
            'Location': np.random.choice(['Main Workshop', 'Service Center A', 'Service Center B', 'Mobile Service'], len(repair_vehicles)),
            'Amount': repair_vehicles['RepairCost'].values,
            'Status': repair_vehicles['RepairStatus'].values,
            'Priority': np.random.choice(['Low', 'Medium', 'High', 'Urgent'], len(repair_vehicles))
        })
    else:
        # Create empty repairs dataframe if no vehicles under repair
        initial_repairs = pd.DataFrame(columns=['RepairID', 'VehicleNumber', 'StartDate', 'EndDate', 'RepairDetails', 'Location', 'Amount', 'Status', 'Priority'])
    st.session_state.repairs_data = initial_repairs.copy()

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
    june_data = st.session_state.vehicles_data[st.session_state.vehicles_data['PurchaseDate'].dt.month == 6]
    
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
        if len(june_weeks) > 0:
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
        else:
            st.info("No June sales data for weekly analysis")
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

# Vehicle Management Page
elif st.session_state.current_page == 'vehicle_management':
    st.title("🚗 Vehicle Management - Real-Time Updates")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Vehicles", "➕ Add Vehicle", "✏️ Update Vehicle", "🔧 Vehicle Actions"])
    
    with tab1:
        st.subheader("All Vehicles (Live Data)")
        
        # Real-time filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            vehicle_type_filter = st.selectbox("Filter by Type", ["All"] + list(st.session_state.vehicles_data['VehicleType'].unique()))
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All"] + list(st.session_state.vehicles_data['Status'].unique()))
        with col3:
            model_filter = st.selectbox("Filter by Model", ["All"] + list(st.session_state.vehicles_data['Model'].unique()))
        with col4:
            st.metric("Total Vehicles", len(st.session_state.vehicles_data))
        
        # Apply filters to real-time data
        filtered_df = st.session_state.vehicles_data.copy()
        if vehicle_type_filter != "All":
            filtered_df = filtered_df[filtered_df['VehicleType'] == vehicle_type_filter]
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['Status'] == status_filter]
        if model_filter != "All":
            filtered_df = filtered_df[filtered_df['Model'] == model_filter]
        
        # Show real-time data
        st.dataframe(filtered_df, use_container_width=True)
        
        # Real-time stats
        col1, col2, col3 = st.columns(3)
        with col1:
            sold_count = len(filtered_df[filtered_df['Status'] == 'Sold'])
            st.success(f"Sold: {sold_count}")
        with col2:
            available_count = len(filtered_df[filtered_df['Status'] == 'Available'])
            st.info(f"Available: {available_count}")
        with col3:
            repair_count = len(filtered_df[filtered_df['Status'] == 'Under Repair'])
            st.warning(f"Under Repair: {repair_count}")
    
    with tab2:
        st.subheader("➕ Add New Vehicle (Real-Time)")
        
        with st.form("add_vehicle_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                vehicle_number = st.text_input("Vehicle Number", placeholder="e.g., WP CAA 1234")
                vehicle_type = st.selectbox("Vehicle Type", ["Bike", "Three Wheeler"])
                
                if vehicle_type == "Bike":
                    model = st.selectbox("Model", ['Dio', 'Pulsar', 'Fz', 'Ct100', 'Platina'])
                    price_range = (400000, 600000)
                else:
                    model = st.selectbox("Model", ['Auto Rickshaw', 'Three Wheeler'])
                    price_range = (800000, 1000000)
                
                purchase_price = st.number_input("Purchase Price (Rs.)", min_value=0, step=1000, value=price_range[0])
                purchase_date = st.date_input("Purchase Date", value=datetime.now())
            
            with col2:
                # Auto-generate customer data
                customer_id = len(st.session_state.customers_data) + 1
                
                # Sri Lankan names for new customer
                first_names = ['Kamal', 'Nimal', 'Sunil', 'Rohan', 'Ajith', 'Chaminda', 'Pradeep', 'Nuwan']
                last_names = ['Silva', 'Perera', 'Fernando', 'Jayawardena', 'Gunasekara', 'Wijesinghe']
                
                customer_name = st.text_input("Customer Name", value=f"{np.random.choice(first_names)} {np.random.choice(last_names)}")
                employee_id = st.number_input("Employee ID", min_value=1, step=1, value=np.random.randint(1, 100))
                payment_method = st.selectbox("Payment Method", ['Cash', 'Credit Card', 'Bank Transfer', 'Cheque'])
                status = st.selectbox("Status", ['Available', 'Sold', 'Under Repair'])
            
            submitted = st.form_submit_button("🚀 Add Vehicle (Real-Time)", type="primary")
            
            if submitted and vehicle_number:
                # Generate additional customer details
                sri_lankan_addresses = ['Colombo 01', 'Colombo 03', 'Dehiwala', 'Mount Lavinia', 'Moratuwa', 'Kandy', 'Galle']
                house_no = np.random.randint(1, 999)
                street = np.random.choice(['Galle Road', 'Kandy Road', 'Main Street'])
                city = np.random.choice(sri_lankan_addresses)
                address = f"{house_no}/{np.random.randint(1, 20)}, {street}, {city}"
                
                # Generate NIC and phone
                birth_year = np.random.randint(70, 99)
                nic = f"{birth_year:02d}{np.random.randint(100, 365):03d}{np.random.randint(1000, 9999):04d}V"
                phone = f"0{np.random.choice([70, 71, 72, 75, 76, 77, 78])}{np.random.randint(1000000, 9999999)}"
                
                # Add to vehicles data
                new_vehicle = pd.DataFrame({
                    'VehicleNumber': [vehicle_number],
                    'CustomerId': [customer_id],
                    'CustomerName': [customer_name],
                    'Address': [address],
                    'NIC': [nic],
                    'Phone': [phone],
                    'VehicleType': [vehicle_type],
                    'Model': [model],
                    'PurchaseDate': [pd.Timestamp(purchase_date)],
                    'Payment': [purchase_price],
                    'PaymentMethod': [payment_method],
                    'EmployeeId': [employee_id],
                    'Status': [status],
                    'RepairCost': [0],
                    'RepairStatus': ['None']
                })
                
                # Update session state
                st.session_state.vehicles_data = pd.concat([st.session_state.vehicles_data, new_vehicle], ignore_index=True)
                
                # Add to customers data
                new_customer = pd.DataFrame({
                    'CustomerId': [customer_id],
                    'CustomerName': [customer_name],
                    'Address': [address],
                    'NIC': [nic],
                    'Phone': [phone]
                })
                st.session_state.customers_data = pd.concat([st.session_state.customers_data, new_customer], ignore_index=True)
                
                st.success(f"✅ Vehicle {vehicle_number} added successfully! Customer {customer_name} created.")
                st.balloons()
                st.rerun()
    
    with tab3:
        st.subheader("✏️ Update Vehicle (Real-Time)")
        
        if len(st.session_state.vehicles_data) > 0:
            vehicle_to_update = st.selectbox("Select Vehicle to Update", st.session_state.vehicles_data['VehicleNumber'].tolist())
            
            if vehicle_to_update:
                selected_vehicle = st.session_state.vehicles_data[st.session_state.vehicles_data['VehicleNumber'] == vehicle_to_update].iloc[0]
                
                with st.form("update_vehicle_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_status = st.selectbox("Status", ['Available', 'Sold', 'Under Repair'], 
                                                index=['Available', 'Sold', 'Under Repair'].index(selected_vehicle['Status']))
                        new_price = st.number_input("Price", value=int(selected_vehicle['Payment']))
                    
                    with col2:
                        new_customer = st.number_input("Customer ID", value=int(selected_vehicle['CustomerId']))
                        new_employee = st.number_input("Employee ID", value=int(selected_vehicle['EmployeeId']))
                    
                    submitted = st.form_submit_button("🔄 Update Vehicle (Real-Time)", type="primary")
                    
                    if submitted:
                        # Update the vehicle data
                        mask = st.session_state.vehicles_data['VehicleNumber'] == vehicle_to_update
                        st.session_state.vehicles_data.loc[mask, 'Status'] = new_status
                        st.session_state.vehicles_data.loc[mask, 'Payment'] = new_price
                        st.session_state.vehicles_data.loc[mask, 'CustomerId'] = new_customer
                        st.session_state.vehicles_data.loc[mask, 'EmployeeId'] = new_employee
                        
                        st.success(f"✅ Vehicle {vehicle_to_update} updated successfully!")
                        st.rerun()
        else:
            st.info("No vehicles available to update")
    
    with tab4:
        st.subheader("🔧 Vehicle Actions (Real-Time)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Submit for Repair")
            with st.form("repair_form"):
                repair_vehicle = st.selectbox("Select Vehicle for Repair", st.session_state.vehicles_data['VehicleNumber'].tolist())
                repair_details = st.text_area("Repair Details", placeholder="Describe the repair work needed...")
                repair_cost = st.number_input("Repair Cost (Rs.)", min_value=0, step=100, value=25000)
                repair_location = st.selectbox("Repair Location", ['Main Workshop', 'Service Center A', 'Service Center B', 'Mobile Service'])
                
                repair_submitted = st.form_submit_button("🔧 Submit for Repair", type="primary")
                
                if repair_submitted and repair_vehicle:
                    # Update vehicle status to Under Repair
                    mask = st.session_state.vehicles_data['VehicleNumber'] == repair_vehicle
                    st.session_state.vehicles_data.loc[mask, 'Status'] = 'Under Repair'
                    st.session_state.vehicles_data.loc[mask, 'RepairCost'] = repair_cost
                    st.session_state.vehicles_data.loc[mask, 'RepairStatus'] = 'In Progress'
                    
                    # Add to repairs data
                    new_repair_id = f"REP{str(len(st.session_state.repairs_data) + 1).zfill(3)}"
                    new_repair = pd.DataFrame({
                        'RepairID': [new_repair_id],
                        'VehicleNumber': [repair_vehicle],
                        'StartDate': [datetime.now().strftime('%Y-%m-%d')],
                        'EndDate': [(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')],
                        'RepairDetails': [repair_details],
                        'Location': [repair_location],
                        'Amount': [repair_cost],
                        'Status': ['In Progress'],
                        'Priority': ['Medium']
                    })
                    st.session_state.repairs_data = pd.concat([st.session_state.repairs_data, new_repair], ignore_index=True)
                    
                    st.success(f"🔧 Vehicle {repair_vehicle} submitted for repair!")
                    st.rerun()
        
        with col2:
            st.subheader("💰 Mark as Sold")
            available_vehicles = st.session_state.vehicles_data[st.session_state.vehicles_data['Status'] == 'Available']['VehicleNumber'].tolist()
            
            if available_vehicles:
                with st.form("sell_form"):
                    sell_vehicle = st.selectbox("Select Vehicle to Sell", available_vehicles)
                    sale_price = st.number_input("Final Sale Price (Rs.)", min_value=0, step=1000)
                    
                    sell_submitted = st.form_submit_button("💰 Mark as Sold", type="primary")
                    
                    if sell_submitted:
                        # Update vehicle status to Sold
                        mask = st.session_state.vehicles_data['VehicleNumber'] == sell_vehicle
                        st.session_state.vehicles_data.loc[mask, 'Status'] = 'Sold'
                        if sale_price > 0:
                            st.session_state.vehicles_data.loc[mask, 'Payment'] = sale_price
                        
                        st.success(f"💰 Vehicle {sell_vehicle} marked as sold!")
                        st.balloons()
                        st.rerun()
            else:
                st.info("No vehicles available for sale")

# Customer Management Page
elif st.session_state.current_page == 'customer_management':
    st.title("👥 Customer Management - Real-Time Updates")
    
    tab1, tab2, tab3 = st.tabs(["📋 All Customers", "➕ Add Customer", "✏️ Update Customer"])
    
    with tab1:
        st.subheader("All Customers (Live Data)")
        
        # Real-time customer stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Customers", len(st.session_state.customers_data))
        with col2:
            if len(st.session_state.customers_data) > 0 and len(st.session_state.vehicles_data) > 0:
                customers_with_vehicles = len(st.session_state.customers_data[st.session_state.customers_data['CustomerId'].isin(st.session_state.vehicles_data['CustomerId'])])
            else:
                customers_with_vehicles = 0
            st.metric("Active Customers", customers_with_vehicles)
        with col3:
            if len(st.session_state.vehicles_data) > 0:
                sold_customers = len(st.session_state.vehicles_data[st.session_state.vehicles_data['Status'] == 'Sold']['CustomerId'].unique())
            else:
                sold_customers = 0
            st.metric("Customers with Sales", sold_customers)
        with col4:
            # Calculate new customers (those added after initial load)
            initial_customer_count = len(df) if 'df' in locals() else 0
            new_customers_today = max(0, len(st.session_state.customers_data) - initial_customer_count)
            st.metric("New Today", new_customers_today)
        
        # Search functionality
        search_term = st.text_input("🔍 Search Customers", placeholder="Search by name, NIC, or phone...")
        
        display_customers = st.session_state.customers_data.copy()
        if search_term:
            display_customers = display_customers[
                display_customers['CustomerName'].str.contains(search_term, case=False, na=False) |
                display_customers['NIC'].str.contains(search_term, case=False, na=False) |
                display_customers['Phone'].str.contains(search_term, case=False, na=False)
            ]
        
        st.dataframe(display_customers, use_container_width=True)
    
    with tab2:
        st.subheader("➕ Add New Customer (Real-Time)")
        
        with st.form("add_customer_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            # Sri Lankan names for selection
            sri_lankan_first_names = ['Kamal', 'Nimal', 'Sunil', 'Rohan', 'Ajith', 'Chaminda', 'Pradeep', 'Nuwan', 'Dinesh', 'Mahesh', 'Raveena', 'Sewwandi', 'Nimali', 'Rashika', 'Sandani']
            sri_lankan_last_names = ['Silva', 'Perera', 'Fernando', 'Jayawardena', 'Gunasekara', 'Wijesinghe', 'Rajapaksa', 'Wickramasinghe', 'Mendis', 'Bandara']
            sri_lankan_cities = ['Colombo 01', 'Colombo 03', 'Dehiwala', 'Mount Lavinia', 'Moratuwa', 'Kandy', 'Galle', 'Negombo', 'Kurunegala', 'Anuradhapura']
            
            with col1:
                first_name = st.selectbox("First Name", sri_lankan_first_names)
                last_name = st.selectbox("Last Name", sri_lankan_last_names)
                
                # Auto-generate address
                house_no = st.number_input("House Number", min_value=1, max_value=999, value=np.random.randint(1, 999))
                street = st.selectbox("Street", ['Galle Road', 'Kandy Road', 'Negombo Road', 'Main Street', 'Temple Road', 'School Lane'])
                city = st.selectbox("City", sri_lankan_cities)
            
            with col2:
                # Auto-generate NIC
                birth_year = st.selectbox("Birth Year", range(1950, 2005))
                day_of_year = st.number_input("Day of Year", min_value=1, max_value=365, value=np.random.randint(1, 365))
                
                # Auto-generate phone
                phone_prefix = st.selectbox("Phone Prefix", ['070', '071', '072', '075', '076', '077', '078'])
                phone_number = st.text_input("Phone Number (7 digits)", value=str(np.random.randint(1000000, 9999999)))
            
            submitted = st.form_submit_button("🚀 Add Customer (Real-Time)", type="primary")
            
            if submitted:
                # Generate full details
                customer_name = f"{first_name} {last_name}"
                address = f"{house_no}/{np.random.randint(1, 20)}, {street}, {city}"
                
                # Generate NIC (old format) - fix the validation
                try:
                    birth_year_short = birth_year % 100
                    serial_number = np.random.randint(1000, 9999)
                    nic = f"{birth_year_short:02d}{day_of_year:03d}{serial_number}V"
                except:
                    # Fallback NIC generation
                    nic = f"{np.random.randint(75, 99):02d}{np.random.randint(100, 365):03d}{np.random.randint(1000, 9999)}V"
                
                phone = f"{phone_prefix}{phone_number}"
                
                # Validate phone number length
                if len(phone_number) != 7:
                    st.error("Phone number must be exactly 7 digits")
                    st.stop()
                
                # Add new customer
                new_customer_id = st.session_state.customers_data['CustomerId'].max() + 1 if len(st.session_state.customers_data) > 0 else 1
                
                new_customer = pd.DataFrame({
                    'CustomerId': [new_customer_id],
                    'CustomerName': [customer_name],
                    'Address': [address],
                    'NIC': [nic],
                    'Phone': [phone]
                })
                
                st.session_state.customers_data = pd.concat([st.session_state.customers_data, new_customer], ignore_index=True)
                
                st.success(f"✅ Customer {customer_name} added successfully! ID: {new_customer_id}")
                st.balloons()
                st.rerun()
    
    with tab3:
        st.subheader("✏️ Update Customer (Real-Time)")
        
        if len(st.session_state.customers_data) > 0:
            customer_to_update = st.selectbox("Select Customer", 
                                            [f"{row['CustomerName']} (ID: {row['CustomerId']})" for _, row in st.session_state.customers_data.iterrows()])
            
            if customer_to_update:
                # Extract customer ID from selection
                customer_id = int(customer_to_update.split("ID: ")[1].split(")")[0])
                selected_customer = st.session_state.customers_data[st.session_state.customers_data['CustomerId'] == customer_id].iloc[0]
                
                with st.form("update_customer_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        current_name_parts = selected_customer['CustomerName'].split(' ')
                        first_name = current_name_parts[0] if len(current_name_parts) > 0 else ""
                        last_name = " ".join(current_name_parts[1:]) if len(current_name_parts) > 1 else ""
                        
                        new_first_name = st.text_input("First Name", value=first_name)
                        new_last_name = st.text_input("Last Name", value=last_name)
                        new_address = st.text_area("Address", value=selected_customer['Address'])
                    
                    with col2:
                        new_nic = st.text_input("NIC Number", value=selected_customer['NIC'])
                        new_phone = st.text_input("Phone Number", value=selected_customer['Phone'])
                        
                        # Show current vehicle info
                        customer_vehicles = st.session_state.vehicles_data[st.session_state.vehicles_data['CustomerId'] == customer_id]
                        if len(customer_vehicles) > 0:
                            st.info(f"🚗 Vehicles: {len(customer_vehicles)} | Sold: {len(customer_vehicles[customer_vehicles['Status'] == 'Sold'])}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        delete_submitted = st.form_submit_button("🗑️ Delete Customer", type="secondary")
                    with col2:
                        update_submitted = st.form_submit_button("🔄 Update Customer", type="primary")
                    
                    if update_submitted:
                        # Update customer data
                        mask = st.session_state.customers_data['CustomerId'] == customer_id
                        st.session_state.customers_data.loc[mask, 'CustomerName'] = f"{new_first_name} {new_last_name}"
                        st.session_state.customers_data.loc[mask, 'Address'] = new_address
                        st.session_state.customers_data.loc[mask, 'NIC'] = new_nic
                        st.session_state.customers_data.loc[mask, 'Phone'] = new_phone
                        
                        # Update corresponding vehicle data
                        vehicle_mask = st.session_state.vehicles_data['CustomerId'] == customer_id
                        st.session_state.vehicles_data.loc[vehicle_mask, 'CustomerName'] = f"{new_first_name} {new_last_name}"
                        st.session_state.vehicles_data.loc[vehicle_mask, 'Address'] = new_address
                        st.session_state.vehicles_data.loc[vehicle_mask, 'NIC'] = new_nic
                        st.session_state.vehicles_data.loc[vehicle_mask, 'Phone'] = new_phone
                        
                        st.success(f"✅ Customer {new_first_name} {new_last_name} updated successfully!")
                        st.rerun()
                    
                    if delete_submitted:
                        # Remove customer and associated vehicles
                        st.session_state.customers_data = st.session_state.customers_data[st.session_state.customers_data['CustomerId'] != customer_id]
                        st.session_state.vehicles_data = st.session_state.vehicles_data[st.session_state.vehicles_data['CustomerId'] != customer_id]
                        
                        st.warning(f"🗑️ Customer and associated vehicles deleted!")
                        st.rerun()
        else:
            st.info("No customers available to update")
            # Repair Management Page
elif st.session_state.current_page == 'repair_management':
    st.title("🔧 Repair Management - Real-Time Updates")
    
    tab1, tab2, tab3 = st.tabs(["🔧 Active Repairs", "➕ Add Repair", "📋 Repair History"])
    
    with tab1:
        st.subheader("Active Repairs (Live Data)")
        
        # Real-time repair stats
        col1, col2, col3, col4 = st.columns(4)
        if len(st.session_state.repairs_data) > 0:
            active_repairs = st.session_state.repairs_data[st.session_state.repairs_data['Status'].isin(['In Progress', 'Pending'])]
            completed_repairs = st.session_state.repairs_data[st.session_state.repairs_data['Status'] == 'Completed']
            
            with col1:
                st.metric("Active Repairs", len(active_repairs))
            with col2:
                st.metric("Completed This Month", len(completed_repairs))
            with col3:
                total_repair_cost = active_repairs['Amount'].sum() if len(active_repairs) > 0 else 0
                st.metric("Active Repair Value", f"Rs.{total_repair_cost/1000:.0f}k")
            with col4:
                avg_repair_time = "5-7 days"  # Sample
                st.metric("Avg Repair Time", avg_repair_time)
        else:
            with col1:
                st.metric("Active Repairs", 0)
            with col2:
                st.metric("Completed This Month", 0)
            with col3:
                st.metric("Active Repair Value", "Rs.0k")
            with col4:
                st.metric("Avg Repair Time", "N/A")
        
        # Filter repairs
        if len(st.session_state.repairs_data) > 0:
            repair_status_filter = st.selectbox("Filter by Status", ["All"] + list(st.session_state.repairs_data['Status'].unique()))
            
            display_repairs = st.session_state.repairs_data.copy()
            if repair_status_filter != "All":
                display_repairs = display_repairs[display_repairs['Status'] == repair_status_filter]
            
            st.dataframe(display_repairs, use_container_width=True)
        else:
            st.info("No repair records available. Add repairs in the 'Add Repair' tab.")
            st.dataframe(pd.DataFrame(columns=['RepairID', 'VehicleNumber', 'StartDate', 'EndDate', 'RepairDetails', 'Location', 'Amount', 'Status']), use_container_width=True)
    
    with tab2:
        st.subheader("➕ Add New Repair (Real-Time)")
        
        with st.form("add_repair_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                available_vehicles = st.session_state.vehicles_data['VehicleNumber'].tolist()
                repair_vehicle = st.selectbox("Vehicle Number", available_vehicles)
                repair_start_date = st.date_input("Repair Start Date", value=datetime.now())
                repair_details = st.text_area("Repair Details", placeholder="Describe repair work needed...")
                repair_location = st.selectbox("Location", ['Main Workshop', 'Service Center A', 'Service Center B', 'Mobile Service'])
            
            with col2:
                repair_end_date = st.date_input("Expected End Date", value=datetime.now() + timedelta(days=7))
                repair_amount = st.number_input("Repair Amount (Rs.)", min_value=0, step=100, value=25000)
                repair_status = st.selectbox("Initial Status", ['Pending', 'In Progress'])
                priority = st.selectbox("Priority", ['Low', 'Medium', 'High', 'Urgent'])
            
            submitted = st.form_submit_button("🔧 Create Repair Job", type="primary")
            
            if submitted and repair_vehicle:
                # Generate new repair ID
                new_repair_id = f"REP{str(len(st.session_state.repairs_data) + 1).zfill(3)}"
                
                # Add Priority field to repairs data if not exists
                if 'Priority' not in st.session_state.repairs_data.columns:
                    st.session_state.repairs_data['Priority'] = 'Medium'
                
                new_repair = pd.DataFrame({
                    'RepairID': [new_repair_id],
                    'VehicleNumber': [repair_vehicle],
                    'StartDate': [repair_start_date.strftime('%Y-%m-%d')],
                    'EndDate': [repair_end_date.strftime('%Y-%m-%d')],
                    'RepairDetails': [repair_details],
                    'Location': [repair_location],
                    'Amount': [repair_amount],
                    'Status': [repair_status],
                    'Priority': [priority]
                })
                
                st.session_state.repairs_data = pd.concat([st.session_state.repairs_data, new_repair], ignore_index=True)
                
                # Update vehicle status if needed
                if repair_status == 'In Progress':
                    mask = st.session_state.vehicles_data['VehicleNumber'] == repair_vehicle
                    st.session_state.vehicles_data.loc[mask, 'Status'] = 'Under Repair'
                    st.session_state.vehicles_data.loc[mask, 'RepairCost'] = repair_amount
                    st.session_state.vehicles_data.loc[mask, 'RepairStatus'] = repair_status
                
                st.success(f"🔧 Repair job {new_repair_id} created for vehicle {repair_vehicle}!")
                st.rerun()
    
    with tab3:
        st.subheader("📋 Repair History & Management")
        
        if len(st.session_state.repairs_data) > 0:
            # Update repair status
    with tab3:
        st.subheader("📋 Repair History & Management")
        
        if len(st.session_state.repairs_data) > 0:
            # Update repair status
            st.subheader("🔄 Update Repair Status")
            
            with st.form("update_repair_form"):
                repair_options = [f"{row['RepairID']} - {row['VehicleNumber']} ({row['Status']})" for _, row in st.session_state.repairs_data.iterrows()]
                
                if repair_options:
                    repair_to_update = st.selectbox("Select Repair Job", repair_options)
                    
                    repair_id = repair_to_update.split(" - ")[0]
                    selected_repair = st.session_state.repairs_data[st.session_state.repairs_data['RepairID'] == repair_id].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        new_status = st.selectbox("New Status", ['Pending', 'In Progress', 'Completed', 'Cancelled'],
                                                index=['Pending', 'In Progress', 'Completed', 'Cancelled'].index(selected_repair['Status']))
                        new_amount = st.number_input("Final Amount", value=float(selected_repair['Amount']))
                    
                    with col2:
                        completion_notes = st.text_area("Completion Notes", placeholder="Add any notes about the repair...")
                        new_end_date = st.date_input("Actual End Date", value=datetime.now())
                    
                    update_submitted = st.form_submit_button("🔄 Update Repair", type="primary")
                    
                    if update_submitted:
                        # Update repair data
                        mask = st.session_state.repairs_data['RepairID'] == repair_id
                        st.session_state.repairs_data.loc[mask, 'Status'] = new_status
                        st.session_state.repairs_data.loc[mask, 'Amount'] = new_amount
                        st.session_state.repairs_data.loc[mask, 'EndDate'] = new_end_date.strftime('%Y-%m-%d')
                        
                        # Update vehicle status based on repair completion
                        vehicle_number = selected_repair['VehicleNumber']
                        vehicle_mask = st.session_state.vehicles_data['VehicleNumber'] == vehicle_number
                        
                        if new_status == 'Completed':
                            st.session_state.vehicles_data.loc[vehicle_mask, 'Status'] = 'Available'
                            st.session_state.vehicles_data.loc[vehicle_mask, 'RepairStatus'] = 'Completed'
                        elif new_status == 'In Progress':
                            st.session_state.vehicles_data.loc[vehicle_mask, 'Status'] = 'Under Repair'
                            st.session_state.vehicles_data.loc[vehicle_mask, 'RepairStatus'] = 'In Progress'
                        
                        st.session_state.vehicles_data.loc[vehicle_mask, 'RepairCost'] = new_amount
                        
                        st.success(f"✅ Repair {repair_id} updated to {new_status}!")
                        if new_status == 'Completed':
                            st.balloons()
                        st.rerun()
                else:
                    st.info("No repair jobs available to update")
            
            # Display all repair history
            st.subheader("📋 All Repair Records")
            st.dataframe(st.session_state.repairs_data, use_container_width=True)
        else:
            st.info("No repair records available. Add repairs in the 'Add Repair' tab.")

# Supplier Management Page
elif st.session_state.current_page == 'supplier_management':
    st.title("🏪 Supplier Management - Real-Time Updates")
    
    tab1, tab2, tab3 = st.tabs(["📋 All Suppliers", "➕ Add Supplier", "✏️ Update Supplier"])
    
    with tab1:
        st.subheader("All Suppliers (Live Data)")
        
        # Real-time supplier stats
        col1, col2, col3, col4 = st.columns(4)
        active_suppliers = st.session_state.suppliers_data[st.session_state.suppliers_data['Status'] == 'Active']
        
        with col1:
            st.metric("Total Suppliers", len(st.session_state.suppliers_data))
        with col2:
            st.metric("Active Suppliers", len(active_suppliers))
        with col3:
            avg_rating = st.session_state.suppliers_data['Rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}⭐")
        with col4:
            total_orders = st.session_state.suppliers_data['TotalOrders'].sum()
            st.metric("Total Orders", total_orders)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            supplier_type_filter = st.selectbox("Filter by Type", ["All"] + list(st.session_state.suppliers_data['SupplierType'].unique()))
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All"] + list(st.session_state.suppliers_data['Status'].unique()))
        with col3:
            rating_filter = st.selectbox("Min Rating", ["All", "4.0+", "4.5+", "4.8+"])
        
        # Apply filters
        display_suppliers = st.session_state.suppliers_data.copy()
        if supplier_type_filter != "All":
            display_suppliers = display_suppliers[display_suppliers['SupplierType'] == supplier_type_filter]
        if status_filter != "All":
            display_suppliers = display_suppliers[display_suppliers['Status'] == status_filter]
        if rating_filter != "All":
            min_rating = float(rating_filter.replace("+", ""))
            display_suppliers = display_suppliers[display_suppliers['Rating'] >= min_rating]
        
        st.dataframe(display_suppliers, use_container_width=True)
        
        # Top performing suppliers
        if len(display_suppliers) > 0:
            st.subheader("🏆 Top Performing Suppliers")
            top_suppliers = display_suppliers.nlargest(3, 'Rating')[['CompanyName', 'Rating', 'TotalOrders', 'SupplierType']]
            
            col1, col2, col3 = st.columns(3)
            for i, (_, supplier) in enumerate(top_suppliers.iterrows()):
                with [col1, col2, col3][i]:
                    st.success(f"🥇 **{supplier['CompanyName']}**")
                    st.write(f"Rating: {supplier['Rating']}⭐")
                    st.write(f"Orders: {supplier['TotalOrders']}")
                    st.write(f"Type: {supplier['SupplierType']}")
    
    with tab2:
        st.subheader("➕ Add New Supplier (Real-Time)")
        
        with st.form("add_supplier_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name", placeholder="e.g., ABC Motors (Pvt) Ltd")
                contact_person = st.text_input("Contact Person")
                supplier_type = st.selectbox("Supplier Type", 
                                           ['Vehicle Importer', 'Parts Supplier', 'Service Provider', 'Finance Partner', 'Insurance Provider', 'Logistics Partner'])
                
                # Address components
                address_number = st.text_input("Address Number", placeholder="e.g., 123/45")
                street = st.selectbox("Street", ['Galle Road', 'Kandy Road', 'Negombo Road', 'Baseline Road', 'Duplication Road', 'Main Street'])
                city = st.selectbox("City", ['Colombo 03', 'Colombo 04', 'Dehiwala', 'Mount Lavinia', 'Moratuwa', 'Kandy', 'Galle', 'Negombo', 'Kurunegala'])
            
            with col2:
                phone_number = st.text_input("Phone Number", placeholder="011XXXXXXX")
                email_address = st.text_input("Email Address", placeholder="info@company.lk")
                rating = st.selectbox("Initial Rating", [5.0, 4.9, 4.8, 4.7, 4.5, 4.2, 4.0, 3.5])
                initial_orders = st.number_input("Initial Order Count", min_value=0, max_value=100, value=0)
                status = st.selectbox("Status", ['Active', 'Pending', 'Suspended'])
            
            submitted = st.form_submit_button("🚀 Add Supplier", type="primary")
            
            if submitted and company_name:
                # Generate new supplier ID
                new_supplier_id = f"SUP{str(len(st.session_state.suppliers_data) + 1).zfill(3)}"
                
                # Combine address
                full_address = f"{address_number}, {street}, {city}"
                
                # Add new supplier
                new_supplier = pd.DataFrame({
                    'SupplierID': [new_supplier_id],
                    'CompanyName': [company_name],
                    'ContactPerson': [contact_person],
                    'SupplierType': [supplier_type],
                    'Address': [full_address],
                    'Phone': [phone_number],
                    'Email': [email_address],
                    'Rating': [rating],
                    'LastDelivery': [datetime.now().strftime('%Y-%m-%d')],
                    'TotalOrders': [initial_orders],
                    'Status': [status]
                })
                
                st.session_state.suppliers_data = pd.concat([st.session_state.suppliers_data, new_supplier], ignore_index=True)
                
                st.success(f"✅ Supplier {company_name} added successfully! ID: {new_supplier_id}")
                st.balloons()
                st.rerun()
    
    with tab3:
        st.subheader("✏️ Update Supplier (Real-Time)")
        
        if len(st.session_state.suppliers_data) > 0:
            supplier_to_update = st.selectbox("Select Supplier", 
                                            [f"{row['CompanyName']} ({row['SupplierID']})" for _, row in st.session_state.suppliers_data.iterrows()])
            
            if supplier_to_update:
                # Extract supplier ID
                supplier_id = supplier_to_update.split("(")[1].replace(")", "")
                selected_supplier = st.session_state.suppliers_data[st.session_state.suppliers_data['SupplierID'] == supplier_id].iloc[0]
                
                with st.form("update_supplier_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_company_name = st.text_input("Company Name", value=selected_supplier['CompanyName'])
                        new_contact_person = st.text_input("Contact Person", value=selected_supplier['ContactPerson'])
                        new_supplier_type = st.selectbox("Supplier Type", 
                                                       ['Vehicle Importer', 'Parts Supplier', 'Service Provider', 'Finance Partner', 'Insurance Provider'],
                                                       index=['Vehicle Importer', 'Parts Supplier', 'Service Provider', 'Finance Partner', 'Insurance Provider'].index(selected_supplier['SupplierType']))
                        new_address = st.text_area("Address", value=selected_supplier['Address'])
                    
                    with col2:
                        new_phone = st.text_input("Phone Number", value=selected_supplier['Phone'])
                        new_email = st.text_input("Email", value=selected_supplier['Email'])
                        new_rating = st.selectbox("Rating", [5.0, 4.9, 4.8, 4.7, 4.5, 4.2, 4.0, 3.5],
                                                 index=[5.0, 4.9, 4.8, 4.7, 4.5, 4.2, 4.0, 3.5].index(selected_supplier['Rating']))
                        new_status = st.selectbox("Status", ['Active', 'Pending', 'Suspended'],
                                                 index=['Active', 'Pending', 'Suspended'].index(selected_supplier['Status']))
                        
                        # Update orders
                        new_total_orders = st.number_input("Total Orders", value=int(selected_supplier['TotalOrders']), min_value=0)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        delete_submitted = st.form_submit_button("🗑️ Delete Supplier", type="secondary")
                    with col2:
                        update_submitted = st.form_submit_button("🔄 Update Supplier", type="primary")
                    
                    if update_submitted:
                        # Update supplier data
                        mask = st.session_state.suppliers_data['SupplierID'] == supplier_id
                        st.session_state.suppliers_data.loc[mask, 'CompanyName'] = new_company_name
                        st.session_state.suppliers_data.loc[mask, 'ContactPerson'] = new_contact_person
                        st.session_state.suppliers_data.loc[mask, 'SupplierType'] = new_supplier_type
                        st.session_state.suppliers_data.loc[mask, 'Address'] = new_address
                        st.session_state.suppliers_data.loc[mask, 'Phone'] = new_phone
                        st.session_state.suppliers_data.loc[mask, 'Email'] = new_email
                        st.session_state.suppliers_data.loc[mask, 'Rating'] = new_rating
                        st.session_state.suppliers_data.loc[mask, 'Status'] = new_status
                        st.session_state.suppliers_data.loc[mask, 'TotalOrders'] = new_total_orders
                        st.session_state.suppliers_data.loc[mask, 'LastDelivery'] = datetime.now().strftime('%Y-%m-%d')
                        
                        st.success(f"✅ Supplier {new_company_name} updated successfully!")
                        st.rerun()
                    
                    if delete_submitted:
                        # Remove supplier
                        st.session_state.suppliers_data = st.session_state.suppliers_data[st.session_state.suppliers_data['SupplierID'] != supplier_id]
                        
                        st.warning(f"🗑️ Supplier {selected_supplier['CompanyName']} deleted!")
                        st.rerun()
        else:
            st.info("No suppliers available to update")

# Sales Reports Page
elif st.session_state.current_page == 'sales_reports':
    st.title("💰 Sales Reports & Analytics - Real-Time Data")
    
    # Use real-time data
    current_data = st.session_state.vehicles_data.copy()
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=365))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Filter data by date range
    filtered_sales = current_data[(current_data['PurchaseDate'].dt.date >= start_date) & 
                                 (current_data['PurchaseDate'].dt.date <= end_date) & 
                                 (current_data['Status'] == 'Sold')]
    
    # Real-time key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics safely
    avg_sale = filtered_sales['Payment'].mean() if len(filtered_sales) > 0 else 0
    original_sales_count = len(df[df['Status'] == 'Sold']) if 'df' in locals() else 0
    sales_delta = len(filtered_sales) - original_sales_count
    
    with col1:
        st.metric("Total Sales", len(filtered_sales), delta=f"+{max(0, sales_delta)}")
    with col2:
        total_revenue = filtered_sales['Payment'].sum()
        st.metric("Total Revenue", f"Rs.{total_revenue/1000000:.2f}M", delta="+12%")
    with col3:
        st.metric("Average Sale", f"Rs.{avg_sale:.0f}", delta="+8%")
    with col4:
        top_model = filtered_sales['Model'].mode().iloc[0] if len(filtered_sales) > 0 else "N/A"
        st.metric("Top Model", top_model)
    
    # Real-time charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales by Model (Real-time)
        st.subheader("Sales by Model (Live Data)")
        if len(filtered_sales) > 0:
            model_sales = filtered_sales['Model'].value_counts()
            fig = px.pie(values=model_sales.values, names=model_sales.index, 
                        title="Sales Distribution by Model")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data for selected period")
    
    with col2:
        # Sales by Payment Method (Real-time)
        st.subheader("Sales by Payment Method (Live Data)")
        if len(filtered_sales) > 0:
            payment_sales = filtered_sales['PaymentMethod'].value_counts()
            fig = px.bar(x=payment_sales.index, y=payment_sales.values,
                        title="Sales by Payment Method")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No payment data for selected period")
    
    # Monthly sales trend with proper 12-month display (Real-time)
    st.subheader("Monthly Sales Trend (Real-Time Data)")
    
    # Create complete 12-month framework
    all_months_df = pd.DataFrame({
        'Month': range(1, 13),
        'MonthName': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    })
    
    # Get actual monthly sales data from real-time data
    if len(filtered_sales) > 0:
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
        fig.update_layout(title_text="Monthly Sales Revenue and Count - Full Year (Real-Time)")
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sales data available for monthly trend analysis")
    
    # Real-time detailed sales table
    st.subheader("Detailed Sales Data (Real-Time)")
    if len(filtered_sales) > 0:
        # Add action buttons for real-time operations
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Export to CSV"):
                csv = filtered_sales.to_csv(index=False)
                st.download_button("Download CSV", csv, "sales_report.csv", "text/csv")
        with col2:
            if st.button("🔄 Refresh Data"):
                st.rerun()
        with col3:
            st.info(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        
        st.dataframe(filtered_sales, use_container_width=True)
        
        # Real-time sales summary
        st.subheader("📈 Real-Time Sales Summary")
        
        if len(filtered_sales) > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success("🚗 **Vehicle Types Sold**")
                vehicle_type_counts = filtered_sales['VehicleType'].value_counts()
                for vehicle_type, count in vehicle_type_counts.items():
                    st.write(f"• {vehicle_type}: {count} units")
            
            with col2:
                st.info("💳 **Payment Methods Used**")
                payment_counts = filtered_sales['PaymentMethod'].value_counts()
                for method, count in payment_counts.items():
                    st.write(f"• {method}: {count} sales")
            
            with col3:
                st.warning("📅 **Recent Activity**")
                recent_sales = filtered_sales.nlargest(3, 'PurchaseDate')[['VehicleNumber', 'CustomerName', 'Payment']]
                for _, sale in recent_sales.iterrows():
                    st.write(f"• {sale['VehicleNumber']}: Rs.{sale['Payment']/1000:.0f}k")
        else:
            st.info("No sales summary available - no sales in selected period")
    else:
        st.info("No sales data available for the selected date range")

# Footer
st.markdown(
<div style="text-align: center; color: #ecf0f1; padding: 2rem; background: linear-gradient(to bottom, #0d0f14, #000000); border-radius: 15px; margin: 2rem 0;">
    <h3> CM Vehicle Management System</h3>
    <p><strong>Real-Time Vehicle Sales & Management Dashboard</strong></p>
    <p>Built with Group AT | © 2025 CM Vehicle Management. All rights reserved.</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        📧 Email: chamod@cmvehicles.com | 📞 Phone: +94 70 520 6400 
    </p>
    <p style="font-size: 0.8rem; opacity: 0.6;">
        ⚡ Real-Time Updates Enabled | 🔄 Data Synced: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </p>
</div>
