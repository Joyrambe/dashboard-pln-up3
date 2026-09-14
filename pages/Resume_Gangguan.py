import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import requests

st.set_page_config(page_title="Resume Gangguan", page_icon="📊", layout="wide")

@st.cache_data(ttl=60)
def fetch_google_sheets():
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
    st.error(f"Gagal menarik data! Error: {e}")
    st.stop()

sub_menu = st.radio(
    "Pilih Tampilan:",
    ["📊 Utama: Grafik & Logsheet", "🥧 Detail: Relay & Penyebab", "📝 Input Baru", "✏️ Edit / Hapus Data"],
    horizontal=True,
    label_visibility="collapsed"
)

st.title("GANGGUAN PENYULANG")
st.markdown("---")
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxvbw68N92VTdSZP4xUT6HnWNvcvYdrYR4vNhUSndaGwyDk-VbVRQSFp0-6bajsWst3/exec"

# =========================================================
# KONTEN 1 & 2 (GRAFIK & PIE CHART)
# =========================================================
if sub_menu in ["📊 Utama: Grafik & Logsheet", "🥧 Detail: Relay & Penyebab"]:
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
    
    if sub_menu == "📊 Utama: Grafik & Logsheet":
        st.subheader("Grafik Total Gangguan per Penyulang")
        bar_data = df_filtered.groupby('PENYULANG')[['TEMPORER', 'PERMANEN']].sum().reset_index()
        bar_data_melted = bar_data.melt(id_vars='PENYULANG', value_vars=['TEMPORER', 'PERMANEN'], var_name='JENIS', value_name='JUMLAH')
        fig_bar = px.bar(bar_data_melted, x='PENYULANG', y='JUMLAH', color='JENIS', barmode='group', text_auto=True, color_discrete_map={'TEMPORER': '#2ca02c', 'PERMANEN': '#1f77b4'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.subheader("LOGSHEET DATA")
        kolom_tabel = ['TANGGAL PADAM', 'PENYULANG', 'NAMA SECTION', 'ULP', 'PENYEBAB', 'RELAY YANG BEKERJA', 'R', 'S', 'T', 'N', 'TITIK KOORDINAT']
        kolom_tersedia = [k for k in kolom_tabel if k in df_filtered.columns]
        st.dataframe(df_filtered[kolom_tersedia], use_container_width=True)

        # FITUR BARU: LACAK PETA DAN FOTO
        st.markdown("---")
        st.markdown("### 📍 Lacak Peta & Bukti Foto")
        st.info("Pilih data gangguan di bawah ini untuk melihat titik koordinat pada peta dan dokumentasi foto.")
        
        if not df_filtered.empty:
            df_filtered['LABEL_CARI'] = df_filtered['PENYULANG'] + " | " + df_filtered['TANGGAL PADAM'].astype(str) + " (" + df_filtered.get('PENYEBAB', 'N/A').astype(str) + ")"
            pilihan = st.selectbox("Pilih Gangguan:", df_filtered['LABEL_CARI'].tolist())
            
            if pilihan:
                row = df_filtered[df_filtered['LABEL_CARI'] == pilihan].iloc[0]
                col_m1, col_m2 = st.columns(2)
                
                with col_m1:
                    st.markdown("**🗺️ Peta Lokasi**")
                    tikor = str(row.get('TITIK KOORDINAT', ''))
                    if pd.notna(tikor) and "," in tikor:
                        try:
                            lat, lon = map(float, tikor.split(','))
                            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}), zoom=14)
                            st.link_button("Buka di Aplikasi Google Maps 🌍", f"https://www.google.com/maps/search/?api=1&query={lat},{lon}")
                        except:
                            st.warning("Format koordinat salah. Gunakan angka latitude, longitude (Contoh: 1.452, 99.123)")
                    else:
                        st.warning("Titik koordinat belum diisi untuk data ini.")
                        
                with col_m2:
                    st.markdown("**📸 Bukti Foto**")
                    foto = str(row.get('FOTO', ''))
                    if pd.notna(foto) and foto.startswith("http"):
                        st.image("https://cdn-icons-png.flaticon.com/512/833/833281.png", width=100) # Ikon ilustrasi
                        st.link_button("🖼️ Lihat Foto Bukti Original", foto, use_container_width=True)
                    else:
                        st.warning("Link foto belum dilampirkan oleh petugas.")
                        
    else:
        col_pie1, col_pie2 = st.columns(2)
        with col_pie1:
            fig_relay = px.pie(df_filtered['RELAY YANG BEKERJA'].value_counts().reset_index(name='JUMLAH'), values='JUMLAH', names='RELAY YANG BEKERJA', title="RELAY YANG BEKERJA", hole=0.4)
            st.plotly_chart(fig_relay, use_container_width=True)
        with col_pie2:
            fig_penyebab = px.pie(df_filtered['PENYEBAB'].value_counts().reset_index(name='JUMLAH'), values='JUMLAH', names='PENYEBAB', title="PENYEBAB GANGGUAN", hole=0.4)
            st.plotly_chart(fig_penyebab, use_container_width=True)

# =========================================================
# KONTEN 3 & 4 (LOGIN ADMIN & FORM)
# =========================================================
elif sub_menu in ["📝 Input Baru", "✏️ Edit / Hapus Data"]:
    if "akses_form" not in st.session_state: st.session_state["akses_form"] = False

    if not st.session_state["akses_form"]:
        st.error("🔒 **AREA TERBATAS ADMIN**")
        with st.form("form_login"):
            pin_input = st.text_input("🔑 Masukkan PIN Akses:", type="password")
            if st.form_submit_button("Buka Kunci"):
                if pin_input == "PLNUP3": 
                    st.session_state["akses_form"] = True
                    st.rerun()
                else: st.error("❌ PIN salah!")

    if st.session_state["akses_form"]:
        if st.button("🔒 Tutup Akses (Logout)"):
            st.session_state["akses_form"] = False
            st.rerun()
            
        if sub_menu == "📝 Input Baru":
            st.success("✅ **Mode Input Aktif.**")
            with st.form("form_insert", clear_on_submit=True):
                st.markdown("##### 📍 Data Lokasi & Jaringan")
                col1, col2, col3 = st.columns(3)
                with col1:
                    penyulang = st.text_input("Penyulang")
                    nama = st.text_input("Nama")
                    ulp = st.selectbox("ULP", ["PADANGSIDIMPUAN", "SIBUHUAN", "KOTANOPAN", "PANYABUNGAN", "SIPIROK", "GUNUNG TUA", "NATAL"])
                with col2:
                    section = st.text_input("Section")
                    nama_section = st.text_input("Nama Section")
                with col3:
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

                st.markdown("##### ⚙️ Detail Teknis & Bukti Lapangan")
                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    penyebab = text_input = st.text_input("Penyebab")
                    relay = st.selectbox("Relay Yang Bekerja", ["OCR", "GFR", "OCR & GFR", "TIDAK ADA"])
                    arus_tertinggi = st.number_input("Arus Tertinggi (A)", min_value=0.0)
                    ens = st.number_input("ENS (kWh)", min_value=0.0)
                with col_t2:
                    temporer = st.number_input("Temporer (Kali)", min_value=0)
                    permanen = st.number_input("Permanen (Kali)", min_value=0)
                    titik_koordinat = st.text_input("Titik Koordinat (Contoh: 1.432, 99.231)")
                    foto = st.text_input("Link Foto Gangguan (Google Drive/Lainnya)")

                st.markdown("**Arus Fasa (A)**")
                col_r, col_s, col_t_fasa, col_n = st.columns(4)
                with col_r: r = st.number_input("R", min_value=0.0)
                with col_s: s = st.number_input("S", min_value=0.0)
                with col_t_fasa: t = st.number_input("T", min_value=0.0)
                with col_n: n = st.number_input("N", min_value=0.0)

                st.markdown("---")
                if st.form_submit_button("💾 Simpan Data Baru", use_container_width=True):
                    if penyulang == "":
                        st.error("⚠️ Penyulang wajib diisi!")
                    else:
                        with st.spinner("Memproses data ke Google Sheets..."):
                            payload = {
                                "action": "insert",
                                "penyulang": penyulang, "nama": nama, "section": section, "nama_section": nama_section,
                                "ulp": ulp, "penyebab": penyebab, "relay": relay, "bulan": bulan,
                                "tanggal_padam": str(tanggal_padam), "jam_padam": str(jam_padam),
                                "tanggal_nyala": str(tanggal_nyala), "jam_nyala": str(jam_nyala),
                                "durasi_jam": durasi_jam, "durasi_menit": durasi_menit,
                                "temporer": temporer, "permanen": permanen, "cuaca": cuaca,
                                "arus_tertinggi": arus_tertinggi, "ens": ens,
                                "r": r, "s": s, "t": t, "n": n, "titik_koordinat": titik_koordinat, "foto": foto
                            }
                            try:
                                req = requests.post(WEBHOOK_URL, json=payload)
                                if "Success" in req.text: st.success("✅ Berhasil disimpan! Refresh web untuk melihat hasilnya.")
                                else: st.error(f"❌ Gagal mengirim data: {req.text}")
                            except Exception as e: st.error(f"❌ Kesalahan jaringan: {e}")

        elif sub_menu == "✏️ Edit / Hapus Data":
            st.warning("⚠️ **Mode Edit/Hapus Aktif.**")
            pilih_peny = st.selectbox("1. Pilih Penyulang", df['PENYULANG'].dropna().unique())
            df_filter_1 = df[df['PENYULANG'] == pilih_peny]
            pilih_tgl = st.selectbox("2. Pilih Tanggal Padam", df_filter_1['TANGGAL PADAM'].astype(str).unique())
            df_target = df_filter_1[df_filter_1['TANGGAL PADAM'].astype(str) == pilih_tgl]

            if not df_target.empty:
                data_asli = df_target.iloc[0]
                with st.form("form_edit_hapus"):
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        edit_penyulang = st.text_input("Penyulang", value=str(data_asli.get('PENYULANG', '')))
                        edit_ulp = st.text_input("ULP", value=str(data_asli.get('ULP', '')))
                        edit_penyebab = st.text_input("Penyebab", value=str(data_asli.get('PENYEBAB', '')))
                        edit_titik_koordinat = st.text_input("Titik Koordinat (Lat, Long)", value=str(data_asli.get('TITIK KOORDINAT', '')))
                    with col_e2:
                        edit_tgl_padam = st.text_input("Tanggal Padam (YYYY-MM-DD)", value=str(data_asli.get('TANGGAL PADAM', '')))
                        edit_relay = st.text_input("Relay Yang Bekerja", value=str(data_asli.get('RELAY YANG BEKERJA', '')))
                        edit_durasi = st.number_input("Durasi Jam", value=float(data_asli.get('DURASI JAM', 0.0) if pd.notna(data_asli.get('DURASI JAM')) else 0.0))
                        edit_foto = st.text_input("Link Foto", value=str(data_asli.get('FOTO', '')))
                    
                    st.markdown("---")
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.form_submit_button("🔄 Update Perubahan", use_container_width=True):
                            with st.spinner("Memperbarui data..."):
                                payload_update = {
                                    "action": "update", "penyulang_lama": str(pilih_peny), "tanggal_padam_lama": str(pilih_tgl),
                                    "penyulang": edit_penyulang, "tanggal_padam": edit_tgl_padam, "penyebab": edit_penyebab, 
                                    "ulp": edit_ulp, "relay": edit_relay, "durasi_jam": edit_durasi, 
                                    "titik_koordinat": edit_titik_koordinat, "foto": edit_foto
                                }
                                req = requests.post(WEBHOOK_URL, json=payload_update)
                                if "Success" in req.text: st.success("✅ Berhasil di-update!")
                                else: st.error(req.text)
                    with col_btn2:
                        if st.form_submit_button("❌ Hapus Permanen", use_container_width=True):
                            payload_delete = {"action": "delete", "penyulang_lama": str(pilih_peny), "tanggal_padam_lama": str(pilih_tgl)}
                            req = requests.post(WEBHOOK_URL, json=payload_delete)
                            if "Success" in req.text: st.success("🗑️ Berhasil dihapus!")
                            else: st.error(req.text)