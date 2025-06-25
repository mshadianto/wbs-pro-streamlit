# -*- coding: utf-8 -*-
"""
WBS Pro – Advanced Whistleblowing System with Real-time Chat
Version 1.8.1: Fixed Landing Page Rendering and Login Logic
Original Author: MS Hadianto
Enhancements by Gemini: 2025-06-25
"""

import streamlit as st
import pandas as pd
import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_option_menu import option_menu
import bcrypt
import os

# -------------------------------------------------------------
# Konfigurasi Halaman & CSS (WAJIB JADI YANG PERTAMA)
# -------------------------------------------------------------
st.set_page_config(
    page_title="WBS Pro - Sistem Whistleblowing",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed", # Sembunyikan sidebar di landing page
)

def load_css():
    """Memuat CSS kustom untuk tampilan aplikasi."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        /* General Styles */
        body { font-family: 'Poppins', sans-serif; background-color: #f8fafc; }
        .main { color: #1e293b; }
        h1, h2, h3, h4, h5, h6 { color: #0f172a; font-weight: 700; }
        
        /* Hide sidebar on landing page */
        div[data-testid="stSidebar"] {
             display: none;
        }

        /* --- Landing Page Styles --- */
        .landing-container {
            padding: 0 !important;
            margin-top: -100px; /* Adjust to pull content up */
        }
        .hero-section {
            text-align: center;
            padding: 6rem 2rem;
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            color: white;
            border-bottom-left-radius: 40px;
            border-bottom-right-radius: 40px;
        }
        .hero-section h1 { font-size: 3.5rem; font-weight: 700; color: white; margin-bottom: 1rem; }
        .hero-section .logo { font-size: 4rem; margin-bottom: 1rem; }
        .hero-section p { font-size: 1.25rem; max-width: 700px; margin: auto; margin-bottom: 2rem; color: #dbeafe; }
        
        .content-section { padding: 4rem 2rem; max-width: 1200px; margin: auto; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 2rem; }
        .feature-card { background: #ffffff; border-radius: 16px; padding: 2.5rem; text-align: center; box-shadow: 0 8px 16px rgba(0,0,0,0.05); transition: all 0.3s ease; }
        .feature-card:hover { transform: translateY(-5px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); }
        .feature-card .icon { font-size: 3rem; color: #3b82f6; margin-bottom: 1rem; }
        
        .login-section .card { background: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0; padding: 2rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); }

    </style>
    """, unsafe_allow_html=True)

load_css()
__version__ = f"1.8.1.{datetime.date.today().strftime('%Y%m%d')}"

# -------------------------------------------------------------
# Inisialisasi Firebase & User Management
# -------------------------------------------------------------
@st.cache_resource
def initialize_firebase():
    """Inisialisasi Firebase & membuat user Super Admin jika belum ada."""
    try:
        if not firebase_admin._apps:
            creds_dict = st.secrets["firebase_credentials"].to_dict()
            creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
            cred = credentials.Certificate(creds_dict)
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        
        users_ref = db.collection('users')
        if not users_ref.limit(1).get():
            super_admin_username = st.secrets.app_secrets.get("default_super_admin_username", "admin")
            super_admin_password = st.secrets.app_secrets.get("default_super_admin_password", "admin123")
            hashed_password = bcrypt.hashpw(super_admin_password.encode('utf-8'), bcrypt.gensalt())
            admin_data = {"password_hash": hashed_password.decode('utf-8'), "role": "SUPER_ADMIN"}
            db.collection('users').document(super_admin_username).set(admin_data)
        return db
    except Exception as e:
        # Tampilkan error di halaman utama jika koneksi gagal
        st.error(f"Gagal koneksi ke Firebase: {e}", icon="🔥")
        return None

db = initialize_firebase()

# --- Fungsi Terkait Pengguna ---
def verify_user(db, username, password):
    if not db: return None
    user_ref = db.collection('users').document(username).get()
    if user_ref.exists:
        user_data = user_ref.to_dict()
        password_hash = user_data.get("password_hash").encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            return user_data.get("role")
    return None

# --- Fungsi-fungsi Terkait Chat ---
def send_message(report_id, sender, text):
    if db is None or not text.strip(): return
    chat_ref = db.collection('chats').document(report_id).collection('messages')
    chat_ref.add({'sender': sender, 'text': text, 'timestamp': firestore.SERVER_TIMESTAMP})

def get_messages(report_id):
    if db is None: return []
    messages_ref = db.collection('chats').document(report_id).collection('messages').order_by('timestamp')
    return [doc.to_dict() for doc in messages_ref.stream()]

def display_chat_interface(report_id, user_role, key_suffix=""):
    st.markdown(f"<h4>💬 Komunikasi untuk Laporan #{report_id}</h4>", unsafe_allow_html=True)
    messages = get_messages(report_id)
    for msg in messages:
        sender_role = msg.get('sender', 'Unknown')
        avatar_icon = "🧑‍💻" if sender_role == "PELAPOR" else "🛡️"
        with st.chat_message(name=sender_role, avatar=avatar_icon):
            st.write(msg.get('text', ''))
            
    prompt = st.chat_input("Ketik pesan Anda di sini...", key=f"chat_input_{report_id}_{key_suffix}")
    if prompt:
        send_message(report_id, user_role, prompt)
        st.rerun()

# -------------------------------------------------------------
# Fungsi Halaman Aplikasi (Setelah Login)
# -------------------------------------------------------------
def show_home():
    st.markdown("<h1>🛡️ Beranda Pelapor</h1>", unsafe_allow_html=True)
    st.markdown("Gunakan menu di samping untuk membuat laporan baru atau melacak laporan Anda.")

def create_report():
    st.markdown("<h3>📝 Buat Laporan Baru</h3>", unsafe_allow_html=True)
    with st.form("report_form"):
        nama = st.text_input("Nama Pelapor", placeholder="Kosongkan untuk tetap anonim")
        jenis = st.selectbox("Jenis Pelanggaran", ["Korupsi", "Penyalahgunaan Wewenang", "Pelanggaran Etika", "Penipuan (Fraud)", "Pelecehan", "Lainnya"])
        detail = st.text_area("Uraian Kronologi Kejadian", height=200, placeholder="Jelaskan detail kejadian secara rinci...")
        if st.form_submit_button("📤 Kirim Laporan Secara Aman", use_container_width=True):
            report_id = str(uuid.uuid4())[:8].upper()
            report_data = {
                "id": report_id, "nama": nama or "Anonim", "jenis_pelanggaran": jenis, "detail": detail,
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "Baru",
            }
            if db:
                db.collection('reports').document(report_id).set(report_data)
                st.success(f"✅ Laporan berhasil dikirim! ID Laporan Anda: **{report_id}**")
                st.balloons()

def show_communication_page():
    st.markdown("<h3> Lacak & Komunikasi</h3>", unsafe_allow_html=True)
    report_id_input = st.text_input("Masukkan ID Laporan Anda:", placeholder="Contoh: A1B2C3D4").upper()
    if st.button("Cari Laporan"):
        if report_id_input and db:
            report_ref = db.collection('reports').document(report_id_input).get()
            st.session_state.active_report_id = report_id_input if report_ref.exists else None
            if not report_ref.exists: st.error("ID Laporan tidak ditemukan.")
    if st.session_state.get('active_report_id'):
        display_chat_interface(st.session_state.active_report_id, user_role="PELAPOR", key_suffix="pelapor")

def manage_reports():
    st.markdown("<h3>📂 Kelola & Tindak Lanjuti Laporan</h3>", unsafe_allow_html=True)
    if db:
        reports = sorted([doc.to_dict() for doc in db.collection('reports').stream()], key=lambda x: x.get('timestamp', ''), reverse=True)
        if not reports: st.info("Belum ada laporan yang masuk.")
        for report in reports:
            with st.expander(f"📄 **ID:** {report['id']} | **Jenis:** {report.get('jenis_pelanggaran', 'N/A')}"):
                display_chat_interface(report['id'], user_role="PENGELOLA", key_suffix=f"pengelola_{report['id']}")

def show_dashboard():
    st.markdown("<h3>📊 Dashboard Analitik Laporan</h3>", unsafe_allow_html=True)
    if db:
        reports = [doc.to_dict() for doc in db.collection('reports').stream()]
        if not reports: st.info("Belum ada data laporan untuk ditampilkan.")
        else:
            df = pd.DataFrame(reports)
            st.markdown("<h4>Distribusi Jenis Pelanggaran</h4>", unsafe_allow_html=True)
            st.bar_chart(df["jenis_pelanggaran"].value_counts())

def manage_users():
    st.markdown("<h3>👑 Manajemen Pengguna</h3>", unsafe_allow_html=True)
    if db:
        users = [{"username": user.id, "role": user.to_dict().get("role")} for user in db.collection('users').stream()]
        st.dataframe(pd.DataFrame(users).set_index("username"), use_container_width=True)
    with st.form("add_user_form", clear_on_submit=True):
        st.markdown("<h4>Tambah Pengguna Baru</h4>", unsafe_allow_html=True)
        new_username = st.text_input("Username Baru")
        new_password = st.text_input("Password Baru", type="password")
        if st.form_submit_button("Tambah Pengguna 'Pengelola'", use_container_width=True):
            if new_username and new_password:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                user_data = {"password_hash": hashed_password.decode('utf-8'), "role": "PENGELOLA"}
                db.collection('users').document(new_username).set(user_data)
                st.success(f"Pengguna '{new_username}' berhasil ditambahkan.")
                st.rerun()
            else: st.error("Username dan Password harus diisi.")

def show_help():
    st.markdown("<h3>ℹ️ Bantuan</h3>", unsafe_allow_html=True)
    st.info("Halaman ini berisi informasi bantuan dan panduan penggunaan aplikasi.")

def show_footer():
    year = datetime.date.today().year
    st.markdown(f"<div style='text-align: center; padding: 2rem; color: #64748b;'><p><b>WBS Pro v{__version__}</b> &copy; {year} | Dibuat oleh <b>MS Hadianto</b></p></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# Fungsi Halaman Depan (Landing Page & Login) DIPERBAIKI
# -------------------------------------------------------------
def show_landing_page():
    # Bagian 1: Hero Section (HTML Murni)
    st.markdown("""
        <div class="landing-container">
            <section class="hero-section">
                <div class="logo">🛡️</div>
                <h1>WBS Pro</h1>
                <p>Laporkan Pelanggaran dengan Aman dan Anonim. Wujudkan Lingkungan Kerja yang Berintegritas.</p>
            </section>
    """, unsafe_allow_html=True)

    # Bagian 2: Features Section (HTML Murni)
    st.markdown("""
            <section class="content-section">
                <h2 style="text-align:center; margin-bottom: 3rem;">Mengapa WBS Pro Penting?</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="icon">🔒</div>
                        <h3>Anonimitas Terjamin</h3>
                        <p>Identitas Anda terlindungi sepenuhnya. Laporkan tanpa rasa khawatir.</p>
                    </div>
                    <div class="feature-card">
                        <div class="icon">💬</div>
                        <h3>Komunikasi Aman</h3>
                        <p>Berkomunikasi langsung dengan tim investigasi melalui saluran terenkripsi.</p>
                    </div>
                    <div class="feature-card">
                        <div class="icon">📈</div>
                        <h3>Proses Transparan</h3>
                        <p>Lacak status laporan Anda kapan saja untuk mengetahui perkembangannya.</p>
                    </div>
                </div>
            </section>
    """, unsafe_allow_html=True)

    # Bagian 3: Video Section (Komponen Streamlit Asli)
    with st.container():
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center; margin-bottom: 2rem;">Video Pengantar</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; max-width: 700px; margin: auto; margin-bottom: 2rem;">Pahami lebih dalam mengenai pentingnya whistleblowing melalui video berikut.</p>', unsafe_allow_html=True)
        st.video("https://youtu.be/wAeGnDx5Ex8?si=5Kzz09nx6jKb0Cpk")
        st.markdown('</div>', unsafe_allow_html=True)

    # Bagian 4: Login Section (Komponen Streamlit Asli)
    with st.container():
        st.markdown('<section id="login" class="content-section login-section">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center; margin-bottom: 2rem;">Pilih Akses Anda</h2>', unsafe_allow_html=True)
        
        _, center_col, _ = st.columns([1, 1.5, 1])
        with center_col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["Portal Pelapor", "Portal Internal"])

            with tab1:
                st.markdown("<h3 style='text-align: center;'>Masuk sebagai Pelapor</h3>", unsafe_allow_html=True)
                st.markdown("Gunakan portal ini untuk membuat atau melacak laporan secara anonim.", unsafe_allow_html=True)
                if st.button("Lanjutkan sebagai Pelapor", use_container_width=True, key="reporter_login"):
                    st.session_state.role = "PELAPOR"
                    st.session_state.logged_in = True
                    st.rerun()

            with tab2:
                st.markdown("<h3 style='text-align: center;'>Login Internal</h3>", unsafe_allow_html=True)
                username = st.text_input("Username", key="internal_username")
                password = st.text_input("Password", type="password", key="internal_password")
                if st.button("Login", use_container_width=True, key="internal_login"):
                    role = verify_user(db, username, password)
                    if role:
                        st.session_state.role = role
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Username atau password salah.")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</section>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Menutup .landing-container

# -------------------------------------------------------------
# Router & Eksekusi Utama
# -------------------------------------------------------------
def main():
    if not st.session_state.get("logged_in"):
        show_landing_page()
        return

    # Jika sudah login, tampilkan sidebar
    st.markdown('<style>div[data-testid="stSidebar"] { display: block; }</style>', unsafe_allow_html=True)
    
    role = st.session_state.get("role")
    
    if role == "SUPER_ADMIN":
        options, icons = ["Manajemen Pengguna", "Dashboard", "Kelola Laporan", "Bantuan"], ["people-fill", "bar-chart-line-fill", "folder-fill", "info-circle-fill"]
    elif role == "PENGELOLA":
        options, icons = ["Dashboard", "Kelola Laporan", "Bantuan"], ["bar-chart-line-fill", "folder-fill", "info-circle-fill"]
    else: # PELAPOR
        options, icons = ["Beranda", "Buat Laporan", "Lacak & Komunikasi", "Bantuan"], ["house-door-fill", "pencil-square", "chat-dots-fill", "info-circle-fill"]

    with st.sidebar:
        display_role = role.replace("_", " ").title()
        st.markdown(f"<h2 style='text-align: center;'>🛡️ WBS Pro</h2><p style='text-align:center;'>Mode: {display_role}</p>", unsafe_allow_html=True)
        selected = option_menu(menu_title=None, options=options, icons=icons, default_index=0)
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

    if db is None:
        st.error("Koneksi database gagal. Aplikasi tidak bisa berjalan.")
        return

    page_functions = {"Beranda": show_home, "Buat Laporan": create_report, "Lacak & Komunikasi": show_communication_page, "Dashboard": show_dashboard, "Kelola Laporan": manage_reports, "Manajemen Pengguna": manage_users, "Bantuan": show_help}
    if selected in page_functions:
        page_functions[selected]()

    show_footer()

if __name__ == "__main__":
    main()
