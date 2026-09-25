"""3. adım — En sık geçen kelimeler.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/ornekler/03_ilk_20.py
"""

DOSYA = "01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt"
NOKTALAMA = ".,!?:;()[]\"'…-–—/"


def turkce_kucult(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()


def temizle(metin):
    for isaret in NOKTALAMA:
        metin = metin.replace(isaret, " ")
    return turkce_kucult(metin)


def kelimeleri_say(kelimeler):
    """Kelime listesinden {kelime: adet} sözlüğü üretir."""
    sayac = {}
    for kelime in kelimeler:
        sayac[kelime] = sayac.get(kelime, 0) + 1
    return sayac


with open(DOSYA, encoding="utf-8") as dosya:
    kelimeler = temizle(dosya.read()).split()

sayac = kelimeleri_say(kelimeler)

# Sıralama:
#   sorted(sayac)                          -> anahtarları alfabetik sıralar
#   sorted(sayac, key=sayac.get)           -> anahtarları DEĞERLERİNE göre sıralar
#   reverse=True                           -> büyükten küçüğe
#
# key=sayac.get  satırında parantez YOK. Fonksiyonun kendisini veriyoruz;
# sıralama her kelime için onu kendisi çağıracak.
sirali = sorted(sayac, key=sayac.get, reverse=True)

print("En sık geçen 20 kelime:\n")
for kelime in sirali[:20]:
    print(f"{sayac[kelime]:>3}  {kelime}")
