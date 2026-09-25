"""SINIF ALIŞTIRMASI — Konu 3 (makine öğrenmesi)

Kendi başına doldur. Süre: ~40 dakika.
Soru tipleri vize ile aynı: boşluk doldurma ve hata bulma.

Çalıştırma (önce konunun klasörüne gir: cd 03-makine-ogrenmesi):
    uv run alistirma/sinif_alistirmasi.py

Doldurmadan önce bu dosyayı aynı klasörde yeni bir adla kopyala
(örneğin benim_alistirmam.py), kopyayı doldur ve çalıştır; böylece git pull çakışmaz.
"""

BOSLUK = None

KAYITLAR = [
    {"hex": "#E63946", "ad": "kırmızı", "etiket": "enerjik"},
    {"hex": "#457B9D", "ad": "orta mavi", "etiket": "sakin"},
    {"hex": "#1D3557", "ad": "lacivert", "etiket": "ciddi"},
    {"hex": "#F4A261", "ad": "şeftali", "etiket": "enerjik"},
]


# =============================================================================
# SORU 1 — Boşlukları doldur (2 boşluk)
# "#E63946" -> (230, 57, 70)
# İpucu: her renk iki karakterle yazılıyor, 16'lık tabanda.
# =============================================================================

def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    kirmizi = int(hex_kod[0:2], BOSLUK)      # (a) hangi taban?
    yesil = int(hex_kod[BOSLUK], 16)         # (b) hangi dilim?
    mavi = int(hex_kod[4:6], 16)
    return (kirmizi, yesil, mavi)


# =============================================================================
# SORU 2 — Boşlukları doldur (2 boşluk)
# Öznitelik listesi X ve etiket listesi y üret. İkisi aynı sırada olmalı.
# =============================================================================

def veriyi_hazirla(kayitlar):
    X = []
    y = []
    for kayit in kayitlar:
        X.append(BOSLUK)                     # (a) sayıya çevrilmiş renk
        y.append(BOSLUK)                     # (b) o rengin etiketi
    return X, y


# =============================================================================
# SORU 3 — Hatayı bul ve düzelt
# Etiket dağılımını saymalı: {"enerjik": 2, "sakin": 1, "ciddi": 1}
#
# Hatanın satırı :
# Nedeni         :
# =============================================================================

def etiket_dagilimi(kayitlar):
    sayac = {}
    for kayit in kayitlar:
        sayac[kayit] = sayac.get(kayit, 0) + 1
    return sayac


# =============================================================================
# SORU 4 — Hatayı bul ve düzelt
# Doğruluk oranı hesaplamalı: kaç tahmin tuttu / toplam tahmin.
#
# Hatanın satırı :
# Nedeni         :
# =============================================================================

def dogruluk(gercekler, tahminler):
    tutan = 0
    for i in range(len(gercekler)):
        if gercekler[i] == tahminler[i]:
            tutan = tutan + 1
    return tutan


# =============================================================================
# SORU 5 — Kısa tamamlama (3-4 satır)
# Belirli bir etikete sahip kayıtların renk ADLARINI liste olarak döndür.
# =============================================================================

def etiketi_olanlar(kayitlar, etiket):
    sonuc = []
    # buraya yaz
    return sonuc


# =============================================================================
# HIZLI BİTİRENLER İÇİN
# =============================================================================

def en_koyu_renk(kayitlar):
    """R+G+B toplamı en küçük olan kaydın ADINI döndür."""
    return ""


def etiket_orani(kayitlar, etiket):
    """Verilen etiketin oranını döndür. 4 kayıttan 2'si enerjikse 0.5."""
    return 0.0


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

    dene("1", lambda: hex_to_rgb("#E63946") == (230, 57, 70))

    def ikinci():
        X, y = veriyi_hazirla(KAYITLAR)
        return X[0] == (230, 57, 70) and y[0] == "enerjik" and len(X) == len(y) == 4

    dene("2", ikinci)
    dene("3", lambda: etiket_dagilimi(KAYITLAR) == {"enerjik": 2, "sakin": 1, "ciddi": 1})
    dene("4", lambda: dogruluk(["a", "b", "c", "d"], ["a", "x", "c", "y"]) == 0.5)
    dene("5", lambda: etiketi_olanlar(KAYITLAR, "enerjik") == ["kırmızı", "şeftali"])

    cekirdek = list(sonuclar)

    dene("E1", lambda: en_koyu_renk(KAYITLAR) == "lacivert")
    dene("E2", lambda: abs(etiket_orani(KAYITLAR, "enerjik") - 0.5) < 0.001)

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
