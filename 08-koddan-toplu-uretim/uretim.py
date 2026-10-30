# Konu 8'in yardımcı dosyası. Defterde yalnızca buradaki fonksiyonları çağırıyoruz; içine merak edersen bak.
# Görseli yapay zekâ üretir (ciz). Yazı, ölçü, onay sayfası ve günlük Python'un işi: modele istek gitmez.

import base64
import csv
import os
import time

import matplotlib.pyplot as plt
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

MODEL = "@cf/black-forest-labs/flux-1-schnell"   # 30 Ekim 2026: bu model tohum (seed) kabul etmiyor
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "veri", "DejaVuSerif.ttf")
KAGIT = "#F4F1EA"       # Sayfa Kahve kılavuzu: kâğıt beyazı (zemin)
MUREKKEP = "#1F3A5F"    # Sayfa Kahve kılavuzu: mürekkep mavisi (yazı)
YAZI_SERIDI = 270       # başlık şeridi: 1350'nin beşte biri (kılavuz: yazı görselin en fazla beşte biri)
# biçim: (en, boy, görselin üst kenarı, başlık puntosu); hikâyede üstte 250, altta 320 piksel boş kalır
BICIMLER = {"gonderi": (1080, 1350, 0, 54), "hikaye": (1080, 1920, 250, 60)}

# ../anahtar.txt dosyasından hesap numarasını ve anahtarı okur (Konu 2'deki dosya)
def anahtari_oku():
    if not os.path.exists("../anahtar.txt"):
        raise FileNotFoundError("anahtar.txt bulunamadı: gita3111 klasöründe durmalı (Konu 2).")
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:   # -sig: Not Defteri'nin gizli işaretini atlar
        for satir in dosya:
            parcalar = satir.split("=", 1)
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    return anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]

# yol'un klasörü yoksa açar (ör. "ciktilar/benim/gunluk.csv" için "ciktilar/benim")
def klasoru_ac(yol):
    if os.path.dirname(yol) != "":
        os.makedirs(os.path.dirname(yol), exist_ok=True)

# yönergeyi görsel modeline gönderir, gelen görseli yol'a kaydeder; başarıda yol'u, olmazsa None verir
def ciz(yonerge, yol):
    hesap, anahtar = anahtari_oku()
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
    try:
        cevap = requests.post(adres, headers={"Authorization": f"Bearer {anahtar}"},
                              json={"prompt": yonerge}, timeout=120)
    except requests.exceptions.RequestException:
        print("Sunucuya ulaşamadım ya da 2 dakikada cevap gelmedi: internet bağlantını kontrol et.")
        return None
    if cevap.status_code != 200:   # 401: anahtar yanlış; 429: çok sık istek ya da kota doldu
        print(f"Görsel gelmedi (durum kodu {cevap.status_code}). 401 ise anahtar.txt'yi kontrol et; "
              "429 ise biraz bekle, olmazsa yarın dene. Ayrıntı:", cevap.text[:150])
        return None
    klasoru_ac(yol)
    with open(yol, "wb") as dosya:   # görsel cevapta metin (base64) olarak gelir; baytlara çevirip yazıyoruz
        dosya.write(base64.b64decode(cevap.json()["result"]["image"]))
    return yol

# ciz'in sabırlı hâli: görsel gelmezse 5 saniye bekleyip yeniden dener, en fazla 3 kez
def sabirli_ciz(yonerge, yol):
    for deneme in [1, 2, 3]:
        if ciz(yonerge, yol) is not None:
            return yol
        if deneme < 3:
            print(f"{deneme}. deneme olmadı; 5 saniye bekleyip yeniden deniyorum.")
            time.sleep(5)
    print("Üç denemede de görsel gelmedi:", yol)
    return None

# metni genişliğe sığan satırlara böler; sonra satır sayısı değişmeyecek kadar daraltıp satırları dengeler
def satirlara_bol(kalem, metin, font, genislik, dengele=True):
    satirlar = [""]
    for kelime in metin.split():
        deneme = (satirlar[-1] + " " + kelime).strip()
        if satirlar[-1] == "" or kalem.textlength(deneme, font=font) <= genislik:
            satirlar[-1] = deneme
        else:
            satirlar.append(kelime)
    while dengele and genislik > 200:   # son satırda tek kelime kalmasın
        dar = satirlara_bol(kalem, metin, font, genislik - 20, dengele=False)
        if len(dar) > len(satirlar):
            break
        satirlar, genislik = dar, genislik - 20
    return satirlar

# görseli zemine yerleştirir, başlığı altına fontla yazar ve yol'a kaydeder; bicim: "gonderi" ya da "hikaye"
def gonderi_yap(gorsel_yolu, baslik, bicim, yol, zemin=KAGIT, renk=MUREKKEP):
    if gorsel_yolu is None or not os.path.exists(gorsel_yolu):
        print("Görsel yok, bu dosyayı atlıyorum:", yol)
        return None
    en, boy, ust, punto = BICIMLER[bicim]
    sayfa = Image.new("RGB", (en, boy), zemin)
    gorsel = Image.open(gorsel_yolu).convert("RGB")
    sayfa.paste(ImageOps.fit(gorsel, (en, en)), (0, ust))   # görseli kare keser, 1080 x 1080 yapar
    kalem = ImageDraw.Draw(sayfa)
    font = ImageFont.truetype(FONT, punto)
    satirlar = satirlara_bol(kalem, baslik, font, en - 160)
    y = ust + en + (YAZI_SERIDI - len(satirlar) * int(punto * 1.35)) // 2
    for satir in satirlar:
        kalem.text(((en - kalem.textlength(satir, font=font)) / 2, y), satir, font=font, fill=renk)   # ortalı
        y = y + int(punto * 1.35)
    klasoru_ac(yol)
    sayfa.save(yol, quality=92)
    return yol

# dosyaların küçük hâllerini, altlarında adlarıyla, satır başına en fazla 5 tane dizip tek bir JPEG'e kaydeder
def onay_sayfasi(yollar, yol):
    sutun = min(5, len(yollar))
    kucukler = []
    for dosya in yollar:
        if dosya is not None and os.path.exists(dosya):
            resim = Image.open(dosya).convert("RGB")
            resim.thumbnail((300, 600))
            kucukler.append((resim, os.path.basename(dosya)))
    siralar = [kucukler[i:i + sutun] for i in range(0, len(kucukler), sutun)]
    boylar = [max(resim.height for resim, ad in sira) + 70 for sira in siralar]
    sayfa = Image.new("RGB", (sutun * 340 + 40, 120 + sum(boylar)), "#FFFFFF")
    kalem = ImageDraw.Draw(sayfa)
    baslik = "Onay sayfası · " + time.strftime("%d.%m.%Y")   # bugünün tarihini Python bilir
    kalem.text((40, 40), baslik, font=ImageFont.truetype(FONT, 36), fill=MUREKKEP)
    y = 110
    for sira, sira_boyu in zip(siralar, boylar):
        for no, (resim, ad) in enumerate(sira):
            x = 40 + no * 340
            sayfa.paste(resim, (x, y))
            kalem.rectangle((x - 1, y - 1, x + resim.width, y + resim.height), outline="#B9B4AA")   # çerçeve
            kalem.text((x, y + resim.height + 12), ad, font=ImageFont.truetype(FONT, 20), fill=MUREKKEP)
        y = y + sira_boyu
    klasoru_ac(yol)
    sayfa.save(yol, quality=90)
    return yol

# günlüğe bir satır ekler: ne zaman, hangi gün, hangi yönerge, hangi dosya (ilk seferde sütun adlarını da yazar)
def gunluge_ekle(gunluk, gun, yonerge, dosya):
    yeni = not os.path.exists(gunluk)
    klasoru_ac(gunluk)
    with open(gunluk, "a", encoding="utf-8-sig", newline="") as f:   # -sig: Excel Türkçe harfleri doğru açsın
        if yeni:
            csv.writer(f).writerow(["zaman", "gun", "yonerge", "dosya"])
        csv.writer(f).writerow([time.strftime("%Y-%m-%d %H:%M"), gun, yonerge, dosya])

# bir görseli defterde gösterir
def goster(yol):
    if yol is None or not os.path.exists(yol):
        print("Gösterilecek dosya yok:", yol)
        return
    resim = Image.open(yol)
    plt.figure(figsize=(6 * resim.width / resim.height, 6))   # en-boy oranını koru
    plt.imshow(resim)
    plt.axis("off")
    plt.show()
