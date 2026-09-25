"""5. adım — Kelime bulutu.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/ornekler/05_kelime_bulutu.py

Konunun görsel çıktısı. Aynı sayaç, bu kez grafik olarak.
"""

import os

from wordcloud import WordCloud

DOSYA = "01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt"
DURAK_DOSYASI = "01-veri-ve-kelime-bulutu/veri/turkce-durak-kelimeler.txt"
CIKTI = "kelime-bulutu.png"
NOKTALAMA = ".,!?:;()[]\"'…-–—/"

# Türkçe harfleri (ş, ğ, ı, İ) doğru gösteren bir yazı tipi bulmaya çalışır.
# Bulamazsa kütüphanenin kendi yazı tipini kullanır; harfler kutu görünürse
# buraya kendi bilgisayarındaki bir .ttf dosyasının yolunu yazabilirsin.
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


def kelimeleri_say(kelimeler):
    sayac = {}
    for kelime in kelimeler:
        sayac[kelime] = sayac.get(kelime, 0) + 1
    return sayac


with open(DOSYA, encoding="utf-8") as dosya:
    kelimeler = temizle(dosya.read()).split()

with open(DURAK_DOSYASI, encoding="utf-8") as dosya:
    durak_kelimeler = set(dosya.read().split())

temiz = []
for kelime in kelimeler:
    if kelime not in durak_kelimeler and len(kelime) > 2:
        temiz.append(kelime)

sayac = kelimeleri_say(temiz)

bulut = WordCloud(
    width=1200,
    height=800,
    background_color="white",
    colormap="viridis",
    font_path=yazi_tipi_bul(),
    prefer_horizontal=0.9,
)
bulut.generate_from_frequencies(sayac)
bulut.to_file(CIKTI)

print(f"Kelime bulutu kaydedildi: {CIKTI}")
print(f"Görselde {len(sayac)} farklı kelime var.")
