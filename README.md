# Jejak Fluktuasi Penumpang Kereta Api Evaluasi Tingkat Permintaan Layanan Berbasis Python


# # Jejak Fluktuasi Penumpang Kereta Api: Evaluasi Tingkat Permintaan Layanan Berbasis Python

Program berbasis Python untuk mengevaluasi tingkat permintaan layanan penumpang kereta api melalui autentikasi pengguna(regritrasi dan login), pemodelan prediksi berbasis **statistika regresi**, serta identifikasi data berfluktuasi tinggi menggunakan **MAD (*Mean Absolute Deviation*)**.  Program ini dirancang untuk mengelola data penumpang kereta api dari _file_ CSV untuk memprediksi fluktasi penumpang di bulan mendatang dan mengevaluasi dan menidaklanjuti jumlah penumpang pada bulan-bulan sebelumnya. Program ini juga dirancang untuk regristrasi dan login untuk menjaga rahasia operasional aplikasi

## Struktur Repositori

- `mini_project_8b.py` — Skrip utama aplikasi yang menangani alur registrasi/login, pemrosesan data CSV, perhitungan regresi, dan analisis fluktuasi MAD.
- `iheq5zumsgcil03ixtjf.csv` — Dataset data penumpang/permintaan layanan kereta api yang dianalisis.
- `requirements.txt` — Daftar pustaka (*library*) Python yang dibutuhkan untuk menjalankan program.
- `README.md` — Dokumentasi proyek dan panduan penggunaan.

## Fitur Utama & Alur Kerja

1. **Registrasi dan Login**
   - Pengguna dapat mendaftarkan akun baru dan melakukan *login* untuk masuk ke menu utama pengolahan data.
   - Membatasi akses fitur analisis agar alur penggunaan program lebih terstruktur.

2. **Prediksi Permintaan dengan Statistika Regresi**
   - Mengolah data historis dari berkas CSV untuk membentuk persamaan regresi.
   - Digunakan untuk memperkirakan tren dan proyeksi tingkat permintaan layanan penumpang.

3. **Deteksi Fluktuasi Tinggi dengan MAD (*Mean Absolute Deviation*)**
   - Menghitung rata-rata deviasi absolut dari data terhadap nilai acuan/rata-rata untuk mengukur tingkat penyebaran data.
   - Memudahkan identifikasi titik atau periode data yang mengalami fluktuasi tinggi sehingga perlu perhatian lebih dalam evaluasi layanan.

## Cara Menjalankan Program

1. **Clone repositori** ke komputer lokal:
   ```bash
   git clone [https://github.com/ferlds-45/Mini-Project-8B.git](https://github.com/ferlds-45/Mini-Project-8B.git)
   cd Mini-Project-8B
