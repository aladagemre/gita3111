"""1. adım — Anahtarı dosyadan okumak.

Çalıştırma (önce konunun klasörüne gir: cd 02-api-ile-konusmak):
    uv run ornekler/01_anahtar_oku.py

Anahtar koda YAZILMAZ. Ayrı bir dosyada durur, kod oradan okur.
Neden: kodunu paylaştığında anahtarın da gitmiş olur. Anahtarı olan senin adına
istek atabilir, kotanı bitirebilir.
"""

# Komutu konu klasöründen (02-api-ile-konusmak) çalıştırıyoruz. ".." bir üst klasör
# demek: "../anahtar.txt" = gita3111 klasörünün içindeki anahtar.txt. Bütün konular
# aynı anahtar dosyasını kullanır.
ANAHTAR_DOSYASI = "../anahtar.txt"


def anahtarlari_oku(yol=ANAHTAR_DOSYASI):
    """anahtar.txt dosyasını okuyup {ACCOUNT_ID: ..., API_TOKEN: ...} döndürür."""
    degerler = {}
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:
            if "=" in satir:
                ad, _, deger = satir.partition("=")
                degerler[ad.strip().upper()] = deger.strip()
    return degerler


try:
    anahtarlar = anahtarlari_oku()
except FileNotFoundError:
    print("anahtar.txt bulunamadı.")
    print("Kurulum yönergesinin 6. adımını yap (../00-hazirlik/kurulum-yonergesi.md): hesabı aç, Account ID ve token'ı")
    print("gita3111 klasörünün içinde anahtar.txt dosyasına kaydet.")
    raise SystemExit(1)

hesap = anahtarlar.get("ACCOUNT_ID", "")
anahtar = anahtarlar.get("API_TOKEN", "")

print("Account ID okundu mu :", "evet" if hesap else "HAYIR")
print("API token okundu mu  :", "evet" if anahtar else "HAYIR")

# Anahtarı ASLA tam olarak ekrana basma. Sadece doğru okunduğunu göster.
if anahtar:
    print("Token'ın ilk 6 karakteri:", anahtar[:6] + "...")
