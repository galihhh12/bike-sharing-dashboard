---
```markdown
# Bike Sharing Data Analysis Dashboard 🚲

## Deskripsi
Projek ini adalah bagian dari tugas akhir analisis data untuk mengeksplorasi pola penyewaan sepeda pada dataset "Bike Sharing". Dashboard ini dibuat menggunakan Streamlit untuk memvisualisasikan pengaruh musim, pola waktu (jam sibuk), dan analisis lanjutan menggunakan teknik RFM (Recency, Frequency, Monetary).

## Struktur Data
- `day.csv`: Dataset penyewaan sepeda harian.
- `hour.csv`: Dataset penyewaan sepeda per jam.

## Fitur Dashboard
- **Metrik Utama**: Menampilkan total penyewaan, rata-rata pengguna terdaftar, dan pengguna kasual.
- **Analisis Musim**: Perbandingan performa penyewaan di musim panas vs musim dingin.
- **Pola Jam Sibuk**: Visualisasi tren penggunaan sepeda oleh pengguna terdaftar pada hari kerja.
- **Analisis RFM**: Analisis lanjutan untuk melihat loyalitas dan frekuensi penggunaan berdasarkan bulan.

## Cara Menjalankan di Local

### 1. Persiapan Lingkungan (Environment)
Pastikan Anda sudah menginstal Python di komputer Anda. Disarankan untuk menggunakan virtual environment.

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
streamlit run dashboard.py
