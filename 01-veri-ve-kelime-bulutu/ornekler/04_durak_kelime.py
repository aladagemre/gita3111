"""4. adım — Durak kelimeleri elemek ve sonucu kaydetmek.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/ornekler/04_durak_kelime.py

"ve", "bir", "bu" gibi kelimeler her metinde en üstte çıkar ve hiçbir şey anlatmaz.
Bunlara durak kelime (stopword) denir; eleriz.
"""

DOSYA = "01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt"
DURAK_DOSYASI = "01-veri-ve-kelime-bulutu/veri/turkce-durak-kelimeler.txt"
CIKTI = "sonuc.txt"
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


def durak_kelimeleri_oku(yol):
    """Durak kelimeleri okur ve tekrarsız bir torbaya (set) koyar.

    set kullanmamızın tek sebebi hız: "bu kelime içinde var mı?" sorusunu
    listeden çok daha çabuk cevaplıyor.
    """
    with open(yol, encoding="utf-8") as dosya:
        return set(dosya.read().split())


with open(DOSYA, encoding="utf-8") as dosya:
    kelimeler = temizle(dosya.read()).split()

durak_kelimeler = durak_kelimeleri_oku(DURAK_DOSYASI)

# Eleme: durak kelime olmayanları ve üç harften kısa olmayanları tut
temiz_kelimeler = []
for kelime in kelimeler:
    if kelime not in durak_kelimeler and len(kelime) > 2:
        temiz_kelimeler.append(kelime)

print(f"Eleme öncesi: {len(kelimeler)} kelime")
print(f"Eleme sonrası: {len(temiz_kelimeler)} kelime")

sayac = kelimeleri_say(temiz_kelimeler)
sirali = sorted(sayac, key=sayac.get, reverse=True)

with open(CIKTI, "w", encoding="utf-8") as dosya:
    for kelime in sirali[:20]:
        dosya.write(f"{sayac[kelime]}\t{kelime}\n")

print(f"\nSonuç kaydedildi: {CIKTI}")
print("\nİlk 10:")
for kelime in sirali[:10]:
    print(f"{sayac[kelime]:>3}  {kelime}")
