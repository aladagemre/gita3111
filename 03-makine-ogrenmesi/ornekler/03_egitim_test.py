"""3. adım — Eğitim ve test ayrımı.

Çalıştırma:  uv run --with scikit-learn 03-makine-ogrenmesi/ornekler/03_egitim_test.py

Modeli bütün veriyle eğitip yine aynı veriyle sınarsak, ezberi ölçmüş oluruz.
Sınavda çıkmış soruyla sınav yapmak gibi.
"""

import csv

from sklearn.model_selection import train_test_split

VERI = "03-makine-ogrenmesi/veri/renkler-etiketli.csv"


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

# Veriyi ikiye böl: %75 eğitim, %25 test
# random_state=42 -> her çalıştırmada AYNI bölme olsun diye (karşılaştırma yapabilelim)
X_egitim, X_test, y_egitim, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print("Eğitim örneği:", len(X_egitim))
print("Test örneği  :", len(X_test))
print()
print("Model test verisini eğitim sırasında HİÇ görmeyecek.")
print("Doğruluğu test üzerinde ölçeceğiz — yani hiç görmediği sorularla.")
