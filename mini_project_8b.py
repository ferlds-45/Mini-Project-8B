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

#fungsi peramalan
def peramalan(a, b, bulan_ke):
  prediksi = a + b*bulan_ke
  return prediksi
  
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

#Pemanggil Fungsi
bulan_ke = (int("Masukkan Bulan ke Berapa Setelah Desember 2025 (Misalnya Januari 2026 = 1) : "
data_valid, data_invalid = validasi(FILE_CSV)
mean, a, b = proses(data_valid)
prediksi = peramalan(a,b)
tabel_evaluasi, kesimpulan = output(data_valid, data_invalid, bulan_ke, mean)


  





