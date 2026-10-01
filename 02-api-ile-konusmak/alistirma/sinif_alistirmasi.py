# Sınıf alıştırması — Konu 2: ___ yerlerini doldur, hatalı satırları düzelt
# Çalıştır: uv run alistirma/sinif_alistirmasi.py

yanit = {
    "result": {
        "response": "Serif yazı tiplerinde harflerin uçlarında küçük tırnaklar bulunur.",
        "usage": {"prompt_tokens": 9, "completion_tokens": 14, "total_tokens": 23},
    },
    "success": True,
    "errors": [],
}

kayitlar = [
    {"soru": "Slogan yaz", "cevap": "Sabahın en güzel hâli"},
    {"soru": "Renk öner", "cevap": "Toprak tonları sıcak durur"},
    {"soru": "Font öner", "cevap": "Okunaklı bir sans-serif iş görür"},
]

# Soru 1 — Doldur: modelin metnini yazmalı (Serif yazı tiplerinde ...)
print(yanit[___][___])

# Soru 2 — Doldur: {'Authorization': 'Bearer abc'} yazmalı
anahtar = "abc"
basliklar = {___: ___}
print(basliklar)

# Soru 3 — Düzelt: bütün cevapların toplam kelime sayısını yazmalı (13)
toplam = 0
for kayit in kayitlar:
    toplam = toplam + len(kayit.split())
print(toplam)

# Soru 4 — Düzelt: "401 Yetki yok" ve "429 Kota doldu" yazmalı
aciklama = {401: "Yetki yok", 429: "Kota doldu", 500: "Sunucu hatası"}
for kod in [401, 429]:
    print(kod, aciklama[401])

# Soru 5 — Doldur: cevabı 3 kelimeden uzun olan kayıtların sorusunu yazmalı
for kayit in kayitlar:
    if ___ > 3:
        print(___)

# Ek soru — Doldur: cevabı en uzun olan kaydın sorusunu yazmalı (Font öner)
en_uzun = kayitlar[0]
for kayit in kayitlar:
    if ___:
        en_uzun = kayit
print(en_uzun["soru"])
