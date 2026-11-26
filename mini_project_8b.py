# Memasukkan library csv dan statistics
import csv
import datetime
import statistics

# Nama file CSV default
FILE_CSV = "iheq5zumsgcil03ixtjf.csv"

REFERENSI_ERROR = {
    "Moving Average 3 Bulan": {
        "MAD": 435.0,
        "MSE": 317750.2,
        "MAPE": 0.060121,
    },
    "Exponential Smoothing alpha=0.6": {
        "MAD": 387.163,
        "MSE": 261914.1,
        "MAPE": 0.055349,
    },
}

# Fungsi penyaring data
def validasi(nama_file):
    data_v = []
    data_inv = 0
    try:
        with open(nama_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    tahun_str = str(row["Tahun"]).strip()
                    bulan_str = str(row["Bulan"]).strip()
                    penumpang_str = str(row["Penumpang"]).strip()

                    if not tahun_str or not bulan_str or not penumpang_str:
                        data_inv += 1
                        continue

                    tahun_val = int(tahun_str)
                    penumpang_val = float(penumpang_str)

                    if penumpang_val < 0:
                        data_inv += 1
                        continue

                    data_v.append({
                        "Tahun": tahun_val,
                        "Bulan": bulan_str,
                        "Penumpang": penumpang_val,
                    })
                except (KeyError, ValueError, TypeError):
                    data_inv += 1
    except FileNotFoundError:
        print("File Tidak Ditemukan : Pastikan Penulisan Nama File CSV Sudah Benar!")
    return data_v, data_inv

def kategori_permintaan(jumlah, rata_rata):
    if jumlah < rata_rata * 0.75:
        return "Rendah"
    elif jumlah <= rata_rata * 1.15:
        return "Sedang"
    else:
        return "Tinggi"

def saran_kuota_kursi(aktual, rata_rata, kategori):
    if kategori == "Tinggi" or aktual > rata_rata * 1.15:
        return "PERINGATAN: Jumlah penumpang melonjak! Tambah kuota kursi untuk mencukupi permintaan penumpang."
    elif kategori == "Rendah" or aktual < rata_rata * 0.75:
        return "SARAN: Permintaan penumpang rendah, sesuaikan kuota kursi agar kapasitas tidak berlebih."
    else:
        return "AMAN: Permintaan penumpang stabil, pertahankan kuota kursi sesuai jadwal reguler."



# Fungsi gabungan: proses regresi + peramalan + output
def hitung_regresi(x_data, y_data):
    mean_x = statistics.mean(x_data)
    mean_y = statistics.mean(y_data)

    atas = sum((x_data[i] - mean_x) * (y_data[i] - mean_y) for i in range(len(x_data)))
    bawah = sum((x_data[i] - mean_x) ** 2 for i in range(len(x_data)))

    b = (atas / bawah) if bawah != 0 else 0.0
    a = mean_y - (b * mean_x)
    return mean_x, mean_y, a, b

def evaluasi_error_regresi(y_data, a, b):
    abs_errors = []
    sq_errors = []
    pct_errors = []
    prediksi_list = []

    for i in range(len(y_data)):
        periode = float(i + 1)
        aktual = y_data[i]
        pred = a + b * periode
        prediksi_list.append(pred)

        err_abs = abs(aktual - pred)
        abs_errors.append(err_abs)
        sq_errors.append((aktual - pred) ** 2)
        if aktual != 0:
            pct_errors.append(err_abs / aktual)

    mad = statistics.mean(abs_errors) if abs_errors else 0.0
    mse = statistics.mean(sq_errors) if sq_errors else 0.0
    mape = statistics.mean(pct_errors) if pct_errors else 0.0
    return prediksi_list, mad, mse, mape

def evaluasi_moving_average_3_bulan(y_data):
    forecast_list = [None] * len(y_data)
    abs_errors = []
    sq_errors = []
    pct_errors = []

    for i in range(len(y_data)):
        if i >= 3:
            jumlah_3_bulan = y_data[i - 3] + y_data[i - 2] + y_data[i - 1]
            ma_3 = jumlah_3_bulan / 3.0
            forecast_list[i] = ma_3

            aktual = y_data[i]
            err_abs = abs(aktual - ma_3)
            abs_errors.append(err_abs)
            sq_errors.append((aktual - ma_3) ** 2)
            if aktual != 0:
                pct_errors.append(err_abs / aktual)

    mad = statistics.mean(abs_errors) if abs_errors else 0.0
    mse = statistics.mean(sq_errors) if sq_errors else 0.0
    mape = statistics.mean(pct_errors) if pct_errors else 0.0
    return forecast_list, mad, mse, mape

def proses_evaluasi_dan_output(data_valid, data_invalid):
    x_data = [float(i + 1) for i in range(len(data_valid))]
    y_data = [float(item["Penumpang"]) for item in data_valid]

    if not y_data:
        print("Tidak ada data valid untuk diproses.")
        return None

    _, mean_y, a, b = hitung_regresi(x_data, y_data)
    pred_regresi, mad_reg, mse_reg, mape_reg = evaluasi_error_regresi(y_data, a, b)
    ma3_forecast, mad_ma3, mse_ma3, mape_ma3 = evaluasi_moving_average_3_bulan(y_data)

    tabel_evaluasi = []
    for i in range(len(data_valid)):
        aktual = y_data[i]
        reg_val = pred_regresi[i]
        ma_val = ma3_forecast[i]
        selisih_reg = aktual - reg_val
        selisih_ma = (aktual - ma_val) if ma_val is not None else None
        kategori = kategori_permintaan(aktual, mean_y)
        peringatan = saran_kuota_kursi(aktual, mean_y, kategori)

        tabel_evaluasi.append({
            "periode": i + 1,
            "tahun": data_valid[i]["Tahun"],
            "bulan": data_valid[i]["Bulan"],
            "aktual": aktual,
            "regresi": reg_val,
            "selisih_reg": selisih_reg,
            "ma_3": ma_val,
            "selisih_ma": selisih_ma,
            "kategori": kategori,
            "peringatan_kuota": peringatan,
        })


    # Peramalan periode target
    periode_target = float(len(data_valid) + bulan_ke)
    prediksi = a + b * periode_target
    kategori_prediksi = kategori_permintaan(prediksi, mean_y)

    # Evaluasi data historis
    tabel_evaluasi = []
    for i in range(len(data_valid)):
        periode = float(i + 1)
        y_aktual = float(data_valid[i]["Penumpang"])
        y_prediksi = a + b * periode
        selisih = y_aktual - y_prediksi
        status = kategori_permintaan(y_aktual, mean_y)
        tabel_evaluasi.append({
            "periode": int(periode),
            "tahun": data_valid[i]["Tahun"],
            "bulan": data_valid[i]["Bulan"],
            "aktual": y_aktual,
            "prediksi": y_prediksi,
            "selisih": selisih,
            "kategori": status,
        })

    kesimpulan = (
        f"Data valid: {len(data_valid)}, Data invalid: {data_invalid}, "
        f"Mean penumpang: {mean_y:,.2f}, Konstanta a: {a:,.4f}, Koefisien b: {b:,.4f}. "
        f"Prediksi bulan ke-{bulan_ke} setelah Desember 2025 adalah {prediksi:,.2f} "
        f"dengan kategori permintaan '{kategori_prediksi}'."
    )

    print("\nTABEL EVALUASI ERROR")
    print(
        "Per | Tahun | Bulan | Aktual     | Regresi    | MA-3 Bln   | Kategori | Peringatan / Saran Kuota Kursi"
    )
    print("-" * 125)
    for row in tabel_evaluasi:
        ma_str = f"{row['ma_3']:>10,.2f}" if row["ma_3"] is not None else f"{'N/A':>10}"
        print(
            f"{row['periode']:<3} | {row['tahun']:<5} | {row['bulan']:<5} | "
            f"{row['aktual']:>10,.0f} | {row['regresi']:>10,.2f} | "
            f"{ma_str} | {row['kategori']:<8} | {row['peringatan_kuota']}"
        )

    metode_terbaik = ("Regresi Linear" if mad_reg < mad_ma3 else "Moving Average 3 Bulan")

    print("\nRINGKASAN EVALUASI ERROR (MAD, MSE, MAPE)")
    print(f"Data Valid: {len(data_valid)} | Data Invalid: {data_invalid} | Mean Penumpang: {mean_y:,.2f}")
    print(f"Persamaan Regresi: Y = {a:,.4f} + ({b:,.4f})X")
    print("-" * 88)
    print(f"{'Metode Evaluasi':<42} | {'MAD':>12} | {'MSE':>14} | {'MAPE':>10}")
    print("-" * 88)
    print(f"{'Regresi Linear':<42} | {mad_reg:>12,.3f} | {mse_reg:>14,.2f} | {mape_reg:>10.6f}")
    print(f"{'Moving Average 3 Bulan':<42} | {mad_ma3:>12,.3f} | {mse_ma3:>14,.2f} | {mape_ma3:>10.6f}")
    for nama_metode, metrik in REFERENSI_ERROR.items():
        print(
            f"{nama_metode:<42} | {metrik['MAD']:>12,.3f} | "
            f"{metrik['MSE']:>14,.2f} | {metrik['MAPE']:>10.6f}"
        )
    print("-" * 88)

    kesimpulan = (
        f"Hasil evaluasi error menunjukkan {metode_terbaik} memiliki MAD lebih kecil pada data ini "
        f"(MAD Regresi: {mad_reg:,.3f} dibandingkan MAD Moving Average 3 Bulan: {mad_ma3:,.3f}). "
        f"Sebagai perbandingan literatur, Moving Average 3 bulan memiliki MAD 435,000 dan "
        f"Exponential Smoothing (alpha=0,6) memiliki MAD 387,163. "
        f"Gunakan baris berstatus 'Tinggi' sebagai acuan penambahan kuota kursi dan 'Rendah' untuk penyesuaian kapasitas."
    )
    print("\nKESIMPULAN DAN SARAN KUOTA PENUMPANG:")
    print(kesimpulan)

    return {
        "tabel": tabel_evaluasi,
        "mad_regresi": mad_reg,
        "mad_ma3": mad_ma3,
        "metode_terbaik": metode_terbaik,
        "kesimpulan": kesimpulan,
    }

# Class Utama
class AplikasiPenumpang:
    def _init_(self, nama_file):
        self.nama_file = nama_file
        self.akun = {
            "admin": {"sandi": "1234", "peran": "Pengelola"},
        }
        self.pengguna_aktif = ""
        self.peran_aktif = ""
        self.riwayat_penggunaan = []

    def catat_riwayat(self, aktivitas, detail=""):
        waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.riwayat_penggunaan.append({
            "waktu": waktu,
            "pengguna": self.pengguna_aktif or "Anonim",
            "peran": self.peran_aktif or "-",
            "aktivitas": aktivitas,
            "detail": detail,
        })

    # Portal Registrasi dan Login
    def registrasi_atau_login(self):
        while True:
            print("\nPORTAL REGISTRASI DAN LOGIN")
            print("1. Registrasi Akun Baru")
            print("2. Login")
            pilih = input("Pilih (1/2): ").strip()

            if pilih == "1":
                user_baru = input("Buat username baru: ").strip()
                sandi_baru = input("Buat password baru: ").strip()
                peran_baru = input("Peran atau unit: ").strip()
                if peran_baru == "":
                    peran_baru = "Pengguna"

                if user_baru == "" or sandi_baru == "":
                    print("Username dan password tidak boleh kosong.")
                elif user_baru in self.akun:
                    print("Username sudah terdaftar.")
                else:
                    self.akun[user_baru] = {"sandi": sandi_baru, "peran": peran_baru}
                    self.pengguna_aktif = user_baru
                    self.peran_aktif = peran_baru
                    self.catat_riwayat("Registrasi Akun", f"Akun baru '{user_baru}' peran '{peran_baru}'")
                    print("Registrasi berhasil. Akun aktif:", user_baru)
                    break

            elif pilih == "2":
                user = input("Username: ").strip()
                sandi = input("Password: ").strip()
                if user in self.akun and self.akun[user]["sandi"] == sandi:
                    self.pengguna_aktif = user
                    self.peran_aktif = self.akun[user]["peran"]
                    self.catat_riwayat("Login", f"Masuk sebagai '{user}' ({self.peran_aktif})")
                    print("Login berhasil. Selamat datang,", user)
                    break
                else:
                    print("Username atau password salah.")

            else:
                print("Pilihan tidak valid.")

    def jalankan_evaluasi(self):
        data_v, data_inv = validasi(self.nama_file)
        hasil = proses_evaluasi_dan_output(data_v, data_inv)
        if hasil:
            self.catat_riwayat(
                "Evaluasi Error dan Kuota",
                f"Terbaik: {hasil['metode_terbaik']} | MAD Reg: {hasil['mad_regresi']:,.2f} | MAD MA-3: {hasil['mad_ma3']:,.2f}",
            )

    def tampilkan_riwayat_penggunaan(self):
        print("\nRIWAYAT PENGGUNAAN SISTEM")
        print(f"Pengguna Aktif : {self.pengguna_aktif} ({self.peran_aktif})")
        print(f"Total Interaksi: {len(self.riwayat_penggunaan)}")
        print("-" * 100)
        if not self.riwayat_penggunaan:
            print("Belum ada riwayat penggunaan.")
            return
        for idx, item in enumerate(self.riwayat_penggunaan, start=1):
            print(
                f"{idx}. [{item['waktu']}] {item['pengguna']} ({item['peran']}) "
                f"-> {item['aktivitas']} | {item['detail']}"
            )

    def mulai(self):
        while True:
            self.registrasi_atau_login()
            self.jalankan_evaluasi()

            while True:
                print("\n=== MENU UTAMA ===")
                print("1. Jalankan Evaluasi Error Regresi vs Moving Average (3 Bulan)")
                print("2. Lihat Riwayat Penggunaan")
                print("0. Keluar")
                pilihan = input("Pilih menu (0/1/2): ").strip()

                if pilihan == "1":
                    self.jalankan_evaluasi()
                elif pilihan == "2":
                    self.catat_riwayat("Lihat Riwayat", "Membuka daftar riwayat penggunaan")
                    self.tampilkan_riwayat_penggunaan()
                elif pilihan == "0":
                    self.catat_riwayat("Logout / Keluar Sesi", f"Keluar dari akun '{self.pengguna_aktif}'")
                    print("\nAnda keluar dari sesi akun:", self.pengguna_aktif)
                    print("1. Kembali ke Portal Registrasi / Login")
                    print("2. Tutup Program")
                    opsi_keluar = input("Pilih (1/2): ").strip()

                    if opsi_keluar == "1":
                        self.pengguna_aktif = ""
                        self.peran_aktif = ""
                        break
                    elif opsi_keluar == "2":
                        print("Program selesai. Terima kasih!")
                        return
                    else:
                        print("Pilihan tidak valid, kembali ke Menu Utama.")
                else:
                    print("Pilihan tidak valid.")

# Pemanggil Fungsi
if __name__ == "__main__":
    aplikasi = AplikasiPenumpang(FILE_CSV)
    aplikasi.mulai()
