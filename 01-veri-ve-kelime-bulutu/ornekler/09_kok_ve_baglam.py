"""Derinleşme (ders notunda Adım 8) — Bulutun söylemediği iki şey: ekler ve bağlam.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/ornekler/09_kok_ve_baglam.py

Kelime bulutu iki şeyi göremez:
1. EKLER: "bahçe", "bahçesi", "bahçede" ayrı kelimeler sayılır; konu olduğundan küçük görünür.
2. BAĞLAM: "kahve" 6 kez geçiyor ama nasıl geçiyor? Övgüyle mi, "fena değil" diye mi?

Bu dosya ikisine de basit bir çözüm getiriyor: kelimeleri başlangıçlarına göre toplamak
ve kelimenin geçtiği yorumları okumak.
"""

DOSYA = "01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt"
DURAK_DOSYASI = "01-veri-ve-kelime-bulutu/veri/turkce-durak-kelimeler.txt"
NOKTALAMA = ".,!?:;()[]\"'…-–—/"


def turkce_kucult(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()


def temizle(metin):
    for isaret in NOKTALAMA:
        metin = metin.replace(isaret, " ")
    return turkce_kucult(metin)


def kelimeleri_say(kelimeler):
    sayac = {}
    for kelime in kelimeler:
        sayac[kelime] = sayac.get(kelime, 0) + 1
    return sayac


def kok_toplami(sayac, kok):
    """`kok` ile başlayan bütün kelimelerin adetlerini toplar.

    Hangi kelimeleri topladığını da döndürür; neyi saydığını görmeden sonuca güvenme.
    """
    toplam = 0
    bulunanlar = []
    for kelime in sayac:
        if kelime.startswith(kok):
            toplam = toplam + sayac[kelime]
            bulunanlar.append(kelime)
    return toplam, bulunanlar


def baglamda_goster(metin, aranan):
    """`aranan` kelimeyi içeren satırları (yorumları) ekrana basar."""
    for satir in metin.splitlines():
        if aranan in turkce_kucult(satir):
            print("   -", satir)


with open(DOSYA, encoding="utf-8") as dosya:
    metin = dosya.read()

with open(DURAK_DOSYASI, encoding="utf-8") as dosya:
    durak_kelimeler = set(dosya.read().split())

temiz_kelimeler = []
for kelime in temizle(metin).split():
    if kelime not in durak_kelimeler and len(kelime) > 2:
        temiz_kelimeler.append(kelime)

sayac = kelimeleri_say(temiz_kelimeler)

# --- 1. Ekleri toplamak -------------------------------------------------------
print("Tek kelime olarak sayınca ve başlangıcına göre toplayınca:\n")
for kok in ["sessiz", "kahve", "bahçe", "priz", "ışık"]:
    toplam, bulunanlar = kok_toplami(sayac, kok)
    print(f"{kok:>8}: tek başına {sayac.get(kok, 0)}, toplamda {toplam}  {bulunanlar}")

print("\nDikkat: 'kahve' toplayınca 6'ya çıktı, 'priz'i geçti.")
print("Bulgumuz çöktü mü? Sayı bunu söyleyemez. Yorumları okuyalım.\n")

# --- 2. Bağlamda okumak -------------------------------------------------------
for aranan in ["kahve", "ışık"]:
    print(f"'{aranan}' geçen yorumlar:")
    baglamda_goster(metin, aranan)
    print()

print("Kahve altı yorumda geçiyor. Üçünde ılık bir sözle ('fena değil', 'ortalama',")
print("'biraz pahalı'), birinde asıl övülen cheesecake, birinde kafe 'kütüphane gibi ama")
print("kahveli' diye anlatılıyor. Kahveyi doğrudan öven tek yorum var. Müşteri kahveden söz")
print("ediyor, ama geliş sebebi o değil.")
print()
print("Işık ise ayrı bir bulgu: iç mekân karanlık, bahçe aydınlık. Kimlik yenilemesi")
print("yalnızca logo değil; iç mekânın aydınlatması da bu işin parçası olabilir.")
