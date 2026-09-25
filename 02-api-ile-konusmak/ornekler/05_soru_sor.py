"""5. adım — Kullanıcıdan soru al, cevabı dosyaya yaz.

Çalıştırma:  uv run --with requests 02-api-ile-konusmak/ornekler/05_soru_sor.py

Bu konunun hedef çıktısı bu dosya.
"""

import json

import requests

MODEL = "@cf/google/gemma-4-26b-a4b-it"
ANAHTAR_DOSYASI = "anahtar.txt"
DEMO_YANIT = "02-api-ile-konusmak/veri/ornek_yanit.json"
CIKTI = "cevap.txt"


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


def modele_sor(soru, hesap, anahtar):
    """Soruyu modele gönderir, cevabın METNİNİ döndürür."""
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
    basliklar = {"Authorization": f"Bearer {anahtar}"}
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    if cevap.status_code != 200:
        return f"[HATA {cevap.status_code}] İstek başarısız oldu."
    return cevap.json()["result"]["response"]


soru = input("Modele ne sormak istiyorsun? ")

durum, anahtarlar = anahtar_durumu()

if durum == "tamam":
    metin = modele_sor(soru, anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"])
else:
    if durum == "bozuk":
        print("[UYARI] anahtar.txt var ama ACCOUNT_ID / API_TOKEN okunamadı — düzeltmen gerek.")
    else:
        print("[DEMO MODU] anahtar.txt yok; kayıtlı bir cevap kullanılıyor.")
    with open(DEMO_YANIT, encoding="utf-8") as dosya:
        metin = json.load(dosya)["result"]["response"]

print("\n--- CEVAP ---")
print(metin)

with open(CIKTI, "w", encoding="utf-8") as dosya:
    dosya.write(f"SORU: {soru}\n\nCEVAP:\n{metin}\n")

print(f"\nKaydedildi: {CIKTI}")
