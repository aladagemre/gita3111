"""10. adım — Hiç görmediği renklerde sınamak.

Çalıştırma:  uv run --with scikit-learn 03-makine-ogrenmesi/ornekler/10_gorulmemis_renkler.py

03'teki rastgele bölmede her renk hem eğitimde hem testte var: model "lacivert"i
teste gelmeden önce başka öğrencilerden zaten duymuş oluyor. Burada her seferinde
BİR rengi tamamen dışarıda bırakıyoruz: model o rengi hiç görmeden eğitiliyor,
sonra o renk soruluyor. Bu, "yeni bir renk gelince ne der?" sorusunun dürüst ölçümü.
"""

import csv

from sklearn.neighbors import KNeighborsClassifier

VERI = "03-makine-ogrenmesi/veri/renkler-etiketli.csv"


def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    return (int(hex_kod[0:2], 16), int(hex_kod[2:4], 16), int(hex_kod[4:6], 16))


with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

# Her rengin kodu, bir kez
renkler = {}
for kayit in kayitlar:
    renkler[kayit["ad"]] = kayit["hex"]

tutan = 0
toplam = 0
print(f"{'Dışarıda kalan renk':<20}{'sınıfın çoğunluğu':<20}{'model':<10}en yakın bildiği renk")
print("-" * 76)
for disarida in renkler:
    # Eğitim: bu renk HARİÇ her şey. Test: sadece bu rengin etiketleri
    X_egitim = []
    y_egitim = []
    adlar_egitim = []
    y_test = []
    for kayit in kayitlar:
        if kayit["ad"] == disarida:
            y_test.append(kayit["etiket"])
        else:
            X_egitim.append(hex_to_rgb(kayit["hex"]))
            y_egitim.append(kayit["etiket"])
            adlar_egitim.append(kayit["ad"])

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_egitim, y_egitim)
    rgb = hex_to_rgb(renkler[disarida])
    tahmin = model.predict([rgb])[0]
    mesafeler, siralar = model.kneighbors([rgb])
    en_yakin = adlar_egitim[siralar[0][0]]

    # Sınıfın bu renge en çok verdiği etiket
    sayac = {}
    for etiket in y_test:
        sayac[etiket] = sayac.get(etiket, 0) + 1
    en_cok = max(sayac.values())
    cogunluk = []
    for etiket in sorted(sayac):
        if sayac[etiket] == en_cok:
            cogunluk.append(etiket)
    # İki etiket eşit sayıdaysa (berabere) ikisi de "çoğunluk" sayılır
    cogunluk_yazisi = " = ".join(cogunluk)

    isaret = "" if tahmin in cogunluk else "  <- ayrıldı"
    print(f"{disarida:<20}{cogunluk_yazisi:<20}{tahmin:<10}{en_yakin}{isaret}")

    tutan = tutan + y_test.count(tahmin)
    toplam = toplam + len(y_test)

print(f"\nHiç görmediği renklerde doğruluk: {tutan / toplam:.2f}")
print("03-04'teki rastgele bölmede bu sayı 0.77 idi. Aradaki fark neyi ölçüyor?")
