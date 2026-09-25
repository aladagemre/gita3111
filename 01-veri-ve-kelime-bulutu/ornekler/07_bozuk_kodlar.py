"""7. adım — Bozuk kodlar galerisi.

Çalıştırma (önce konunun klasörüne gir: cd 01-veri-ve-kelime-bulutu):
    uv run ornekler/07_bozuk_kodlar.py

Düzeltmeden önce bu dosyayı aynı klasörde yeni bir adla kopyala
(örneğin benim_bozuklarim.py), kopyada düzelt; böylece git pull çakışmaz.

Beş küçük fonksiyon, beş farklı hata türü. Her biri bu konudan.
Düzelt, çalıştır, TAMAM yazsın.

Bu alıştırmanın amacı kod yazmak değil, HATA OKUMAK. Vizede de böyle sorular var:
"hangi satır, neden, nasıl düzeltilir".
"""

# -----------------------------------------------------------------------------
# 1) Sözlükten yanlış yoldan okuma
#    Hata türü: KeyError
# -----------------------------------------------------------------------------

def en_pahali_urun(fiyatlar):
    """{'kahve': 45, 'çay': 30} gibi bir sözlükten en pahalının adını döndürür."""
    sirali = sorted(fiyatlar, key=fiyatlar.get, reverse=True)
    return sirali[0], fiyatlar[0]


# -----------------------------------------------------------------------------
# 2) Sayaç sıfırdan başlatılmamış
#    Hata türü: NameError
# -----------------------------------------------------------------------------

def sesli_harf_say(kelime):
    for harf in kelime:
        if harf in "aeıioöuü":
            adet = adet + 1
    return adet


# -----------------------------------------------------------------------------
# 3) return döngünün içinde
#    Hata türü: yanlış sonuç (hata mesajı YOK — en sinsi tür)
# -----------------------------------------------------------------------------

def uzun_kelimeleri_bul(kelimeler, sinir=5):
    sonuc = []
    for kelime in kelimeler:
        if len(kelime) > sinir:
            sonuc.append(kelime)
        return sonuc


# -----------------------------------------------------------------------------
# 4) Liste ile sözlük karıştırılmış
#    Hata türü: TypeError
# -----------------------------------------------------------------------------

def toplam_adet(sayac):
    """{'a': 2, 'b': 3} sözlüğündeki değerleri toplar."""
    toplam = 0
    for kelime in sayac:
        toplam = toplam + kelime
    return toplam


# -----------------------------------------------------------------------------
# 5) Türkçe küçültme tuzağı
#    Hata türü: yanlış sonuç — sayaç aynı kelimeyi ikiye böler
# -----------------------------------------------------------------------------

def kelime_sayaci(metin):
    sayac = {}
    for kelime in metin.lower().split():
        sayac[kelime] = sayac.get(kelime, 0) + 1
    return sayac


# =============================================================================
# KONTROL — değiştirme
# =============================================================================

# Not: aşağıdaki `lambda`, tek satırlık fonksiyon yazmanın kısa yolu. Derste
# kullanmıyoruz ve senden beklenmiyor; burada kontrol bölümünü kısa tutmak için var.
def kontrol():
    sonuclar = []

    def dene(ad, islev):
        try:
            sonuclar.append((ad, bool(islev())))
        except Exception:
            sonuclar.append((ad, False))

    dene("1 (KeyError)", lambda: en_pahali_urun({"kahve": 45, "çay": 30}) == ("kahve", 45))
    dene("2 (NameError)", lambda: sesli_harf_say("istanbul") == 3)
    dene("3 (sessiz hata)", lambda: uzun_kelimeleri_bul(["ev", "kütüphane", "bilgisayar"]) == ["kütüphane", "bilgisayar"])
    dene("4 (TypeError)", lambda: toplam_adet({"a": 2, "b": 3}) == 5)
    dene("5 (Türkçe)", lambda: kelime_sayaci("İstanbul istanbul İSTANBUL") == {"istanbul": 3})

    print("--- sonuç ---")
    for ad, durum in sonuclar:
        print(f"{ad}: {'doğru' if durum else 'henüz değil'}")
    if all(d for _, d in sonuclar):
        print("\nTAMAM")


if __name__ == "__main__":
    kontrol()
