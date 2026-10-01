# Adım 5 — Soruyu fonksiyona koy, cevabı dosyaya yaz
# Çalıştır: uv run ornekler/05_soru_sor.py

import requests

anahtarlar = {}
with open("../anahtar.txt", encoding="utf-8") as dosya:
    for satir in dosya:
        ad, _, deger = satir.partition("=")
        anahtarlar[ad.strip()] = deger.strip()

hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]

MODEL = "@cf/google/gemma-4-26b-a4b-it"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": f"Bearer {anahtar}"}


def modele_sor(soru):
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    return cevap.json()["result"]["response"]


soru = input("Modele ne sormak istiyorsun? ")
metin = modele_sor(soru)
print(metin)

with open("cevap.txt", "w", encoding="utf-8") as dosya:
    dosya.write(f"SORU: {soru}\n\nCEVAP:\n{metin}\n")
