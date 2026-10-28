# Konu 12'nin yardımcı dosyası: ajanın araçlarının içinde çalışacak hazır parçalar.
# Araçların kendisini (modelin göreceği fonksiyonları) defterde sen yazıyorsun.
#
# ciz: Konu 8'deki fonksiyon. Yönerge, tohum ve dosya yolu alır; görseli o yola kaydeder (klasör yoksa açar).
#   Başarılıysa yolu, başarısızsa None verir.
# duzenle: var olan bir görseli yönergeye göre değiştirir (Konu 7'deki duzenle; bu kez tohum ve kayıt yolu da var).
#   Girdi dosyasının yolu, yönerge, tohum ve çıktı yolu alır; sonucu ciz gibi kaydeder, yolu ya da None verir.
#   Girdi dosyası yoksa istek göndermez.
# en_yakin_paragraflar: Konu 11'deki kilavuzda_ara'nın içindeki iş, aynı kodla. Kılavuzun paragraflarını bir kez
#   vektöre çevirir ve Konu 11'deki gibi ciktilar/kilavuz_vektorleri.json dosyasına saklar (sonraki seferlerde oradan
#   okur); sorunun vektörünü her paragrafla karşılaştırır, soruya en yakın `kac` paragrafı tek bir metin olarak verir.
#   Konu 11'deki kilavuzda_ara'yı defterde araç olarak sen yazıyorsun; içinde bu fonksiyon çalışıyor.
# modele_sor: Konu 5'te yazdığın fonksiyon (soru ve sıcaklık alır, cevabı metin olarak verir; başarısızsa None).
# tarifi_goster: Agno'nun bir fonksiyondan kurup modele göndereceği araç tarifini ekrana yazar.
# hesap, anahtar, basliklar, adres: anahtar.txt'den okunan bilgiler ve Konu 2'deki adres kalıbı.
# timeout: cevap bu kadar saniyede gelmezse istek bırakılır; hücre sonsuza kadar asılı kalmaz.

import base64
import io
import json
import os
from collections import Counter

import requests
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

METIN_MODELI = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
GORSEL_MODELI = "@cf/black-forest-labs/flux-1-schnell"
DUZENLEYICI = "@cf/black-forest-labs/flux-2-klein-4b"
VEKTOR_MODELI = "@cf/google/embeddinggemma-300m"

KILAVUZ = "veri/kilavuz.txt"
VEKTOR_DOSYASI = "ciktilar/kilavuz_vektorleri.json"


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


def gonder(model, **istek):
    # Bütün isteklerin ortak kısmı: gönder, ağ hatasını ve 200 dışı kodu yakala, "result" bölümünü ver (olmazsa None)
    try:
        cevap = requests.post(adres(model), headers=basliklar, timeout=120, **istek)
    except requests.exceptions.RequestException:
        print("Bağlanamadım ya da cevap gelmedi")
        return None
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    yanit = cevap.json()
    return yanit["result"]


def gorseli_kaydet(sonuc, yol):
    # Üretimde de düzenlemede de görsel, metne çevrilmiş (base64) olarak "image" alanında geliyor
    if sonuc is None:
        return None
    resim = base64.b64decode(sonuc["image"])
    klasor = os.path.dirname(yol)
    if klasor != "":
        os.makedirs(klasor, exist_ok=True)
    with open(yol, "wb") as dosya:
        dosya.write(resim)
    return yol


def ciz(yonerge, tohum, yol):
    sonuc = gonder(GORSEL_MODELI, json={"prompt": yonerge, "seed": tohum})
    return gorseli_kaydet(sonuc, yol)


def duzenle(girdi_yolu, yonerge, tohum, yol):
    if not os.path.exists(girdi_yolu):
        print("Böyle bir dosya yok:", girdi_yolu)
        return None
    # Düzenleyici en fazla 512 x 512 piksel kabul ediyor: en-boy oranını koruyarak küçült, belleğe yaz
    gorsel = Image.open(girdi_yolu).convert("RGB")
    gorsel.thumbnail((512, 512))
    tampon = io.BytesIO()
    gorsel.save(tampon, "JPEG")
    tampon.seek(0)
    # Form gibi gönderiyoruz: yazı alanları data= ile (hepsi metin), dosya files= ile
    alanlar = {"prompt": yonerge, "width": "512", "height": "512", "seed": str(tohum)}
    dosyalar = {"input_image_0": ("girdi.jpg", tampon, "image/jpeg")}
    sonuc = gonder(DUZENLEYICI, data=alanlar, files=dosyalar)
    return gorseli_kaydet(sonuc, yol)


def modele_sor(soru, sicaklik):
    sonuc = gonder(METIN_MODELI, json={"prompt": soru, "temperature": sicaklik})
    if sonuc is None:
        return None
    return sonuc["response"]


def vektorleri_al(metinler):
    # Konu 11'deki vektorleri_al: bir metin listesini tek istekte gönderir, aynı sırayla vektörleri verir
    sonuc = gonder(VEKTOR_MODELI, json={"text": metinler})
    if sonuc is None:
        return None
    return sonuc["data"]


def benzerlik(a, b):
    # Konu 4'teki fonksiyon
    sonuc = cosine_similarity([a], [b])
    satir = sonuc[0]
    return satir[0]


def kilavuzu_hazirla():
    # Konu 11'in Adım 2–3'ü: kılavuzun her satırı bir paragraf; vektörler bir kez istenir, ciktilar/ içine saklanır.
    # Saklı dosyadaki paragraflar kılavuzdakilerle aynı değilse (kılavuz değiştiyse) vektörler yeniden istenir.
    paragraflar = []
    with open(KILAVUZ, encoding="utf-8") as dosya:
        for satir in dosya:
            paragraf = satir.strip()
            if paragraf != "":
                paragraflar.append(paragraf)
    if os.path.exists(VEKTOR_DOSYASI):
        with open(VEKTOR_DOSYASI, encoding="utf-8") as dosya:
            kilavuz_vektorleri = json.load(dosya)
        if list(kilavuz_vektorleri) == paragraflar:
            return kilavuz_vektorleri
    vektorler = vektorleri_al(paragraflar)
    if vektorler is None:
        return None
    kilavuz_vektorleri = {}
    sira = 0
    for paragraf in paragraflar:
        kilavuz_vektorleri[paragraf] = vektorler[sira]
        sira = sira + 1
    klasor = os.path.dirname(VEKTOR_DOSYASI)
    os.makedirs(klasor, exist_ok=True)
    with open(VEKTOR_DOSYASI, "w", encoding="utf-8") as dosya:
        json.dump(kilavuz_vektorleri, dosya, ensure_ascii=False, indent=2)
    return kilavuz_vektorleri


def en_yakin_paragraflar(soru, kac):
    # Konu 11'deki kilavuzda_ara'nın içi; tek fark, kaç paragraf geleceğini `kac` söylüyor
    kilavuz_vektorleri = kilavuzu_hazirla()
    soru_vektorleri = vektorleri_al([soru])
    if kilavuz_vektorleri is None or soru_vektorleri is None:
        return "Kılavuza şu an ulaşılamadı."
    soru_vektoru = soru_vektorleri[0]
    skorlar = {}
    for paragraf in kilavuz_vektorleri:
        vektor = kilavuz_vektorleri[paragraf]
        skorlar[paragraf] = benzerlik(soru_vektoru, vektor)
    sirali = Counter(skorlar)
    bilgiler = ""
    for paragraf, skor in sirali.most_common(kac):
        bilgiler = bilgiler + paragraf + "\n"
    return bilgiler


def tarifi_goster(fonksiyon):
    # Agno'nun bu fonksiyondan kuracağı araç tarifi: ad, açıklama (docstring) ve bilgiler (parametreler, tür ipuçları)
    from agno.tools.function import Function
    tarif = Function.from_callable(fonksiyon).to_dict()
    print(json.dumps(tarif, ensure_ascii=False, indent=2))
