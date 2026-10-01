# Adım 3 — Veriyi ikiye böl: eğitim ve test
# Çalıştır: uv run ornekler/03_egitim_test.py

import csv
from sklearn.model_selection import train_test_split

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

X_egitim, X_test, y_egitim, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
print(len(X_egitim), len(X_test))
