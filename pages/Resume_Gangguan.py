import streamlit as st
import pandas as pd
import plotly.express as px
import io
import datetime
import requests

st.set_page_config(page_title="Resume Gangguan", page_icon="📊", layout="wide")

# =========================================================
# 1. LOAD DATA GOOGLE SHEETS (LINK BARU)
# =========================================================
@st.cache_data(ttl=60)
def fetch_google_sheets():
    # LINK BARU YANG SUDAH DIUBAH FORMAT EXPORT-NYA
    sheet_url = "https://docs.google.com/spreadsheets/d/1OtEMnkxNkh0KfsxhywreqozLGPZmhCt5ynBi-UlzYHM/export?format=xlsx"
    return pd.read_excel(sheet_url, sheet_name='ENTRI GANGGUAN')

def load_data():
    df = fetch_google_sheets()
    df.columns = df.columns.str.strip().str.upper()
    
    if 'TANGGAL PADAM' in df.columns and 'PENYULANG' in df.columns:
        df = df.dropna(subset=['TANGGAL PADAM', 'PENYULANG'])
        df['TANGGAL PADAM'] = pd.to_datetime(df['TANGGAL PADAM'], errors='coerce').dt.date
        
    if 'TEMPORER' in df.columns: df['TEMPORER'] = df['TEMPORER'].fillna(0)
    if 'PERMANEN' in df.columns: df['PERMANEN'] = df['PERMANEN'].fillna(0)
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal menarik data! Pastikan file Sheets sudah diset 'Siapa saja memiliki link'. Error: {e}")
    st.stop()

# =========================================================
# 2. SUB-MENU DI POJOK KIRI ATAS
# =========================================================
sub_menu = st.radio(
    "Pilih Tampilan:",
    ["📊 Utama: Grafik & Logsheet", "🥧 Detail: Relay & Penyebab", "📝 Input Gangguan Baru"],
    horizontal=True,
    label_visibility="collapsed"
)

st.title("GANGGUAN PENYULANG")
st.markdown("---")

# =========================================================
# 3. KONTEN HALAMAN BERDASARKAN SUB-MENU
# =========================================================

# ---> MENU 1: GRAFIK & TABEL UTAMA <---
if sub_menu == "📊 Utama: Grafik & Logsheet":
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1: filter_penyulang = st.selectbox("PENYULANG", ["Semua"] + list(df['PENYULANG'].dropna().unique()))
    with col_f2: filter_tanggal = st.selectbox("TANGGAL", ["Semua"] + list(df['TANGGAL PADAM'].dropna().unique()))
    with col_f3: filter_ulp = st.selectbox("ULP", ["Semua"] + list(df['ULP'].dropna().unique()))
    with col_f4: filter_bulan = st.selectbox("BULAN", ["Semua"] + list(df['BULAN'].dropna().unique()))

    df_filtered = df.copy()
    if filter_penyulang != "Semua": df_filtered = df_filtered[df_filtered['PENYULANG'] == filter_penyulang]
    if filter_tanggal != "Semua": df_filtered = df_filtered[df_filtered['TANGGAL PADAM'] == filter_tanggal]
    if filter_ulp != "Semua": df_filtered = df_filtered[df_filtered['ULP'] == filter_ulp]
    if filter_bulan != "Semua": df_filtered = df_filtered[df_filtered['BULAN'] == filter_bulan]
    
    st.markdown("---")
    st.subheader("Grafik Total Gangguan per Penyulang")
    bar_data = df_filtered.groupby('PENYULANG')[['TEMPORER', 'PERMANEN']].sum().reset_index()
    bar_data_melted = bar_data.melt(id_vars='PENYULANG', value_vars=['TEMPORER', 'PERMANEN'], 
                                    var_name='JENIS', value_name='JUMLAH')
    fig_bar = px.bar(bar_data_melted, x='PENYULANG', y='JUMLAH', color='JENIS',
                     barmode='group', text_auto=True,
                     color_discrete_map={'TEMPORER': '#2ca02c', 'PERMANEN': '#1f77b4'})
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.subheader("LOGSHEET DATA")
    kolom_tabel = ['TANGGAL PADAM', 'PENYULANG', 'NAMA SECTION', 'ULP', 'PENYEBAB', 'RELAY YANG BEKERJA', 'R', 'S', 'T', 'N']
    kolom_tersedia = [k for k in kolom_tabel if k in df_filtered.columns]
    st.dataframe(df_filtered[kolom_tersedia], use_container_width=True)

# ---> MENU 2: DETAIL PIE CHART <---
elif sub_menu == "🥧 Detail: Relay & Penyebab":
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1: filter_penyulang = st.selectbox("PENYULANG", ["Semua"] + list(df['PENYULANG'].dropna().unique()))
    with col_f2: filter_tanggal = st.selectbox("TANGGAL", ["Semua"] + list(df['TANGGAL PADAM'].dropna().unique()))
    with col_f3: filter_ulp = st.selectbox("ULP", ["Semua"] + list(df['ULP'].dropna().unique()))
    with col_f4: filter_bulan = st.selectbox("BULAN", ["Semua"] + list(df['BULAN'].dropna().unique()))

    df_filtered = df.copy()
    if filter_penyulang != "Semua": df_filtered = df_filtered[df_filtered['PENYULANG'] == filter_penyulang]
    if filter_tanggal != "Semua": df_filtered = df_filtered[df_filtered['TANGGAL PADAM'] == filter_tanggal]
    if filter_ulp != "Semua": df_filtered = df_filtered[df_filtered['ULP'] == filter_ulp]
    if filter_bulan != "Semua": df_filtered = df_filtered[df_filtered['BULAN'] == filter_bulan]

    st.markdown("---")
    col_pie1, col_pie2 = st.columns(2)
    with col_pie1:
        st.subheader("RELAY YANG BEKERJA")
        relay_counts = df_filtered['RELAY YANG BEKERJA'].value_counts().reset_index()
        relay_counts.columns = ['RELAY', 'JUMLAH']
        fig_relay = px.pie(relay_counts, values='JUMLAH', names='RELAY', hole=0.4,
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_relay, use_container_width=True)

    with col_pie2:
        st.subheader("PENYEBAB GANGGUAN")
        penyebab_counts = df_filtered['PENYEBAB'].value_counts().reset_index()
        penyebab_counts.columns = ['PENYEBAB', 'JUMLAH']
        fig_penyebab = px.pie(penyebab_counts, values='JUMLAH', names='PENYEBAB', hole=0.4,
                              color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_penyebab, use_container_width=True)

# ---> MENU 3: INPUT DATA BARU <---
elif sub_menu == "📝 Input Gangguan Baru":
    st.subheader("Form Entri Data Gangguan (Real-time)")
    
    with st.form("form_entri_gangguan", clear_on_submit=True):
        st.markdown("##### 📍 Data Lokasi & Jaringan")
        col1, col2, col3 = st.columns(3)
        with col1:
            penyulang = st.text_input("Penyulang")
            nama = st.text_input("Nama")
            ulp = st.selectbox("ULP", ["PADANGSIDIMPUAN", "SIBUHUAN", "KOTANOPAN", "PANYABUNGAN", "SIPIROK"])
        with col2:
            section = st.text_input("Section")
            nama_section = st.text_input("Nama Section")
        with col3:
            titik_koordinat = st.text_input("Titik Koordinat")
            cuaca = st.text_input("Cuaca")

        st.markdown("##### 🕒 Detail Waktu")
        col_w1, col_w2, col_w3, col_w4 = st.columns(4)
        with col_w1:
            bulan = st.selectbox("Bulan", ["JANUARI", "FEBRUARI", "MARET", "APRIL", "MEI", "JUNI", "JULI", "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOVEMBER", "DESEMBER"])
            tanggal_padam = st.date_input("Tanggal Padam")
        with col_w2:
            jam_padam = st.time_input("Jam Padam")
            tanggal_nyala = st.date_input("Tanggal Nyala")
        with col_w3:
            jam_nyala = st.time_input("Jam Nyala")
            durasi_jam = st.number_input("Durasi Jam", min_value=0.0, step=0.1)
        with col_w4:
            durasi_menit = st.number_input("Durasi Menit", min_value=0)

        st.markdown("##### ⚙️ Detail Teknis & Gangguan")
        col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        with col_t1:
            penyebab = st.text_input("Penyebab")
            relay = st.selectbox("Relay Yang Bekerja", ["OCR", "GFR", "OCR & GFR", "TIDAK ADA"])
        with col_t2:
            temporer = st.number_input("Temporer (Kali)", min_value=0)
            permanen = st.number_input("Permanen (Kali)", min_value=0)
        with col_t3:
            arus_tertinggi = st.number_input("Arus Tertinggi (A)", min_value=0.0)
            ens = st.number_input("ENS (kWh)", min_value=0.0)
        with col_t4:
            st.markdown("**Arus Fasa (A)**")
            col_r, col_s = st.columns(2)
            col_t_fasa, col_n = st.columns(2)
            with col_r: r = st.number_input("R", min_value=0.0)
            with col_s: s = st.number_input("S", min_value=0.0)
            with col_t_fasa: t = st.number_input("T", min_value=0.0)
            with col_n: n = st.number_input("N", min_value=0.0)

        st.markdown("---")
        submit_button = st.form_submit_button("💾 Simpan Data Baru", use_container_width=True)

        if submit_button:
            if penyulang == "":
                st.error("⚠️ Penyulang wajib diisi!")
            else:
                with st.spinner("Memproses data ke Google Sheets..."):
                    # >>> WEBHOOK URL MILIKMU SUDAH AKTIF DI SINI <<<
                    webhook_url = "https://script.google.com/macros/s/AKfycbxvbw68N92VTdSZP4xUT6HnWNvcvYdrYR4vNhUSndaGwyDk-VbVRQSFp0-6bajsWst3/exec" 
                    
                    payload = {
                        "penyulang": penyulang, "nama": nama, "section": section, "nama_section": nama_section,
                        "ulp": ulp, "penyebab": penyebab, "relay": relay, "bulan": bulan,
                        "tanggal_padam": str(tanggal_padam), "jam_padam": str(jam_padam),
                        "tanggal_nyala": str(tanggal_nyala), "jam_nyala": str(jam_nyala),
                        "durasi_jam": durasi_jam, "durasi_menit": durasi_menit,
                        "temporer": temporer, "permanen": permanen, "cuaca": cuaca,
                        "arus_tertinggi": arus_tertinggi, "ens": ens,
                        "r": r, "s": s, "t": t, "n": n, "titik_koordinat": titik_koordinat
                    }
                    try:
                        response = requests.post(webhook_url, json=payload)
                        if response.status_code == 200:
                            st.success(f"✅ Hore! Data {penyulang} sukses masuk ke Google Sheets! Refresh web untuk melihat hasilnya.")
                        else:
                            st.error(f"❌ Gagal mengirim data: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Terjadi kesalahan jaringan: {e}")