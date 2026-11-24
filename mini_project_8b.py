#memasukkan library csv dan statistics
import csv
import statistics
#inisialisasisi csv dan penampung data
FILE_CSV = "iheq5zumsgcil03ixtjf.csv"
data_valid = []
data_invalid = 0
#fungsi penyaring data
def validasi(FILE_CSV):
  with open ("FILE CSV", mode = "r", encoding = "utf-8") as file:
    reader = csv.DictReader(file) 
    for row in reader:
      try:
        if not row["Tahun"] or not row["Bulan"] or not row["Penumpang"]:
          data_invalid += 1
          continue
        elif row["Penumpang"] < 0:
          data_invalid += 1
          continue
        else:
          data_valid.append(row)
      except ValueError, FileNotFoundError:
        pesan = "File Tidak Ditemukan : Pastikan Penulisan Nama File CSV Sudah Benar!"
  return data_valid, data_invalid

 def jalankan_perhitungan_utama(self, bulan_ke):
      data_v = []
      data_inv = 0
      with open(self.nama_file, mode="r", encoding="utf-8") as berkas:
          pembaca = csv.DictReader(berkas)
          for baris in pembaca:
              try:
                  tahun_val = int(baris["Tahun"])
                  bulan_val = str(baris["Bulan"]).strip()
                  penumpang_val = float(baris["Penumpang"])
                  if bulan_val == "" or penumpang_val < 0:
                      data_inv += 1
                  else:
                      data_v.append({
                          "Tahun": tahun_val,
                          "Bulan": bulan_val,
                          "Penumpang": penumpang_val })
              except (KeyError, ValueError, TypeError):
                    data_inv += 1

#fungsi proses
def proses(data_valid):
    x_data = []
    y_data = []
    for i in range(len(data_valid)):
        x_data.append(float(i + 1))
        y_data.append(float(data_valid[i]["Penumpang"]))

    if len(x_data) == 0:
        return 0.0, 0.0, 0.0

    mean_x = statistics.mean(x_data)
    mean_x = statistics.mean(x_data)

  atas = 0.0
  bawah = 0.0
  for i in range(len(x_data)):
      atas += (x_data[i] - mean_x) * (y_data[i] - mean_y)
      bawah += (x_data[i] - mean_x) ** 2            

  if bawah == 0:
      b = 0.0
  else:
      b = atas / bawah

  a = mean_y - (b * mean_x)
  return mean_y, a, b

      mean_val, a_val, b_val = proses(data_v)
      periode_target = float(len(data_v) + bulan_ke)

#fungsi peramalan
def peramalan(a, b, bulan_ke):
  prediksi = a + b*bulan_ke
  return prediksi

  kategori_prediksi = kategori_permintaan(prediksi, mean)
  kesimpulan = (
        f"Data valid: {len(data_valid)}, Data invalid: {data_invalid}, "
        f"Mean penumpang: {mean:,.2f}, Konstanta a: {a:,.4f}, Koefisien b: {b:,.4f}. "
        f"Prediksi bulan ke-{bulan_ke} setelah Desember 2025 adalah {prediksi:,.2f} "
        f"dengan kategori permintaan '{kategori_prediksi}'.")
  return tabel_evaluasi, kesimpulan

      prediksi_val = peramalan(a_val, b_val, periode_target)

#fungsi output
def kategori_permintaan(jumlah, rata_rata):
  if jumlah < rata_rata * 0.75:
      return "Rendah"
  elif jumlah <= rata_rata * 1.15:
      return "Sedang"
  else:
      return "Tinggi"

  def output(data_valid, data_invalid, bulan_ke, mean, a, b, prediksi):
    tabel_evaluasi = []
    for i in range(len(data_valid)):
      periode = float(i + 1)
      y_aktual = float(data_valid[i]["Penumpang"])
      y_prediksi = peramalan(a, b, periode)
      selisih = y_aktual - y_prediksi
      status = kategori_permintaan(y_aktual, mean)
      tabel_evaluasi.append({
          "periode": int(periode),
          "tahun": data_valid[i]["Tahun"],
          "bulan": data_valid[i]["Bulan"],
          "aktual": y_aktual,
          "prediksi": y_prediksi,
          "selisih": selisih,
          "kategori": status })

      tabel_eval, ringkasan = output(data_v, data_inv, bulan_ke, mean_val, a_val, b_val, prediksi_val)
        
    print("\nTABEL OUTPUT REGRESI DAN KLASIFIKASI (10 DATA PERTAMA)")
    print("Periode | Tahun | Bulan | Aktual     | Prediksi   | Selisih    | Kategori")
    for baris in tabel_evaluasi[:10]:
        print(f"{baris['periode']:<7} | {baris['tahun']:<5} | {baris['bulan']:<5} | "
              f"{baris['aktual']:>10,.0f} | {baris['prediksi']:>10,.2f} | "
              f"{baris['selisih']:>10,.2f} | {baris['kategori']}")

        print("\nRINGKASAN DAN KESIMPULAN:")
        print(ringkasan)
        self.riwayat.append({
            "bulan_ke": bulan_ke,
            "prediksi": prediksi_val,
            "ringkasan": ringkasan
        })
        return tabel_eval, ringkasan

#Pemanggil Fungsi
bulan_ke = (int("Masukkan Bulan ke Berapa Setelah Desember 2025 (Misalnya Januari 2026 = 1) : "
data_valid, data_invalid = validasi(FILE_CSV)
mean, a, b = proses(data_valid)
prediksi = peramalan(a,b)
tabel_evaluasi, kesimpulan = output(data_valid, data_invalid, bulan_ke, mean)

#Class Utama
class AplikasiPenumpang:
    def _init_(self, nama_file):
        self.nama_file = nama_file
        self.akun = {"admin": {"sandi": "1234", "peran": "Pengelola"}}
        self.pengguna_aktif = ""
        self.riwayat = []
#Fungsi Registrasi
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


