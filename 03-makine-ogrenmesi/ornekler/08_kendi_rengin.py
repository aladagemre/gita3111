# Bonus — Kendi renklerini modele sor
# Çalıştır: uv run ornekler/08_kendi_rengin.py

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

# Ölçmüyoruz, sadece soruyoruz: tüm veriyle eğit
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X, y)

# Listeye kendi renklerini yaz
for kod in ["#FF0000", "#000080", "#FFFFFF", "#7CFC00", "#8B4513"]:
    rgb = (int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16))
    print(kod, model.predict([rgb])[0])
