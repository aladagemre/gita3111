# Adım 7 — Soruya bağlam koymak cevabı değiştiriyor mu?
# Çalıştır: uv run ornekler/09_baglam_farki.py

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


KELIMELER = ["kahve", "fincan", "aroma", "köpü", "yudum", "sessiz", "odak", "çalış", "priz", "sakin"]

baglamsiz = ""
baglamli = ""
for _ in range(3):  # model her seferinde başka cümle kurar; üçer kez soruyoruz
    baglamsiz = baglamsiz + modele_sor("Bir kafe için üç kısa slogan yaz.") + "\n"
    baglamli = baglamli + modele_sor("Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz.") + "\n"

print(baglamsiz)
print(baglamli)

for kelime in KELIMELER:
    print(kelime, baglamsiz.lower().count(kelime), baglamli.lower().count(kelime))
