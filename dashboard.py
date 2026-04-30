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
    return day_df, hour_df

day_df, hour_df = load_data()

# Header
st.title("🚲 Bike Sharing Analysis Dashboard")

# Sidebar Filter
st.sidebar.header("Filter Data")
start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu",
    [day_df["dteday"].min(), day_df["dteday"].max()],
    min_value=day_df["dteday"].min(),
    max_value=day_df["dteday"].max()
)

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                 (day_df["dteday"] <= str(end_date))]

# Baris 1: Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", value=f"{main_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Registered", value=f"{main_df['registered'].mean():.0f}")
with col3:
    st.metric("Rata-rata Casual", value=f"{main_df['casual'].mean():.0f}")

st.divider()

# Baris 2: Visualisasi Utama (Pertanyaan Bisnis)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Penyewaan: Musim Panas vs Musim Dingin")
    fig1, ax1 = plt.subplots()
    season_data = main_df[main_df['season'].isin([2, 4])]
    sns.barplot(x='season', y='cnt', data=season_data, palette='coolwarm', ax=ax1)
    ax1.set_xticklabels(['Summer', 'Winter'])
    st.pyplot(fig1)

with col_right:
    st.subheader("Pola Jam Sibuk (Hari Kerja)")
    fig2, ax2 = plt.subplots()
    workday_data = hour_df[hour_df['workingday'] == 1].groupby('hr')['registered'].mean()
    ax2.plot(workday_data.index, workday_data.values, marker='o', color='#2E7D32')
    ax2.set_xticks(range(0, 24, 2))
    st.pyplot(fig2)

st.divider()

# Baris 3: Analisis Lanjutan (RFM)
st.subheader("Analisis Lanjutan: RFM Analysis (By Month)")
rfm_df = main_df.groupby("mnth").agg({
    "dteday": "max",
    "instant": "count",
    "cnt": "sum"
}).reset_index()
rfm_df.columns = ["month", "max_date", "frequency", "monetary"]
recent_date = main_df["dteday"].max()
rfm_df["recency"] = rfm_df["max_date"].apply(lambda x: (recent_date - x).days)

col_r, col_f, col_m = st.columns(3)

with col_r:
    fig_r, ax_r = plt.subplots()
    sns.barplot(y="recency", x="month", data=rfm_df.sort_values(by="recency", ascending=True).head(5), color="#72BCD4", ax=ax_r)
    ax_r.set_title("Recency (Days)")
    st.pyplot(fig_r)

with col_f:
    fig_f, ax_f = plt.subplots()
    sns.barplot(y="frequency", x="month", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), color="#72BCD4", ax=ax_f)
    ax_f.set_title("Frequency")
    st.pyplot(fig_f)

with col_m:
    fig_m, ax_m = plt.subplots()
    sns.barplot(y="monetary", x="month", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), color="#72BCD4", ax=ax_m)
    ax_m.set_title("Monetary (Total Rental)")
    st.pyplot(fig_m)

st.caption("Copyright © Galih 2026 - Data Analyst Project")