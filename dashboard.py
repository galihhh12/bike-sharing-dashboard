import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page title
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Cleaning
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    day_df['season'] = day_df['season'].map(season_mapping)
    
    weather_mapping = {1: 'Clear/Cloudy', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain'}
    day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# --- Sidebar ---
with st.sidebar:
    st.title("Proyek Analisis Data")
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.write("**Nama:** Galih Fathurahman Ardiansyah")
    
    # Date Filter - Menentukan rentang bulan yang tersedia
    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()
    
    # User dapat memilih rentang bulan/tanggal secara fleksibel
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu (Bulan/Tahun)',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Dataframes berdasarkan input
main_day_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]
main_hour_df = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & (hour_df['dteday'] <= pd.to_datetime(end_date))]

# --- Main Header ---
st.title('Bike Sharing Dashboard 🚲')

# Row 1: Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rentals", value=f"{main_day_df['cnt'].sum():,}")
with col2:
    st.metric("Registered Users", value=f"{main_day_df['registered'].sum():,}")
with col3:
    st.metric("Casual Users", value=f"{main_day_df['casual'].sum():,}")

# Row 2: Pertanyaan 1 (Peak Hours)
st.subheader('Pola Pengguna Registered pada Jam Sibuk (Hari Kerja)')
workingday_df = main_hour_df[main_hour_df['workingday'] == 1]
if not workingday_df.empty:
    peak_data = workingday_df.groupby('hr')['registered'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=peak_data, x='hr', y='registered', marker='o', color='#2b7bba', ax=ax)
    ax.set_xticks(range(0, 24))
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data hari kerja pada rentang waktu yang dipilih.")

# Row 3: Pertanyaan 2 (Holidays & Weather)
st.subheader('Penyewaan pada Hari Libur & Pengaruh Cuaca')
col_a, col_b = st.columns(2)

with col_a:
    holiday_data = main_day_df[main_day_df['holiday'] == 1]
    if not holiday_data.empty:
        holiday_yearly = holiday_data.groupby(holiday_data['dteday'].dt.year)['cnt'].sum().reset_index()
        holiday_yearly.columns = ['Year', 'Total']
        fig2, ax2 = plt.subplots()
        sns.barplot(data=holiday_yearly, x='Year', y='Total', color='#2b7bba', ax=ax2)
        st.pyplot(fig2)
    else:
        st.info("Tidak ada hari libur pada periode ini.")

with col_b:
    weather_impact = main_day_df.groupby('weathersit')['cnt'].mean().reset_index()
    fig3, ax3 = plt.subplots()
    sns.barplot(data=weather_impact, x='weathersit', y='cnt', color='#2b7bba', ax=ax3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)

st.caption('Copyright (c) Galih Fathurahman 2024')