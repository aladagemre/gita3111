# Adım 2–3 — Temizle ve say
# Çalıştır: uv run ornekler/02_kelime_say.py

with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

temiz = metin.replace("I", "ı").replace("İ", "i").lower()   # .lower() en sonda
for isaret in ".,!?:;()[]\"'…-–—/":
    temiz = temiz.replace(isaret, " ")
kelimeler = temiz.split()
print(kelimeler[:8])

sayac = {}
for kelime in kelimeler:
    if kelime in sayac:
        sayac[kelime] = sayac[kelime] + 1
    else:
        sayac[kelime] = 1

print(len(sayac))
print(sayac["sessiz"])
