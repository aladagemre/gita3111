"""1. adım — Sınıfın ürettiği veriyi okumak.

Çalıştırma (önce konunun klasörüne gir: cd 03-makine-ogrenmesi):
    uv run ornekler/01_veriyi_oku.py

Konu 2'nin ödevinde herkes 20 rengi etiketledi. Hepsi tek dosyada birleşti.
"""

import csv

VERI = "veri/renkler-etiketli.csv"

with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

print("Toplam satır:", len(kayitlar))
print("İlk kayıt   :", kayitlar[0])

# Kaç öğrenci etiketlemiş?
ogrenciler = set()
for kayit in kayitlar:
    ogrenciler.add(kayit["ogrenci"])
print("Öğrenci sayısı:", len(ogrenciler))

# Etiket dağılımı — Konu 1'deki sayaç kalıbının aynısı
sayac = {}
for kayit in kayitlar:
    sayac[kayit["etiket"]] = sayac.get(kayit["etiket"], 0) + 1

print("\nEtiket dağılımı:")
for etiket in sorted(sayac, key=sayac.get, reverse=True):
    print(f"  {sayac[etiket]:>4}  {etiket}")

# Asıl ilginç soru: aynı renge herkes aynı etiketi vermiş mi?
print("\nAynı renge verilen farklı etiketler:")
renkler = {}
for kayit in kayitlar:
    ad = kayit["ad"]
    if ad not in renkler:
        renkler[ad] = set()
    renkler[ad].add(kayit["etiket"])

anlasmazlik = 0
for ad in list(renkler)[:6]:
    etiketler = ", ".join(sorted(renkler[ad]))
    print(f"  {ad:<15} -> {etiketler}")
for ad in renkler:
    if len(renkler[ad]) > 1:
        anlasmazlik = anlasmazlik + 1

print(f"\n{anlasmazlik}/{len(renkler)} renkte sınıf anlaşamamış.")

# Anlaşmazlık her renkte aynı ölçüde mi? Her renk için ayrı bir sayaç tutalım
renk_sayaclari = {}
for kayit in kayitlar:
    ad = kayit["ad"]
    if ad not in renk_sayaclari:
        renk_sayaclari[ad] = {}
    renk_sayaclari[ad][kayit["etiket"]] = renk_sayaclari[ad].get(kayit["etiket"], 0) + 1

# uzlasma: o renge en çok verilen etiketi kaç kişi seçmiş
uzlasma = {}
for ad in renk_sayaclari:
    uzlasma[ad] = max(renk_sayaclari[ad].values())

print("\nEn çok tartışılan renkler:")
for ad in sorted(uzlasma, key=uzlasma.get)[:3]:
    print(f"  {ad:<12} {uzlasma[ad]}/{sum(renk_sayaclari[ad].values())}  {renk_sayaclari[ad]}")
print("En çok anlaşılan renkler:")
for ad in sorted(uzlasma, key=uzlasma.get, reverse=True)[:3]:
    print(f"  {ad:<12} {uzlasma[ad]}/{sum(renk_sayaclari[ad].values())}  {renk_sayaclari[ad]}")

# Model bir renk için tek cevap verebilir; en iyi ihtimalle çoğunluğu söyler
tavan = sum(uzlasma.values()) / len(kayitlar)
print(f"\nSadece renge bakan bir modelin çıkabileceği en yüksek doğruluk (tavan): {tavan:.2f}")
print("Bu bir sorun değil, bu konunun asıl sorusu: model kararsız veriyle ne yapıyor?")
