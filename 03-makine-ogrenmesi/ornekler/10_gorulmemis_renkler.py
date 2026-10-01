# Adım 8 — Hiç görmediği renklerde sına
# Çalıştır: uv run ornekler/10_gorulmemis_renkler.py

import csv
from sklearn.neighbors import KNeighborsClassifier

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

renkler = {}
for kayit in kayitlar:
    renkler[kayit["ad"]] = kayit["hex"]

tutan = 0
for disarida in renkler:
    # Bu rengin hiçbir satırını görmeyen bir model
    X = []
    y = []
    for kayit in kayitlar:
        if kayit["ad"] != disarida:
            kod = kayit["hex"]
            X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
            y.append(kayit["etiket"])
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X, y)

    kod = renkler[disarida]
    tahmin = model.predict([(int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16))])[0]
    print(disarida, tahmin)
    for kayit in kayitlar:
        if kayit["ad"] == disarida and kayit["etiket"] == tahmin:
            tutan = tutan + 1

print("Hiç görmediği renklerde doğruluk:", round(tutan / len(kayitlar), 2))
