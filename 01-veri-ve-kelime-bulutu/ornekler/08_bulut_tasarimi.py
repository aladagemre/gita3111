# Bonus — Bulutun tasarımı: ayarları değiştir, yeniden çalıştır, karşılaştır
# Çalıştır: uv run ornekler/08_bulut_tasarimi.py

from wordcloud import WordCloud

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

bulut = WordCloud(
    width=1200, height=800,
    background_color="black",   # "white", "#1a1a2e"
    colormap="magma",           # "viridis", "cividis", "Pastel1"
    prefer_horizontal=0.5,      # 1 yaparsan hepsi yatay
    max_words=25,               # en fazla kaç kelime
)
bulut.generate_from_frequencies(sayac)
bulut.to_file("bulut-tasarim.png")
