# Adım 2 — İlk istek: soruyu modele gönder, ham yanıtı gör
# Çalıştır: uv run ornekler/02_ilk_istek.py

import json

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
govde = {"prompt": "Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz."}

cevap = requests.post(adres, headers=basliklar, json=govde, timeout=60)
print("Durum kodu:", cevap.status_code)

yanit = cevap.json()
print(json.dumps(yanit, ensure_ascii=False, indent=2))
