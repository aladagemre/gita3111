"""7. adım — Bozuk kodlar galerisi (makine öğrenmesi sürümü).

Çalıştırma (önce konunun klasörüne gir: cd 03-makine-ogrenmesi):
    uv run ornekler/07_bozuk_kodlar.py

Düzeltmeden önce bu dosyayı aynı klasörde yeni bir adla kopyala
(örneğin benim_bozuklarim.py), kopyada düzelt; böylece git pull çakışmaz.

Beş hata, beşi de bu konunun içinden. Bazıları programı çöktürüyor (eğitmeden
tahmin istemek gibi), bazıları hiçbir hata vermeden yanlış sonuç veriyor (doğruluğu
eğitim verisinde ölçmek gibi) — ve sessiz olanlar tehlikeli olanlar.
"""

from sklearn.neighbors import KNeighborsClassifier

KAYITLAR = [
    {"hex": "#E63946", "etiket": "enerjik"},
    {"hex": "#457B9D", "etiket": "sakin"},
    {"hex": "#1D3557", "etiket": "ciddi"},
    {"hex": "#F4A261", "etiket": "enerjik"},
    {"hex": "#A8DADC", "etiket": "sakin"},
    {"hex": "#264653", "etiket": "ciddi"},
]


# -----------------------------------------------------------------------------
# 1) Renk kodu yanlış parçalanıyor
#    "#E63946" -> (230, 57, 70) olmalı
# -----------------------------------------------------------------------------

def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    return (int(hex_kod[0:1], 16), int(hex_kod[1:2], 16), int(hex_kod[2:3], 16))


# -----------------------------------------------------------------------------
# 2) X ve y farklı süzgeçlerden geçmiş — hizaları bozulmuş
#    Model X[3]'ün cevabı olarak y[3]'e bakar. Kaymışsa sessizce yanlış öğrenir.
# -----------------------------------------------------------------------------

def veriyi_hazirla(kayitlar):
    X = []
    y = []
    for kayit in kayitlar:
        if kayit["etiket"] != "ciddi":
            X.append(hex_to_rgb(kayit["hex"]))
    for kayit in kayitlar:
        y.append(kayit["etiket"])
    return X, y


# -----------------------------------------------------------------------------
# 3) Etiket, özniteliğin içine karışmış
#    Modele cevabı da veriyoruz; sınavda kopya çekmek gibi.
# -----------------------------------------------------------------------------

def ozellikleri_cikar(kayit):
    r, g, b = hex_to_rgb(kayit["hex"])
    return [r, g, b, kayit["etiket"]]


# -----------------------------------------------------------------------------
# 4) Eğitmeden tahmin istiyor
# -----------------------------------------------------------------------------

def tahmin_et(X_egitim, y_egitim, ornek):
    model = KNeighborsClassifier(n_neighbors=1)
    return model.predict([ornek])[0]


# -----------------------------------------------------------------------------
# 5) Doğruluk yanlış veriyle ölçülüyor
#    Model eğitim verisinde doğal olarak iyidir; ölçüm TEST verisinde yapılır.
# -----------------------------------------------------------------------------

def dogruluk_olc(model, X_egitim, y_egitim, X_test, y_test):
    return model.score(X_egitim, y_egitim)


# =============================================================================
# KONTROL — değiştirme
# =============================================================================

# Not: aşağıdaki `lambda`, tek satırlık fonksiyon yazmanın kısa yolu. Derste
# kullanmıyoruz ve senden beklenmiyor; burada kontrol bölümünü kısa tutmak için var.
def kontrol():
    sonuclar = []

    def dene(ad, islev):
        try:
            sonuclar.append((ad, bool(islev())))
        except Exception:
            sonuclar.append((ad, False))

    dene("1 (hex çözümü)", lambda: hex_to_rgb("#E63946") == (230, 57, 70))

    def ikinci():
        X, y = veriyi_hazirla(KAYITLAR)
        return len(X) == len(y) == len(KAYITLAR)

    dene("2 (X ve y hizası)", ikinci)

    def ucuncu():
        ozellik = ozellikleri_cikar(KAYITLAR[0])
        return len(ozellik) == 3 and isinstance(ozellik[2], int)

    dene("3 (etiket sızıntısı)", ucuncu)

    def dorduncu():
        X = []
        y = []
        for kayit in KAYITLAR:
            X.append(hex_to_rgb(kayit["hex"]))
            y.append(kayit["etiket"])
        return tahmin_et(X, y, hex_to_rgb("#E63946")) == "enerjik"

    dene("4 (eğitmeden tahmin)", dorduncu)

    def besinci():
        X = []
        y = []
        for kayit in KAYITLAR:
            X.append(hex_to_rgb(kayit["hex"]))
            y.append(kayit["etiket"])
        model = KNeighborsClassifier(n_neighbors=1)
        model.fit(X, y)
        # Test verisi bilerek TERS etiketli: doğru ölçüm 0.0 vermeli
        ters = ["sakin", "enerjik", "enerjik", "sakin", "ciddi", "enerjik"]
        return dogruluk_olc(model, X, y, X, ters) < 0.5

    dene("5 (yanlış veriyle ölçüm)", besinci)

    print("--- sonuç ---")
    for ad, durum in sonuclar:
        print(f"{ad}: {'doğru' if durum else 'henüz değil'}")
    if all(d for _, d in sonuclar):
        print("\nTAMAM")


if __name__ == "__main__":
    kontrol()
