"""8. adım (bonus) — Kaydettiğin cevaplardan rapor çıkarmak.

Çalıştırma:  uv run --with wordcloud 02-api-ile-konusmak/ornekler/08_cevap_raporu.py

Konu 1'de bir metin dosyasından kelime bulutu ürettik. Bu konuda metni kendimiz
üretiyoruz. İkisini birleştirelim: modelin verdiği cevapların kelime bulutu.

Önce 06_coklu_soru.py çalıştırılmalı (cevaplar.json üretir).
"""

import json
import os

from wordcloud import WordCloud

KAYNAK = "cevaplar.json"
DURAK_DOSYASI = "01-veri-ve-kelime-bulutu/veri/turkce-durak-kelimeler.txt"
CIKTI = "cevaplar-bulutu.png"
NOKTALAMA = ".,!?:;()[]\"'…-–—/"

FONT_ADAYLARI = [
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def yazi_tipi_bul():
    for yol in FONT_ADAYLARI:
        if os.path.exists(yol):
            return yol
    return None


def turkce_kucult(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()


def temizle(metin):
    for isaret in NOKTALAMA:
        metin = metin.replace(isaret, " ")
    return turkce_kucult(metin)


try:
    with open(KAYNAK, encoding="utf-8") as dosya:
        kayitlar = json.load(dosya)
except FileNotFoundError:
    print(f"{KAYNAK} yok. Önce 06_coklu_soru.py dosyasını çalıştır.")
    raise SystemExit(1)

print(f"{len(kayitlar)} kayıt okundu.\n")

# Rapor: her sorunun cevabı kaç kelime?
toplam_kelime = 0
for kayit in kayitlar:
    adet = len(kayit["cevap"].split())
    toplam_kelime = toplam_kelime + adet
    print(f"{adet:>4} kelime — {kayit['soru'][:50]}")

print(f"\nToplam {toplam_kelime} kelime üretilmiş.")

# Tüm cevapları birleştirip bulut çıkar
butun_metin = ""
for kayit in kayitlar:
    butun_metin = butun_metin + " " + kayit["cevap"]

with open(DURAK_DOSYASI, encoding="utf-8") as dosya:
    durak_kelimeler = set(dosya.read().split())

sayac = {}
for kelime in temizle(butun_metin).split():
    if kelime not in durak_kelimeler and len(kelime) > 2:
        sayac[kelime] = sayac.get(kelime, 0) + 1

if sayac:
    bulut = WordCloud(width=1200, height=800, background_color="white",
                      colormap="cividis", font_path=yazi_tipi_bul())
    bulut.generate_from_frequencies(sayac)
    bulut.to_file(CIKTI)
    print(f"Kelime bulutu kaydedildi: {CIKTI}")
    print("\nSoru: modelin dili senin metninden farklı mı görünüyor?")
