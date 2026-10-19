# Konu 9'un yardımcı dosyası.
# ciz: Konu 8'de yazdığın fonksiyonun aynısı (yönerge ve tohum alır, görselin baytlarını verir).
# gorsele_sor: bir görseli ve bir soruyu görsel anlayan bir modele gönderir, cevabı metin olarak verir.
# timeout: cevap bu kadar saniyede gelmezse istek bırakılır (requests.exceptions.Timeout); hücre sonsuza kadar asılı kalmaz.

import base64

import requests

GORSEL_MODELI = "@cf/black-forest-labs/flux-1-schnell"
GOZ_MODELI = "@cf/google/gemma-4-26b-a4b-it"      # görseli okuyup soruya cevap veren model


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


def ciz(yonerge, tohum):
    govde = {"prompt": yonerge, "seed": tohum}
    cevap = requests.post(adres(GORSEL_MODELI), headers=basliklar, json=govde, timeout=120)
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    yanit = cevap.json()
    sonuc = yanit["result"]
    metin = sonuc["image"]
    return base64.b64decode(metin)


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
