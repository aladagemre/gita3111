# Konu 8'in yardımcı dosyası. İçini okuman gerekmiyor: defterde yalnızca bu üç fonksiyonu çağırıyoruz.
# ciz(yonerge, tohum, yol): görseli üretir ve yol'a kaydeder (ör. "ciktilar/afis.jpg"; klasör yoksa kendisi açar).
#   Başarılıysa yol'u, olmazsa None verir. yol'da aynı adda bir dosya varsa üzerine yazar.
# sabirli_ciz(yonerge, tohum, yol): ciz'in aynısı; olmazsa 5 saniye bekleyip yeniden dener (en fazla 3 kez).
# gorsele_sor(yol, soru): bir görseli ve bir soruyu görsel anlayan bir modele gönderir, cevabı metin olarak verir.
# Anahtarı ../anahtar.txt'den bir kez, bu dosya ilk alındığında okur.

import base64
import os
import time

import requests

GORSEL_MODELI = "@cf/black-forest-labs/flux-1-schnell"
GOZ_MODELI = "@cf/google/gemma-4-26b-a4b-it"      # görseli okuyup soruya cevap veren model


def anahtari_oku():
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:   # -sig: Not Defteri'nin gizli işaretini atlar
        for satir in dosya:
            parcalar = satir.split("=", 1)
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    return anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]


hesap, anahtar = anahtari_oku()
basliklar = {"Authorization": f"Bearer {anahtar}"}


def adres(model):
    return f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{model}"


def ciz(yonerge, tohum, yol):
    govde = {"prompt": yonerge, "seed": tohum}
    try:
        cevap = requests.post(adres(GORSEL_MODELI), headers=basliklar, json=govde, timeout=120)
    except requests.exceptions.RequestException:          # internet yok ya da 2 dakikada cevap gelmedi
        print("Bağlanamadım ya da cevap gelmedi")
        return None
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None

    # Görsel cevabın içinde metin (base64) olarak geliyor: metni görselin baytlarına çevirip dosyaya yazıyoruz
    resim = base64.b64decode(cevap.json()["result"]["image"])
    klasor = os.path.dirname(yol)
    if klasor != "":
        os.makedirs(klasor, exist_ok=True)
    with open(yol, "wb") as dosya:
        dosya.write(resim)
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


def gorsele_sor(yol, soru):
    with open(yol, "rb") as dosya:
        baytlar = dosya.read()
    metin = base64.b64encode(baytlar).decode()
    gorsel_adresi = "data:image/jpeg;base64," + metin      # görseli metin olarak, adresin içinde gönderiyoruz

    icerik = [
        {"type": "text", "text": soru},
        {"type": "image_url", "image_url": {"url": gorsel_adresi}},
    ]
    govde = {"messages": [{"role": "user", "content": icerik}]}
    try:
        cevap = requests.post(adres(GOZ_MODELI), headers=basliklar, json=govde, timeout=180)
    except requests.exceptions.RequestException:
        print("Bağlanamadım ya da cevap gelmedi")
        return None
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None

    sonuc = cevap.json()["result"]
    if "response" in sonuc:                      # bazı modeller cevabı burada verir
        return sonuc["response"]
    secenek = sonuc["choices"][0]                # bazıları sohbet biçiminde, burada
    return secenek["message"]["content"]
