import streamlit as st

st.set_page_config(page_title="Upload Data Baru", page_icon="📁")

st.title("📁 Upload Data Logsheet Baru")
st.markdown("Upload file Excel terbaru di sini. Data akan otomatis diproses dan seluruh grafik di menu laporan akan langsung berubah.")

# Tombol untuk upload file
uploaded_file = st.file_uploader("Masukkan file Excel (LOGSHEET GANGGUAN.xlsx)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Menyimpan file yang diupload ke memori sementara web (session_state)
        st.session_state['uploaded_excel'] = uploaded_file.getvalue()
        st.success("✅ Data berhasil di-upload! Silakan buka menu laporan di samping, grafiknya sudah otomatis berubah mengikuti file barumu.")
    except Exception as e:
        st.error(f"Gagal memproses file: {e}")