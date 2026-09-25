"""ISINMA — Konu 1'den iki tamir, bu konuya hazırlık.

Çalıştırma (önce konunun klasörüne gir: cd 02-api-ile-konusmak):
    uv run ornekler/00_isinma.py

Bugün sunucudan gelen cevabı okuyacağız. O cevap İÇ İÇE bir sözlük olarak geliyor.
Bu iki alıştırma tam olarak onun provası.
"""

# =============================================================================
# TAMİR 1 — İç içe sözlükten değer çekmek
#
# Bu fonksiyon cevabın metnini döndürmeli: "Merhaba!"
# =============================================================================

YANIT = {
    "success": True,
    "result": {
        "response": "Merhaba!",
        "usage": {"prompt_tokens": 4, "completion_tokens": 2},
    },
    "errors": [],
}


def cevabi_getir(yanit):
    return yanit["response"]


# =============================================================================
# TAMİR 2 — Sözlüğün içindeki listeden değer çekmek
#
# Bu fonksiyon ilk hatanın mesajını döndürmeli: "Authentication error"
# =============================================================================

HATALI_YANIT = {
    "success": False,
    "result": None,
    "errors": [{"code": 10000, "message": "Authentication error"}],
}


def ilk_hata_mesaji(yanit):
    return yanit["errors"]["message"]


# =============================================================================
# KONTROL
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

    dene("Tamir 1", lambda: cevabi_getir(YANIT) == "Merhaba!")
    dene("Tamir 2", lambda: ilk_hata_mesaji(HATALI_YANIT) == "Authentication error")

    for ad, durum in sonuclar:
        print(f"{ad}: {'doğru' if durum else 'henüz değil'}")
    if all(d for _, d in sonuclar):
        print("\nTAMAM — bugünkü yanıtları okumaya hazırsın")
    else:
        print("\nİpucu 1: 'response' anahtarı 'result'ın İÇİNDE. Önce dışa, sonra içe.")
        print("İpucu 2: 'errors' bir LİSTE. Önce kaçıncı hatayı istediğini söylemelisin.")


if __name__ == "__main__":
    kontrol()
