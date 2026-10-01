# Adım 1 — Anahtarı dosyadan oku
# Çalıştır: uv run ornekler/01_anahtar_oku.py

anahtarlar = {}
with open("../anahtar.txt", encoding="utf-8") as dosya:  # ".." = bir üst klasör
    for satir in dosya:
        ad, _, deger = satir.partition("=")  # "=" işaretinden ikiye böl
        anahtarlar[ad.strip()] = deger.strip()

hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]

print("Hesap:", hesap)
print("Anahtar okundu.")
