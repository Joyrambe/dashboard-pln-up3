import streamlit as st

st.set_page_config(page_title="DASHBOARD PLN UP3", page_icon="⚡", layout="wide")

# =========================================================
# 1. CSS SAKTI UNTUK MENYULAP TOMBOL MENJADI KOTAK (CARD)
# =========================================================
st.markdown("""
<style>
    /* Menyembunyikan styling tombol bawaan dan mengubahnya jadi kotak */
    div.stButton > button {
        height: 180px;
        width: 100%;
        border-radius: 15px;
        border: 1px solid #333;
        background-color: #1E1E2F;
        color: white;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 15px;
    }
    
    /* Efek menyala saat kursor diarahkan ke kotak (Hover) */
    div.stButton > button:hover {
        border-color: #00BFA5;
        background-color: #2A2A3D;
        transform: translateY(-5px);
        box-shadow: 0px 10px 20px rgba(0, 191, 165, 0.2);
        color: #00BFA5;
    }
    
    /* Mengatur teks agar bisa lebih dari 1 baris dan rapi */
    div.stButton > button p {
        font-size: 15px;
        margin: 0;
        white-space: pre-wrap; 
        text-align: center;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2. HEADER HALAMAN UTAMA
# =========================================================
st.markdown("<h1 style='text-align: center; color: #00BFA5;'>⚡ DASHBOARD PLN UP3</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a1a1aa;'>Pusat Kendali & Analisis Terpadu | Padangsidimpuan</p>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# =========================================================
# 3. KOTAK MENU YANG BISA DIKLIK (BARIS 1)
# =========================================================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊\nRESUME GANGGUAN\n\nData logsheet, grafik, dan analisis penyebab.", use_container_width=True):
        st.switch_page("pages/Resume_Gangguan.py")

with col2:
    if st.button("🛠️\nRESUME PEMELIHARAAN\n\nRekapitulasi pekerjaan dan evaluasi tindakan.", use_container_width=True):
        st.switch_page("pages/Resume_Pemeliharaan.py")

with col3:
    if st.button("📝\nRPT RCT\n\nLaporan harian dan pencatatan operasional rutin.", use_container_width=True):
        st.switch_page("pages/RPT_RCT.py")

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# 4. KOTAK MENU YANG BISA DIKLIK (BARIS 2)
# =========================================================
col4, col5, col6 = st.columns(3)

with col4:
    if st.button("🔄\nRESUME RECLOSER\n\nStatus dan riwayat kerja perangkat recloser.", use_container_width=True):
        st.switch_page("pages/Resume_Reclosers.py")

with col5:
    if st.button("🔍\nINSPEKSI\n\nPengecekan progres hasil inspeksi lapangan.", use_container_width=True):
        st.switch_page("pages/Inspeksi.py")

with col6:
    if st.button("🏆\nTOP 10 PENYULANG KRONIS\n\nInfografis penyulang dengan frekuensi tertinggi.", use_container_width=True):
        st.switch_page("pages/Infografis_Kronis.py")