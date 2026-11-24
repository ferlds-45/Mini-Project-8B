import csv
import statistics
FILE_CSV = 
def baca_validasi(FILE_CSV):
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
