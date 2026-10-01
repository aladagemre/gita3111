# Adım 5–6 — Durak kelimeleri ele, sonucu dosyaya yaz
# Çalıştır: uv run ornekler/04_durak_kelime.py

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
for kelime in sirali[:10]:
    print(sayac[kelime], kelime)

with open("sonuc.txt", "w", encoding="utf-8") as dosya:   # "w": yazma modu
    for kelime in sirali[:20]:
        dosya.write(f"{sayac[kelime]}\t{kelime}\n")
