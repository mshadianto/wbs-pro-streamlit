<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTF1a2s2YXAzZmpmbjloejZ3d2IzZ2I4bnd4ejJ4ajVwMm5pczFwMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oKIPc07HWE3pAGAlq/giphy.gif" alt="Security Shield Animation" width="200"/>
  <h1>🛡️ WBS Pro - Sistem Whistleblowing Modern 🛡️</h1>
  <p><strong>Platform Pelaporan Pelanggaran Generasi Berikutnya dengan Chat Real-time, Analisis Risiko AI, dan Jaminan Anonimitas Penuh.</strong></p>

  <!-- Dynamic Badges -->
  <p>
    <img src="https://img.shields.io/github/stars/mshadianto/wbs-pro-streamlit?style=for-the-badge&logo=github&color=3b82f6" alt="Bintang GitHub"/>
    <img src="https://img.shields.io/github/forks/mshadianto/wbs-pro-streamlit?style=for-the-badge&logo=github&color=60a5fa" alt="Fork GitHub"/>
    <img src="https://img.shields.io/github/last-commit/mshadianto/wbs-pro-streamlit?style=for-the-badge&logo=git&color=1e293b" alt="Commit Terakhir"/>
    <img src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge" alt="Lisensi"/>
  </p>
</div>

---

## 🚀 Demo Aplikasi Langsung

Coba langsung aplikasi WBS Pro yang sudah di-deploy! Rasakan pengalaman melaporkan secara aman dan berkomunikasi secara *real-time*.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_blue_light.svg)](https://wbs-pro-streamlit.streamlit.app/)
*(Ganti dengan URL aplikasi Anda jika berbeda)*

<br>

<div align="center">
  <img src="https://placehold.co/800x450/f0f2f6/3b82f6?text=Screenshot+Aplikasi+WBS+Pro&font=poppins" alt="Screenshot Aplikasi WBS Pro"/>
</div>

---

## ✨ Tentang Proyek Ini

**WBS Pro** bukan sekadar sistem pelaporan biasa. Ini adalah sebuah ekosistem lengkap yang dirancang untuk membangun budaya transparansi dan integritas. Kami memahami bahwa keberanian untuk berbicara memerlukan jaminan keamanan dan kemudahan. Oleh karena itu, WBS Pro mengintegrasikan teknologi canggih untuk memberikan pengalaman pelaporan yang aman, anonim, dan interaktif.

Dari analisis risiko laporan menggunakan AI hingga komunikasi dua arah secara *real-time* antara pelapor dan pengelola, WBS Pro adalah solusi definitif untuk organisasi modern yang serius dalam memberantas pelanggaran.

### Fitur Unggulan

* 💬 **Komunikasi Real-time:** Pelapor dapat berinteraksi langsung dengan pengelola secara anonim melalui ID Laporan unik, memungkinkan klarifikasi dan tindak lanjut yang efektif.
* 🤖 **Analisis Risiko AI:** Setiap laporan secara otomatis dianalisis untuk menghasilkan skor risiko, membantu tim investigasi memprioritaskan kasus paling krusial.
* 🤫 **Anonimitas Absolut:** Identitas pelapor terlindungi sepenuhnya. Pelapor dapat mengirimkan laporan tanpa rasa takut akan pembalasan.
* 📊 **Dashboard Analitik:** Pantau tren, distribusi kasus, dan metrik penting lainnya melalui dashboard yang interaktif dan mudah dipahami.
* 🎨 **UI/UX Modern:** Antarmuka yang bersih, profesional, dan responsif dengan tema terang yang nyaman di mata.
* 🔒 **Keamanan Terjamin:** Dibangun dengan database Firebase Firestore yang andal dan aman untuk menyimpan semua data laporan dan percakapan.

---

## 🛠️ Teknologi yang Digunakan

Proyek ini dibangun menggunakan teknologi Python modern yang handal:

| Teknologi | Deskripsi |
| :--- | :--- |
| **Python** | Bahasa pemrograman utama untuk semua logika aplikasi. |
| **Streamlit** | Framework untuk membangun dan men-deploy antarmuka pengguna web interaktif dengan cepat. |
| **Pandas** | Digunakan untuk manipulasi dan analisis data laporan di dashboard. |
| **Firebase Firestore** | Database NoSQL dari Google yang digunakan untuk penyimpanan data laporan dan chat secara *real-time*. |
| **Streamlit Option Menu** | Untuk menciptakan navigasi sidebar yang lebih baik dan menarik secara visual. |

---

## ⚙️ Instalasi & Menjalankan Secara Lokal

Ingin menjalankan proyek ini di komputer Anda? Ikuti langkah-langkah mudah berikut:

1.  **Clone Repositori**
    ```bash
    git clone [https://github.com/mshadianto/wbs-pro-streamlit.git](https://github.com/mshadianto/wbs-pro-streamlit.git)
    cd wbs-pro-streamlit
    ```

2.  **Buat & Aktifkan Virtual Environment** (Sangat Direkomendasikan)
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
    
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Library yang Dibutuhkan**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Kredensial Firebase (PENTING!)**
    Aplikasi ini membutuhkan koneksi ke Firebase.
    * Di dalam folder proyek Anda, buat folder baru bernama **`.streamlit`**.
    * Di dalam folder `.streamlit`, buat file baru bernama **`secrets.toml`**.
    * Buka file tersebut dan isi dengan kredensial dari file JSON yang Anda unduh dari Firebase, seperti contoh di bawah:
        ```toml
        [firebase_credentials]
        type = "service_account"
        project_id = "NAMA_PROYEK_ANDA"
        private_key_id = "ID_KUNCI_PRIVAT_ANDA"
        private_key = """-----BEGIN PRIVATE KEY-----\nKUNCI_PRIVAT_PANJANG_ANDA_DISINI\n-----END PRIVATE KEY-----\n"""
        client_email = "EMAIL_SERVICE_ACCOUNT_ANDA"
        # ...dan seterusnya sesuai isi file JSON Anda.
        ```

5.  **Jalankan Aplikasi Streamlit**
    ```bash
    streamlit run app.py
    ```
    Aplikasi akan secara otomatis terbuka di browser default Anda!

---

## 🤝 Kontribusi

Kontribusi Anda sangat kami hargai! Jika Anda memiliki ide untuk perbaikan atau menemukan bug, silakan:
1.  Fork repositori ini.
2.  Buat *branch* baru (`git checkout -b fitur-keren-baru`).
3.  Lakukan perubahan dan *commit* (`git commit -m 'Menambahkan fitur keren baru'`).
4.  Push ke *branch* Anda (`git push origin fitur-keren-baru`).
5.  Buka sebuah *Pull Request*.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License**.

---

<div align="center">
  <p><strong>Dibangun dengan ❤️ oleh MS Hadianto</strong></p>
</div>
