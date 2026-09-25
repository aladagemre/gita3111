"""Derinleşme (ders notunda Adım 9) — Aynı sayaç, çubuk grafik olarak.

Çalıştırma:  uv run 01-veri-ve-kelime-bulutu/ornekler/10_cubuk_grafik.py

Kelime bulutu bir İZLENİM verir: "sessiz" büyük, gerisi küçük.
Çubuk grafik ise KARŞILAŞTIRMA verir: "sessiz" ikinci sıradakinden kaç fazla?
Hangisini seçeceğin, izleyicine ne söylemek istediğine bağlı. Bu bir tasarım kararı.

Hazırlık klasöründeki grafik.py'yi yalnızca çalıştırmıştın; burada satır satır yazıyoruz.
"""

import matplotlib
matplotlib.use("Agg")          # ekran açmadan doğrudan dosyaya çizer
import matplotlib.pyplot as plt

DOSYA = "01-veri-ve-kelime-bulutu/veri/kafe-yorumlari.txt"
DURAK_DOSYASI = "01-veri-ve-kelime-bulutu/veri/turkce-durak-kelimeler.txt"
CIKTI = "kelime-grafik.png"
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


with open(DOSYA, encoding="utf-8") as dosya:
    kelimeler = temizle(dosya.read()).split()

with open(DURAK_DOSYASI, encoding="utf-8") as dosya:
    durak_kelimeler = set(dosya.read().split())

temiz_kelimeler = []
for kelime in kelimeler:
    if kelime not in durak_kelimeler and len(kelime) > 2:
        temiz_kelimeler.append(kelime)

sayac = kelimeleri_say(temiz_kelimeler)
sirali = sorted(sayac, key=sayac.get, reverse=True)

# Grafik iki ayrı liste ister: çubukların adları ve boyları.
# Sözlükten ikisini de ANAHTARLA çıkarıyoruz.
etiketler = []
degerler = []
for kelime in sirali[:10]:
    etiketler.append(kelime)
    degerler.append(sayac[kelime])

plt.figure(figsize=(8, 4.5))             # tuvalin boyu: genişlik, yükseklik (inç)
plt.bar(etiketler, degerler, color="#4a6fa5")
plt.title("Müşteri yorumlarında en sık 10 kelime")
plt.ylabel("Kaç kez geçti")
plt.xticks(rotation=45, ha="right")      # uzun kelimeler üst üste binmesin
plt.tight_layout()                       # kenarlarda yazı kesilmesin
plt.savefig(CIKTI, dpi=150)
plt.close()                              # tuvali kapat, bellekte kalmasın

print(f"Grafik kaydedildi: {CIKTI}")
for kelime in etiketler:
    print(f"{sayac[kelime]:>3}  {kelime}")
print("\nBulutta 'çalışmak', 'yer' ve 'priz' aynı boyda görünüyordu; grafikte de eşitler.")
print("Ama 'sessiz' onlardan belirgin biçimde uzun: 8'e 5. Bulut bunu sezdirir, grafik ölçer.")
