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
  #fungsi output
def output(data_valid, data_invalid, bulan_ke, mean):
  jumlah_data = len(data_valid[Bulan])
  


