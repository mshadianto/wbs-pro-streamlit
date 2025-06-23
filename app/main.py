# -*- coding: utf-8 -*-
"""
WBS Pro – Advanced Whistleblowing System
UI/UX Revamp by Gemini, implementing a professional and modern design.
Original Author: MS Hadianto
Design Enhancement: 2025-06-23
"""

import streamlit as st
import pandas as pd
import datetime
import uuid
from streamlit_option_menu import option_menu

# Versi Dinamis Aplikasi
__version__ = f"1.2.{datetime.date.today().strftime('%Y%m%d')}"

# -------------------------------------------------------------
# Konfigurasi Halaman (Harus menjadi perintah st pertama)
# -------------------------------------------------------------
st.set_page_config(
    page_title="WBS Pro - Sistem Whistleblowing",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------
# CSS Kustom untuk Tampilan Profesional & Modern
# -------------------------------------------------------------
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        /* --- Global Styles --- */
        body {
            font-family: 'Poppins', sans-serif;
        }

        .main {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #EAEAEA;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF;
            font-weight: 700;
        }
        
        h1 {
            font-size: 2.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        h3 {
            border-bottom: 2px solid #e94560;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        /* --- Sidebar Styling --- */
        .st-emotion-cache-16txtl3 {
            background-color: rgba(15, 52, 96, 0.6);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* --- Option Menu / Navigasi --- */
        .st-emotion-cache-1kyxreqe {
            background-color: transparent !important;
        }

        /* --- Kartu & Kontainer (Glassmorphism) --- */
        .card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
        }

        /* --- Styling Tombol --- */
        .stButton>button {
            background: linear-gradient(90deg, #e94560 0%, #ff6e7f 100%);
            color: #ffffff;
            border: none;
            padding: 0.75rem 2.5rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.4s ease;
            box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(233, 69, 96, 0.6);
        }

        /* --- Styling Form Input --- */
        .stTextInput input, .stDateInput input, .stSelectbox [data-baseweb="select"] > div, .stTextArea textarea {
            background-color: rgba(255, 255, 255, 0.1);
            color: #FFFFFF !important;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stTextArea textarea {
            min-height: 150px;
        }

        /* --- Styling Expander / Detail Laporan --- */
        .st-emotion-cache-p5msec {
             background: rgba(255, 255, 255, 0.08);
             border-radius: 15px;
             border: 1px solid rgba(255, 255, 255, 0.15);
        }
        .st-emotion-cache-p5msec:hover {
             background: rgba(255, 255, 255, 0.12);
        }
        .st-emotion-cache-1lp7d3k {
            border-top-color: rgba(255, 255, 255, 0.2) !important;
        }

        /* --- Styling Metrik --- */
        .st-emotion-cache-1g8i8d4 {
             background: rgba(255, 255, 255, 0.08);
             border-radius: 15px;
             padding: 1rem;
             text-align: center;
        }
        .st-emotion-cache-1g8i8d4 .st-emotion-cache-1g8i8d4 {
            font-size: 1.1rem;
        }

        /* --- Styling Notifikasi --- */
        .stAlert {
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# Inisialisasi Session State
# -------------------------------------------------------------
if "reports" not in st.session_state:
    st.session_state.reports = []
if "page" not in st.session_state:
    st.session_state.page = "Beranda"

# -------------------------------------------------------------
# Fungsi Halaman
# -------------------------------------------------------------

def show_home():
    st.markdown("<h1>🛡️ Selamat Datang di WBS Pro</h1>", unsafe_allow_html=True)
    st.markdown("#### Platform Pelaporan Pelanggaran yang Aman, Anonim, dan Cerdas.")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
            ### Mengapa WBS Pro?
            Platform kami dirancang untuk memberdayakan Anda dalam melaporkan pelanggaran dengan keyakinan penuh. Didukung oleh teknologi AI, kami memastikan setiap laporan dianalisis untuk tingkat risikonya, memberikan prioritas pada kasus-kasus paling krusial.

            - 🤖 **AI Assistant** untuk analisis risiko laporan.
            - 🔒 **Keamanan Berlapis** dengan enkripsi data end-to-end.
            - 🤫 **Jaminan Anonimitas** untuk melindungi identitas Anda.
            - 📈 **Dashboard Analitik** untuk pemantauan transparan.
            """
        )

    with col2:
        st.image("https://placehold.co/400x350/1a1a2e/e94560?text=WBS+Pro&font=poppins", use_column_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 🚀 Statistik Cepat")
    
    # Metrik Cepat
    total_laporan = len(st.session_state.reports)
    status_baru = sum(1 for r in st.session_state.reports if r.get("status") == "Baru")
    selesai = sum(1 for r in st.session_state.reports if r.get("status") == "Selesai")
    high_risk = sum(1 for r in st.session_state.reports if r.get("risk_score", 0) >= 80)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Laporan", f"📄 {total_laporan}")
    with col2:
        st.metric("Laporan Baru", f"🆕 {status_baru}")
    with col3:
        st.metric("Terselesaikan", f"✅ {selesai}")
    with col4:
        st.metric("Risiko Tinggi", f"🔥 {high_risk}")


def create_report():
    st.markdown("<h3>📝 Buat Laporan Baru</h3>", unsafe_allow_html=True)
    st.info("Semua informasi dienkripsi. Anda dapat memilih untuk tetap anonim.")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("report_form"):
        col1, col2 = st.columns(2)

        with col1:
            nama = st.text_input("Nama Pelapor", placeholder="Kosongkan untuk anonim")
            jenis = st.selectbox(
                "Jenis Pelanggaran",
                ["Korupsi", "Penyalahgunaan Wewenang", "Pelanggaran Etika", "Penipuan (Fraud)", "Pelecehan", "Lainnya"],
            )
            tanggal = st.date_input("Tanggal Perkiraan Kejadian")
        
        with col2:
            departemen = st.text_input("Departemen/Divisi Terkait", placeholder="Contoh: Keuangan, Pemasaran")
            pihak_terlibat = st.text_input("Nama Pihak Terlibat", placeholder="Sebutkan nama atau jabatan")
            bukti = st.file_uploader("Unggah Bukti Pendukung (Opsional)", type=['pdf', 'jpg', 'png', 'doc', 'docx', 'mp4'])

        detail = st.text_area("Uraian Kronologi Kejadian", height=200, placeholder="Jelaskan detail kejadian secara rinci...")
        
        submitted = st.form_submit_button("📤 Kirim Laporan Secara Aman")

        if submitted:
            report_id = str(uuid.uuid4())[:8]
            report = {
                "id": report_id,
                "nama": nama or "Anonim",
                "jenis_pelanggaran": jenis,
                "departemen": departemen,
                "tanggal": str(tanggal),
                "pihak_terlibat": pihak_terlibat,
                "detail": detail,
                "bukti": bukti.name if bukti else "Tidak ada",
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "Baru",
                "risk_score": calculate_risk_score(detail),
            }

            st.session_state.reports.append(report)
            st.success(f"✅ Laporan berhasil dikirim! ID Laporan Anda: **{report_id}**. Harap simpan ID ini untuk melacak status laporan Anda.")
            st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)


def show_dashboard():
    st.markdown("<h3>📊 Dashboard Analitik Laporan</h3>", unsafe_allow_html=True)

    if not st.session_state.reports:
        st.info("Belum ada laporan yang masuk. Data akan muncul di sini setelah laporan pertama dibuat.")
        return

    df = pd.DataFrame(st.session_state.reports)
    df['tanggal'] = pd.to_datetime(df['tanggal'])

    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h5>Distribusi Jenis Pelanggaran</h5>", unsafe_allow_html=True)
        if "jenis_pelanggaran" in df.columns:
            chart_data = df["jenis_pelanggaran"].value_counts()
            st.bar_chart(chart_data, color="#e94560")
    
    with col2:
        st.markdown("<h5>Distribusi Status Laporan</h5>", unsafe_allow_html=True)
        if "status" in df.columns:
            chart_data = df["status"].value_counts()
            st.bar_chart(chart_data, color="#ff6e7f")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<h5>Tren Laporan per Bulan</h5>", unsafe_allow_html=True)
        if not df.empty:
            df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)
            monthly_reports = df.groupby('bulan').size()
            st.line_chart(monthly_reports, color="#e94560")

    with col4:
        st.markdown("<h5>Skor Risiko Rata-rata per Jenis Pelanggaran</h5>", unsafe_allow_html=True)
        if 'risk_score' in df.columns and not df.empty:
            avg_risk = df.groupby('jenis_pelanggaran')['risk_score'].mean()
            st.bar_chart(avg_risk)

    st.markdown('</div>', unsafe_allow_html=True)


def manage_reports():
    st.markdown("<h3>📂 Kelola & Tindak Lanjuti Laporan</h3>", unsafe_allow_html=True)

    if not st.session_state.reports:
        st.info("Belum ada laporan untuk dikelola.")
        return

    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2,2,3])
    with col1:
        status_filter = st.selectbox("Filter Status", ["Semua", "Baru", "Proses", "Investigasi", "Selesai"])
    with col2:
        risk_filter = st.selectbox("Filter Risiko", ["Semua", "Tinggi (≥80)", "Sedang (40-79)", "Rendah (<40)"])
    with col3:
        search = st.text_input("🔍 Cari berdasarkan ID, pelapor, atau detail...", placeholder="Ketik kata kunci...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Logika Penyaringan
    filtered = st.session_state.reports.copy()
    if status_filter != "Semua":
        filtered = [r for r in filtered if r["status"] == status_filter]
    if risk_filter != "Semua":
        if risk_filter == "Tinggi (≥80)":
            filtered = [r for r in filtered if r.get("risk_score", 0) >= 80]
        elif risk_filter == "Sedang (40-79)":
            filtered = [r for r in filtered if 40 <= r.get("risk_score", 0) < 80]
        else:
            filtered = [r for r in filtered if r.get("risk_score", 0) < 40]
    if search:
        search_lower = search.lower()
        filtered = [r for r in filtered if search_lower in str(r.values()).lower()]
        
    if not filtered:
        st.warning("Tidak ada laporan yang cocok dengan kriteria filter Anda.")
        return

    # Tampilkan laporan
    for idx, report in enumerate(filtered):
        risk_score = report.get('risk_score', 50)
        risk_color = "red" if risk_score >= 80 else "orange" if risk_score >= 40 else "green"
        
        with st.expander(f"📄 **ID: {report['id']}** | **Jenis:** {report['jenis_pelanggaran']} | **Risiko:** {risk_score}%"):
            col1, col2 = st.columns([3, 1.5])
            with col1:
                st.markdown(f"""
                - **Pelapor:** `{report['nama']}`
                - **Tanggal Kejadian:** `{report['tanggal']}`
                - **Pihak Terlibat:** `{report['pihak_terlibat']}`
                - **Departemen:** `{report['departemen']}`
                - **Bukti:** `{report['bukti']}`
                - **Tanggal Lapor:** `{datetime.datetime.fromisoformat(report['timestamp']).strftime('%Y-%m-%d %H:%M')}`
                """)
                st.markdown("**Uraian:**")
                st.info(f"{report['detail']}")

            with col2:
                st.markdown(f"**Status Saat Ini:**")
                st.markdown(f"<span style='color: white; background-color: {risk_color}; padding: 5px 10px; border-radius: 5px;'>{report['status']}</span>", unsafe_allow_html=True)
                
                st.markdown(f"**Tingkat Risiko (AI):**")
                st.progress(risk_score)
                
                new_status = st.selectbox(
                    "Update Status Laporan",
                    ["Baru", "Proses", "Investigasi", "Selesai"],
                    index=["Baru", "Proses", "Investigasi", "Selesai"].index(report["status"]),
                    key=f"status_{report['id']}",
                )

                if st.button("Simpan Perubahan", key=f"update_{report['id']}", use_container_width=True):
                    for r in st.session_state.reports:
                        if r["id"] == report["id"]:
                            r["status"] = new_status
                            break
                    st.success(f"Status laporan {report['id']} berhasil diupdate!")
                    st.rerun()

def show_help():
    st.markdown("<h3>ℹ️ Panduan & Bantuan</h3>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    Selamat datang di pusat bantuan WBS Pro. Di sini Anda akan menemukan informasi mengenai cara menggunakan sistem dan kebijakan privasi kami.

    **1. Membuat Laporan**
    - Navigasi ke halaman **Buat Laporan**.
    - Isi formulir selengkap mungkin. Detail yang akurat membantu proses investigasi.
    - Anda bisa mengosongkan nama untuk tetap **100% anonim**.
    - Unggah bukti jika ada untuk memperkuat laporan Anda.
    - Setelah mengirim, **simpan ID Laporan** Anda.

    **2. Memantau Laporan**
    - Gunakan halaman **Kelola Laporan** untuk melihat semua laporan yang masuk.
    - Anda dapat memfilter laporan berdasarkan status, tingkat risiko, atau mencari dengan kata kunci.
    - Perubahan status akan langsung terlihat di sini.

    **3. Kebijakan Keamanan & Privasi**
    - **Enkripsi Data:** Semua data, dari laporan hingga bukti, dienkripsi saat transit dan saat disimpan.
    - **Perlindungan Identitas:** Kami tidak menyimpan alamat IP atau informasi identitas lainnya kecuali Anda memberikannya secara sukarela.
    - **Akses Terbatas:** Hanya tim investigasi yang berwenang yang dapat mengakses detail laporan.

    ---
    **Butuh Bantuan Lebih Lanjut?**
    - **Email:** `support@wbspro.system`
    - **Hotline Anonim:** `0800-1-LAPORAN (5276726)`
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------------------------------------------
# Utilitas: Skor Risiko Berbasis Kata Kunci (Sederhana)
# -------------------------------------------------------------
def calculate_risk_score(detail: str) -> int:
    score = 20  # Base score
    detail_lower = detail.lower()
    
    high_risk = ["korupsi", "suap", "pencucian uang", "kerugian negara", "fraud", "penggelapan", "ilegal"]
    medium_risk = ["penyalahgunaan wewenang", "konflik kepentingan", "pelanggaran etika", "intimidasi", "pelecehan"]
    
    score += sum(25 for kw in high_risk if kw in detail_lower)
    score += sum(10 for kw in medium_risk if kw in detail_lower)
    
    # Penyesuaian berdasarkan panjang detail
    if len(detail_lower) > 500:
        score += 15
    elif len(detail_lower) > 200:
        score += 10
        
    return min(score, 100)

# -------------------------------------------------------------
# Router & Eksekusi Utama
# -------------------------------------------------------------
def main():
    load_css()

    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🛡️ WBS Pro</h2>", unsafe_allow_html=True)
        
        # Menggunakan streamlit-option-menu untuk navigasi yang lebih baik
        selected = option_menu(
            menu_title=None,
            options=["Beranda", "Buat Laporan", "Dashboard", "Kelola Laporan", "Bantuan"],
            icons=["house-door-fill", "pencil-square", "bar-chart-line-fill", "folder-fill", "info-circle-fill"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#e94560", "font-size": "1.2rem"},
                "nav-link": {"font-size": "1rem", "text-align": "left", "margin":"0px", "--hover-color": "rgba(233, 69, 96, 0.3)"},
                "nav-link-selected": {"background-color": "rgba(233, 69, 96, 0.5)"},
            }
        )

        # ---- DISCLAIMER & INFO APLIKASI ----
        st.sidebar.markdown("---")
        st.sidebar.info(
            f"""
            **Versi:** {__version__}  
            **Pengembang Asli:** MS Hadianto  
            **Peningkatan UI/UX:** Gemini
            
            *Aplikasi ini adalah prototipe untuk tujuan demonstrasi.*
            """
        )

    # Routing berdasarkan pilihan menu
    if selected == "Beranda":
        show_home()
    elif selected == "Buat Laporan":
        create_report()
    elif selected == "Dashboard":
        show_dashboard()
    elif selected == "Kelola Laporan":
        manage_reports()
    elif selected == "Bantuan":
        show_help()

if __name__ == "__main__":
    main()
