"""4. adım — Modeli eğit ve ölç.

Çalıştırma:  uv run --with scikit-learn 03-makine-ogrenmesi/ornekler/04_model_egit.py

Kullandığımız model: en yakın komşular (k-NN).
Mantığı tek cümle: "Bu renge en çok benzeyen 5 rengi bul, onlar ne dediyse onu de."
"""

import csv

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

VERI = "03-makine-ogrenmesi/veri/renkler-etiketli.csv"
KOMSU_SAYISI = 5


def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    return (int(hex_kod[0:2], 16), int(hex_kod[2:4], 16), int(hex_kod[4:6], 16))


def veriyi_hazirla(yol):
    with open(yol, encoding="utf-8") as dosya:
        kayitlar = list(csv.DictReader(dosya))
    X = []
    y = []
    for kayit in kayitlar:
        X.append(hex_to_rgb(kayit["hex"]))
        y.append(kayit["etiket"])
    return X, y


X, y = veriyi_hazirla(VERI)
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 1) Modeli kur
model = KNeighborsClassifier(n_neighbors=KOMSU_SAYISI)

# 2) Eğit — "bu örneklere bak ve öğren"
model.fit(X_egitim, y_egitim)

# 3) Ölç — hiç görmediği örneklerde
dogruluk = model.score(X_test, y_test)
print(f"Test doğruluğu: {dogruluk:.2f}  ({dogruluk * 100:.0f}%)")

# Kıyas: hep en sık etiketi deseydik ne olurdu?
sayac = {}
for etiket in y_egitim:
    sayac[etiket] = sayac.get(etiket, 0) + 1
en_sik = sorted(sayac, key=sayac.get, reverse=True)[0]
kor_tahmin = y_test.count(en_sik) / len(y_test)
print(f"Hep '{en_sik}' deseydik: {kor_tahmin:.2f}  ({kor_tahmin * 100:.0f}%)")

print()
if dogruluk > kor_tahmin:
    print("Model, körü körüne tahminden İYİ. Yani bir şey öğrenmiş.")
else:
    print("Model körü körüne tahminden iyi değil. Öğrenecek bir örüntü bulamamış.")

# Tek bir rengi tahmin ettirelim
ornek = hex_to_rgb("#E63946")   # kırmızı
print(f"\n#E63946 için tahmin: {model.predict([ornek])[0]}")
