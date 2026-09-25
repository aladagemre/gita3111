"""8. adım (bonus) — Bulutun tasarımıyla oynamak.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/ornekler/08_bulut_tasarimi.py

Hızlı bitirdiysen burası senin. Aşağıdaki AYARLAR sözlüğünü değiştir, tekrar çalıştır,
farkı gör. Kod aynı kalıyor; değişen tek şey ayarlar.
"""

import os

from wordcloud import WordCloud

DOSYA = "01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt"
DURAK_DOSYASI = "01-veri-ve-kelime-bulutu/veri/turkce-durak-kelimeler.txt"
NOKTALAMA = ".,!?:;()[]\"'…-–—/"

# ---- OYNAYACAĞIN YER -------------------------------------------------------
AYARLAR = {
    "width": 1200,
    "height": 800,
    "background_color": "white",   # "black", "#1a1a2e" de dene
    "colormap": "viridis",         # "magma", "cividis", "Pastel1", "coolwarm"
    "prefer_horizontal": 0.9,      # 0.5 yaparsan yazılar daha çok dikleşir
    "max_words": 100,              # 25 yaparsan sadece en güçlüler kalır
    "min_font_size": 10,
    "relative_scaling": 0.5,       # 1.0 = boyut sıklıkla tam orantılı
}
CIKTI = "bulut-tasarim.png"
# ---------------------------------------------------------------------------

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


with open(DOSYA, encoding="utf-8") as dosya:
    kelimeler = temizle(dosya.read()).split()

with open(DURAK_DOSYASI, encoding="utf-8") as dosya:
    durak_kelimeler = set(dosya.read().split())

sayac = {}
for kelime in kelimeler:
    if kelime not in durak_kelimeler and len(kelime) > 2:
        sayac[kelime] = sayac.get(kelime, 0) + 1

bulut = WordCloud(font_path=yazi_tipi_bul(), **AYARLAR)
bulut.generate_from_frequencies(sayac)
bulut.to_file(CIKTI)

print(f"Kaydedildi: {CIKTI}")
print("Ayarlardan birini değiştir, tekrar çalıştır, iki görseli yan yana koy.")
