"""ISINMA — CSV satırlarını sözlüğe çevirmek.

Çalıştırma:  uv run 03-makine-ogrenmesi/ornekler/00_isinma.py

Bu konuda tablo hâlinde veriyle çalışacağız. Her satır bir sözlük olacak —
Konu 2'deki API yanıtları gibi. İki alıştırma, o yapının provası.
"""

# Bir CSV dosyasından okunmuş üç satır (başlık ayrı)
BASLIK = ["hex", "ad", "etiket"]
SATIRLAR = [
    ["#E63946", "kırmızı", "enerjik"],
    ["#457B9D", "orta mavi", "sakin"],
    ["#1D3557", "lacivert", "ciddi"],
]


# =============================================================================
# TAMİR 1 — Satırı sözlüğe çevir
#
# ["#E63946", "kırmızı", "enerjik"]  ->  {"hex": "#E63946", "ad": "kırmızı", ...}
# =============================================================================

def satiri_sozluge_cevir(baslik, satir):
    sozluk = {}
    for i in range(len(baslik)):
        sozluk[satir[i]] = baslik[i]
    return sozluk


# =============================================================================
# TAMİR 2 — Etiketleri say
#
# Sözlük listesinden {"enerjik": 1, "sakin": 1, "ciddi": 1} üretmeli.
# =============================================================================

def etiketleri_say(kayitlar):
    sayac = {}
    for kayit in kayitlar:
        sayac[kayit] = sayac.get(kayit, 0) + 1
    return sayac


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

    beklenen = {"hex": "#E63946", "ad": "kırmızı", "etiket": "enerjik"}
    dene("Tamir 1", lambda: satiri_sozluge_cevir(BASLIK, SATIRLAR[0]) == beklenen)

    kayitlar = []
    for satir in SATIRLAR:
        kayitlar.append(satiri_sozluge_cevir(BASLIK, satir))
    dene("Tamir 2", lambda: etiketleri_say(kayitlar) == {"enerjik": 1, "sakin": 1, "ciddi": 1})

    for ad, durum in sonuclar:
        print(f"{ad}: {'doğru' if durum else 'henüz değil'}")
    if all(d for _, d in sonuclar):
        print("\nTAMAM — bu konunun verisiyle çalışmaya hazırsın")
    else:
        print("\nİpucu 1: anahtar başlıktan, değer satırdan gelmeli. Ters yazılmış.")
        print("İpucu 2: sayaç kaydın kendisini değil, 'etiket' alanını saymalı.")


if __name__ == "__main__":
    kontrol()
