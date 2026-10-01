# Adım 1 — Dosyayı aç, kelimelere böl
# Çalıştır: uv run ornekler/01_dosya_oku.py

with open("veri/kafe-yorumlari.txt", encoding="utf-8") as dosya:
    metin = dosya.read()

print(len(metin))
print(metin[:150])

kelimeler = metin.split()
print(len(kelimeler))
print(kelimeler[:8])
