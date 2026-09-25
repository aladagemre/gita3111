"""2. adım — Öznitelik ve etiket.

Çalıştırma:  uv run 03-makine-ogrenmesi/ornekler/02_ozellik_etiket.py

Model renk ADINI anlamaz, sayı ister. "#E63946" metnini üç sayıya çevireceğiz:
kırmızı, yeşil, mavi miktarları.
"""

import csv

VERI = "03-makine-ogrenmesi/veri/renkler-etiketli.csv"


def hex_to_rgb(hex_kod):
    """'#E63946' -> (230, 57, 70)"""
    hex_kod = hex_kod.lstrip("#")
    kirmizi = int(hex_kod[0:2], 16)
    yesil = int(hex_kod[2:4], 16)
    mavi = int(hex_kod[4:6], 16)
    return (kirmizi, yesil, mavi)


print("Örnek dönüşümler:")
for ornek in ["#E63946", "#457B9D", "#1D3557"]:
    print(f"  {ornek} -> {hex_to_rgb(ornek)}")

with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

# X = öznitelikler (modelin BAKTIĞI şey)
# y = etiketler   (modelin TAHMİN ETMESİ gereken şey)
X = []
y = []
for kayit in kayitlar:
    X.append(hex_to_rgb(kayit["hex"]))
    y.append(kayit["etiket"])

print(f"\nX: {len(X)} örnek, her biri {len(X[0])} sayıdan oluşuyor")
print(f"y: {len(y)} etiket")
print(f"\nİlk üç örnek:")
for i in range(3):
    print(f"  {X[i]}  ->  {y[i]}")

print("\nX ve y AYNI SIRADA olmalı. X[5]'in cevabı y[5]'tir.")
print("Karışırlarsa model yanlış şeyi öğrenir ve bunu kimse fark etmez.")
