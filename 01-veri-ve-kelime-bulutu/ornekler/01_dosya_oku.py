"""1. adım — Dosyayı okumak.

Çalıştırma (önce konunun klasörüne gir: cd 01-veri-ve-kelime-bulutu):
    uv run ornekler/01_dosya_oku.py

Bu konunun ilk sorusu: bir dosya nasıl açılır ve kod onu nerede arar?
"""

# Dosya yolu: kodun ÇALIŞTIĞI klasöre göre yazılır.
# "veri/..." demek: bulunduğum klasörün (01-veri-ve-kelime-bulutu) içindeki veri klasörüne gir.
DOSYA = "veri/kafe-yorumlari.txt"

# encoding="utf-8" yazmazsan Türkçe harfler bozulabilir ya da hata alırsın.
with open(DOSYA, encoding="utf-8") as dosya:
    metin = dosya.read()

print("Karakter sayısı:", len(metin))
print("Satır sayısı:", len(metin.splitlines()))
print()
print("İlk 200 karakter:")
print(metin[:200])
