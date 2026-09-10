import streamlit as st
import pandas as pd
import plotly.express as px
import io # Wajib ditambahkan untuk membaca file dari memori web

st.set_page_config(page_title="Resume Gangguan", page_icon="📊", layout="wide")

# =========================================================
# 1. LOAD DATA (HYBRID: UPLOAD & GOOGLE SHEETS)
# =========================================================
@st.cache_data(ttl=60)
def fetch_google_sheets():
    sheet_url = "https://docs.google.com/spreadsheets/d/1T8WjaUJfeRxCuOJWDWtUtLBxiK7-tyvH/export?format=xlsx"
    # UBAH NAMA SHEET DI SINI MENJADI SHEET PEMELIHARAAN (misal: 'ENTRI HAR')
    return pd.read_excel(sheet_url, sheet_name='ENTRI HAR')

def load_data():
    if 'uploaded_excel' in st.session_state:
        excel_data = io.BytesIO(st.session_state['uploaded_excel'])
        # UBAH JUGA DI SINI
        df = pd.read_excel(excel_data, sheet_name='ENTRI HAR')
    else:
        df = fetch_google_sheets()
        
    # Pastikan nama kolom di bawah ini sesuai dengan yang ada di sheet ENTRI HAR
    # Hapus kode pembersihan TEMPORER/PERMANEN karena itu khusus Gangguan
    if 'KODE PENYULANG' in df.columns:
        df = df.dropna(subset=['KODE PENYULANG'])
        
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal menarik data! Error: {e}")
    st.stop()

# =========================================================
# 2. SUB-MENU DI POJOK KIRI ATAS
# =========================================================
sub_menu = st.radio(
    "Pilih Tampilan:",
    ["📊 Utama: Grafik & Logsheet", "🥧 Detail: Relay & Penyebab"],
    horizontal=True,
    label_visibility="collapsed"
)

st.title("GANGGUAN PENYULANG")

# =========================================================
# 3. AREA FILTER
# =========================================================
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
    list_penyulang = ["Semua"] + list(df['PENYULANG'].dropna().unique())
    filter_penyulang = st.selectbox("PENYULANG", list_penyulang)
with col_f2:
    list_tanggal = ["Semua"] + list(df['TANGGAL PADAM'].dropna().unique())
    filter_tanggal = st.selectbox("TANGGAL", list_tanggal)
with col_f3:
    list_ulp = ["Semua"] + list(df['ULP'].dropna().unique())
    filter_ulp = st.selectbox("ULP", list_ulp)
with col_f4:
    list_bulan = ["Semua"] + list(df['BULAN'].dropna().unique())
    filter_bulan = st.selectbox("BULAN", list_bulan)

df_filtered = df.copy()
if filter_penyulang != "Semua": df_filtered = df_filtered[df_filtered['PENYULANG'] == filter_penyulang]
if filter_tanggal != "Semua": df_filtered = df_filtered[df_filtered['TANGGAL PADAM'] == filter_tanggal]
if filter_ulp != "Semua": df_filtered = df_filtered[df_filtered['ULP'] == filter_ulp]
if filter_bulan != "Semua": df_filtered = df_filtered[df_filtered['BULAN'] == filter_bulan]

st.markdown("---")

# =========================================================
# 4. KONTEN HALAMAN BERDASARKAN SUB-MENU
# =========================================================
if sub_menu == "📊 Utama: Grafik & Logsheet":
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
    st.dataframe(df_filtered[kolom_tabel], use_container_width=True)

elif sub_menu == "🥧 Detail: Relay & Penyebab":
    st.info("💡 Klik langsung pada **WARNA POTONGAN BULATAN** untuk memfilter tabel.")
    
    col_pie1, col_pie2 = st.columns(2)
    clicked_relay = None
    clicked_penyebab = None

    with col_pie1:
        st.subheader("RELAY YANG BEKERJA")
        relay_counts = df_filtered['RELAY YANG BEKERJA'].value_counts().reset_index()
        relay_counts.columns = ['RELAY', 'JUMLAH']
        fig_relay = px.pie(relay_counts, values='JUMLAH', names='RELAY', hole=0.4,
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        event_relay = st.plotly_chart(fig_relay, use_container_width=True, on_select="rerun", selection_mode="points", key="pie_relay")
        if event_relay and len(event_relay.selection.points) > 0:
            clicked_relay = event_relay.selection.points[0].get("label")

    with col_pie2:
        st.subheader("PENYEBAB GANGGUAN")
        penyebab_counts = df_filtered['PENYEBAB'].value_counts().reset_index()
        penyebab_counts.columns = ['PENYEBAB', 'JUMLAH']
        fig_penyebab = px.pie(penyebab_counts, values='JUMLAH', names='PENYEBAB', hole=0.4,
                              color_discrete_sequence=px.colors.qualitative.Set2)
        event_penyebab = st.plotly_chart(fig_penyebab, use_container_width=True, on_select="rerun", selection_mode="points", key="pie_penyebab")
        if event_penyebab and len(event_penyebab.selection.points) > 0:
            clicked_penyebab = event_penyebab.selection.points[0].get("label")

    df_detail = df_filtered.copy()
    if clicked_relay:
        st.success(f"✅ Filter Aktif - Relay: **{clicked_relay}**")
        df_detail = df_detail[df_detail['RELAY YANG BEKERJA'] == clicked_relay]
    if clicked_penyebab:
        st.success(f"✅ Filter Aktif - Penyebab: **{clicked_penyebab}**")
        df_detail = df_detail[df_detail['PENYEBAB'] == clicked_penyebab]

    st.markdown("---")
    st.subheader("DATA TERKAIT (Tabel Otomatis Terfilter)")
    kolom_tabel_detail = ['TANGGAL PADAM', 'PENYULANG', 'ULP', 'PENYEBAB', 'RELAY YANG BEKERJA']
    
    if len(df_detail) == 0:
        st.warning("⚠️ Tidak ada data untuk filter tersebut.")
    else:
        st.dataframe(df_detail[kolom_tabel_detail], use_container_width=True)