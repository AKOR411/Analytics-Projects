import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Settings & Setup
st.set_page_config(page_title="Clinic Executive Dashboard", layout="wide")

# 2. Data Loading & Quick-Cleaning Function
@st.cache_data
def load_and_clean_data():
    # Smart Fallback check to find the file whether it's in the root or folder
    if os.path.exists('healthcare-dashboard/KaggleV2-May-2016.csv'):
        file_path = 'healthcare-dashboard/KaggleV2-May-2016.csv'
    elif os.path.exists('KaggleV2-May-2016.csv'):
        file_path = 'KaggleV2-May-2016.csv'
    else:
        raise FileNotFoundError("Could not find KaggleV2-May-2016.csv in root or folder path.")
        
    df = pd.read_csv(file_path)
    
    # Standardize Column Names
    df.rename(columns={
        'PatientId': 'patient_id', 'AppointmentID': 'appointment_id', 'Gender': 'gender',
        'ScheduledDay': 'scheduled_day', 'AppointmentDay': 'appointment_day', 'Age': 'age',
        'Neighbourhood': 'neighborhood', 'Scholarship': 'scholarship', 'Hipertension': 'hypertension',
        'Diabetes': 'diabetes', 'Alcoholism': 'alcoholism', 'Handcap': 'handicap',
        'SMS_received': 'sms_received', 'No-show': 'no_show'
    }, inplace=True)
    
    # Clean Anomalies & Dates
    df = df[df['age'] >= 0]
    df['scheduled_day'] = pd.to_datetime(df['scheduled_day'])
    df['appointment_day'] = pd.to_datetime(df['appointment_day'])
    df = df[df['appointment_day'].dt.normalize() >= df['scheduled_day'].dt.normalize()]
    
    # Engineer Lead Time Metric & Target Mapping
    df['lead_time'] = (df['appointment_day'].dt.normalize() - df['scheduled_day'].dt.normalize()).dt.days
    df['no_show_numeric'] = df['no_show'].map({'Yes': 1, 'No': 0})
    
    return df

df = load_and_clean_data()

# 3. INTERACTIVE SIDEBAR FILTERS
st.sidebar.header("📊 Filter Command Panel")

# Filter 1: Gender Dropdown
gender_options = ['All'] + list(df['gender'].unique())
selected_gender = st.sidebar.selectbox("Select Patient Gender:", gender_options)

# Filter 2: Age Slider
min_age, max_age = int(df['age'].min()), int(df['age'].max())
selected_age_range = st.sidebar.slider("Select Patient Age Range:", min_age, max_age, (min_age, max_age))

# Apply Filters Dynamically to Dataset
filtered_df = df[(df['age'] >= selected_age_range[0]) & (df['age'] <= selected_age_range[1])]
if selected_gender != 'All':
    filtered_df = filtered_df[filtered_df['gender'] == selected_gender]

# 4. APP HEADER & THE DYNAMIC KPI CARDS
st.title("🏥 Clinic Executive Performance Command Center")
st.markdown("---")

total_appts = len(filtered_df)
total_missed = filtered_df['no_show_numeric'].sum()
missed_rate = (total_missed / total_appts * 100) if total_appts > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Filtered Appointments", value=f"{total_appts:,}")
with col2:
    st.metric(label="Total Patient No-Shows", value=f"{total_missed:,}")
with col3:
    st.metric(label="Live Attendance No-Show Rate", value=f"{missed_rate:.2f}%")

st.markdown("---")

# 5. DYNAMIC INTERACTIVE PLOTLY CHART
st.subheader("⏳ The Impact of Wait Times on Attendance Metrics")

# Group data by lead time for our interactive line plot
lead_time_df = filtered_df.groupby('lead_time')['no_show_numeric'].agg(['count', 'mean']).reset_index()
lead_time_df['no_show_pct'] = lead_time_df['mean'] * 100
# Filter down to the first 45 days of wait times for cleaner visualization
lead_time_df = lead_time_df[lead_time_df['lead_time'] <= 45]

fig = px.line(
    lead_time_df, 
    x='lead_time', 
    y='no_show_pct',
    labels={'lead_time': 'Wait Time Lag (Days between Booking & Visit)', 'no_show_pct': 'No-Show Rate (%)'},
    title="Real-Time Probability Line of Missed Medical Appointments by Booking Distance",
    markers=True,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)
