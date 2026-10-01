# Isınma — Geçen dönemin iki hatası
# Çalıştır: uv run ornekler/00_isinma.py

# Tamir 1: öğrencinin puanını (85) döndürmeli. Hata veriyor.
def puani_getir(ogrenci):
    return ogrenci[1]

# Tamir 2: sayıların toplamını (60) döndürmeli. Yanlış sonuç veriyor.
def topla(sayilar):
    toplam = 0
    for sayi in sayilar:
        toplam = toplam + sayi
        return toplam

print(topla([10, 20, 30]))
print(puani_getir({"ad": "Deniz", "puan": 85}))
