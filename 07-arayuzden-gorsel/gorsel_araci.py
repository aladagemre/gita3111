# Konu 7'nin görsel üretim aracı.
# Şimdilik bir arayüz gibi kullan: ciz(...), duzenle(...), yan_yana(...).
# Konu 2'de yazdığın modele_sor'un akrabası: istek atar, gelen görseli dosyaya kaydeder.

import base64
import pathlib

import matplotlib.pyplot as plt
import requests
from PIL import Image

MODELLER = {
    "flux": "@cf/black-forest-labs/flux-1-schnell",
    "sdxl": "@cf/stabilityai/stable-diffusion-xl-base-1.0",
}
DUZENLEYICI = "@cf/black-forest-labs/flux-2-klein-4b"
KLASOR = pathlib.Path("ciktilar")


def anahtari_oku():
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:   # -sig: Not Defteri'nin gizli işaretini atlar
        for satir in dosya:
            parcalar = satir.split("=", 1)                         # yalnızca ilk = işaretinden böl
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    if "ACCOUNT_ID" not in anahtarlar or "API_TOKEN" not in anahtarlar:
        raise RuntimeError("anahtar.txt okunamadı: iki satır olmalı, 'ACCOUNT_ID = ...' ve 'API_TOKEN = ...'")
    return anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]


def adres_ve_baslik(model):
    hesap, anahtar = anahtari_oku()
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{model}"
    basliklar = {"Authorization": f"Bearer {anahtar}"}
    return adres, basliklar


def yeni_dosya_adi(uzanti):
    KLASOR.mkdir(exist_ok=True)
    sira = 1
    while list(KLASOR.glob(f"{sira:03d}.*")):    # bu numara alınmışsa bir sonrakine geç
        sira = sira + 1
    return KLASOR / f"{sira:03d}.{uzanti}"


def durumu_denetle(cevap):
    if cevap.status_code != 200:
        raise RuntimeError(f"İstek başarısız, durum kodu {cevap.status_code}: {cevap.text[:200]}")


def resmi_goster(yol, baslik=""):
    plt.imshow(Image.open(yol))
    plt.title(baslik)
    plt.axis("off")
    plt.show()


def ciz(yonerge, tohum=None, adim=None, model="flux", negatif=None, en=None, boy=None, goster=True):
    adres, basliklar = adres_ve_baslik(MODELLER[model])
    govde = {"prompt": yonerge}
    if tohum is not None:
        govde["seed"] = tohum

    if model == "flux":
        if negatif is not None or en is not None or boy is not None:
            raise ValueError("flux negatif yönerge, en ve boy almıyor; bunlar için model=\"sdxl\" kullan.")
        if adim is not None:
            govde["steps"] = adim                     # flux: en fazla 8
        cevap = requests.post(adres, headers=basliklar, json=govde)
        durumu_denetle(cevap)
        yanit = cevap.json()
        resim = base64.b64decode(yanit["result"]["image"])
        yol = yeni_dosya_adi("jpg")
    else:
        if adim is not None:
            govde["num_steps"] = adim                 # sdxl: en fazla 20
        if negatif is not None:
            govde["negative_prompt"] = negatif
        if en is not None:
            govde["width"] = en
        if boy is not None:
            govde["height"] = boy
        cevap = requests.post(adres, headers=basliklar, json=govde)
        durumu_denetle(cevap)
        resim = cevap.content                         # sdxl doğrudan PNG dosyası gönderir
        yol = yeni_dosya_adi("png")

    yol.write_bytes(resim)
    if goster:
        resmi_goster(yol, yonerge[:60])
    return yol


def duzenle(yol, talimat, tohum=None, goster=True):
    adres, basliklar = adres_ve_baslik(DUZENLEYICI)
    kucuk = yeni_dosya_adi("png")
    resim = Image.open(yol).convert("RGB")
    resim.thumbnail((512, 512))                       # düzenleyici en fazla 512x512 kabul ediyor
    resim.save(kucuk)

    alanlar = {"prompt": talimat, "width": "512", "height": "512"}
    if tohum is not None:
        alanlar["seed"] = str(tohum)
    with open(kucuk, "rb") as dosya:
        cevap = requests.post(adres, headers=basliklar, data=alanlar,
                              files={"input_image_0": dosya})
    durumu_denetle(cevap)
    yanit = cevap.json()
    yeni_yol = yeni_dosya_adi("jpg")
    yeni_yol.write_bytes(base64.b64decode(yanit["result"]["image"]))
    if goster:
        resmi_goster(yeni_yol, talimat[:60])
    return yeni_yol


def yan_yana(yollar, basliklar=None, kaydet=None):
    plt.figure(figsize=(4 * len(yollar), 4.5))
    sira = 1
    for yol in yollar:
        plt.subplot(1, len(yollar), sira)
        plt.imshow(Image.open(yol))
        if basliklar is not None:
            plt.title(basliklar[sira - 1])
        plt.axis("off")
        sira = sira + 1
    if kaydet is not None:
        plt.savefig(kaydet, bbox_inches="tight")
    plt.show()
