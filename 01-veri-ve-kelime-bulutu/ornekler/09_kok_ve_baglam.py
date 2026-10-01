# Adım 8 — Ekleri topla, kelimeyi bağlamında oku
# Çalıştır: uv run ornekler/09_kok_ve_baglam.py

with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

temiz = metin.replace("I", "ı").replace("İ", "i").lower()
for isaret in ".,!?:;()[]\"'…-–—/":
    temiz = temiz.replace(isaret, " ")
kelimeler = temiz.split()

for kok in ["sessiz", "kahve", "bahçe", "priz", "ışık"]:
    bulunanlar = []
    for kelime in kelimeler:
        if kelime.startswith(kok):   # bu harflerle mi başlıyor?
            bulunanlar.append(kelime)
    print(kok, len(bulunanlar), bulunanlar)

for aranan in ["kahve", "ışık"]:
    print(aranan)
    for satir in temiz.splitlines():   # her satır bir yorum
        if aranan in satir:
            print("  ", satir)
