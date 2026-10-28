# Konu 11'in yardımcı dosyası: kılavuzda aramak ve modele sormak için hazır fonksiyonlar.
# Bunları birbirine bağlamak (paragrafları vektöre çevirmek, en ilgilileri bulmak, yönergeyi kurmak) defterde senin işin.
# vektor_al: Konu 4'te yazdığın fonksiyon (bir metin alır, gömme vektörünü verir).
# vektorleri_al: aynı işin liste hâli. Bir metin listesini TEK istekte gönderir, aynı sırayla bir vektör listesi verir.
#   İkisi de istek başarısız olursa durum koduyla birlikte açık bir hata verip durur: vektör gelmeden devam etmenin anlamı yok.
# modele_sor: Konu 5'te yazdığın fonksiyon (soru ve sıcaklık alır, modelin cevabını metin olarak verir).
#   Konu 5'tekinden tek farkı: istek başarısız olursa çökmez, None verir (Konu 10'daki gibi).
# ciz: Konu 8'deki fonksiyon. Yönerge, tohum ve dosya yolu alır; görseli o yola kaydeder.
#   Başarılıysa yolu, başarısızsa None verir. Klasör yoksa kendisi açar.
# timeout: cevap bu kadar saniyede gelmezse istek bırakılır; hücre sonsuza kadar asılı kalmaz.

import base64
from pathlib import Path

import requests

VEKTOR_MODELI = "@cf/google/embeddinggemma-300m"
METIN_MODELI = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
GORSEL_MODELI = "@cf/black-forest-labs/flux-1-schnell"


def anahtari_oku():
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:
        for satir in dosya:
            parcalar = satir.split("=", 1)
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    return anahtarlar


anahtarlar = anahtari_oku()
hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]
basliklar = {"Authorization": f"Bearer {anahtar}"}


def adres(model):
    return f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{model}"


def vektorleri_al(metinler):
    govde = {"text": metinler}
    try:
        cevap = requests.post(adres(VEKTOR_MODELI), headers=basliklar, json=govde, timeout=60)
    except requests.exceptions.RequestException:
        raise RuntimeError("Vektör isteği: bağlanamadım ya da cevap gelmedi") from None
    if cevap.status_code != 200:
        raise RuntimeError(f"Vektör isteği başarısız, durum kodu: {cevap.status_code} "
                           "(401 anahtar yanlış, 404 hesap kimliği yanlış, 429 kota doldu)")
    yanit = cevap.json()
    sonuc = yanit["result"]
    return sonuc["data"]


def vektor_al(metin):
    vektorler = vektorleri_al([metin])
    return vektorler[0]


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
    baytlar = base64.b64decode(sonuc["image"])     # görsel metin olarak geliyor; dosyaya yazılacak hâline çeviriyoruz
    dosya_yolu = Path(yol)
    dosya_yolu.parent.mkdir(parents=True, exist_ok=True)
    dosya_yolu.write_bytes(baytlar)
    return yol
