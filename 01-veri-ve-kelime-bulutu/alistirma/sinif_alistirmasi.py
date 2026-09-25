"""SINIF ALIŞTIRMASI — Konu 1

Kendi başına doldur. Süre: ~40 dakika.
Soru tipleri vize ile aynı: boşluk doldurma ve hata bulma.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/alistirma/sinif_alistirmasi.py

Dosya baştan ÇALIŞIR. Her soru için "henüz değil" yazar; doldurdukça "doğru"ya döner.
Hepsi doğru olunca en altta TAMAM yazar.
"""

# Doldurulacak yerlere bu yazıyor. Sen doğru ifadeyle değiştireceksin.
BOSLUK = None


# =============================================================================
# SORU 1 — Boşlukları doldur (3 boşluk)
# Bir metindeki HARF sayısını (boşluklar hariç) sayar.
# =============================================================================

def harf_say(metin):
    toplam = BOSLUK              # (a) sayaç kaçtan başlamalı?
    for karakter in metin:
        if karakter != " ":
            toplam = BOSLUK      # (b) sayacı bir artır
    return BOSLUK                # (c) ne döndürmeli?


# =============================================================================
# SORU 2 — Boşlukları doldur (2 boşluk)
# Kelime listesinden {kelime: adet} sözlüğü üretir.
# =============================================================================

def kelime_sayaci(kelimeler):
    sayac = BOSLUK                       # (a) boş SÖZLÜK (liste değil!)
    for kelime in kelimeler:
        sayac[kelime] = BOSLUK           # (b) ipucu: sayac.get(kelime, 0) işine yarar
    return sayac


# =============================================================================
# SORU 3 — Hatayı bul ve düzelt
# En uzun kelimeyi döndürmeli ama döndürmüyor.
#
# Hatanın satırı :
# Nedeni         :
# =============================================================================

def en_uzun_kelime(kelimeler):
    en_uzun = ""
    for kelime in kelimeler:
        if len(kelime) > len(en_uzun):
            en_uzun = kelime
        return en_uzun


# =============================================================================
# SORU 4 — Hatayı bul ve düzelt
# Sözlükten değeri yanlış yoldan okumaya çalışıyor.
#
# Hatanın satırı :
# Nedeni         :
# =============================================================================

def en_cok_gecen(sayac):
    sirali = sorted(sayac, key=sayac.get, reverse=True)
    birinci = sirali[0]
    return birinci, sayac[0]


# =============================================================================
# SORU 5 — Kısa tamamlama (3-4 satır)
# Adedi `esik` değerinden BÜYÜK olan kelimelerin listesini döndür.
# =============================================================================

def esigin_ustundekiler(sayac, esik):
    sonuc = []
    # buraya yaz
    return sonuc


# =============================================================================
# HIZLI BİTİRENLER İÇİN — üç ek soru
# Zorunlu değil. Eksik bırakırsan "TAMAM" yerine "ÇEKİRDEK TAMAM" yazar, o da yeterli.
# =============================================================================

def en_az_gecenler(sayac, adet=2):
    """En AZ geçen `adet` kelimeyi liste olarak döndür (sıralama önemli değil)."""
    return []


def toplam_kelime(sayac):
    """Sözlükteki tüm adetlerin toplamı. {"a": 2, "b": 3} -> 5"""
    return 0


def harf_ile_baslayanlar(sayac, harf):
    """Verilen harfle başlayan kelimeleri liste olarak döndür."""
    return []

# =============================================================================
# KONTROL — buradan aşağısını değiştirme
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

    dene("1", lambda: harf_say("ali topu at") == 9)
    dene("2", lambda: kelime_sayaci(["a", "b", "a"]) == {"a": 2, "b": 1})
    dene("3", lambda: en_uzun_kelime(["ev", "okul", "kütüphane", "yol"]) == "kütüphane")
    dene("4", lambda: en_cok_gecen({"kahve": 8, "çay": 3}) == ("kahve", 8))
    dene("5", lambda: sorted(esigin_ustundekiler({"a": 5, "b": 2, "c": 9}, 3)) == ["a", "c"])

    cekirdek = list(sonuclar)

    dene("E1", lambda: sorted(en_az_gecenler({"a": 9, "b": 1, "c": 2}, 2)) == ["b", "c"])
    dene("E2", lambda: toplam_kelime({"a": 2, "b": 3}) == 5)
    dene("E3", lambda: sorted(harf_ile_baslayanlar({"kahve": 2, "kek": 1, "çay": 5}, "k")) == ["kahve", "kek"])

    print("--- sonuç ---")
    for ad, durum in sonuclar:
        etiket = "Ek soru" if ad.startswith("E") else "Soru"
        print(f"{etiket} {ad}: {'doğru' if durum else 'henüz değil'}")

    if all(durum for _, durum in sonuclar):
        print("\nTAMAM — ek sorular dahil")
    elif all(durum for _, durum in cekirdek):
        print("\nÇEKİRDEK TAMAM — ek soruları istersen dene")


if __name__ == "__main__":
    kontrol()
