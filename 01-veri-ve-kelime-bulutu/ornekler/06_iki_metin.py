# Bonus — Aynı kod, farklı metin: kafenin kendi gönderileri
# Çalıştır: uv run ornekler/06_iki_metin.py

with open("veri/kafe-gonderileri.txt", encoding="utf-8") as dosya:
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
for kelime in sirali[:10]:
    print(sayac[kelime], kelime)
