# Konu 12'nin yardımcı dosyası: ajanın araçlarının içinde çalışacak hazır parçalar.
# Araçların kendisini (modelin göreceği fonksiyonları) defterde sen yazıyorsun.
#
# ciz: Konu 8'deki fonksiyon. Yönerge, tohum ve dosya yolu alır; görseli o yola kaydeder (klasör yoksa açar).
#   Başarılıysa yolu, başarısızsa None verir.
# duzenle: var olan bir görseli yönergeye göre değiştirir (Konu 7'deki duzenle; bu kez tohum ve kayıt yolu da var).
#   Girdi dosyasının yolu, yönerge, tohum ve çıktı yolu alır; sonucu ciz gibi kaydeder, yolu ya da None verir.
#   Girdi dosyası yoksa istek göndermez.
# en_yakin_paragraflar: Konu 11'deki kilavuzda_ara'nın içindeki iş. Kılavuzun paragraflarını bir kez vektöre çevirir
#   ve ciktilar/kilavuz_vektorleri.json dosyasına saklar (sonraki seferlerde oradan okur); sorunun vektörünü her
#   paragrafla karşılaştırır, soruya en yakın `kac` paragrafı tek bir metin olarak verir. Konu 11'deki kilavuzda_ara'yı
#   defterde araç olarak sen yazıyorsun; içinde bu fonksiyon çalışıyor.
# modele_sor: Konu 5'te yazdığın fonksiyon (soru ve sıcaklık alır, cevabı metin olarak verir; başarısızsa None).
# tarifi_goster: Agno'nun bir fonksiyondan kurup modele göndereceği araç tarifini ekrana yazar.
# hesap, anahtar, basliklar, adres: anahtar.txt'den okunan bilgiler ve Konu 2'deki adres kalıbı.
# timeout: cevap bu kadar saniyede gelmezse istek bırakılır; hücre sonsuza kadar asılı kalmaz.

import base64
import io
import json
from pathlib import Path

import requests
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

METIN_MODELI = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
GORSEL_MODELI = "@cf/black-forest-labs/flux-1-schnell"
DUZENLEYICI = "@cf/black-forest-labs/flux-2-klein-4b"
GOMME_MODELI = "@cf/google/embeddinggemma-300m"

KILAVUZ = Path("veri/kilavuz.txt")
VEKTOR_DOSYASI = Path("ciktilar/kilavuz_vektorleri.json")


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
    return cevap.json()["result"]


def gorseli_kaydet(sonuc, yol):
    # Üretimde de düzenlemede de görsel, metne çevrilmiş (base64) olarak "image" alanında geliyor
    if sonuc is None:
        return None
    dosya = Path(yol)
    dosya.parent.mkdir(parents=True, exist_ok=True)
    dosya.write_bytes(base64.b64decode(sonuc["image"]))
    return yol


def ciz(yonerge, tohum, yol):
    sonuc = gonder(GORSEL_MODELI, json={"prompt": yonerge, "seed": tohum})
    return gorseli_kaydet(sonuc, yol)


def duzenle(girdi_yolu, yonerge, tohum, yol):
    if not Path(girdi_yolu).exists():
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


def vektorlere_cevir(metinler):
    sonuc = gonder(GOMME_MODELI, json={"text": metinler})
    if sonuc is None:
        return None
    return sonuc["data"]


def kilavuzu_hazirla():
    # Kılavuzun her satırı bir paragraf. Vektörler daha önce saklandıysa ve kılavuz değişmediyse yeniden istemiyoruz.
    paragraflar = []
    for satir in KILAVUZ.read_text(encoding="utf-8").splitlines():
        if satir.strip() != "":
            paragraflar.append(satir.strip())
    if VEKTOR_DOSYASI.exists():
        sakli = json.loads(VEKTOR_DOSYASI.read_text(encoding="utf-8"))
        if sakli["paragraflar"] == paragraflar:
            return paragraflar, sakli["vektorler"]
    vektorler = vektorlere_cevir(paragraflar)
    if vektorler is None:
        return paragraflar, None
    VEKTOR_DOSYASI.parent.mkdir(parents=True, exist_ok=True)
    kayit = {"paragraflar": paragraflar, "vektorler": vektorler}
    VEKTOR_DOSYASI.write_text(json.dumps(kayit, ensure_ascii=False), encoding="utf-8")
    return paragraflar, vektorler


def en_yakin_paragraflar(soru, kac):
    paragraflar, vektorler = kilavuzu_hazirla()
    soru_vektorleri = vektorlere_cevir([soru])
    if vektorler is None or soru_vektorleri is None:
        return "Kılavuza şu an ulaşılamadı."
    puanlar = cosine_similarity([soru_vektorleri[0]], vektorler)[0]       # Konu 4'teki benzerlik, her paragraf için
    siralama = sorted(range(len(paragraflar)), key=lambda sira: puanlar[sira], reverse=True)
    secilenler = [paragraflar[sira] for sira in siralama[:kac]]
    return "\n".join(secilenler)


def tarifi_goster(fonksiyon):
    # Agno'nun bu fonksiyondan kuracağı araç tarifi: ad, açıklama (docstring) ve bilgiler (parametreler, tür ipuçları)
    from agno.tools.function import Function
    tarif = Function.from_callable(fonksiyon).to_dict()
    print(json.dumps(tarif, ensure_ascii=False, indent=2))
