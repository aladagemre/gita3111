# Konu 10'un yardımcı dosyası.
# anahtarlari_oku: ../anahtar.txt'deki bütün satırları bir sözlük olarak verir (Konu 9'daki gibi).
# sahte_baslat, sahte_durum: internetsiz, sahte bir video işi. Gerçek aracı hizmet gibi cevap verir;
#   iş 5 saniyede "biter". Defterin Adım 2'si ve alıştırma bunları kullanır.
# video_uret: dersteki bütün adımlar tek fonksiyonda (başlat, bekle, indir). Konu 11'de kullanacağız.
# Bu dosya içe aktarılınca anahtar okunmaz; sahte fonksiyonlar anahtarsız çalışır.

import base64
import time
from pathlib import Path

import requests


def anahtarlari_oku():
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:
        for satir in dosya:
            parcalar = satir.split("=", 1)
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    return anahtarlar


# ---------------------------------------------------------------- sahte iş (internetsiz)

SAHTE_IS_SURESI = 5          # saniye: sahte işin "bitmesi" için geçmesi gereken süre
_sahte_isler = {}            # iş numarası -> başlama zamanı


def sahte_baslat(govde):
    if govde["yonerge"] == "":
        return {"hata": "yönerge boş"}
    is_no = "sahte_" + str(len(_sahte_isler) + 1)
    _sahte_isler[is_no] = time.time()
    return {"is_no": is_no}


def sahte_durum(is_no):
    if is_no not in _sahte_isler:
        return {"hata": "böyle bir iş yok: " + str(is_no)}
    gecen = time.time() - _sahte_isler[is_no]
    if gecen < SAHTE_IS_SURESI:
        return {"bitti": False}
    return {"bitti": True, "video": "sahte_video.mp4"}


# ---------------------------------------------------------------- gerçek iş, tek fonksiyonda

def video_uret(yonerge, yol, gorsel_yolu=None, sure="4", oran="16:9", aralik=10, en_fazla=36):
    """Bir video üretir ve yol'a kaydeder. Başarılıysa yol'u, değilse None verir.

    gorsel_yolu verilirse o görsel videonun ilk karesi olur (görselden video).
    yol zaten varsa hiç istek göndermez (kaldığı yerden devam: video pahalı).
    En fazla en_fazla x aralik saniye bekler (varsayılan 36 x 10 = 6 dakika).
    """
    yol = Path(yol)
    if yol.exists():
        print("Zaten var, yeni iş başlatmıyorum:", yol)
        return yol

    anahtarlar = anahtarlari_oku()
    adres = anahtarlar["VIDEO_ADRES"]
    basliklar = {"Authorization": "Bearer " + anahtarlar["VIDEO_KOD"]}

    govde = {"yonerge": yonerge, "sure": sure, "oran": oran}
    if gorsel_yolu is not None:
        baytlar = Path(gorsel_yolu).read_bytes()
        govde["gorsel"] = base64.b64encode(baytlar).decode()

    # 1) başlat
    try:
        cevap = requests.post(adres + "/baslat", headers=basliklar, json=govde, timeout=60)
        yanit = cevap.json()
    except (requests.exceptions.RequestException, ValueError):
        print("Aracı hizmete bağlanamadım ya da cevabı okuyamadım")
        return None
    if cevap.status_code != 200 or "is_no" not in yanit:
        print("Başlatılamadı:", cevap.status_code, yanit)
        return None
    is_no = yanit["is_no"]
    print("İş başladı:", is_no)

    # 2) bekle: aralıklarla durum sor, zaman aşımıyla
    video_adresi = None
    for deneme in range(en_fazla):
        try:
            durum = requests.get(adres + "/durum/" + is_no, headers=basliklar, timeout=30).json()
        except (requests.exceptions.RequestException, ValueError):
            print("Durumu soramadım, biraz sonra yeniden soracağım")
            time.sleep(aralik)
            continue
        if "hata" in durum:
            print("İş başarısız:", durum["hata"])
            return None
        if durum["bitti"]:
            video_adresi = durum["video"]
            break
        print("Henüz bitmedi, geçen süre:", deneme * aralik, "saniye")
        time.sleep(aralik)
    if video_adresi is None:
        print("Zaman aşımı; iş sürüyor olabilir. İş numarası:", is_no)
        return None

    # 3) indir
    try:
        cevap = requests.get(video_adresi, headers=basliklar, timeout=120)
    except requests.exceptions.RequestException:
        print("Videoyu indiremedim. İş numarası:", is_no)
        return None
    if cevap.status_code != 200:
        print("Videoyu indiremedim, durum kodu:", cevap.status_code)
        return None
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_bytes(cevap.content)
    print("Kaydedildi:", yol)
    return yol
