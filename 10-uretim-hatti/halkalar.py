# Konu 10'un yardımcı dosyası: hattın hazır halkaları. Halkaları birbirine bağlamak defterde senin işin.
# modele_sor: Konu 5'te yazdığın fonksiyon (soru ve sıcaklık alır, modelin cevabını metin olarak verir).
#   Konu 5'tekinden tek farkı: istek başarısız olursa çökmez, None verir.
# ciz: Konu 8'deki fonksiyon. Yönerge, tohum ve dosya yolu alır; görseli o yola kaydeder (klasör yoksa açar).
#   Başarılıysa yolu, başarısızsa None verir.
# sabirli_ciz: Konu 8'deki sabırlı hâli. ciz'i en fazla üç kez dener, aralarda 5 saniye bekler. Dönüşü ciz'inki gibi.
# timeout: cevap bu kadar saniyede gelmezse istek bırakılır; hücre sonsuza kadar asılı kalmaz.

import base64
import time
from pathlib import Path

import requests

METIN_MODELI = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
GORSEL_MODELI = "@cf/black-forest-labs/flux-1-schnell"


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


def modele_sor(soru, sicaklik):
    govde = {"prompt": soru, "temperature": sicaklik}
    try:
        cevap = requests.post(adres(METIN_MODELI), headers=basliklar, json=govde, timeout=60)
    except requests.exceptions.RequestException:
        print("Bağlanamadım ya da cevap gelmedi")
        return None
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    yanit = cevap.json()
    sonuc = yanit["result"]
    return sonuc["response"]


def ciz(yonerge, tohum, yol):
    govde = {"prompt": yonerge, "seed": tohum}
    try:
        cevap = requests.post(adres(GORSEL_MODELI), headers=basliklar, json=govde, timeout=120)
    except requests.exceptions.RequestException:
        print("Bağlanamadım ya da cevap gelmedi")
        return None
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    yanit = cevap.json()
    sonuc = yanit["result"]
    metin = sonuc["image"]                       # görsel, metne çevrilmiş (base64) olarak geliyor
    dosya = Path(yol)
    dosya.parent.mkdir(parents=True, exist_ok=True)
    dosya.write_bytes(base64.b64decode(metin))
    return yol


def sabirli_ciz(yonerge, tohum, yol):
    for deneme in [1, 2, 3]:
        sonuc = ciz(yonerge, tohum, yol)
        if sonuc is not None:
            return sonuc
        if deneme < 3:
            print("Deneme", deneme, "olmadı, 5 saniye bekliyorum")
            time.sleep(5)
    return None
