"""2. adım — İlk istek.

Çalıştırma (önce konunun klasörüne gir: cd 02-api-ile-konusmak):
    uv run ornekler/02_ilk_istek.py

Bu dosya ilk kez bilgisayarının dışına çıkıyor: bir soruyu uzaktaki bir modele
gönderiyor ve cevabı geri alıyor.

anahtar.txt yoksa DEMO modunda çalışır — kayıtlı bir yanıtla aynı şeyi gösterir.
"""

import json

import requests

MODEL = "@cf/google/gemma-4-26b-a4b-it"
ANAHTAR_DOSYASI = "../anahtar.txt"
DEMO_YANIT = "veri/ornek_yanit.json"
SORU = "Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz."


def anahtarlari_oku(yol=ANAHTAR_DOSYASI):
    degerler = {}
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:
            if "=" in satir:
                ad, _, deger = satir.partition("=")
                degerler[ad.strip().upper()] = deger.strip()
    return degerler


def anahtar_durumu(yol=ANAHTAR_DOSYASI):
    """Anahtar dosyasının durumunu döndürür: 'tamam', 'yok' ya da 'bozuk'.

    Bozuk ile yok'u ayırmak önemli: dosyası olmayan öğrenci demo moduyla dersi
    izleyebilir, ama dosyası BOZUK olan öğrenci "çalışıyor" sanıp yoluna devam
    etmemeli.
    """
    try:
        degerler = anahtarlari_oku(yol)
    except FileNotFoundError:
        return "yok", {}
    if degerler.get("ACCOUNT_ID") and degerler.get("API_TOKEN"):
        return "tamam", degerler
    return "bozuk", degerler


durum, anahtarlar = anahtar_durumu()
demo = durum != "tamam"

if durum == "bozuk":
    print("[UYARI] anahtar.txt var ama içinden ACCOUNT_ID / API_TOKEN okunamadı.")
    print("        Dosyanın içi tam olarak şöyle olmalı (iki satır, eşittir işaretli):")
    print("        ACCOUNT_ID = ...")
    print("        API_TOKEN = ...")
    print("        Şimdilik demo moduna geçiliyor, ama bunu düzeltmen gerekiyor.\n")
elif durum == "yok":
    print("[DEMO MODU] anahtar.txt yok; kayıtlı bir yanıt kullanılıyor.\n")

if not demo:
    hesap = anahtarlar["ACCOUNT_ID"]
    anahtar = anahtarlar["API_TOKEN"]

if demo:
    with open(DEMO_YANIT, encoding="utf-8") as dosya:
        yanit = json.load(dosya)
else:
    # Adres üç parçadan oluşuyor: sunucu + hesabın + çalıştırmak istediğin model
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"

    # Başlık (header): "ben kimim" bilgisi. Anahtar burada gider.
    basliklar = {"Authorization": f"Bearer {anahtar}"}

    # Gövde (body): "ne istiyorum" bilgisi.
    govde = {"prompt": SORU}

    print("İstek gönderiliyor...")
    cevap = requests.post(adres, headers=basliklar, json=govde, timeout=60)
    print("Durum kodu:", cevap.status_code)
    yanit = cevap.json()

print("\n--- GELEN HAM YANIT ---")
print(json.dumps(yanit, ensure_ascii=False, indent=2)[:600])
print("\nBu bir SÖZLÜK. İçinden metni nasıl çekeceğimiz bir sonraki dosyada.")
