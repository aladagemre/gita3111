# Adım 2 — Rengi sayıya çevir: X ve y
# Çalıştır: uv run ornekler/02_ozellik_etiket.py

import csv

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

print(len(X), len(y))
print(kayitlar[0]["hex"], X[0], y[0])
