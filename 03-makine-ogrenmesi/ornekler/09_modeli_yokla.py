# Adım 7 — Model ne öğrendi? Kafe paletini sor
# Çalıştır: uv run ornekler/09_modeli_yokla.py

import csv
from sklearn.neighbors import KNeighborsClassifier

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(kayit["etiket"])

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X, y)

for kod in ["#E8DCC4", "#D4A373", "#A3B18A", "#344E41", "#F5F5F5"]:
    rgb = (int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16))
    # kneighbors: cevabı hangi komşulara bakarak verdin?
    mesafeler, siralar = model.kneighbors([rgb])
    print(kod, model.predict([rgb])[0], "en yakın:", kayitlar[siralar[0][0]]["ad"])
