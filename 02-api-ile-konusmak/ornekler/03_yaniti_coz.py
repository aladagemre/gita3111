# Adım 3 — Yanıtın içinden metni çek
# Çalıştır: uv run ornekler/03_yaniti_coz.py

import json

# Sunucudan gelmiş bir yanıtın kayıtlı kopyası
with open("veri/ornek_yanit.json", encoding="utf-8") as dosya:
    yanit = json.load(dosya)

print(list(yanit.keys()))
print(list(yanit["result"].keys()))

metin = yanit["result"]["response"]
print(metin)

kullanim = yanit["result"]["usage"]
print("Harcanan belirteç:", kullanim["total_tokens"])
