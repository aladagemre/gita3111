"""2. adım — Kelimeleri saymak.

Çalıştırma (önce konunun klasörüne gir: cd 01-veri-ve-kelime-bulutu):
    uv run ornekler/02_kelime_say.py

Bu dosyanın konusu SÖZLÜK. Sayaç tutmak, sözlüğün en sık işidir.
"""

DOSYA = "veri/kafe-yorumlari.txt"
NOKTALAMA = ".,!?:;()[]\"'…-–—/"


def turkce_kucult(metin):
    """Türkçe için güvenli küçültme.

    Neden gerekli:  "İSTANBUL".lower()  beklediğin sonucu VERMEZ.
    Python büyük İ'yi küçültürken üstteki noktayı ayrı bir işaret olarak bırakır,
    sonuçta "istanbul" ile aynı görünen ama farklı olan bir metin çıkar —
    ve sayacın aynı kelimeyi ikiye böler.
    """
    return metin.replace("I", "ı").replace("İ", "i").lower()


def temizle(metin):
    """Noktalamayı boşluğa çevirir, küçültür."""
    for isaret in NOKTALAMA:
        metin = metin.replace(isaret, " ")
    return turkce_kucult(metin)


with open(DOSYA, encoding="utf-8") as dosya:
    metin = dosya.read()

# --- ÖNCE ham hâliyle bölelim: sorunu görmek için -------------------------
ham_kelimeler = metin.split()
print("Ham bölme -> kelime sayısı:", len(ham_kelimeler))
print("İlk sekiz :", ham_kelimeler[:8])
print("Dikkat: 'demledik.' noktayla yapışık, 'Bugün' büyük harfle başlıyor.\n")

# --- ŞİMDİ temizleyerek bölelim -------------------------------------------
kelimeler = temizle(metin).split()
print("Temiz bölme -> kelime sayısı:", len(kelimeler))
print("İlk sekiz   :", kelimeler[:8])
print()

# --- Sayaç: UZUN HÂLİ -------------------------------------------------------
# Önce böyle yazıyoruz, çünkü ne olduğu açıkça görünüyor.
sayac = {}
for kelime in kelimeler:
    if kelime in sayac:
        sayac[kelime] = sayac[kelime] + 1
    else:
        sayac[kelime] = 1

print("Farklı kelime:", len(sayac))
print("'sessiz' kaç kez geçmiş:", sayac["sessiz"])

# --- Aynı şeyin KISA HÂLİ ---------------------------------------------------
# sayac.get(kelime, 0) demek: "varsa değerini ver, yoksa 0 ver".
sayac2 = {}
for kelime in kelimeler:
    sayac2[kelime] = sayac2.get(kelime, 0) + 1

print("İki yöntem aynı sonucu verdi mi:", sayac == sayac2)

# DİKKAT: sayac bir SÖZLÜK. Değere anahtarla erişilir:  sayac["sessiz"]
# Liste değil — sayac[0] yazarsan hata alırsın, çünkü 0 diye bir anahtar yok.
