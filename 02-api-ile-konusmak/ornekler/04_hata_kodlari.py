"""4. adım — Hatalarla tanışmak.

Çalıştırma:  uv run --with requests 02-api-ile-konusmak/ornekler/04_hata_kodlari.py

Bu dersin geri kalanında en çok göreceğin üç sayı: 401, 429, 500.
Ne anlama geldiklerini bugün öğrenirsen, ilerideki konularda saatler kazanırsın.
"""

import json

import requests

MODEL = "@cf/google/gemma-4-26b-a4b-it"
ANAHTAR_DOSYASI = "anahtar.txt"

HATA_SOZLUGU = {
    200: "Her şey yolunda.",
    400: "İstek bozuk. Gövdede yanlış bir alan göndermiş olabilirsin.",
    401: "Yetki yok. Anahtar yanlış, eksik ya da kopyalarken bir karakter düşmüş.",
    403: "Anahtar doğru ama bu işlem için izni yok.",
    404: "Adres yanlış. Model adını ya da hesap kimliğini kontrol et.",
    429: "Çok fazla istek. Günlük kotan bitmiş olabilir; kota her gün 00:00 UTC'de sıfırlanır.",
    500: "Sunucu tarafında hata. Senin kodunda sorun yok, biraz sonra tekrar dene.",
}


def acikla(kod):
    return HATA_SOZLUGU.get(kod, "Tanımadığım bir kod. İnternette arat.")


print("--- Hata kodları sözlüğü ---")
for kod in sorted(HATA_SOZLUGU):
    print(f"{kod}: {acikla(kod)}")

print("\n--- Canlı deney: kasten YANLIŞ anahtar gönderiyoruz ---")

try:
    with open(ANAHTAR_DOSYASI, encoding="utf-8") as dosya:
        satirlar = dict(
            (p[0].strip().upper(), p[2].strip())
            for p in (s.partition("=") for s in dosya if "=" in s)
        )
    hesap = satirlar["ACCOUNT_ID"]
except (FileNotFoundError, KeyError):
    print("anahtar.txt yok, canlı deney atlandı. Sözlüğü okumak yine de işine yarar.")
    raise SystemExit(0)

adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
basliklar = {"Authorization": "Bearer bu-anahtar-sahte"}

cevap = requests.post(adres, headers=basliklar, json={"prompt": "merhaba"}, timeout=60)
print("Durum kodu:", cevap.status_code, "->", acikla(cevap.status_code))
print("\nSunucunun söyledikleri:")
print(json.dumps(cevap.json(), ensure_ascii=False, indent=2)[:400])

print("\nDers: hata aldığında önce DURUM KODUNA bak. Kod sana nereye bakacağını söyler.")
