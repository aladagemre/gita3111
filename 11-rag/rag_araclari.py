# Konu 11'in yardımcı dosyası: müşteri hafızasının hazır parçaları. Defterde bunları çağırıyoruz; içine merak edersen bak.
# Anlamca arama (vektör modeli) ve notlara dayanan cevap (metin modeli) yapay zekânın işi.
# Dosya okuma, not ekleme, puanları sıralama Python'un işi: bunlar için modele istek gitmez.
# Konu 12'deki asistanın araçları (kurallara_bak, hatirla) bu aramanın ve not eklemenin kopyasını kullanır;
# hafızanın kendi kopyasına (12-ajan/ciktilar/hafiza.txt) yazar.

import os
from collections import Counter

import requests
from sklearn.metrics.pairwise import cosine_similarity

VEKTOR_MODELI = "@cf/google/embeddinggemma-300m"            # Konu 4'teki gömme modeli
METIN_MODELI = "@cf/google/gemma-4-26b-a4b-it"   # notları afişle karşılaştırmada llama'dan tutarlı (30 Ekim 2026 provası)
DURUMLAR = {401: "Anahtar kabul edilmedi: anahtar.txt'deki API_TOKEN satırını kontrol et (Konu 2).",
            404: "Adres bulunamadı: anahtar.txt'deki ACCOUNT_ID satırını kontrol et (Konu 2).",
            429: "Çok sık istek gitti ya da günlük kota doldu: biraz bekle, olmazsa yarın dene."}


# ../anahtar.txt dosyasından hesap kimliğini ve anahtarı okur (Konu 2'deki dosya, gita3111 klasöründe)
def anahtari_oku():
    if not os.path.exists("../anahtar.txt"):
        raise FileNotFoundError("anahtar.txt bulunamadı: gita3111 klasöründe durmalı (Konu 2).")
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:   # -sig: Not Defteri'nin gizli işaretini atlar
        for satir in dosya:
            parcalar = satir.split("=", 1)
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    if "ACCOUNT_ID" not in anahtarlar or "API_TOKEN" not in anahtarlar:
        raise RuntimeError("anahtar.txt okunamadı: 'ACCOUNT_ID = ...' ve 'API_TOKEN = ...' satırları olmalı.")
    return anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]


# Bir modele istek gönderir (Konu 2), cevabın "result" bölümünü verir; olmazsa nedenini yazar ve None verir
def istek_gonder(model, govde):
    hesap, anahtar = anahtari_oku()
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{model}"
    try:
        cevap = requests.post(adres, headers={"Authorization": f"Bearer {anahtar}"}, json=govde, timeout=60)
    except requests.exceptions.RequestException:
        print("Sunucuya ulaşamadım ya da 1 dakikada cevap gelmedi: internet bağlantını kontrol et.")
        return None
    if cevap.status_code != 200:
        aciklama = DURUMLAR.get(cevap.status_code, "Sunucu şu an cevap veremedi; biraz sonra yeniden dene.")
        print(f"İstek başarısız (durum kodu {cevap.status_code}). {aciklama}")
        return None
    return cevap.json()["result"]


# Bir metin listesini TEK istekte vektöre çevirir; aynı sırayla bir vektör listesi verir
def vektorleri_al(metinler):
    sonuc = istek_gonder(VEKTOR_MODELI, {"text": metinler})
    if sonuc is None:
        raise RuntimeError("Vektörler gelmedi: yukarıdaki nedeni oku, düzelt, hücreyi yeniden çalıştır.")
    return sonuc["data"]


# Konu 4'teki vektor_al: tek bir metnin vektörü (768 sayı)
def vektor_al(metin):
    vektorler = vektorleri_al([metin])
    return vektorler[0]


# Konu 4'teki benzerlik: iki vektör aynı yöne bakıyorsa 1'e yakın, ilgisizse 0'a yakın bir sayı
def benzerlik(a, b):
    sonuc = cosine_similarity([a], [b])
    satir = sonuc[0]
    return satir[0]


# Bir metin dosyasının boş olmayan satırlarını liste olarak verir (defterin ısınmasındaki dört satırın aynısı)
def notlari_oku(yol):
    notlar = []
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:
            if satir.strip() != "":
                notlar.append(satir.strip())
    return notlar


# Hafızayı kurar: her not anahtar, vektörü değer olan bir sözlük. Bütün notlar tek istekte gider
def hafizayi_kur(notlar):
    vektorler = vektorleri_al(notlar)
    hafiza = {}
    for not_metni, vektor in zip(notlar, vektorler):
        hafiza[not_metni] = vektor
    return hafiza


# Soruya anlamca en yakın `kac` notu liste olarak verir: defterdeki puan hücresinin aynısı, sonra sıralama
def hafizada_ara(soru, hafiza, kac):
    soru_vektoru = vektor_al(soru)
    puanlar = {}
    for not_metni in hafiza:
        puanlar[not_metni] = benzerlik(soru_vektoru, hafiza[not_metni])
    bulunanlar = []
    for not_metni, puan in Counter(puanlar).most_common(kac):   # Konu 4'teki most_common: en büyük `kac` puan
        bulunanlar.append(not_metni)
    return bulunanlar


# Yeni notu dosyanın sonuna ekler ("a": eski notlar silinmez) ve vektörüyle hafızaya koyar (defterin Adım 4'ü)
def not_ekle(not_metni, hafiza, yol):
    with open(yol, "a", encoding="utf-8") as dosya:
        dosya.write(not_metni + "\n")
    hafiza[not_metni] = vektor_al(not_metni)


# Konu 5'teki modele_sor'un benzeri: yönergeyi metin modeline gönderir, cevabı metin olarak verir; olmazsa None
def modele_sor(yonerge, sicaklik):
    mesajlar = [{"role": "user", "content": yonerge}]   # sohbet biçimi: düz "prompt" ile model yönergeyi sürdürülecek bir belge sanıyor
    govde = {"messages": mesajlar, "temperature": sicaklik, "max_completion_tokens": 1000,
             "chat_template_kwargs": {"enable_thinking": False}}   # "düşünme" kapalı: hızlı, az kota, boş cevap yok
    sonuc = istek_gonder(METIN_MODELI, govde)
    if sonuc is None:
        return None
    secenek = sonuc["choices"][0]
    return secenek["message"]["content"]
