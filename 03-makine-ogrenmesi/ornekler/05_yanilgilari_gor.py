"""5. adım — Modelin yanıldığı yerlere bakmak.

Çalıştırma (önce konunun klasörüne gir: cd 03-makine-ogrenmesi):
    uv run ornekler/05_yanilgilari_gor.py

Doğruluk oranı tek bir sayı. Asıl öğretici olan, NEREDE yanıldığı.
Bu yüzden yanlış sınıflanan renkleri kare kare çizdiriyoruz.
"""

import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

VERI = "veri/renkler-etiketli.csv"
CIKTI = "yanilgilar.png"


def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    return (int(hex_kod[0:2], 16), int(hex_kod[2:4], 16), int(hex_kod[4:6], 16))


with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
etiketler = []          # (hex, renk adı) ikilileri
for kayit in kayitlar:
    X.append(hex_to_rgb(kayit["hex"]))
    y.append(kayit["etiket"])
    etiketler.append((kayit["hex"], kayit["ad"]))

# Renk bilgisini de bölmeye dahil ediyoruz ki hangi rengin yanlış gittiğini bilelim
X_egitim, X_test, y_egitim, y_test, bilgi_egitim, bilgi_test = train_test_split(
    X, y, etiketler, test_size=0.25, random_state=42
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_egitim, y_egitim)
tahminler = model.predict(X_test)

# Yanlışları topla
yanlislar = []
for i in range(len(y_test)):
    if tahminler[i] != y_test[i]:
        yanlislar.append({"hex": bilgi_test[i][0], "ad": bilgi_test[i][1],
                          "gercek": y_test[i], "tahmin": tahminler[i]})

print(f"{len(y_test)} test örneğinden {len(yanlislar)} tanesinde yanıldı.\n")
for yanlis in yanlislar[:10]:
    print(f"  {yanlis['hex']}  {yanlis['ad']:<15} sınıf: {yanlis['gercek']:<8} model: {yanlis['tahmin']}")

# Çizdir: her yanlış bir kare, altında gerçek ve tahmin
if yanlislar:
    gosterilecek = yanlislar[:12]
    satir = 3
    sutun = 4
    plt.figure(figsize=(10, 7))
    sira = 0
    for yanlis in gosterilecek:
        sira = sira + 1
        plt.subplot(satir, sutun, sira)
        plt.imshow([[tuple(d / 255 for d in hex_to_rgb(yanlis["hex"]))]])
        # Renk adı ve kodu da yazılıyor: görsel, rengi ayırt edemeyen biri için de okunur olsun
        plt.title(f"{yanlis['ad']} ({yanlis['hex']})\n"
                  f"sınıf: {yanlis['gercek']}  model: {yanlis['tahmin']}", fontsize=8)
        plt.axis("off")
    plt.tight_layout()
    plt.savefig(CIKTI, dpi=120)
    plt.close()
    print(f"\nGörsel kaydedildi: {CIKTI}")
    print("Bak: model bu renklerde neden yanılmış olabilir?")
