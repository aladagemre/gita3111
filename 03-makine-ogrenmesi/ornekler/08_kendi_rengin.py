"""8. adım (bonus) — Kendi rengini tahmin ettir.

Çalıştırma:  uv run --with scikit-learn 03-makine-ogrenmesi/ornekler/08_kendi_rengin.py

Aşağıdaki listeye kendi seçtiğin renkleri ekle, modelin ne dediğine bak.
Sen aynı fikirde misin?
"""

import csv

from sklearn.neighbors import KNeighborsClassifier

VERI = "03-makine-ogrenmesi/veri/renkler-etiketli.csv"

# ---- OYNAYACAĞIN YER ----
DENEMELER = [
    ("#FF0000", "tam kırmızı"),
    ("#000080", "koyu lacivert"),
    ("#FFFFFF", "beyaz"),
    ("#7CFC00", "parlak yeşil"),
    ("#8B4513", "kahverengi"),
]
# -------------------------


def hex_to_rgb(hex_kod):
    hex_kod = hex_kod.lstrip("#")
    return (int(hex_kod[0:2], 16), int(hex_kod[2:4], 16), int(hex_kod[4:6], 16))


with open(VERI, encoding="utf-8") as dosya:
    kayitlar = list(csv.DictReader(dosya))

X = []
y = []
for kayit in kayitlar:
    X.append(hex_to_rgb(kayit["hex"]))
    y.append(kayit["etiket"])

# Bu kez TÜM veriyle eğitiyoruz: ölçüm yapmıyoruz, sadece tahmin alıyoruz
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X, y)

print("Renk              Modelin tahmini")
print("-" * 34)
for hex_kod, ad in DENEMELER:
    tahmin = model.predict([hex_to_rgb(hex_kod)])[0]
    print(f"{ad:<18}{tahmin}")

print("\nModelin gördüğü tek şey üç sayı. Sen renge bakarken kültür, alışkanlık ve")
print("bağlam da devrede. Ayrıldığınız yerler en ilginç yerler.")
