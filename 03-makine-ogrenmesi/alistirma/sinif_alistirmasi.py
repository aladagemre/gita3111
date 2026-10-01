# Sınıf alıştırması — Konu 3 (scikit-learn gerekmez)
# Çalıştır: uv run alistirma/sinif_alistirmasi.py

kayitlar = [
    {"hex": "#E63946", "ad": "kırmızı", "etiket": "enerjik"},
    {"hex": "#457B9D", "ad": "orta mavi", "etiket": "sakin"},
    {"hex": "#1D3557", "ad": "lacivert", "etiket": "ciddi"},
    {"hex": "#F4A261", "ad": "şeftali", "etiket": "enerjik"},
]

# Soru 1 — Boşlukları doldur: 230 57 70 yazmalı
kod = "#E63946"
kirmizi = int(kod[1:3], ___)
yesil = int(kod[___], 16)
mavi = int(kod[5:7], 16)
print(kirmizi, yesil, mavi)

# Soru 2 — Boşluğu doldur: X ve y aynı sırada, ikisi de 4 elemanlı olmalı
X = []
y = []
for kayit in kayitlar:
    kod = kayit["hex"]
    X.append((int(kod[1:3], 16), int(kod[3:5], 16), int(kod[5:7], 16)))
    y.append(___)
print(X[0], y[0], len(X), len(y))

# Soru 3 — Hatayı bul: {'enerjik': 2, 'sakin': 1, 'ciddi': 1} yazmalı
sayac = {}
for kayit in kayitlar:
    sayac[kayit["ad"]] = sayac.get(kayit["ad"], 0) + 1
print(sayac)

# Soru 4 — Hatayı bul: 4 tahminden 2'si tuttu, 0.5 yazmalı
gercekler = ["enerjik", "sakin", "ciddi", "sakin"]
tahminler = ["enerjik", "ciddi", "ciddi", "enerjik"]
tutan = 0
for i in range(len(gercekler)):
    if gercekler[i] == tahminler[i]:
        tutan = tutan + 1
print(tutan)

# Soru 5 — Tamamla: enerjik renklerin adları, ['kırmızı', 'şeftali'] yazmalı
enerjikler = []

print(enerjikler)

# Ek 1 — En koyu rengin adı (R+G+B toplamı en küçük olan): lacivert yazmalı

# Ek 2 — Kayıtların kaçta kaçı enerjik: 0.5 yazmalı
