"""7. adım — Bozuk kodlar galerisi (API sürümü).

Çalıştırma (önce konunun klasörüne gir: cd 02-api-ile-konusmak):
    uv run ornekler/07_bozuk_kodlar.py

Düzeltmeden önce bu dosyayı aynı klasörde yeni bir adla kopyala
(örneğin benim_bozuklarim.py), kopyada düzelt; böylece git pull çakışmaz.

Beş küçük fonksiyon, beşi de bu konudan. İnternet gerekmiyor;
hepsi kayıtlı bir yanıt üzerinde çalışıyor.

Vizede tam olarak bu tip sorular var: "hangi satır, neden, nasıl düzeltilir".
"""

YANIT = {
    "result": {
        "response": "Üç slogan: 1) Sessizliğin adresi 2) Kahven, prizin, zamanın 3) Burada odaklanırsın",
        "usage": {"prompt_tokens": 12, "completion_tokens": 30, "total_tokens": 42},
    },
    "success": True,
    "errors": [],
}

HATALI_YANIT = {
    "result": None,
    "success": False,
    "errors": [{"code": 10000, "message": "Authentication error"}],
}


# -----------------------------------------------------------------------------
# 1) Yanıtın içine yeterince girmemiş
# -----------------------------------------------------------------------------

def cevap_metni(yanit):
    """Modelin ürettiği metni döndürmeli."""
    return yanit["response"]


# -----------------------------------------------------------------------------
# 2) Liste ile sözlük karışmış — 'errors' bir liste
# -----------------------------------------------------------------------------

def hata_mesaji(yanit):
    """İlk hatanın mesajını döndürmeli."""
    return yanit["errors"]["message"]


# -----------------------------------------------------------------------------
# 3) Başarı kontrolü ters yazılmış
# -----------------------------------------------------------------------------

def istek_basarili_mi(yanit):
    """Başarılıysa True, değilse False döndürmeli."""
    if yanit["success"]:
        return False
    return True


# -----------------------------------------------------------------------------
# 4) Anahtar kodun içine yazılmış — çalışır ama YAPILMAZ
#    Burada testi geçmek yetmez: anahtarı koddan çıkarıp parametre yap.
# -----------------------------------------------------------------------------

def istek_basligi_yap(anahtar="cf_gercek_anahtarim_12345"):
    """Authorization başlığını üretmeli. Anahtar koda gömülmemeli."""
    return {"Authorization": f"Bearer {anahtar}"}


# -----------------------------------------------------------------------------
# 5) Belirteç toplamı yanlış yerden okunuyor
# -----------------------------------------------------------------------------

def harcanan_belirtec(yanit):
    """Toplam belirteç sayısını döndürmeli."""
    return yanit["result"]["total_tokens"]


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

    dene("1 (iç içe sözlük)", lambda: cevap_metni(YANIT).startswith("Üç slogan"))
    dene("2 (liste mi sözlük mü)", lambda: hata_mesaji(HATALI_YANIT) == "Authentication error")
    dene("3 (ters mantık)", lambda: istek_basarili_mi(YANIT) is True and istek_basarili_mi(HATALI_YANIT) is False)
    def dorduncu():
        # Anahtar koddan çıkarılmış olmalı: parametresiz çağrı HATA vermeli.
        try:
            istek_basligi_yap()
        except TypeError:
            return istek_basligi_yap("abc") == {"Authorization": "Bearer abc"}
        return False

    dene("4 (anahtar koda gömülü)", dorduncu)
    dene("5 (yanlış katman)", lambda: harcanan_belirtec(YANIT) == 42)

    print("--- sonuç ---")
    for ad, durum in sonuclar:
        print(f"{ad}: {'doğru' if durum else 'henüz değil'}")
    if all(d for _, d in sonuclar):
        print("\nTAMAM")


if __name__ == "__main__":
    kontrol()
