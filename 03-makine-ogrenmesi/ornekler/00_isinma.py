# Isınma — CSV satırını sözlüğe çevir
# Çalıştır: uv run ornekler/00_isinma.py

baslik = ["hex", "ad", "etiket"]
satir = ["#E63946", "kırmızı", "enerjik"]

# Tamir 1: {'hex': '#E63946', 'ad': 'kırmızı', 'etiket': 'enerjik'} yazmalı
kayit = {}
for i in range(len(baslik)):
    kayit[satir[i]] = baslik[i]
print(kayit)

# Tamir 2: {'enerjik': 2, 'sakin': 1} yazmalı
kayitlar = [
    {"hex": "#E63946", "ad": "kırmızı", "etiket": "enerjik"},
    {"hex": "#457B9D", "ad": "orta mavi", "etiket": "sakin"},
    {"hex": "#F4A261", "ad": "şeftali", "etiket": "enerjik"},
]
sayac = {}
for kayit in kayitlar:
    sayac[kayit["ad"]] = sayac.get(kayit["ad"], 0) + 1
print(sayac)
