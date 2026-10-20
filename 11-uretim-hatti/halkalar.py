# Konu 11'in yardımcı dosyası: hattın hazır halkaları. Halkaları birbirine bağlamak defterde senin işin.
# modele_sor: Konu 5'te yazdığın fonksiyon (soru ve sıcaklık alır, modelin cevabını metin olarak verir).
#   Konu 5'tekinden tek farkı: istek başarısız olursa çökmez, None verir.
# ciz: Konu 8'de yazdığın fonksiyon (yönerge ve tohum alır, görselin baytlarını verir; başarısızsa None).
# sabirli_ciz: Konu 9'da yazdığın fonksiyon (ciz'i en fazla üç kez dener, aralarda 5 saniye bekler).
# video_uret: Konu 10'daki fonksiyon. Video aracı hizmetine bir yönerge ve (istersen) bir görsel gönderir, video hazır
#   olana kadar bekler (Konu 10'daki bekleme döngüsü), videoyu verilen yola kaydeder. Başarılıysa yolu, olmazsa None verir.
#   Video zaten varsa hiç istek göndermez.
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
    return anahtarlar


anahtarlar = anahtari_oku()
hesap = anahtarlar["ACCOUNT_ID"]
anahtar = anahtarlar["API_TOKEN"]
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


def sabirli_ciz(yonerge, tohum):
    for deneme in [1, 2, 3]:
        try:
            resim = ciz(yonerge, tohum)
        except requests.exceptions.RequestException:
            print("Bağlanamadım ya da cevap gelmedi")
            resim = None
        if resim is not None:
            return resim
        if deneme < 3:
            print("Deneme", deneme, "olmadı, 5 saniye bekliyorum")
            time.sleep(5)
    return None


def video_uret(yonerge, yol, gorsel_yolu=None):
    # Konu 10'daki video_uret'in aynısı (kısaltılmış): videoyu yol'a kaydeder; başarılıysa yol'u, değilse None verir.
    # gorsel_yolu verilirse o görsel videonun ilk karesi olur. yol zaten varsa hiç istek göndermez (video pahalı).
    yol = Path(yol)
    if yol.exists():
        print("Zaten var, yeni iş başlatmıyorum:", yol)
        return yol
    if "VIDEO_ADRES" not in anahtarlar or "VIDEO_KOD" not in anahtarlar:
        print("anahtar.txt'de VIDEO_ADRES ya da VIDEO_KOD satırı yok (Konu 10)")
        return None
    adres_video = anahtarlar["VIDEO_ADRES"]
    basliklar_video = {"Authorization": "Bearer " + anahtarlar["VIDEO_KOD"]}

    govde = {"yonerge": yonerge, "sure": "4", "oran": "16:9"}
    if gorsel_yolu is not None:
        baytlar = Path(gorsel_yolu).read_bytes()
        govde["gorsel"] = base64.b64encode(baytlar).decode()     # görseli metne çeviriyoruz (Konu 10)

    try:
        cevap = requests.post(adres_video + "/baslat", headers=basliklar_video, json=govde, timeout=60)
        if cevap.status_code != 200:
            print("Başlatılamadı, durum kodu:", cevap.status_code)
            return None
        is_no = cevap.json()["is_no"]
        print("İş başladı:", is_no)

        for deneme in range(36):                          # en fazla 36 × 10 saniye = 6 dakika
            cevap = requests.get(adres_video + "/durum/" + is_no, headers=basliklar_video, timeout=30)
            durum = cevap.json()
            if "hata" in durum:
                print("İş başarısız:", durum["hata"])
                return None
            if durum["bitti"]:
                cevap = requests.get(durum["video"], headers=basliklar_video, timeout=120)
                if cevap.status_code != 200:
                    print("Videoyu indiremedim, durum kodu:", cevap.status_code)
                    return None
                yol.write_bytes(cevap.content)
                print("Kaydedildi:", yol)
                return yol
            print("Henüz bitmedi, geçen süre:", deneme * 10, "saniye")
            time.sleep(10)
    except requests.exceptions.RequestException:
        print("Aracı hizmete bağlanamadım ya da cevap gelmedi")
        return None

    print("Zaman aşımı; iş sürüyor olabilir. İş numarası:", is_no)
    return None
