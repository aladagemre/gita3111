# Adım 4 — En sık geçen 20 kelime
# Çalıştır: uv run ornekler/03_ilk_20.py

with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

temiz = metin.replace("I", "ı").replace("İ", "i").lower()
for isaret in ".,!?:;()[]\"'…-–—/":
    temiz = temiz.replace(isaret, " ")
kelimeler = temiz.split()

sayac = {}
for kelime in kelimeler:
    if kelime in sayac:
        sayac[kelime] = sayac[kelime] + 1
    else:
        sayac[kelime] = 1

sirali = sorted(sayac, key=sayac.get, reverse=True)   # değere göre; parantez yok
for kelime in sirali[:20]:
    print(sayac[kelime], kelime)
