import csv
import datetime
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

def peringatan_kuota_error(aktual, rata_rata, kategori, persen_error):
    if persen_error >= 25.0:
        tingkat = "SANGAT GENTING"
    elif persen_error >= 10.0:
        tingkat = "GENTING"
    elif persen_error > 0.0:
        tingkat = "WASPADA"
    else:
        tingkat = "OPTIMAL (0%)"

    if kategori == "Tinggi" or aktual > rata_rata * 1.15:
        aksi = "maka harus tambah kursi untuk mengantisipasi lonjakan penumpang"
    elif kategori == "Rendah" or aktual < rata_rata * 0.75:
        aksi = "maka sesuaikan/kurangi kuota kursi agar tidak terjadi kelebihan kapasitas"
    else:
        aksi = "maka pertahankan kuota kursi reguler"

    return f"Peringatan [{tingkat}, error {persen_error:.2f}%]: berdasarkan persentase error, {aksi}."

# Fungsi proses regresi, peramalan bulan ke-X, dan evaluasi error
def hitung_regresi(x_data, y_data):
    mean_x = statistics.mean(x_data)
    mean_y = statistics.mean(y_data)

    atas = sum((x_data[i] - mean_x) * (y_data[i] - mean_y) for i in range(len(x_data)))
    bawah = sum((x_data[i] - mean_x) ** 2 for i in range(len(x_data)))

    b = (atas / bawah) if bawah != 0 else 0.0
    a = mean_y - (b * mean_x)
    return mean_x, mean_y, a, b

def ramalkan_bulan_ke(data_valid, bulan_ke):
    x_data = [float(i + 1) for i in range(len(data_valid))]
    y_data = [float(item["Penumpang"]) for item in data_valid]

    if not y_data:
        return None

    _, mean_y, a, b = hitung_regresi(x_data, y_data)
    periode_target = float(len(data_valid) + bulan_ke)
    prediksi = a + b * periode_target
    kategori = kategori_permintaan(prediksi, mean_y)

    return {
        "bulan_ke": bulan_ke,
        "periode_target": int(periode_target),
        "prediksi": prediksi,
        "kategori": kategori,
    }

def evaluasi_error_regresi(y_data, a, b):
    prediksi_list = []
    selisih_list = []
    abs_pe_list = []
    persen_error_list = []

    for i in range(len(y_data)):
        periode = float(i + 1)
        aktual = y_data[i]
        pred = a + b * periode
        selisih = aktual - pred
        abs_pe = (abs(selisih) / aktual) if aktual != 0 else 0.0
        persen_error = abs_pe * 100.0

        prediksi_list.append(pred)
        selisih_list.append(selisih)
        abs_pe_list.append(abs_pe)
        persen_error_list.append(persen_error)

    rata_persen_error = statistics.mean(persen_error_list) if persen_error_list else 0.0
    rata_abs_pe = statistics.mean(abs_pe_list) if abs_pe_list else 0.0

    return prediksi_list, selisih_list, abs_pe_list, persen_error_list, rata_persen_error, rata_abs_pe

def proses_evaluasi_dan_output(data_valid, data_invalid):
    x_data = [float(i + 1) for i in range(len(data_valid))]
    y_data = [float(item["Penumpang"]) for item in data_valid]

    if not y_data:
        print("Tidak ada data valid untuk diproses.")
        return None

    _, mean_y, a, b = hitung_regresi(x_data, y_data)
    (
        pred_regresi,
        selisih_list,
        abs_pe_list,
        persen_error_list,
        rata_persen_error,
        rata_abs_pe,
    ) = evaluasi_error_regresi(y_data, a, b)

    tabel_evaluasi = []
    for i in range(len(data_valid)):
        aktual = y_data[i]
        reg_val = pred_regresi[i]
        selisih_reg = selisih_list[i]
        abs_pe_val = abs_pe_list[i]
        persen_err = persen_error_list[i]
        kategori = kategori_permintaan(aktual, mean_y)
        peringatan = peringatan_kuota_error(aktual, mean_y, kategori, persen_err)

        tabel_evaluasi.append({
            "periode": i + 1,
            "tahun": data_valid[i]["Tahun"],
            "bulan": data_valid[i]["Bulan"],
            "aktual": aktual,
            "regresi": reg_val,
            "selisih_reg": selisih_reg,
            "persen_error": persen_err,
            "abs_pe": abs_pe_val,
            "kategori": kategori,
            "peringatan": peringatan,
        })

    print("\nTABEL EVALUASI ERROR")
    print(
        "Periode | Tahun | Bulan | Aktual     | Regresi    | Selisih Reg | % Error  | |PE|     | Kategori | Peringatan"
    )
    print("-" * 140)
    for row in tabel_evaluasi:
        print(
            f"{row['periode']:<7} | {row['tahun']:<5} | {row['bulan']:<5} | "
            f"{row['aktual']:>10,.0f} | {row['regresi']:>10,.2f} | "
            f"{row['selisih_reg']:>+11,.2f} | {row['persen_error']:>7.2f}% | "
            f"{row['abs_pe']:>8.4f} | {row['kategori']:<8} | {row['peringatan']}"
        )

    print("\nRINGKASAN EVALUASI ERROR REGRESI")
    print(f"Data Valid: {len(data_valid)} | Data Invalid: {data_invalid} | Mean Penumpang: {mean_y:,.2f}")
    print(f"Persamaan Regresi: Y = {a:,.4f} + ({b:,.4f})X")
    print(f"Rata-rata Persentase Error: {rata_persen_error:.2f}% | Rata-rata |PE|: {rata_abs_pe:.4f}")

    kesimpulan = (
        f"Hasil evaluasi regresi menghasilkan rata-rata |PE| sebesar {rata_abs_pe:.4f} "
        f"dengan rata-rata persentase error {rata_persen_error:.2f}%. Semakin mendekati 0%, "
        f"akurasi semakin baik; semakin tinggi persentase error, semakin genting penyesuaian "
        f"kuota kursi sesuai kategori permintaan."
    )
    print("\nKESIMPULAN DAN SARAN KUOTA PENUMPANG:")
    print(kesimpulan)

    return {
        "tabel": tabel_evaluasi,
        "rata_persen_error": rata_persen_error,
        "rata_abs_pe": rata_abs_pe,
        "kesimpulan": kesimpulan,
    }

# Class Utama
class AplikasiFluktasiPenumpang:
    def __init__(self, nama_file):
        self.nama_file = nama_file
        self.akun = {
            "admin": {"sandi": "1234", "peran": "Pengelola"},
        }
        # Menyimpan akun yang sudah pernah login agar tidak perlu registrasi ulang
        self.sudah_pernah_login = set()
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
            if self.sudah_pernah_login:
                daftar_tersimpan = ", ".join(sorted(self.sudah_pernah_login))
                print(f"Akun tersimpan (sudah pernah login): {daftar_tersimpan}")
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
                elif user_baru in self.sudah_pernah_login:
                    print("Akun ini sudah pernah login sebelumnya, silakan langsung Login tanpa registrasi ulang.")
                elif user_baru in self.akun:
                    print("Username sudah terdaftar.")
                else:
                    self.akun[user_baru] = {"sandi": sandi_baru, "peran": peran_baru}
                    self.sudah_pernah_login.add(user_baru)
                    self.pengguna_aktif = user_baru
                    self.peran_aktif = peran_baru
                    self.catat_riwayat("Registrasi Akun", f"Akun baru '{user_baru}' peran '{peran_baru}'")
                    print("Registrasi berhasil. Akun aktif:", user_baru)
                    break

            elif pilih == "2":
                user = input("Username: ").strip()
                if user in self.sudah_pernah_login and user in self.akun:
                    # Akun yang sudah pernah login langsung masuk tanpa registrasi ulang
                    self.pengguna_aktif = user
                    self.peran_aktif = self.akun[user]["peran"]
                    self.catat_riwayat("Login Otomatis (Tersimpan)", f"Masuk sebagai '{user}' ({self.peran_aktif})")
                    print(f"Akun '{user}' sudah tersimpan (pernah login). Selamat datang kembali!")
                    break

                sandi = input("Password: ").strip()
                if user in self.akun and self.akun[user]["sandi"] == sandi:
                    self.sudah_pernah_login.add(user)
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
                f"Rata-rata |PE|: {hasil['rata_abs_pe']:.4f} | Rata-rata % Error: {hasil['rata_persen_error']:.2f}%",
            )

    def ramalkan_bulan(self):
        print("\nPERAMALAN JUMLAH PENUMPANG BULAN KE-X")
        try:
            bulan_ke = int(input("Masukkan bulan ke berapa setelah data terakhir (misal 1 = bulan depan): ").strip())
            if bulan_ke <= 0:
                print("Angka bulan harus lebih besar dari 0.")
                return
        except ValueError:
            print("Input harus berupa angka bulat.")
            return

        data_v, _ = validasi(self.nama_file)
        hasil = ramalkan_bulan_ke(data_v, bulan_ke)
        if not hasil:
            print("Tidak ada data valid untuk meramalkan.")
            return

        print(f"Periode ke-{hasil['periode_target']} (Bulan ke-{hasil['bulan_ke']} ke depan)")
        print(f"Perkiraan Penumpang : {hasil['prediksi']:,.2f}")
        print(f"Kategori Permintaan : {hasil['kategori']}")

        self.catat_riwayat(
            "Peramalan Bulan",
            f"Bulan ke-{hasil['bulan_ke']} (Per {hasil['periode_target']}) -> {hasil['prediksi']:,.2f} ({hasil['kategori']})",
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

            while True:
                print("\n=== MENU UTAMA ===")
                print("1. Jalankan Evaluasi Error Regresi")
                print("2. Lihat Riwayat Penggunaan")
                print("3. Ramalkan Jumlah Penumpang Bulan Ke-X")
                print("0. Keluar")
                pilihan = input("Pilih menu (0/1/2/3): ").strip()

                if pilihan == "1":
                    self.jalankan_evaluasi()
                elif pilihan == "2":
                    self.catat_riwayat("Lihat Riwayat", "Membuka daftar riwayat penggunaan")
                    self.tampilkan_riwayat_penggunaan()
                elif pilihan == "3":
                    self.ramalkan_bulan()
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
    aplikasi = AplikasiFluktasiPenumpang(FILE_CSV)
    aplikasi.mulai()
