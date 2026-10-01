# Adım 4 — Hata kodları: kasten yanlış anahtar gönder, durum koduna bak
# Çalıştır: uv run ornekler/04_hata_kodlari.py

import requests

anahtarlar = {}
with open("../anahtar.txt", encoding="utf-8") as dosya:
    for satir in dosya:
        ad, _, deger = satir.partition("=")
        anahtarlar[ad.strip()] = deger.strip()

hesap = anahtarlar["ACCOUNT_ID"]

MODEL = "@cf/google/gemma-4-26b-a4b-it"
adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
sahte_basliklar = {"Authorization": "Bearer bu-anahtar-sahte"}

cevap = requests.post(adres, headers=sahte_basliklar, json={"prompt": "merhaba"}, timeout=60)

if cevap.status_code == 200:
    print(cevap.json()["result"]["response"])
else:
    print("İstek başarısız:", cevap.status_code)
    print(cevap.text)
