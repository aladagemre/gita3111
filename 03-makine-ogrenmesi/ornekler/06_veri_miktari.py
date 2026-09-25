"""6. adım — Veri arttıkça ne oluyor?

Çalıştırma (önce konunun klasörüne gir: cd 03-makine-ogrenmesi):
    uv run ornekler/06_veri_miktari.py

Aynı modeli önce az veriyle, sonra çok veriyle eğitip doğruluğu karşılaştırıyoruz.
"""

import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

VERI = "veri/renkler-etiketli.csv"
CIKTI = "veri-miktari.png"
ORANLAR = [0.1, 0.25, 0.5, 0.75, 1.0]


def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    return (int(hex_kod[0:2], 16), int(hex_kod[2:4], 16), int(hex_kod[4:6], 16))


with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    X.append(hex_to_rgb(kayit["hex"]))
    y.append(kayit["etiket"])

X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

miktarlar = []
dogruluklar = []

print("Eğitim verisi   Doğruluk")
print("-" * 26)
for oran in ORANLAR:
    adet = int(len(X_egitim) * oran)
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_egitim[:adet], y_egitim[:adet])
    dogruluk = model.score(X_test, y_test)
    miktarlar.append(adet)
    dogruluklar.append(dogruluk)
    print(f"{adet:>10} örnek   {dogruluk:.2f}")

plt.figure(figsize=(7, 4))
plt.plot(miktarlar, dogruluklar, marker="o")
plt.xlabel("Eğitim örneği sayısı")
plt.ylabel("Test doğruluğu")
plt.title("Veri arttıkça doğruluk")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(CIKTI, dpi=120)
plt.close()

print(f"\nGrafik kaydedildi: {CIKTI}")
print("Soru: eğri sonunda düzleşiyor mu? Düzleşiyorsa daha fazla veri işe yaramaz demektir.")
