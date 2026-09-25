"""9. adım — Model ne öğrendi? Yeni renklerle yoklamak.

Çalıştırma:  uv run --with scikit-learn 03-makine-ogrenmesi/ornekler/09_modeli_yokla.py

Modelin içini açıp "kuralını" okuyamayız; ama ona hiç görmediği renkleri
sorup cevaplarından ne öğrendiğini çıkarabiliriz. Her cevabın yanında,
modelin o cevabı hangi komşulara bakarak verdiğini de yazdırıyoruz.
"""

import csv

from sklearn.neighbors import KNeighborsClassifier

VERI = "03-makine-ogrenmesi/veri/renkler-etiketli.csv"

# Aynı rengin koyudan açığa üç sürümü: koyuluk etiketi değiştiriyor mu?
MAVILER = [("#0A1F44", "çok koyu mavi"), ("#4A7FB0", "orta mavi"), ("#CFE3F2", "buz mavisi")]
KIRMIZILAR = [("#5C0010", "çok koyu kırmızı"), ("#D62828", "canlı kırmızı"), ("#FAD4D4", "toz pembe")]

# Konu 1'deki "sessiz çalışma kafesi" için aday bir palet
KAFE_PALETI = [
    ("#E8DCC4", "bej"),
    ("#D4A373", "sütlü kahve"),
    ("#A3B18A", "adaçayı"),
    ("#344E41", "orman yeşili"),
    ("#F5F5F5", "kirli beyaz"),
]


def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    return (int(hex_kod[0:2], 16), int(hex_kod[2:4], 16), int(hex_kod[4:6], 16))


with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
adlar = []
for kayit in kayitlar:
    X.append(hex_to_rgb(kayit["hex"]))
    y.append(kayit["etiket"])
    adlar.append(kayit["ad"])

# Ölçüm yapmıyoruz, yokluyoruz: bu yüzden tüm veriyle eğitiyoruz
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X, y)


def yokla(baslik, renkler):
    print(baslik)
    for hex_kod, ad in renkler:
        rgb = hex_to_rgb(hex_kod)
        tahmin = model.predict([rgb])[0]
        # kneighbors: en yakın 5 komşunun uzaklığını ve sıra numarasını verir
        mesafeler, siralar = model.kneighbors([rgb])
        oylar = []
        komsu_renkler = set()
        for sira in siralar[0]:
            oylar.append(y[sira])
            komsu_renkler.add(adlar[sira])
        print(f"  {ad:<17}{hex_kod}  -> {tahmin:<8}"
              f"komşu: {', '.join(sorted(komsu_renkler))}  oylar: {', '.join(oylar)}")
    print()


yokla("Mavi koyulaştıkça:", MAVILER)
yokla("Kırmızı koyulaştıkça:", KIRMIZILAR)
yokla("Sessiz kafe için aday palet:", KAFE_PALETI)

print("Modelin bildiği dünya 20 renkten ibaret. Yeni bir renge verdiği cevap,")
print("o 20 renkten hangisine en çok benzediğine bağlı. Komşu sütununa bak:")
print("cevabı modelin değil, o komşu rengi etiketleyen arkadaşlarının verdiğini görürsün.")
