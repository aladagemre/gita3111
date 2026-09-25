"""SINIF ALIŞTIRMASI — Konu 2 (API ve JSON)

Kendi başına doldur. Süre: ~40 dakika. İnternet gerekmiyor.
Soru tipleri vize ile aynı: boşluk doldurma ve hata bulma.

Çalıştırma (önce konunun klasörüne gir: cd 02-api-ile-konusmak):
    uv run alistirma/sinif_alistirmasi.py

Doldurmadan önce bu dosyayı aynı klasörde yeni bir adla kopyala
(örneğin benim_alistirmam.py), kopyayı doldur ve çalıştır; böylece git pull çakışmaz.
"""

BOSLUK = None

# Derste gördüğümüz yanıt yapısı
YANIT = {
    "result": {
        "response": "Serif yazı tiplerinde harflerin uçlarında küçük tırnaklar bulunur.",
        "usage": {"prompt_tokens": 9, "completion_tokens": 14, "total_tokens": 23},
    },
    "success": True,
    "errors": [],
}

KAYITLAR = [
    {"soru": "Slogan yaz", "cevap": "Sabahın en güzel hâli"},
    {"soru": "Renk öner", "cevap": "Toprak tonları sıcak durur"},
    {"soru": "Font öner", "cevap": "Okunaklı bir sans-serif iş görür"},
]


# =============================================================================
# SORU 1 — Boşlukları doldur (2 boşluk)
# Yanıttan modelin ürettiği metni çek.
# =============================================================================

def metni_al(yanit):
    ic_sozluk = yanit[BOSLUK]        # (a) hangi anahtar?
    return ic_sozluk[BOSLUK]         # (b) hangi anahtar?


# =============================================================================
# SORU 2 — Boşlukları doldur (2 boşluk)
# İstek için gereken başlık sözlüğünü üret.
# Doğrusu:  {"Authorization": "Bearer <anahtar>"}
# =============================================================================

def baslik_yap(anahtar):
    return {BOSLUK: BOSLUK}          # (a) anahtar adı, (b) değeri (f-string kullan)


# =============================================================================
# SORU 3 — Hatayı bul ve düzelt
# Kayıtlardaki TÜM cevapların toplam kelime sayısını döndürmeli.
#
# Hatanın satırı :
# Nedeni         :
# =============================================================================

def toplam_kelime(kayitlar):
    toplam = 0
    for kayit in kayitlar:
        toplam = toplam + len(kayit.split())
    return toplam


# =============================================================================
# SORU 4 — Hatayı bul ve düzelt
# Durum koduna göre açıklama döndürmeli. Şu an her zaman aynı şeyi söylüyor.
#
# Hatanın satırı :
# Nedeni         :
# =============================================================================

def kod_acikla(kod):
    aciklama = {401: "Yetki yok", 429: "Kota doldu", 500: "Sunucu hatası"}
    if kod in aciklama:
        return aciklama[401]
    return "Bilinmeyen kod"


# =============================================================================
# SORU 5 — Kısa tamamlama (3-4 satır)
# Cevabı 3 kelimeden UZUN olan kayıtların sorularını liste olarak döndür.
# =============================================================================

def uzun_cevaplilar(kayitlar):
    sonuc = []
    # buraya yaz
    return sonuc


# =============================================================================
# HIZLI BİTİRENLER İÇİN
# =============================================================================

def en_uzun_cevap(kayitlar):
    """Cevabı en uzun olan kaydın SORUSUNU döndür."""
    return ""


def basarili_mi(yanit):
    """Yanıt başarılıysa ve hiç hata yoksa True döndür."""
    return False


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

    dene("1", lambda: metni_al(YANIT).startswith("Serif"))
    dene("2", lambda: baslik_yap("abc") == {"Authorization": "Bearer abc"})
    dene("3", lambda: toplam_kelime(KAYITLAR) == 13)
    dene("4", lambda: kod_acikla(429) == "Kota doldu" and kod_acikla(401) == "Yetki yok")
    dene("5", lambda: uzun_cevaplilar(KAYITLAR) == ["Slogan yaz", "Renk öner", "Font öner"])

    cekirdek = list(sonuclar)

    dene("E1", lambda: en_uzun_cevap(KAYITLAR) == "Font öner")
    dene("E2", lambda: basarili_mi(YANIT) is True)

    print("--- sonuç ---")
    for ad, durum in sonuclar:
        etiket = "Ek soru" if ad.startswith("E") else "Soru"
        print(f"{etiket} {ad}: {'doğru' if durum else 'henüz değil'}")

    if all(d for _, d in sonuclar):
        print("\nTAMAM — ek sorular dahil")
    elif all(d for _, d in cekirdek):
        print("\nÇEKİRDEK TAMAM — ek soruları istersen dene")


if __name__ == "__main__":
    kontrol()
