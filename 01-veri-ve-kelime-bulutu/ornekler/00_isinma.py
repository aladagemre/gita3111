"""ISINMA — Geçen dönemden iki tamir.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/ornekler/00_isinma.py

İki fonksiyon da bozuk. Düzelt, çalıştır, en altta TAMAM yazsın.
Bu ikisi geçen dönemin en sık iki hatasıydı; bu konunun tamamı bunlara dayanıyor.
"""

# =============================================================================
# TAMİR 1 — Sözlük anahtarla açılır
#
# Bu fonksiyon bir öğrencinin puanını döndürmeli. Döndürmüyor.
# =============================================================================

def puani_getir(ogrenci):
    return ogrenci[1]


# =============================================================================
# TAMİR 2 — return nerede durmalı
#
# Bu fonksiyon listedeki sayıların toplamını döndürmeli. Yanlış sonuç veriyor.
# =============================================================================

def topla(sayilar):
    toplam = 0
    for sayi in sayilar:
        toplam = toplam + sayi
        return toplam


# =============================================================================
# KONTROL
# =============================================================================

def kontrol():
    ogrenci = {"ad": "Deniz", "puan": 85}
    testler = []

    try:
        testler.append(("Tamir 1", puani_getir(ogrenci) == 85))
    except Exception:
        testler.append(("Tamir 1", False))

    try:
        testler.append(("Tamir 2", topla([10, 20, 30]) == 60))
    except Exception:
        testler.append(("Tamir 2", False))

    for ad, durum in testler:
        print(f"{ad}: {'doğru' if durum else 'henüz değil'}")
    if all(d for _, d in testler):
        print("\nTAMAM")
    else:
        print("\nİpucu 1: sözlükten değer alırken köşeli parantez içine ANAHTAR yazılır.")
        print("İpucu 2: return, döngü bittikten sonra çalışmalı. Girintiye bak.")


if __name__ == "__main__":
    kontrol()
