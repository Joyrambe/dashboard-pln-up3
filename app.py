import streamlit as st

st.set_page_config(
    page_title="PLN UP3 Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi status login & file Excel secara global
if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

if 'uploaded_excel_file' not in st.session_state:
    st.session_state['uploaded_excel_file'] = None

# =========================================================
# CSS CUSTOM TAMPILAN
# =========================================================
st.markdown("""
<style>
    .main-header {
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: -15px;
        padding-top: 10px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #8892b0;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 400;
    }
    .card-link { text-decoration: none !important; color: inherit !important; display: block; height: 100%; }
    
    .info-card {
        background: rgba(30, 30, 47, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
        text-align: center;
        height: 100%;
        cursor: pointer;
    }
    .info-card:hover {
        transform: translateY(-8px);
        border-color: #00C9FF;
        box-shadow: 0 10px 40px 0 rgba(0, 201, 255, 0.2);
    }
    .card-icon { font-size: 2.8rem; margin-bottom: 10px; }
    .card-title { font-size: 1.05rem; font-weight: 700; color: #e2e8f0; margin-bottom: 8px; line-height: 1.3;}
    .card-text { color: #94a3b8; font-size: 0.85rem; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">⚡ DASHBOARD PLN UP3</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Pusat Kendali & Analisis Terpadu | Padangsidimpuan</p>', unsafe_allow_html=True)

# =========================================================
# KARTU MENU UTAMA (6 MENU)
# =========================================================
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <a href="Resume_Gangguan" target="_self" class="card-link">
        <div class="info-card">
            <div class="card-icon">📊</div>
            <div class="card-title">RESUME GANGGUAN</div>
            <div class="card-text">Data logsheet, grafik, dan analisis penyebab gangguan.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <a href="Resume_Pemeliharaan" target="_self" class="card-link">
        <div class="info-card">
            <div class="card-icon">🛠️</div>
            <div class="card-title">RESUME PEMELIHARAAN</div>
            <div class="card-text">Rekapitulasi pekerjaan dan evaluasi tindakan.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <a href="RPT_RCT" target="_self" class="card-link">
        <div class="info-card">
            <div class="card-icon">📝</div>
            <div class="card-title">RPT RCT</div>
            <div class="card-text">Laporan harian dan pencatatan operasional rutin.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.write("") 

c4, c5, c6 = st.columns(3)
with c4:
    st.markdown("""
    <a href="Resume_Recloser" target="_self" class="card-link">
        <div class="info-card">
            <div class="card-icon">🔄</div>
            <div class="card-title">RESUME RECLOSER</div>
            <div class="card-text">Status dan riwayat kerja perangkat recloser penyulang.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)
with c5:
    st.markdown("""
    <a href="Inspeksi" target="_self" class="card-link">
        <div class="info-card">
            <div class="card-icon">🔍</div>
            <div class="card-title">INSPEKSI</div>
            <div class="card-text">Pengecekan progres hasil inspeksi lapangan (Tier 1 & 2).</div>
        </div>
    </a>
    """, unsafe_allow_html=True)
with c6:
    st.markdown("""
    <a href="Infografis_Kronis" target="_self" class="card-link">
        <div class="info-card">
            <div class="card-icon">🏆</div>
            <div class="card-title">TOP 10 PENYULANG KRONIS</div>
            <div class="card-text">Infografis penyulang dengan frekuensi gangguan tertinggi.</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown("---")

