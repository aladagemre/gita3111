# Adım 6 — Veri arttıkça doğruluk nasıl değişiyor?
# Çalıştır: uv run ornekler/06_veri_miktari.py

import csv
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

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

adetler = []
dogruluklar = []
for oran in [0.1, 0.25, 0.5, 0.75, 1.0]:
    adet = int(len(X_egitim) * oran)
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_egitim[:adet], y_egitim[:adet])
    adetler.append(adet)
    dogruluklar.append(round(model.score(X_test, y_test), 2))

print(adetler)
print(dogruluklar)
plt.plot(adetler, dogruluklar, marker="o")
plt.xlabel("Eğitim örneği sayısı")
plt.ylabel("Test doğruluğu")
plt.savefig("veri-miktari.png")
