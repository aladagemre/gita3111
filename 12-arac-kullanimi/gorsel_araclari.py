# Konu 12'nin yardımcı dosyası: modelin seçeceği araçlar burada hazır duruyor.
# ciz: Konu 8'de yazdığın, Konu 9'da kullandığın fonksiyonun aynısı (yönerge ve tohum alır, görselin baytlarını verir).
# duzenle: Konu 8 Adım 9'daki düzenleme isteğinin fonksiyon hâli (bir görsel dosyası, yönerge ve tohum alır).
# metin_yaz: dil modeline düz bir soru sorar, cevabı metin olarak verir (ödevdeki üçüncü araç için).
# adres ve basliklar: defterde metin modeline istek gönderirken kullanılır.
# Başarısız olan her fonksiyon None verir; timeout: cevap bu kadar saniyede gelmezse istek bırakılır.

import base64
import io

import requests
from PIL import Image

GORSEL_MODELI = "@cf/black-forest-labs/flux-1-schnell"
DUZENLEYICI = "@cf/black-forest-labs/flux-2-klein-4b"
METIN_MODELI = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"


def anahtari_oku():
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:
        for satir in dosya:
            parcalar = satir.split("=", 1)
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    return anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]


hesap, anahtar = anahtari_oku()
basliklar = {"Authorization": f"Bearer {anahtar}"}


def adres(model):
    return f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{model}"


def gorseli_coz(cevap):
    # Üretimde de düzenlemede de cevap aynı: result -> image (base64 metni) -> baytlar
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    yanit = cevap.json()
    sonuc = yanit["result"]
    metin = sonuc["image"]
    return base64.b64decode(metin)


def ciz(yonerge, tohum):
    govde = {"prompt": yonerge, "seed": tohum}
    cevap = requests.post(adres(GORSEL_MODELI), headers=basliklar, json=govde, timeout=120)
    return gorseli_coz(cevap)


def duzenle(girdi_yolu, yonerge, tohum):
    # Düzenleyici en fazla 512 x 512 piksel kabul ediyor: önce en-boy oranını koruyarak küçült (Konu 8, Adım 9)
    gorsel = Image.open(girdi_yolu).convert("RGB")
    gorsel.thumbnail((512, 512))
    tampon = io.BytesIO()                      # küçük görseli diske değil belleğe yazıyoruz
    gorsel.save(tampon, "JPEG")
    tampon.seek(0)

    # Form gibi gönderiyoruz: yazı alanları data= ile (hepsi metin), dosya files= ile
    alanlar = {"prompt": yonerge, "width": "512", "height": "512", "seed": str(tohum)}
    dosyalar = {"input_image_0": ("girdi.jpg", tampon, "image/jpeg")}
    cevap = requests.post(adres(DUZENLEYICI), headers=basliklar, data=alanlar, files=dosyalar, timeout=120)
    return gorseli_coz(cevap)


def metin_yaz(yonerge):
    govde = {"prompt": yonerge}
    cevap = requests.post(adres(METIN_MODELI), headers=basliklar, json=govde, timeout=60)
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    yanit = cevap.json()
    sonuc = yanit["result"]
    return sonuc["response"]
