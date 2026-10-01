# Adım 5 — Modelin yanıldığı renklere bak
# Çalıştır: uv run ornekler/05_yanilgilari_gor.py

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

X_egitim, X_test, y_egitim, y_test, k_egitim, k_test = train_test_split(
    X, y, kayitlar, test_size=0.25, random_state=42
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_egitim, y_egitim)
tahminler = model.predict(X_test)

yazilar = []
kodlar = []
for i in range(len(y_test)):
    if tahminler[i] != y_test[i]:
        yazi = k_test[i]["ad"] + ": öğrenci " + y_test[i] + ", model " + tahminler[i]
        print(yazi)
        yazilar.append(yazi)
        kodlar.append(k_test[i]["hex"])

plt.barh(range(len(yazilar)), 1, color=kodlar, tick_label=yazilar)
plt.xticks([])
plt.savefig("yanilgilar.png", bbox_inches="tight")
