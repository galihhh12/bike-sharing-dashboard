import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set page title
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Menambahkan label cuaca untuk visualisasi yang lebih intuitif
    weather_mapping = {1: 'Clear', 2: 'Misty', 3: 'Light Snow/Rain', 4: 'Severe'}
    day_df['weather_label'] = day_df['weathersit'].map(weather_mapping)
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Header
st.title("🚲 Bike Sharing Analysis Dashboard")

# --- SIDEBAR FILTER (GLOBAL) ---
st.sidebar.header("Filter Data")
try:
    start_date, end_date = st.sidebar.date_input(
        "Rentang Waktu",
        [day_df["dteday"].min(), day_df["dteday"].max()],
        min_value=day_df["dteday"].min(),
        max_value=day_df["dteday"].max()
    )
except ValueError:
    st.error("Mohon pilih rentang waktu yang valid.")
    st.stop()

# --- SINKRONISASI FILTER KE SEMUA DATAFRAME ---
# Filter ini akan mempengaruhi main_day dan main_hour secara konsisten
main_day_df = day_df[(day_df["dteday"] >= pd.to_datetime(start_date)) & 
                     (day_df["dteday"] <= pd.to_datetime(end_date))]

main_hour_df = hour_df[(hour_df["dteday"] >= pd.to_datetime(start_date)) & 
                       (hour_df["dteday"] <= pd.to_datetime(end_date))]

# Baris 1: Metrics (Terhubung ke Filter)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_day_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Registered", value=f"{main_day_df['registered'].mean():.0f}")
with col3:
    st.metric("Rata-rata Casual", value=f"{main_day_df['casual'].mean():.0f}")

st.divider()

# Baris 2: Visualisasi Utama (Pertanyaan Bisnis)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Pengaruh Kondisi Cuaca")
    fig1, ax1 = plt.subplots()
    # Menggunakan main_day_df agar sinkron dengan filter
    sns.barplot(x='weather_label', y='cnt', data=main_day_df, palette='Blues_r', ax=ax1)
    ax1.set_xlabel("Kondisi Cuaca")
    ax1.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig1)

with col_right:
    st.subheader("Pola Jam Sibuk (Hari Kerja)")
    fig2, ax2 = plt.subplots()
    # SEKARANG MENGGUNAKAN main_hour_df (Sudah Sinkron dengan Filter Tanggal)
    workday_data = main_hour_df[main_hour_df['workingday'] == 1].groupby('hr')['cnt'].mean()
    ax2.plot(workday_data.index, workday_data.values, marker='o', color='#3274A1')
    ax2.set_xticks(range(0, 24, 2))
    ax2.set_xlabel("Jam (0-23)")
    ax2.set_ylabel("Rata-rata Penyewaan")
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

st.divider()

# --- BARIS 3: ANALISIS LANJUTAN (CLUSTERING MANUAL) ---
st.subheader("Analisis Lanjutan: Manual Grouping & Binning")

# Helper function untuk grouping waktu
def get_time_group(hour):
    if 5 <= hour < 12: return 'Pagi'
    elif 12 <= hour < 17: return 'Siang'
    elif 17 <= hour < 21: return 'Sore'
    else: return 'Malam'

main_hour_df['time_group'] = main_hour_df['hr'].apply(get_time_group)
# Binning kelembaban
main_hour_df['humidity_bin'] = pd.cut(main_hour_df['hum'], bins=[0, 0.3, 0.6, 1], labels=['Kering', 'Ideal', 'Lembab'])

col_group, col_bin = st.columns(2)

with col_group:
    st.write("**Manual Grouping: Penyewaan Berdasarkan Waktu**")
    fig_g, ax_g = plt.subplots()
    time_data = main_hour_df.groupby('time_group')['cnt'].mean().reindex(['Pagi', 'Siang', 'Sore', 'Malam'])
    time_data.plot(kind='bar', color='#3274A1', ax=ax_g)
    plt.xticks(rotation=0)
    st.pyplot(fig_g)

with col_bin:
    st.write("**Binning: Penyewaan Berdasarkan Kelembaban**")
    fig_b, ax_b = plt.subplots()
    hum_data = main_hour_df.groupby('humidity_bin')['cnt'].mean()
    hum_data.plot(kind='bar', color='#3274A1', ax=ax_b)
    plt.xticks(rotation=0)
    st.pyplot(fig_b)

st.caption("Copyright © Galih 2026 - Data Analyst Project (Revision Applied)")