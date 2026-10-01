# Adım 6 — Beş soruyu döngüyle sor, cevapları JSON dosyasına kaydet
# Çalıştır: uv run ornekler/06_coklu_soru.py

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


def modele_sor(soru):
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    return cevap.json()["result"]["response"]


sorular = []
with open("veri/ornek_sorular.txt", encoding="utf-8") as dosya:
    for satir in dosya:  # her satır bir soru
        sorular.append(satir.strip())

kayitlar = []
for soru in sorular:
    print(soru)
    kayitlar.append({"soru": soru, "cevap": modele_sor(soru)})

with open("cevaplar.json", "w", encoding="utf-8") as dosya:
    json.dump(kayitlar, dosya, ensure_ascii=False, indent=2)
