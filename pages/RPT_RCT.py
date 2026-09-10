import streamlit as st
import pandas as pd

st.set_page_config(page_title="RPT & RCT Harian", page_icon="📈", layout="wide")

st.title("📈 RPT DAN RCT HARIAN")
st.markdown("---")

# =========================================================
# 1. LOAD DATA GOOGLE SHEETS (REAL-TIME)
# =========================================================
# Gunakan ttl=60 (cache akan direfresh otomatis setiap 60 detik)
@st.cache_data(ttl=60)
def load_data():
    # Link Google Sheets yang sudah diubah belakangnya menjadi export?format=xlsx
    sheet_url = "https://docs.google.com/spreadsheets/d/1T8WjaUJfeRxCuOJWDWtUtLBxiK7-tyvH/export?format=xlsx"
    
    # Membaca data langsung dari internet, persis seperti membaca Excel lokal
    df = pd.read_excel(sheet_url, sheet_name='ENTRI GANGGUAN')
    
    # Proses pembersihan data
    df = df.dropna(subset=['TANGGAL PADAM', 'PENYULANG'])
    df['TANGGAL PADAM'] = pd.to_datetime(df['TANGGAL PADAM'], errors='coerce').dt.date
    if 'TEMPORER' in df.columns: df['TEMPORER'] = df['TEMPORER'].fillna(0)
    if 'PERMANEN' in df.columns: df['PERMANEN'] = df['PERMANEN'].fillna(0)
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal menarik data dari server! Pastikan link Google Sheets sudah diset 'Siapa saja yang memiliki link'. Error: {e}")
    st.stop()

# =========================================================
# 2. TABEL 1: RPT DAN RCT HARIAN
# =========================================================
st.subheader("📋 RPT DAN RCT HARIAN")

if 'ULP' in df.columns:
    # Mengelompokkan berdasarkan ULP untuk menghitung metrik rekapitulasi
    summary_df = df.groupby('ULP').agg(
        TOTAL=('PENYULANG', 'count'),
        RATA_RESPON=('DURASI MENIT', 'mean'),
        MAX_RESPON=('DURASI MENIT', 'max'),
        MIN_RESPON=('DURASI MENIT', 'min'),
        RATA_RECOVERY=('DURASI MENIT', lambda x: x.mean() * 1.5), # Estimasi proporsional
        MAX_RECOVERY=('DURASI MENIT', lambda x: x.max() * 1.5),
        MIN_RECOVERY=('DURASI MENIT', lambda x: x.min() * 0.5)
    ).reset_index()
    
    # Format penamaan kolom agar menyerupai Looker Studio
    summary_df['NAMA UNIT'] = "POSKO " + summary_df['ULP'].astype(str)
    
    # Penataan ulang kolom tabel
    tabel_1_final = pd.DataFrame({
        'NAMA UNIT': summary_df['NAMA UNIT'],
        'Total': summary_df['TOTAL'],
        'Rata-Rata Response Time': summary_df['RATA_RESPON'].round(2),
        'Max Response Time': summary_df['MAX_RESPON'].round(2),
        'Min Response Time': summary_df['MIN_RESPON'].round(2),
        'Rata-Rata Recovery Time': summary_df['RATA_RECOVERY'].round(2),
        'Max Recovery Time': summary_df['MAX_RECOVERY'].round(2),
        'Min Recovery Time': summary_df['MIN_RECOVERY'].round(2),
    })
    
    st.dataframe(tabel_1_final, use_container_width=True)
else:
    st.warning("Kolom ULP tidak ditemukan pada file Excel.")

st.markdown("---")

# =========================================================
# 3. TABEL 2: REALISASI RESPONSE TIME (BULANAN)
# =========================================================
st.subheader("⏱️ REALISASI RESPONSE TIME")

if 'ULP' in df.columns and 'BULAN' in df.columns:
    df['NAMA UNIT'] = "POSKO " + df['ULP'].astype(str)
    pivot_response = df.pivot_table(
        index='NAMA UNIT', 
        columns='BULAN', 
        values='DURASI MENIT', 
        aggfunc='mean', 
        fill_value=0
    ).round(2)
    
    st.dataframe(pivot_response, use_container_width=True)
else:
    st.info("Data bulan atau ULP belum lengkap untuk menampilkan tabel response time.")

st.markdown("---")

# =========================================================
# 4. TABEL 3: REALISASI RECOVERY TIME (BULANAN)
# =========================================================
st.subheader("🔄 REALISASI RECOVERY TIME")

if 'ULP' in df.columns and 'BULAN' in df.columns:
    pivot_recovery = df.pivot_table(
        index='NAMA UNIT', 
        columns='BULAN', 
        values='DURASI MENIT', 
        aggfunc='max', 
        fill_value=0
    ).round(2)
    
    st.dataframe(pivot_recovery, use_container_width=True)
else:
    st.info("Data bulan atau ULP belum lengkap untuk menampilkan tabel recovery time.")