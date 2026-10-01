# Bonus — Kaydedilen cevaplardan kelime bulutu (önce 06'yı çalıştır)
# Çalıştır: uv run ornekler/08_cevap_raporu.py

import json

from wordcloud import WordCloud

with open("cevaplar.json", encoding="utf-8") as dosya:
    kayitlar = json.load(dosya)

with open("../01-veri-ve-kelime-bulutu/veri/turkce-durak-kelimeler.txt", encoding="utf-8") as dosya:
    durak_kelimeler = dosya.read().split()

butun_metin = ""
for kayit in kayitlar:
    print(len(kayit["cevap"].split()), "kelime:", kayit["soru"])
    butun_metin = butun_metin + " " + kayit["cevap"]

bulut = WordCloud(width=1200, height=800, background_color="white", stopwords=durak_kelimeler)
bulut.generate(butun_metin)
bulut.to_file("cevaplar-bulutu.png")
