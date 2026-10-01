# Bozuk kodlar — beş parça, her birinde bir hata
# Çalıştır: uv run ornekler/07_bozuk_kodlar.py

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

X = [(230, 57, 70), (244, 162, 97), (231, 111, 81), (69, 123, 157), (168, 218, 220), (29, 53, 87)]
y = ["enerjik", "enerjik", "enerjik", "sakin", "sakin", "ciddi"]

# 1) "#E63946" için 230 57 70 yazmalı
kod = "#E63946"
print(int(kod[1:2], 16), int(kod[2:3], 16), int(kod[3:4], 16))

# 2) Yalnız enerjik renkler: iki liste de 3 elemanlı olmalı
X_enerjik = []
y_enerjik = []
for i in range(len(X)):
    if y[i] == "enerjik":
        X_enerjik.append(X[i])
    y_enerjik.append(y[i])
print(len(X_enerjik), len(y_enerjik))

# 3) y_egitim etiketlerden oluşmalı
X_egitim, y_egitim, X_test, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
print(y_egitim)

# 4) Kör tahmin en sık etiketi söylemeli: enerjik
sayac = {}
for etiket in y:
    sayac[etiket] = sayac.get(etiket, 0) + 1
print(sorted(sayac, key=sayac.get)[0])

# 5) Doğruluk, modelin görmediği renklerde ölçülmeli
X_egitim, X_test, y_egitim, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
model = KNeighborsClassifier(n_neighbors=1)
model.fit(X_egitim, y_egitim)
print(model.score(X_egitim, y_egitim))
