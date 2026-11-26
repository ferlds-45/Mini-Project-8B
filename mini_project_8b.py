# Memasukkan library csv dan statistics
import csv
import statistics

# Nama file CSV default
FILE_CSV = "iheq5zumsgcil03ixtjf.csv"


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


# Fungsi gabungan: proses regresi + peramalan + output
def proses_peramalan_output(data_valid, data_invalid, bulan_ke):
    x_data = []
    y_data = []
    for i in range(len(data_valid)):
        x_data.append(float(i + 1))
        y_data.append(float(data_valid[i]["Penumpang"]))

    if len(x_data) == 0:
        return [], "Tidak ada data valid untuk diproses.", 0.0

    mean_y = statistics.mean(y_data)
    mean_x = statistics.mean(x_data)

    atas = 0.0
    bawah = 0.0
    for i in range(len(x_data)):
        atas += (x_data[i] - mean_x) * (y_data[i] - mean_y)
        bawah += (x_data[i] - mean_x) ** 2

    b = (atas / bawah) if bawah != 0 else 0.0
    a = mean_y - (b * mean_x)

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

    print("\nTABEL OUTPUT REGRESI DAN KLASIFIKASI")
    print("Periode | Tahun | Bulan | Aktual     | Prediksi   | Selisih    | Kategori")
    for baris in tabel_evaluasi:
        print(
            f"{baris['periode']:<7} | {baris['tahun']:<5} | {baris['bulan']:<5} | "
            f"{baris['aktual']:>10,.0f} | {baris['prediksi']:>10,.2f} | "
            f"{baris['selisih']:>10,.2f} | {baris['kategori']}"
        )

    print("\nRINGKASAN DAN KESIMPULAN:")
    print(kesimpulan)
    return tabel_evaluasi, kesimpulan, prediksi

# Class Utama
class AplikasiPenumpang:
    def __init__(self, nama_file):
        self.nama_file = nama_file
        self.akun = {"admin": {"sandi": "1234", "peran": "Pengelola"}}
        self.pengguna_aktif = ""
        self.riwayat = []

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
                    print("Registrasi berhasil. Akun aktif:", user_baru)
                    break

            elif pilih == "2":
                user = input("Username: ").strip()
                sandi = input("Password: ").strip()
                if user in self.akun and self.akun[user]["sandi"] == sandi:
                    self.pengguna_aktif = user
                    print("Login berhasil. Selamat datang,", user)
                    break
                else:
                    print("Username atau password salah.")

            else:
                print("Pilihan tidak valid.")

       def jalankan_perhitungan_utama(self, bulan_ke):
        data_v, data_inv = validasi(self.nama_file)
        if len(data_v) == 0:
            print("Tidak ada data valid untuk diproses.")
            return

        tabel_eval, ringkasan, prediksi_val = proses_peramalan_output(
            data_v, data_inv, bulan_ke
        )
        self.riwayat.append({
            "pengguna": self.pengguna_aktif,
            "bulan_ke": bulan_ke,
            "prediksi": prediksi_val,
            "ringkasan": ringkasan,
        })
        return tabel_eval, ringkasan

    # Menu 1: Peramalan Penumpang
    def menu_satu_peramalan(self):
        print("\nMENU 1 PERAMALAN PENUMPANG")
        try:
            bulan_ke = int(
                input("Masukkan Bulan ke Berapa Setelah Desember 2025 (Januari 2026 = 1): ").strip()
            )
            if bulan_ke <= 0:
                print("Angka bulan harus lebih dari 0.")
                return
            self.jalankan_perhitungan_utama(bulan_ke)
        except ValueError:
            print("Input harus berupa angka bulat.")

    # Menu 2: Riwayat Peramalan dan Statistik
    def menu_dua_riwayat_dan_statistik(self):
        print("\nMENU 2 RIWAYAT PERAMALAN DAN STATISTIK")
        print("Pengguna aktif:", self.pengguna_aktif)
        print("Jumlah riwayat prediksi:", len(self.riwayat))
        for idx, item in enumerate(self.riwayat, start=1):
            print(
                f"{idx}. [{item['pengguna']}] Bulan ke-{item['bulan_ke']} -> "
                f"Prediksi: {item['prediksi']:,.2f}"
            )

    def mulai(self):
        while True:
            self.registrasi_atau_login()
            self.jalankan_perhitungan_utama(1)

            while True:
                print("\n=== MENU UTAMA ===")
                print("1. Peramalan Jumlah Penumpang")
                print("2. Riwayat Peramalan dan Statistik")
                print("0. Keluar")
                pilihan = input("Pilih menu (0/1/2): ").strip()

                if pilihan == "1":
                    self.menu_satu_peramalan()
                elif pilihan == "2":
                    self.menu_dua_riwayat_dan_statistik()
                elif pilihan == "0":
                    print("\nAnda keluar dari sesi akun:", self.pengguna_aktif)
                    print("1. Kembali ke Portal Registrasi / Login")
                    print("2. Tutup Program")
                    opsi_keluar = input("Pilih (1/2): ").strip()

                    if opsi_keluar == "1":
                        self.pengguna_aktif = ""
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
