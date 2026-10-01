# Bozuk kodlar — sırayla düzelt; her düzeltmeden sonra yeniden çalıştır
# Çalıştır: uv run ornekler/07_bozuk_kodlar.py

# 1) "kahve 45" yazmalı
fiyatlar = {"kahve": 45, "çay": 30}
sirali = sorted(fiyatlar, key=fiyatlar.get, reverse=True)
print(sirali[0], fiyatlar[0])

# 2) "istanbul" içindeki sesli harf sayısını (3) yazmalı
for harf in "istanbul":
    if harf in "aeıioöuü":
        adet = adet + 1
print(adet)

# 3) Beş harften uzun kelimeleri yazmalı: ['kütüphane', 'bilgisayar']
for kelime in ["ev", "kütüphane", "bilgisayar"]:
    uzunlar = []
    if len(kelime) > 5:
        uzunlar.append(kelime)
print(uzunlar)

# 4) Adetlerin toplamını (5) yazmalı
sayac = {"kahve": 2, "çay": 3}
toplam = 0
for kelime in sayac:
    toplam = toplam + kelime
print(toplam)

# 5) "istanbul" kelimesini 3 kez saymalı
kelimeler = "İstanbul istanbul İSTANBUL".lower().split()
print(kelimeler.count("istanbul"))
