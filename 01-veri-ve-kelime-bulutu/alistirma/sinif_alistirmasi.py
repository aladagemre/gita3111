# Sınıf alıştırması — Konu 1 (boşluk doldurma ve hata bulma, vizedeki gibi)
# Çalıştır: uv run alistirma/sinif_alistirmasi.py
# Önce bu dosyayı yeni bir adla kopyala (ör. benim_alistirmam.py), kopyada çalış.
# Soruları sırayla çöz. Doldurmadığın ilk ___ "NameError" verir; orası sıradaki soru.

# Soru 1 — Boşlukları doldur. Boşluklar hariç harf sayısını (9) yazmalı
metin = "ali topu at"
toplam = ___
for karakter in metin:
    if karakter != " ":
        toplam = ___
print(___)

# Soru 2 — Boşlukları doldur. {'a': 2, 'b': 1} yazmalı
sayac = ___                     # boş sözlük
for kelime in ["a", "b", "a"]:
    if kelime in sayac:
        sayac[kelime] = ___
    else:
        sayac[kelime] = 1
print(sayac)

# Soru 3 — Hatayı bul (hangi satır, neden?). "kütüphane" yazmalı
def en_uzun_kelime(kelimeler):
    en_uzun = ""
    for kelime in kelimeler:
        if len(kelime) > len(en_uzun):
            en_uzun = kelime
        return en_uzun

print(en_uzun_kelime(["ev", "okul", "kütüphane", "yol"]))

# Soru 4 — Hatayı bul (hangi satır, neden?). "kahve 8" yazmalı
sayac = {"kahve": 8, "çay": 3}
sirali = sorted(sayac, key=sayac.get, reverse=True)
print(sirali[0], sayac[0])

# Soru 5 — Tamamla. Adedi 3'ten büyük kelimeleri yazmalı: ['a', 'c']
sayac = {"a": 5, "b": 2, "c": 9}
sonuc = []
# buraya yaz
print(sonuc)

# Ek soru 1 (isteğe bağlı) — En az geçen iki kelimeyi yazmalı: ['b', 'c']
sayac = {"a": 9, "b": 1, "c": 2}
# buraya yaz

# Ek soru 2 (isteğe bağlı) — Adetlerin toplamını (5) yazmalı
sayac = {"a": 2, "b": 3}
# buraya yaz

# Ek soru 3 (isteğe bağlı) — "k" ile başlayan kelimeleri yazmalı: ['kahve', 'kek']
sayac = {"kahve": 2, "kek": 1, "çay": 5}
# buraya yaz
