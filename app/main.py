# -*- coding: utf-8 -*-
"""
WBS Pro – Advanced Whistleblowing System with Real-time Chat
Version 1.5.2: Fixed Indentation and Page Config Errors
Original Author: MS Hadianto
Enhancements by Gemini: 2025-06-24
"""

import streamlit as st
import pandas as pd
import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_option_menu import option_menu
import os

# -------------------------------------------------------------
# Konfigurasi Halaman & CSS (WAJIB JADI YANG PERTAMA)
# -------------------------------------------------------------
# Aturan Streamlit: set_page_config() harus menjadi perintah st.* pertama.
st.set_page_config(
    page_title="WBS Pro - Sistem Whistleblowing",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    """Memuat CSS kustom untuk tampilan aplikasi."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        body { font-family: 'Poppins', sans-serif; background-color: #f0f2f6; }
        .main { background-color: #f0f2f6; color: #1e293b; }
        h1, h2, h3, h4, h5, h6 { color: #0f172a; font-weight: 700; }
        h3 { border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-bottom: 20px; }
        .st-emotion-cache-16txtl3 { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
        .card { background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); transition: all 0.3s ease; }
        .stButton>button { background-color: #2563eb; color: #ffffff; border: none; padding: 0.75rem 2.5rem; border-radius: 50px; font-weight: 600; font-size: 1rem; transition: all 0.3s ease; }
        [data-testid="chat-container"] { background-color: #f8fafc; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Memuat CSS di awal
load_css()

# Versi Dinamis Aplikasi
__version__ = f"1.5.2.{datetime.date.today().strftime('%Y%m%d')}"

# -------------------------------------------------------------
# Inisialisasi Firebase (Hanya berjalan sekali)
# -------------------------------------------------------------
@st.cache_resource
def initialize_firebase():
    """Menginisialisasi Firebase Admin SDK menggunakan Streamlit secrets."""
    try:
        # Cek apakah aplikasi sudah diinisialisasi
        if not firebase_admin._apps:
            # Ambil kredensial dari Streamlit secrets
            creds_dict = st.secrets["firebase_credentials"].to_dict()
            # Ganti escape character '\n' dengan newline character asli
            creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred)
        # Kembalikan instance client Firestore
        return firestore.client()
    except Exception as e:
        # Tampilkan error di console atau log, tapi untuk UI akan ditangani di main()
        print(f"Gagal koneksi ke Firebase: {e}")
        return None

# Panggil fungsi inisialisasi
db = initialize_firebase()

# -------------------------------------------------------------
# Fungsi-fungsi Terkait Chat
# -------------------------------------------------------------
def send_message(report_id, sender, text):
    """Mengirim pesan ke koleksi chat di Firestore."""
    if db is None or not text.strip(): return
    chat_ref = db.collection('chats').document(report_id).collection('messages')
    chat_ref.add({'sender': sender, 'text': text, 'timestamp': firestore.SERVER_TIMESTAMP})

def get_messages(report_id):
    """Mengambil semua pesan untuk sebuah laporan dari Firestore."""
    if db is None: return []
    messages_ref = db.collection('chats').document(report_id).collection('messages').order_by('timestamp')
    return [doc.to_dict() for doc in messages_ref.stream()]

def display_chat_interface(report_id, user_role, key_suffix=""):
    """Merender antarmuka chat untuk ID laporan dan peran pengguna tertentu."""
    st.markdown(f"<h4>💬 Komunikasi untuk Laporan #{report_id}</h4>", unsafe_allow_html=True)
    messages = get_messages(report_id)
    for msg in messages:
        # Tentukan avatar berdasarkan pengirim pesan
        is_user_sender = msg.get('sender') == user_role
        avatar_icon = "🧑‍💻" if is_user_sender else "🛡️"
        with st.chat_message(name=msg.get('sender', 'Unknown'), avatar=avatar_icon):
            st.write(msg.get('text', ''))

    # PERBAIKAN: Menggunakan key yang unik untuk setiap chat input
    # untuk menghindari Streamlit's DuplicateWidgetID error.
    unique_key = f"chat_input_{report_id}_{key_suffix}"
    prompt = st.chat_input("Ketik pesan Anda di sini...", key=unique_key)

    if prompt:
        send_message(report_id, user_role, prompt)
        st.rerun()

# -------------------------------------------------------------
# Fungsi Halaman
# -------------------------------------------------------------
def show_home():
    """Menampilkan halaman beranda."""
    st.markdown("<h1>🛡️ Selamat Datang di WBS Pro</h1>", unsafe_allow_html=True)
    st.markdown("#### Platform Pelaporan Pelanggaran yang Aman, Anonim, dan Cerdas.")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### Memahami Whistleblowing System (WBS)
    
    Sebuah *Whistleblowing System* (Sistem Pelaporan Pelanggaran) adalah mekanisme vital bagi setiap organisasi yang berkomitmen pada tata kelola yang baik, transparansi, dan integritas. Sistem ini menyediakan saluran yang aman dan rahasia bagi siapa saja—baik karyawan, mitra, maupun pihak eksternal—untuk melaporkan dugaan pelanggaran, penipuan, atau tindakan tidak etis lainnya tanpa rasa takut akan pembalasan.

    **Mengapa WBS Penting?**
    - **Deteksi Dini:** Berfungsi sebagai sistem peringatan dini untuk mengidentifikasi masalah sebelum menjadi krisis.
    - **Membangun Kepercayaan:** Menunjukkan komitmen organisasi terhadap lingkungan kerja yang jujur dan etis.
    - **Kepatuhan & Tata Kelola:** Memperkuat kerangka kerja *Good Corporate Governance* (GCG).

    **WBS Pro adalah Solusi Anda.** Keberanian Anda untuk melapor adalah langkah pertama dalam menciptakan lingkungan yang lebih baik.
    """)
    st.markdown("---")
    st.markdown("### Fitur Unggulan\n- 💬 Komunikasi Real-time\n- 🤖 Analisis Risiko AI\n- 🔒 Keamanan & Anonimitas")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if db:
        st.success("Koneksi ke Database Real-time berhasil!", icon="✅")

def create_report():
    """Menampilkan form untuk membuat laporan baru."""
    st.markdown("<h3>📝 Buat Laporan Baru</h3>", unsafe_allow_html=True)
    st.info("Setelah mengirim, Anda akan mendapatkan ID Laporan unik untuk melacak dan berkomunikasi dengan pengelola.")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("report_form"):
        col1, col2 = st.columns(2)

        with col1:
            nama = st.text_input("Nama Pelapor", placeholder="Kosongkan untuk tetap anonim")
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
            report_id = str(uuid.uuid4())[:8].upper()
            report_data = {
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
            if db:
                db.collection('reports').document(report_id).set(report_data)
                # Tambahkan laporan baru ke session state agar UI update
                st.session_state.reports.append(report_data)
                st.success(f"✅ Laporan berhasil dikirim! ID Laporan Anda: **{report_id}**")
                st.info("Harap simpan ID ini di tempat aman untuk melacak status laporan Anda.", icon="ℹ️")
                st.balloons()
            else:
                 st.error("Gagal mengirim laporan karena tidak ada koneksi database.")

    st.markdown('</div>', unsafe_allow_html=True)

def show_communication_page():
    """Menampilkan halaman untuk melacak laporan dan berkomunikasi."""
    st.markdown("<h3> Lacak & Komunikasi</h3>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if 'active_report_id' not in st.session_state:
        st.session_state.active_report_id = None

    report_id_input = st.text_input("Masukkan ID Laporan Anda:", placeholder="Contoh: A1B2C3D4").upper()
    
    if st.button("Cari Laporan", key="search_report_btn"):
        if report_id_input and db:
            report_ref = db.collection('reports').document(report_id_input).get()
            if report_ref.exists:
                st.session_state.active_report_id = report_id_input
            else:
                st.session_state.active_report_id = None
                st.error("ID Laporan tidak ditemukan. Periksa kembali ID Anda.")
        else:
            st.warning("Silakan masukkan ID Laporan.")

    if st.session_state.active_report_id:
        # Menambahkan 'pelapor' sebagai suffix untuk memastikan keunikan key
        display_chat_interface(st.session_state.active_report_id, user_role="Pelapor", key_suffix="pelapor")

    st.markdown('</div>', unsafe_allow_html=True)

def manage_reports():
    """Menampilkan halaman untuk pengelola laporan."""
    st.markdown("<h3>📂 Kelola & Tindak Lanjuti Laporan</h3>", unsafe_allow_html=True)
    
    # Refresh data dari Firestore setiap kali halaman ini dikunjungi
    if db:
        reports_ref = db.collection('reports').stream()
        # Urutkan laporan dari yang terbaru
        st.session_state.reports = sorted([doc.to_dict() for doc in reports_ref], key=lambda x: x['timestamp'], reverse=True)

    if not st.session_state.get('reports'):
        st.info("Belum ada laporan untuk dikelola.")
        return
        
    for report in st.session_state.reports:
        risk_score = report.get('risk_score', 50)
        risk_color = "#ef4444" if risk_score >= 80 else "#f97316" if risk_score >= 40 else "#22c55e"

        with st.expander(f"📄 **ID: {report['id']}** | **Jenis:** {report.get('jenis_pelanggaran', 'N/A')} | **Risiko:** {risk_score}%"):
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"""
                - **Pelapor:** `{report.get('nama', 'N/A')}`
                - **Tanggal Kejadian:** `{report.get('tanggal', 'N/A')}`
                - **Pihak Terlibat:** `{report.get('pihak_terlibat', 'N/A')}`
                - **Status:** <span style='color: white; background-color: {risk_color}; padding: 2px 8px; border-radius: 5px; font-weight: 500;'>{report.get('status', 'N/A')}</span>
                """, unsafe_allow_html=True)
                st.markdown("**Uraian:**")
                st.info(f"{report.get('detail', 'Tidak ada detail.')}")
            with col2:
                if db:
                    # Menambahkan 'pengelola' sebagai suffix untuk memastikan keunikan key
                    display_chat_interface(report['id'], user_role="Pengelola", key_suffix=f"pengelola_{report['id']}")

def show_dashboard():
    """Menampilkan dashboard analitik laporan."""
    st.markdown("<h3>📊 Dashboard Analitik Laporan</h3>", unsafe_allow_html=True)

    if not st.session_state.get('reports'):
        # Coba muat data jika kosong
        if db:
            reports_ref = db.collection('reports').stream()
            st.session_state.reports = [doc.to_dict() for doc in reports_ref]

    if not st.session_state.get('reports'):
        st.info("Belum ada data laporan untuk ditampilkan di dashboard.")
        return

    df = pd.DataFrame(st.session_state.reports)
    df['tanggal'] = pd.to_datetime(df['tanggal'])

    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Laporan", len(df))
    col2.metric("Laporan 'Baru'", len(df[df['status'] == 'Baru']))
    col3.metric("Rata-rata Skor Risiko", f"{df['risk_score'].mean():.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)


    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h5>Distribusi Jenis Pelanggaran</h5>", unsafe_allow_html=True)
        if "jenis_pelanggaran" in df.columns:
            chart_data = df["jenis_pelanggaran"].value_counts()
            st.bar_chart(chart_data, color="#3b82f6")
    
    with col2:
        st.markdown("<h5>Distribusi Status Laporan</h5>", unsafe_allow_html=True)
        if "status" in df.columns:
            chart_data = df["status"].value_counts()
            st.bar_chart(chart_data, color="#60a5fa")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_help():
    """Menampilkan halaman panduan dan bantuan."""
    st.markdown("<h3>ℹ️ Panduan & Bantuan</h3>", unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    Selamat datang di pusat bantuan WBS Pro. Di sini Anda akan menemukan informasi mengenai cara menggunakan sistem dan kebijakan privasi kami.

    **1. Membuat Laporan**
    - Navigasi ke halaman **Buat Laporan**.
    - Isi formulir selengkap mungkin. Detail yang akurat membantu proses investigasi.
    - Anda bisa mengosongkan nama untuk tetap **100% anonim**.
    - Unggah bukti jika ada untuk memperkuat laporan Anda.
    - Setelah mengirim, **simpan ID Laporan** Anda. ID ini sangat penting.

    **2. Berkomunikasi Secara Anonim**
    - Buka halaman **Lacak & Komunikasi**.
    - Masukkan ID Laporan Anda untuk membuka ruang obrolan aman dengan pengelola.
    
    **3. Kebijakan Keamanan & Privasi**
    - **Enkripsi Data:** Semua data, dari laporan hingga bukti, dienkripsi saat transit dan saat disimpan.
    - **Perlindungan Identitas:** Kami tidak melacak alamat IP atau informasi identitas lainnya. Nama Anda opsional.
    - **Akses Terbatas:** Hanya tim investigasi yang berwenang yang dapat mengakses detail laporan.

    ---
    **Butuh Bantuan Lebih Lanjut?**
    - **Email:** `support@wbspro.system`
    - **Hotline Anonim:** `0800-1-LAPORAN (5276726)`
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def calculate_risk_score(detail):
    """Menghitung skor risiko berdasarkan kata kunci dalam detail laporan."""
    score = 20  # Skor dasar
    detail_lower = detail.lower()
    high_risk = ["korupsi", "suap", "pencucian uang", "kerugian negara", "fraud", "penggelapan", "ilegal"]
    medium_risk = ["penyalahgunaan wewenang", "konflik kepentingan", "pelanggaran etika", "intimidasi", "pelecehan"]
    
    # Tambah skor berdasarkan kata kunci risiko tinggi
    if any(kw in detail_lower for kw in high_risk):
        score += 40
    # Tambah skor berdasarkan kata kunci risiko sedang
    elif any(kw in detail_lower for kw in medium_risk):
        score += 25

    # Tambah skor berdasarkan panjang detail
    if len(detail_lower) > 500:
        score += 15
    elif len(detail_lower) > 200:
        score += 10
        
    return min(score, 100) # Pastikan skor maksimal 100

# -------------------------------------------------------------
# Router & Eksekusi Utama
# -------------------------------------------------------------
def main():
    """Fungsi utama untuk menjalankan aplikasi Streamlit."""
    
    # Inisialisasi session_state jika belum ada
    if "reports" not in st.session_state:
        st.session_state.reports = []
    
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #0f172a;'>🛡️ WBS Pro</h2>", unsafe_allow_html=True)
        selected = option_menu(
            menu_title=None,
            options=["Beranda", "Buat Laporan", "Lacak & Komunikasi", "Dashboard", "Kelola Laporan", "Bantuan"],
            icons=["house-door-fill", "pencil-square", "chat-dots-fill", "bar-chart-line-fill", "folder-fill", "info-circle-fill"],
            menu_icon="cast", default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#ffffff"},
                "icon": {"color": "#3b82f6", "font-size": "1.2rem"},
                "nav-link": {"font-size": "1rem", "text-align": "left", "margin":"0px", "--hover-color": "#eff6ff"},
                "nav-link-selected": {"background-color": "#dbeafe", "color": "#1e40af"},
            }
        )
        st.sidebar.markdown("---")
        st.sidebar.info(f"**Versi:** {__version__}\n\n*Dibangun oleh MS Hadi - Email: [sopian.hadianto@gmail.com]*")

    # Guard clause jika koneksi Firebase gagal
    if db is None:
        st.error("Aplikasi tidak dapat berjalan tanpa koneksi database. Harap periksa konfigurasi `secrets.toml` Anda.")
        return

    # Routing Halaman
    if selected == "Beranda":
        show_home()
    elif selected == "Buat Laporan":
        create_report()
    elif selected == "Lacak & Komunikasi":
        show_communication_page()
    elif selected == "Dashboard":
        show_dashboard()
    elif selected == "Kelola Laporan":
        manage_reports()
    elif selected == "Bantuan":
        show_help()

if __name__ == "__main__":
    main()
