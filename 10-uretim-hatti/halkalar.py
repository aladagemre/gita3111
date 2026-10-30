# Konu 10'un yardımcı dosyası: afiş son kontrol hattının hazır parçaları (halkaları); defterde bunları birbirine bağlıyorsun.
# Yalnızca afisi_oku ve modele_sor anahtar ister (../anahtar.txt); ötekiler anahtarsız, internetsiz çalışır.
import base64, datetime, io, os, re, time

import requests
from IPython.display import display
from PIL import Image

SUNUCU = "https://api.cloudflare.com"
METIN_MODELI = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
GOZ_MODELI = "@cf/google/gemma-4-26b-a4b-it"          # görseldeki yazıyı okuyan model
CEVAP_YOK = "(Model cevap vermedi; bu adımı biraz sonra yeniden çalıştır.)"
AYLAR = ["ocak", "şubat", "mart", "nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım", "aralık"]
GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
TARIH_DESENI = r"(\d{1,2})\s+(" + "|".join(AYLAR) + r")\s+(\d{4})"   # "14 kasım 2026"

# Hesap numarasını ve anahtarı ../anahtar.txt'den okur
def anahtari_oku():
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:   # -sig: Not Defteri'nin gizli işaretini atlar
        for satir in dosya:
            parcalar = satir.split("=", 1)
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    return anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]

# Modele sorar; cevap gelmez ya da boş gelirse 5 saniye bekleyip yeniden dener (en fazla 3 kez), olmazsa CEVAP_YOK verir
def sabirli_sor(model, govde):
    hesap, anahtar = anahtari_oku()
    adres = f"{SUNUCU}/client/v4/accounts/{hesap}/ai/run/{model}"
    for deneme in [1, 2, 3]:
        metin = ""
        try:
            cevap = requests.post(adres, headers={"Authorization": f"Bearer {anahtar}"}, json=govde, timeout=180)
            if cevap.status_code != 200:
                print("İstek başarısız, durum kodu:", cevap.status_code)
            elif "response" in cevap.json()["result"]:     # metin modeli cevabı burada verir
                metin = str(cevap.json()["result"]["response"]).strip()
            else:                                          # görsel okuyan model sohbet biçiminde verir
                secenek = cevap.json()["result"]["choices"][0]
                metin = str(secenek["message"]["content"] or "").strip()
        except requests.exceptions.RequestException:      # internet yok ya da 3 dakikada cevap gelmedi
            print("Sunucuya ulaşamadım.")
        if metin != "":
            return metin
        if deneme < 3:
            print("Deneme", deneme, "olmadı; 5 saniye bekleyip yeniden soruyorum.")
            time.sleep(5)
    print("Model 3 denemede de cevap vermedi.")
    return CEVAP_YOK

# Afişteki bütün yazıları, düzeltmeden, satır satır metne çevirir (görsel okuyan model)
def afisi_oku(yol):
    gorsel = Image.open(yol).convert("RGB")
    gorsel.thumbnail((1200, 1200))                         # çok büyük dosyalar istekte sorun çıkarmasın
    tampon = io.BytesIO()
    gorsel.save(tampon, "JPEG", quality=90)
    gorsel_adresi = "data:image/jpeg;base64," + base64.b64encode(tampon.getvalue()).decode()
    soru = ("Bu afişteki bütün yazıları yukarıdan aşağı, satır satır yaz. Harfi harfine yaz: "
            "yazım hatası varsa düzeltme, olduğu gibi bırak. Başka hiçbir şey ekleme.")
    icerik = [{"type": "text", "text": soru}, {"type": "image_url", "image_url": {"url": gorsel_adresi}}]
    govde = {"messages": [{"role": "user", "content": icerik}], "temperature": 0, "max_completion_tokens": 2000}
    return sabirli_sor(GOZ_MODELI, govde)

# Metin modeline (Konu 5'teki llama) soru sorar, cevabı metin olarak verir
def modele_sor(soru, sicaklik):
    mesajlar = [{"role": "user", "content": soru}]   # sohbet biçimi: düz yönergede model metni sürdürmeye kalkabiliyor
    return sabirli_sor(METIN_MODELI, {"messages": mesajlar, "temperature": sicaklik, "max_tokens": 800})

# Türkçe küçük harfe çevirir ("KASIM" -> "kasım", "CUMARTESİ" -> "cumartesi")
def kucult(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()

# "14 Kasım 2026" gibi bir tarihin Türkçe gün adını takvimden hesaplar; tarih okunamazsa "?"
def gun_adi(tarih):
    bulunan = re.search(TARIH_DESENI, kucult(tarih))
    if bulunan is None:
        return "?"
    gun = datetime.date(int(bulunan[3]), AYLAR.index(bulunan[2]) + 1, int(bulunan[1]))
    return GUNLER[gun.weekday()]                           # weekday(): Pazartesi 0, Pazar 6

# Metindeki ilk tarihi "14 Kasım 2026" biçiminde verir; yoksa "yok"
def tarihi_bul(metin):
    bulunan = re.search(TARIH_DESENI, kucult(metin))
    if bulunan is None:
        return "yok"
    return bulunan[1] + " " + bulunan[2].capitalize() + " " + bulunan[3]

# Metinde geçen ilk gün adını verir ("Cuma"); yoksa "yok"
def gunu_bul(metin):
    for kelime in re.findall(r"\w+", kucult(metin)):
        for gun in GUNLER:
            if kucult(gun) == kelime:
                return gun
    return "yok"

# Görseldeki en yaygın `kac` rengi, en yaygından başlayarak HEX listesi olarak verir (ilki çoğu zaman zemindir)
def renkleri_cikar(yol, kac):
    gorsel = Image.open(yol).convert("RGB")
    gorsel.thumbnail((1200, 1200))
    az_renkli = gorsel.quantize(colors=kac, method=Image.Quantize.FASTOCTREE)
    palet = az_renkli.getpalette()
    renkler = []
    for adet, sira in sorted(az_renkli.getcolors(), reverse=True):
        renkler.append("#%02X%02X%02X" % tuple(palet[sira * 3:sira * 3 + 3]))   # (kırmızı, yeşil, mavi) -> "#1F3A5F"
    return renkler

# İki rengin WCAG kontrast oranı: 1 (aynı renk) ile 21 (siyah-beyaz) arası; küçük yazı için en az 4.5
def kontrast(renk1, renk2):
    parlakliklar = []
    for renk in [renk1, renk2]:                           # WCAG'nin göreli parlaklık formülü: 0 siyah, 1 beyaz
        toplam = 0
        for sira, agirlik in [(1, 0.2126), (3, 0.7152), (5, 0.0722)]:
            kanal = int(renk[sira:sira + 2], 16) / 255
            if kanal <= 0.04045:
                toplam += agirlik * kanal / 12.92
            else:
                toplam += agirlik * ((kanal + 0.055) / 1.055) ** 2.4
        parlakliklar.append(toplam + 0.05)
    return round(max(parlakliklar) / min(parlakliklar), 2)

# Metni dosyaya yazar (klasör yoksa açar); "model cevap vermedi" notunu kaydetmez
def dosyaya_yaz(metin, yol):
    if metin == CEVAP_YOK:
        print("Kaydetmedim, çünkü model cevap vermedi:", yol)
        return
    os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
    with open(yol, "w", encoding="utf-8") as dosya:
        dosya.write(metin)
    print("Kaydedildi:", yol)

# Dosyadaki metni okur
def dosyadan_oku(yol):
    with open(yol, encoding="utf-8") as dosya:
        return dosya.read()

# Görseli defterde küçük boyda gösterir
def goster(yol):
    gorsel = Image.open(yol)
    gorsel.thumbnail((420, 420))
    display(gorsel)
