"""6. adım (bonus) — Aynı kod, farklı metin.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/ornekler/06_iki_metin.py

Aynı kafe, iki kaynak: müşterilerin yorumları ve kafenin kendi sosyal medya gönderileri.
Soru: kafe kendini nasıl anlatıyor, müşteri onu nasıl anlatıyor?
Kod aynı; sonuç değişiyorsa fark koddan değil VERİDEN geliyor. Bu, dersin geri kalanının
da özeti.
"""

METINLER = [
    ("Müşteri yorumları", "01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt"),
    ("Kafenin kendi gönderileri", "01-veri-ve-kelime-bulutu/veri/kafe-gonderileri.txt"),
]
DURAK_DOSYASI = "01-veri-ve-kelime-bulutu/veri/turkce-durak-kelimeler.txt"
NOKTALAMA = ".,!?:;()[]\"'…-–—/"


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


def en_sik(yol, durak_kelimeler, adet=8):
    with open(yol, encoding="utf-8") as dosya:
        kelimeler = temizle(dosya.read()).split()
    temiz = []
    for kelime in kelimeler:
        if kelime not in durak_kelimeler and len(kelime) > 2:
            temiz.append(kelime)
    sayac = kelimeleri_say(temiz)
    sirali = sorted(sayac, key=sayac.get, reverse=True)
    return [(kelime, sayac[kelime]) for kelime in sirali[:adet]]


with open(DURAK_DOSYASI, encoding="utf-8") as dosya:
    durak_kelimeler = set(dosya.read().split())

for ad, yol in METINLER:
    print(f"\n=== {ad} ===")
    for kelime, adet in en_sik(yol, durak_kelimeler):
        print(f"{adet:>3}  {kelime}")

print("\nAynı kod, iki farklı sonuç. Kafe kendini kahveyle anlatıyor; müşteri ise")
print("sessiz bir çalışma yeri olarak. Yeni kimlik hangisini öne çıkarmalı?")
