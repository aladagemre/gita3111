# Adım 9 — Aynı sayaç, çubuk grafik
# Çalıştır: uv run ornekler/10_cubuk_grafik.py

import matplotlib.pyplot as plt

with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

temiz = metin.replace("I", "ı").replace("İ", "i").lower()
for isaret in ".,!?:;()[]\"'…-–—/":
    temiz = temiz.replace(isaret, " ")
kelimeler = temiz.split()

with open("veri/turkce-durak-kelimeler.txt", encoding="utf-8") as dosya:
    durak_kelimeler = dosya.read().split()

sayac = {}
for kelime in kelimeler:
    if kelime not in durak_kelimeler and len(kelime) > 2:
        if kelime in sayac:
            sayac[kelime] = sayac[kelime] + 1
        else:
            sayac[kelime] = 1

sirali = sorted(sayac, key=sayac.get, reverse=True)
etiketler = sirali[:10]
degerler = []
for kelime in etiketler:
    degerler.append(sayac[kelime])

plt.bar(etiketler, degerler, color="#4a6fa5")
plt.title("Müşteri yorumlarında en sık 10 kelime")
plt.ylabel("Kaç kez geçti")
plt.xticks(rotation=45, ha="right")   # kelimeler üst üste binmesin
plt.tight_layout()                    # kenardaki yazılar kesilmesin
plt.savefig("kelime-grafik.png", dpi=150)
