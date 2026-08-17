import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import hashlib
import json
import os

st.set_page_config(page_title="Admission & Enrollment Analytics", layout="wide", page_icon="🎓")

# User Management Functions
USER_DB = "users.json"

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_users():
    if not os.path.exists(USER_DB):
        with open(USER_DB, 'w') as f:
            json.dump({}, f)
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    with open(USER_DB, 'w') as f:
        json.dump(users, f)
    return True

def verify_user(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True
    return False

# CSS for styling and interactive animations
st.markdown("""
<style>
    /* Professional Corporate Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-size: cover;
        background-attachment: fixed;
    }

    /* Glassmorphism for Auth Cards */
    .auth-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        max-width: 450px;
        margin: auto;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 25, 35, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Card Styling */
    .st-emotion-cache-12w0qpk {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
    }
    
    /* Main Title Styling */
    h1 {
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        background: linear-gradient(90deg, #ffffff, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h3 {
        color: #ecf0f1 !important;
        font-weight: 400 !important;
    }

    /* Metric Cards Interactive Hover */
    .metric-card {
        background-color: rgba(20, 35, 45, 0.75);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        text-align: center;
        border-top: 4px solid #3498db;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        border-left: 1px solid rgba(255,255,255,0.1);
        border-right: 1px solid rgba(255,255,255,0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        border-top: 4px solid #9b59b6;
        background-color: rgba(25, 45, 60, 0.85);
    }

    .metric-value {
        font-size: 2.2em;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-title {
        color: #bdc3c7;
        text-transform: uppercase;
        font-size: 0.9em;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Hyper-Interactive Buttons */
    .stButton > button {
        background: linear-gradient(270deg, #ff6a00, #ee0979, #8e2de2, #4a00e0);
        background-size: 800% 800%;
        animation: buttonGlow 4s ease infinite;
        color: white !important;
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.5rem;
        font-weight: 800;
        font-size: 1.05em;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    
    @keyframes buttonGlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.08);
        box-shadow: 0 15px 25px rgba(238, 9, 121, 0.6);
        letter-spacing: 2px;
    }
    
    .stButton > button:active {
        transform: translateY(2px) scale(0.95);
        box-shadow: 0 5px 10px rgba(238, 9, 121, 0.3);
    }

    /* Enhance tabs interactivity */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(20, 35, 45, 0.6);
        border-radius: 10px 10px 0px 0px;
        padding: 10px 25px;
        font-size: 16px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.05);
        border-bottom: none;
        transition: all 0.3s ease;
        color: #bdc3c7;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(30, 50, 65, 0.9);
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(15, 32, 39, 0.95);
        border-top: 3px solid #00c6ff !important;
        color: #ffffff !important;
        box-shadow: 0 -4px 10px rgba(0,0,0,0.3);
    }
    
    /* Interactive Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 32, 39, 0.75) !important;
        backdrop-filter: blur(20px);
        box-shadow: 5px 0 25px rgba(0,0,0,0.5);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Interactive Selectors */
    .stMultiSelect [data-baseweb="select"] {
        transition: all 0.3s ease;
        border-radius: 8px;
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stMultiSelect [data-baseweb="select"]:hover {
        box-shadow: 0 4px 10px rgba(0, 198, 255, 0.3);
        border-color: #00c6ff;
    }
    
    /* Login Page Specifics */
    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .login-header h1 {
        color: #ffffff;
        font-weight: 700;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    .login-header p {
        color: #bdc3c7;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Authentication Page
def auth_page():
    # Hide sidebar and header during login for a true standalone app feel
    st.markdown("""
        <style>
            [data-testid="collapsedControl"] {display: none;}
            [data-testid="stSidebar"] {display: none;}
            .stAppHeader {display: none;}
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='login-header' style='margin-top: 8vh;'><h1>🎓 Enrollment AI</h1><p style='font-size: 1.2em;'>Professional Admission Analytics Platform</p></div>", unsafe_allow_html=True)
    
    # Center the login tabs using columns
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Secure Login", "📝 Register New Account"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("### Welcome Back")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit:
                    if verify_user(username, password):
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
        
        with tab2:
            with st.form("register_form"):
                st.markdown("### Create an Account")
                new_username = st.text_input("Choose Username")
                new_password = st.text_input("Choose Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                register = st.form_submit_button("Create Account", use_container_width=True)
                
                if register:
                    if not new_username or not new_password:
                        st.error("Please fill all fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        if save_user(new_username, new_password):
                            st.success("Account created successfully! Please login.")
                        else:
                            st.error("Username already exists")

if not st.session_state['authenticated']:
    auth_page()
    st.stop()

# --- Logout in Sidebar ---
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state['username']}! 👋")
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.rerun()
    st.markdown("---")

@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

@st.cache_data
def load_data():
    leads = pd.read_csv("leads.csv")
    counselling = pd.read_csv("counselling.csv")
    applications = pd.read_csv("applications.csv")
    enrollment = pd.read_csv("enrollment.csv")
    
    df = leads.merge(counselling, on="Lead_ID", how="left")
    df = df.merge(applications, on="Lead_ID", how="left")
    df = df.merge(enrollment, on="Lead_ID", how="left")
    
    df['Date_Lead'] = pd.to_datetime(df['Date_Lead'])
    df['Date_Counselling'] = pd.to_datetime(df['Date_Counselling'])
    df['Date_Application'] = pd.to_datetime(df['Date_Application'])
    df['Date_Enrollment'] = pd.to_datetime(df['Date_Enrollment'])
    
    df['Month'] = df['Date_Lead'].dt.to_period('M').astype(str)
    
    # Calculate Lead Times
    df['Days_Lead_to_Counselling'] = (df['Date_Counselling'] - df['Date_Lead']).dt.days
    df['Days_Counselling_to_App'] = (df['Date_Application'] - df['Date_Counselling']).dt.days
    df['Days_App_to_Enroll'] = (df['Date_Enrollment'] - df['Date_Application']).dt.days
    
    # Target for ML
    df['Enrolled_Binary'] = df['Enrolled'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    return df

df = load_data()

# --- Sidebar Filters ---
with st.sidebar:
    st.markdown("### 🎛️ Interactive Data Controls")
    st.caption("Adjust parameters to instantly update all dashboard insights.")
    st.markdown("---")
    
    # Interactive Toggle + Multiselect for City
    all_cities = st.checkbox("📍 Select All Cities", value=True)
    if all_cities:
        selected_city = st.multiselect("Select City", options=df['City'].unique(), default=df['City'].unique(), label_visibility="collapsed")
    else:
        selected_city = st.multiselect("Select City", options=df['City'].unique(), default=[], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Toggle + Multiselect for Channel
    all_channels = st.checkbox("📢 Select All Channels", value=True)
    if all_channels:
        selected_channel = st.multiselect("Select Channel", options=df['Source_Channel'].unique(), default=df['Source_Channel'].unique(), label_visibility="collapsed")
    else:
        selected_channel = st.multiselect("Select Channel", options=df['Source_Channel'].unique(), default=[], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Select Slider for Time Range Scrubbing
    st.markdown("**📅 Select Month Range**")
    months_list = sorted(df['Month'].unique().tolist())
    if len(months_list) > 1:
        start_month, end_month = st.select_slider(
            "Month Range",
            options=months_list,
            value=(months_list[0], months_list[-1]),
            label_visibility="collapsed"
        )
        start_idx = months_list.index(start_month)
        end_idx = months_list.index(end_month)
        selected_month = months_list[start_idx:end_idx+1]
    else:
        selected_month = months_list
        st.info(f"Only data for {months_list[0]} available.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Toggle + Multiselect for Course
    all_courses = st.checkbox("📚 Select All Courses", value=True)
    course_options = df[df['Enrolled']=='Yes']['Course'].dropna().unique()
    if all_courses:
        selected_course = st.multiselect("Select Course", options=course_options, default=course_options, label_visibility="collapsed")
    else:
        selected_course = st.multiselect("Select Course", options=course_options, default=[], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("#### ⚡ Active View Summary")
    st.info(f"Filtering **{len(selected_city)}** cities, **{len(selected_channel)}** channels across a **{len(selected_month)}**-month timeframe.")

# Filter data
filtered_df = df[
    (df['City'].isin(selected_city)) &
    (df['Source_Channel'].isin(selected_channel)) &
    (df['Month'].isin(selected_month))
]

if selected_course:
    filtered_df_enrolled = filtered_df[(filtered_df['Enrolled'] == 'Yes') & (filtered_df['Course'].isin(selected_course))]
else:
    filtered_df_enrolled = filtered_df[filtered_df['Enrolled'] == 'Yes']

# --- Main Layout ---
lottie_url = "https://assets9.lottiefiles.com/packages/lf20_1a8wq6.json" # Alternative: https://assets3.lottiefiles.com/packages/lf20_qp1q7mct.json
lottie_edu = load_lottieurl(lottie_url)

col1, col2 = st.columns([3, 1])
with col1:
    st.title("🎓 Admission & Enrollment Analytics")
    st.markdown("### A premium, AI-powered platform for tracking student acquisition and optimizing the enrollment funnel.")
with col2:
    if lottie_edu:
        st_lottie(lottie_edu, height=120, key="edu_animation")

st.markdown("---")

# Tabs
tab_overview, tab_marketing, tab_operations, tab_financials, tab_predictive, tab_scenario = st.tabs([
    "🏠 Overview", "📈 Marketing Insights", "👥 Operations & Funnel", "💰 Financials", "🤖 Predictive Analytics", "🔮 Scenario Planner"
])

# Shared Metrics
total_leads = filtered_df.shape[0]
counselling_count = filtered_df[filtered_df["Counselling_Attended"] == "Yes"].shape[0]
application_count = filtered_df[filtered_df["Application_Submitted"] == "Yes"].shape[0]
enrolled_count = filtered_df_enrolled.shape[0]

counselling_rate = (counselling_count / total_leads) * 100 if total_leads > 0 else 0
application_rate = (application_count / counselling_count) * 100 if counselling_count > 0 else 0
enrollment_rate = (enrolled_count / application_count) * 100 if application_count > 0 else 0
overall_rate = (enrolled_count / total_leads) * 100 if total_leads > 0 else 0

with tab_overview:
    # Dynamic Insights Generator
    st.markdown("### 🌟 Real-Time Performance Snapshot")
    insight_col1, insight_col2 = st.columns([2, 1])
    with insight_col1:
        st.info(f"**Currently viewing data for {len(filtered_df):,} leads.** "
                f"Your overall conversion rate stands at **{overall_rate:.1f}%**. "
                f"{'Great job! 🎉' if overall_rate > 10 else 'There is room for funnel optimization. 🔍'}")
    
    # Custom CSS Metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    
    def metric_card(col, title, value, prefix="", suffix=""):
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{prefix}{value}{suffix}</div>
        </div>
        """, unsafe_allow_html=True)
        
    metric_card(c1, "Total Leads", total_leads)
    metric_card(c2, "Counselling Rate", f"{counselling_rate:.1f}", suffix="%")
    metric_card(c3, "Application Rate", f"{application_rate:.1f}", suffix="%")
    metric_card(c4, "Enrollment Rate", f"{enrollment_rate:.1f}", suffix="%")
    metric_card(c5, "Overall Conversion", f"{overall_rate:.1f}", suffix="%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Interactive Layout: 2 Columns
    ov_col1, ov_col2 = st.columns([1, 1])
    
    with ov_col1:
        # Chart Customization Selector
        chart_type_monthly = st.selectbox(
            "📊 Customize Monthly Trend Type",
            options=["Area Chart", "Bar Chart", "Line Chart"],
            index=0,
            key="ov_monthly_type"
        )
        
        # High level chart
        monthly_analysis = filtered_df.groupby("Month").agg(
            leads=("Lead_ID", "count"),
            enrolled=("Enrolled", lambda x: (x == "Yes").sum())
        ).reset_index()
        monthly_analysis[['leads', 'enrolled']] = monthly_analysis[['leads', 'enrolled']].astype(int)
        
        if chart_type_monthly == "Area Chart":
            fig_monthly = px.area(
                monthly_analysis, x='Month', y=['leads', 'enrolled'],
                title="Monthly Trend (Area)", color_discrete_map={'leads': '#3498db', 'enrolled': '#2ecc71'}, markers=True
            )
        elif chart_type_monthly == "Bar Chart":
            fig_monthly = px.bar(
                monthly_analysis, x='Month', y=['leads', 'enrolled'],
                title="Monthly Trend (Bar)", barmode='group', color_discrete_map={'leads': '#3498db', 'enrolled': '#2ecc71'}
            )
        else:
            fig_monthly = px.line(
                monthly_analysis, x='Month', y=['leads', 'enrolled'],
                title="Monthly Trend (Line)", color_discrete_map={'leads': '#3498db', 'enrolled': '#2ecc71'}, markers=True
            )
            
        fig_monthly.update_layout(height=400, hovermode="x unified")
        st.plotly_chart(fig_monthly, use_container_width=True)
        
    with ov_col2:
        # Interactive Sunburst Chart for Landscape view
        st.markdown("**🔍 Interactive Acquisition Landscape**")
        st.caption("Click on any slice to zoom in and explore the breakdown.")
        
        # Prepare data for Sunburst
        sunburst_df = filtered_df.copy()
        sunburst_df['Status'] = sunburst_df['Enrolled'].apply(lambda x: 'Enrolled' if x == 'Yes' else 'Dropped')
        
        # Sunburst Chart: City -> Channel -> Status
        fig_sunburst = px.sunburst(
            sunburst_df, 
            path=['City', 'Source_Channel', 'Status'], 
            title="City to Channel to Enrollment Flow",
            color='Status',
            color_discrete_map={'Enrolled': '#2ecc71', 'Dropped': '#e74c3c', '(?)': '#bdc3c7'}
        )
        fig_sunburst.update_layout(height=400, margin=dict(t=30, l=0, r=0, b=0))
        st.plotly_chart(fig_sunburst, use_container_width=True)

with tab_operations:
    st.subheader("Funnel & Flow Analysis")
    
    # Sankey Diagram
    drop_leads = total_leads - counselling_count
    drop_counselling = counselling_count - application_count
    drop_application = application_count - enrolled_count
    
    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 20,
          thickness = 25,
          line = dict(color = "black", width = 0.5),
          label = ["Leads", "Counselling", "Application", "Enrollment", "Dropped"],
          color = ["#3498db", "#f39c12", "#9b59b6", "#2ecc71", "#e74c3c"]
        ),
        link = dict(
          source = [0, 0, 1, 1, 2, 2],
          target = [1, 4, 2, 4, 3, 4],
          value =  [counselling_count, drop_leads, application_count, drop_counselling, enrolled_count, drop_application],
          color = ["rgba(52, 152, 219, 0.4)", "rgba(231, 76, 60, 0.4)", "rgba(243, 156, 18, 0.4)", "rgba(231, 76, 60, 0.4)", "rgba(155, 89, 182, 0.4)", "rgba(231, 76, 60, 0.4)"]
      ))])
    fig_sankey.update_layout(title_text="Detailed Student Journey (Sankey Flow)", font_size=12, height=450)
    st.plotly_chart(fig_sankey, use_container_width=True)

    st.markdown("---")
    # Lead Time Analysis
    st.subheader("Lead Time Analysis (Days between stages)")
    time_df = filtered_df[['Days_Lead_to_Counselling', 'Days_Counselling_to_App', 'Days_App_to_Enroll']].melt(var_name="Stage", value_name="Days").dropna()
    # Format labels
    time_df['Stage'] = time_df['Stage'].replace({
        'Days_Lead_to_Counselling': 'Lead -> Counselling',
        'Days_Counselling_to_App': 'Counselling -> Application',
        'Days_App_to_Enroll': 'Application -> Enrollment'
    })
    fig_time = px.box(time_df, x="Stage", y="Days", color="Stage", title="Distribution of Days Between Stages", 
                      color_discrete_map={'Lead -> Counselling': '#3498db', 'Counselling -> Application': '#f39c12', 'Application -> Enrollment': '#2ecc71'})
    st.plotly_chart(fig_time, use_container_width=True)

with tab_marketing:
    st.subheader("Marketing Performance")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        # Chart Customization Selector
        m_chart_type = st.selectbox(
            "📊 Channel Chart Type",
            options=["Bar Chart", "Stacked Bar", "Line Chart"],
            index=0,
            key="m_channel_type"
        )
        
        channel_analysis = filtered_df.groupby("Source_Channel").agg(
            leads=("Lead_ID", "count"),
            enrolled=("Enrolled", lambda x: (x == "Yes").sum())
        ).reset_index()
        channel_analysis[['leads', 'enrolled']] = channel_analysis[['leads', 'enrolled']].astype(int)
        
        if m_chart_type == "Bar Chart":
            fig_channel = px.bar(
                channel_analysis, x='Source_Channel', y=['leads', 'enrolled'],
                title="Lead vs Enrollment by Channel", barmode='group',
                color_discrete_map={'leads': '#3498db', 'enrolled': '#2ecc71'}
            )
        elif m_chart_type == "Stacked Bar":
            fig_channel = px.bar(
                channel_analysis, x='Source_Channel', y=['leads', 'enrolled'],
                title="Lead vs Enrollment by Channel (Stacked)", barmode='relative',
                color_discrete_map={'leads': '#3498db', 'enrolled': '#2ecc71'}
            )
        else:
            fig_channel = px.line(
                channel_analysis, x='Source_Channel', y=['leads', 'enrolled'],
                title="Lead vs Enrollment by Channel (Line)", markers=True,
                color_discrete_map={'leads': '#3498db', 'enrolled': '#2ecc71'}
            )
        st.plotly_chart(fig_channel, use_container_width=True)
        
    with m_col2:
        # Chart Customization Selector
        city_chart_type = st.selectbox(
            "📊 City Chart Type",
            options=["Pie Chart", "Donut Chart", "Horizontal Bar"],
            index=0,
            key="m_city_type"
        )
        
        city_analysis = filtered_df.groupby("City").agg(
            leads=("Lead_ID", "count"),
            enrolled=("Enrolled", lambda x: (x == "Yes").sum())
        ).reset_index()
        city_analysis[['leads', 'enrolled']] = city_analysis[['leads', 'enrolled']].astype(int)
        
        if city_chart_type == "Pie Chart":
            fig_city = px.pie(
                city_analysis, values='enrolled', names='City',
                title="Enrollment Distribution by City"
            )
        elif city_chart_type == "Donut Chart":
            fig_city = px.pie(
                city_analysis, values='enrolled', names='City',
                title="Enrollment Distribution by City", hole=0.5
            )
        else:
            fig_city = px.bar(
                city_analysis.sort_values('enrolled'), x='enrolled', y='City',
                title="Enrollment Count by City", orientation='h',
                color='enrolled', color_continuous_scale='Blues'
            )
            
        if "Pie" in city_chart_type:
            fig_city.update_traces(textposition='inside', textinfo='percent+label')
            
        st.plotly_chart(fig_city, use_container_width=True)

with tab_financials:
    st.subheader("Revenue & Financials")
    revenue_data = filtered_df_enrolled.groupby('Course').agg(
        enrollments=('Lead_ID', 'count'),
        total_revenue=('Fee', 'sum')
    ).reset_index()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Generated Revenue", f"₹{revenue_data['total_revenue'].sum():,}")
    c2.metric("Average Deal Size (Fee)", f"₹{revenue_data['total_revenue'].sum() // enrolled_count:,}" if enrolled_count > 0 else "₹0")
    c3.metric("Paid Enrollments", enrolled_count)

    st.markdown("<br>", unsafe_allow_html=True)

    # Chart Customization Selector
    rev_chart_type = st.selectbox(
        "📊 Revenue Chart Type",
        options=["Vertical Bar", "Horizontal Bar", "Pie Chart"],
        index=0,
        key="fin_rev_type"
    )

    if rev_chart_type == "Vertical Bar":
        fig_revenue = px.bar(
            revenue_data, x='Course', y='total_revenue',
            title="Revenue Contribution by Course", text='total_revenue', color='Course',
            color_discrete_map={'Data Science': '#3498db', 'Digital Marketing': '#2ecc71', 'Web Development': '#e74c3c'}
        )
        fig_revenue.update_traces(textposition='outside')
    elif rev_chart_type == "Horizontal Bar":
        fig_revenue = px.bar(
            revenue_data, x='total_revenue', y='Course',
            title="Revenue Contribution by Course (Horizontal)", text='total_revenue', color='Course',
            orientation='h',
            color_discrete_map={'Data Science': '#3498db', 'Digital Marketing': '#2ecc71', 'Web Development': '#e74c3c'}
        )
        fig_revenue.update_traces(textposition='outside')
    else:
        fig_revenue = px.pie(
            revenue_data, values='total_revenue', names='Course',
            title="Revenue Distribution by Course",
            color='Course',
            color_discrete_map={'Data Science': '#3498db', 'Digital Marketing': '#2ecc71', 'Web Development': '#e74c3c'}
        )
        fig_revenue.update_traces(textinfo='percent+label')
        
    st.plotly_chart(fig_revenue, use_container_width=True)

with tab_predictive:
    st.subheader("🤖 AI-Powered Lead Scoring")
    st.markdown("Predict the probability of a lead enrolling based on historical patterns using a trained Random Forest model.")
    
    # Train Model (Cached)
    @st.cache_resource
    def train_model(data):
        ml_df = data[['City', 'Source_Channel', 'Enrolled_Binary']].dropna()
        if len(ml_df) < 20:
            return None, None, None # Need more data
        
        le_city = LabelEncoder()
        le_channel = LabelEncoder()
        
        ml_df['City'] = le_city.fit_transform(ml_df['City'])
        ml_df['Source_Channel'] = le_channel.fit_transform(ml_df['Source_Channel'])
        
        X = ml_df[['City', 'Source_Channel']]
        y = ml_df['Enrolled_Binary']
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model, le_city, le_channel

    model, le_city, le_channel = train_model(df)
    
    if model:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Input Prospect Details")
            with st.form("predict_form"):
                pred_city = st.selectbox("Select Prospect City", options=le_city.classes_)
                pred_channel = st.selectbox("Select Source Channel", options=le_channel.classes_)
                submit = st.form_submit_button("Predict Probability", type="primary")
                
        with col2:
            if submit:
                c = le_city.transform([pred_city])[0]
                ch = le_channel.transform([pred_channel])[0]
                prob = model.predict_proba([[c, ch]])[0][1] # Probability of Class 1
                
                st.markdown("#### Prediction Result")
                if prob > 0.6:
                    st.success(f"🔥 **High Intent Lead**: {prob*100:.1f}% probability of enrollment.")
                elif prob > 0.3:
                    st.warning(f"⚡ **Warm Lead**: {prob*100:.1f}% probability of enrollment.")
                else:
                    st.error(f"❄️ **Cold Lead**: {prob*100:.1f}% probability of enrollment.")
                
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prob * 100,
                    title = {'text': "Enrollment Probability (%)"},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#2c3e50"},
                        'steps': [
                            {'range': [0, 30], 'color': "#e74c3c"},
                            {'range': [30, 70], 'color': "#f1c40f"},
                            {'range': [70, 100], 'color': "#2ecc71"}]
                    }
                ))
                fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True)
            else:
                st.info("👈 Fill out the details and click 'Predict Probability' to see the AI score.")
    else:
        st.info("Not enough data to train the predictive model.")

with tab_scenario:
    st.subheader("🔮 Scenario Planner")
    st.markdown("Adjust the sliders below to see how theoretical changes in conversion rates impact total enrollments and revenue.")
    
    sc1, sc2 = st.columns([1, 1])
    with sc1:
        st.markdown("#### Adjust Funnel Parameters")
        sim_counselling_rate = st.slider("Simulate Counselling Rate (%)", min_value=0.0, max_value=100.0, value=float(counselling_rate), step=1.0)
        sim_application_rate = st.slider("Simulate Application Rate (%)", min_value=0.0, max_value=100.0, value=float(application_rate), step=1.0)
        sim_enrollment_rate = st.slider("Simulate Enrollment Rate (%)", min_value=0.0, max_value=100.0, value=float(enrollment_rate), step=1.0)
        
    with sc2:
        st.markdown("#### Projected Outcomes")
        sim_counselling = total_leads * (sim_counselling_rate / 100)
        sim_applications = sim_counselling * (sim_application_rate / 100)
        sim_enrollments = sim_applications * (sim_enrollment_rate / 100)
        
        avg_fee = revenue_data['total_revenue'].sum() / enrolled_count if enrolled_count > 0 else 50000
        sim_revenue = sim_enrollments * avg_fee
        
        st.metric("Projected Enrollments", int(sim_enrollments), delta=f"{int(sim_enrollments - enrolled_count)} from current")
        st.metric("Projected Revenue", f"₹{sim_revenue:,.0f}", delta=f"₹{sim_revenue - revenue_data['total_revenue'].sum():,.0f} from current")
        
        st.caption(f"Based on total leads ({total_leads}) and average deal size (₹{avg_fee:,.0f}).")

st.markdown("---")
st.caption("🎓 Built with Streamlit, Plotly & Scikit-Learn | Advanced Analytics Dashboard")
