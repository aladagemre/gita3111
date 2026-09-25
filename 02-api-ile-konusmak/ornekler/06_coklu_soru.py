"""6. adım — Beş soruyu döngüyle sorup JSON'a kaydetmek.

Çalıştırma:  uv run --with requests 02-api-ile-konusmak/ornekler/06_coklu_soru.py

Tek soru sormak güzel ama kodun asıl gücü burada: aynı işi elli kez yapmak.
"""

import json
import time

import requests

MODEL = "@cf/google/gemma-4-26b-a4b-it"
ANAHTAR_DOSYASI = "anahtar.txt"
SORULAR_DOSYASI = "02-api-ile-konusmak/veri/ornek_sorular.txt"
DEMO_YANIT = "02-api-ile-konusmak/veri/ornek_yanit.json"
CIKTI = "cevaplar.json"
BEKLEME = 1  # istekler arasında saniye — sunucuyu yormamak için


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
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
    basliklar = {"Authorization": f"Bearer {anahtar}"}
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    if cevap.status_code != 200:
        return f"[HATA {cevap.status_code}]"
    return cevap.json()["result"]["response"]


sorular = []
with open(SORULAR_DOSYASI, encoding="utf-8") as dosya:
    for satir in dosya:
        if satir.strip():
            sorular.append(satir.strip())

durum, anahtarlar = anahtar_durumu()
demo = durum != "tamam"

if durum == "bozuk":
    print("[UYARI] anahtar.txt var ama ACCOUNT_ID / API_TOKEN okunamadı — düzeltmen gerek.\n")
elif durum == "yok":
    print("[DEMO MODU] anahtar.txt yok; her soruya kayıtlı cevap veriliyor.\n")

if demo:
    with open(DEMO_YANIT, encoding="utf-8") as dosya:
        demo_metin = json.load(dosya)["result"]["response"]
else:
    hesap, anahtar = anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]

kayitlar = []
sira = 0
for soru in sorular:
    sira = sira + 1
    print(f"[{sira}/{len(sorular)}] {soru}")
    if demo:
        metin = demo_metin
    else:
        metin = modele_sor(soru, hesap, anahtar)
        time.sleep(BEKLEME)
    kayitlar.append({"soru": soru, "cevap": metin})

with open(CIKTI, "w", encoding="utf-8") as dosya:
    json.dump(kayitlar, dosya, ensure_ascii=False, indent=2)

print(f"\n{len(kayitlar)} cevap kaydedildi: {CIKTI}")
print("Dosyayı aç ve bak: bir LİSTE içinde SÖZLÜKLER var.")
