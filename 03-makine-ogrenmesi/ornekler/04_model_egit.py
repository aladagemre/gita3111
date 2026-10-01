# Adım 4 — Modeli eğit ve ölç
# Çalıştır: uv run ornekler/04_model_egit.py

import csv
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

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_egitim, y_egitim)
print("Model:", round(model.score(X_test, y_test), 2))

print("Hep enerjik:", round(y_test.count("enerjik") / len(y_test), 2))
