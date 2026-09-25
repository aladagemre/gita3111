"""3. adım — Yanıtın içinden metni çekmek.

Çalıştırma (önce konunun klasörüne gir: cd 02-api-ile-konusmak):
    uv run ornekler/03_yaniti_coz.py

Sunucu sana düz metin göndermiyor; İÇ İÇE bir sözlük gönderiyor. Buna JSON denir.
JSON = sözlüğün ağ üzerinde yazılmış hâli.
"""

import json

DEMO_YANIT = "veri/ornek_yanit.json"

with open(DEMO_YANIT, encoding="utf-8") as dosya:
    yanit = json.load(dosya)

# Adım adım içeri girelim.
print("1) En dıştaki anahtarlar:", list(yanit.keys()))
print("2) 'result' neyin nesi   :", type(yanit["result"]).__name__)
print("3) result'ın anahtarları :", list(yanit["result"].keys()))

# İstediğimiz metin iki kat içeride:
metin = yanit["result"]["response"]
print("\n4) Aradığımız metin:")
print(metin)

# Kaç belirteç (token) harcadık?
kullanim = yanit["result"]["usage"]
print("\n5) Harcanan belirteç:", kullanim["total_tokens"])

# Hata var mı? 'errors' bir LİSTE.
if yanit["errors"]:
    print("\nHata var:", yanit["errors"][0]["message"])
else:
    print("\nHata yok.")

print("\nKural: yanıtın yapısını bilmiyorsan ÖNCE ham hâlini bas, sonra içine gir.")
