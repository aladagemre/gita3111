# Adım 1 — Sınıfın verisine bak
# Çalıştır: uv run ornekler/01_veriyi_oku.py

import csv

with open("veri/renkler-etiketli.csv", encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

print(len(kayitlar))
print(kayitlar[0])

renkler = {}  # her renk için ayrı bir sayaç
for kayit in kayitlar:
    ad = kayit["ad"]
    if ad not in renkler:
        renkler[ad] = {}
    renkler[ad][kayit["etiket"]] = renkler[ad].get(kayit["etiket"], 0) + 1

for ad in renkler:
    print(ad, renkler[ad])

tutan = 0  # model her renkte en iyi ihtimalle çoğunluğu bilir
for ad in renkler:
    tutan = tutan + max(renkler[ad].values())
print("Tavan:", round(tutan / len(kayitlar), 2))
