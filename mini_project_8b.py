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
      if not row["Tahun"] or not row["Bulan"] or not row["Penumpang"]:
        data_invalid += 1
        continue
      elif row["Penumpang"] < 0:
        data_invalid += 1
        continue
      else:
        data_valid.append(row)
    return data_valid, data_invalid
    
#fungsi proses
def proses(data_valid):

#fungsi peramalan
def peramalan(a, b, bulan_ke):
  prediksi = a + b*bulan_ke
  return prediksi
  
#fungsi output
def output(data_valid, data_invalid, bulan_ke, mean):

#Pemanggil Fungsi
bulan_ke = (int("Masukkan Bulan ke Berapa Setelah Desember 2025 (Misalnya Januari 2026 = 1) : "
data_valid, data_invalid = validasi(FILE_CSV)
mean, a, b = proses(data_valid)
prediksi = peramalan(a,b)
tabel_evaluasi, kesimpulan = output(data_valid, data_invalid, bulan_ke, mean)

print(tabel_evaluasi)
print(kesimpulan)
print(prediksi)


  


