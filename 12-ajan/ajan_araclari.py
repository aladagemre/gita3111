# Konu 12'nin yardımcı dosyası: araçların İÇİNDE çalışan hazır işler.
# Araçların kendisini (modelin seçeceği fonksiyonları ve tariflerini) defterde sen yazıyorsun.
# Konu 10'daki görsel okuma ve gün hesabı, Konu 11'deki hafıza burada kopya olarak duruyor; konular birbirini çağırmaz.
# Hafıza sadeleştirildi: kural sayısı az olduğu için vektörler her aramada yeniden hesaplanır (tek istek).

import base64
import datetime
import os

import requests
from sklearn.metrics.pairwise import cosine_similarity

AJAN_MODELI = "@cf/google/gemma-4-26b-a4b-it"      # hem ajanın beyni hem afişi okuyan göz
VEKTOR_MODELI = "@cf/google/embeddinggemma-300m"   # Konu 11'deki gömme modeli
HAFIZA = "ciktilar/hafiza.txt"                     # ilk kullanımda kılavuz + notlardan açılır; veri/ değişmez
AYLAR = ["ocak", "subat", "mart", "nisan", "mayis", "haziran",
         "temmuz", "agustos", "eylul", "ekim", "kasim", "aralik"]
GUNLER = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
SADE = str.maketrans("ışğüçö.,/-", "isguco    ", "̇")   # "Kasım" → "kasim", "14.11.2026" → "14 11 2026"

# anahtar.txt'den hesap kimliğini ve anahtarı okur (Konu 2'deki dosya, bir üst klasörde)
def anahtari_oku():
    anahtarlar = {}
    with open("../anahtar.txt", encoding="utf-8-sig") as dosya:
        for satir in dosya:
            parcalar = satir.split("=", 1)
            if len(parcalar) == 2:
                anahtarlar[parcalar[0].strip()] = parcalar[1].strip()
    return anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]

# Ajanın modelini kurar. OpenAILike "OpenAI biçiminde konuşan" demek: istek Cloudflare'e gider, OpenAI hesabı gerekmez
def model_kur():
    from agno.models.openai.like import OpenAILike
    hesap, anahtar = anahtari_oku()
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/v1"
    return OpenAILike(id=AJAN_MODELI, api_key=anahtar, base_url=adres)

# Cloudflare'e bir istek gönderir (Konu 2), cevabın "result" bölümünü verir; olmazsa nedenini yazar, None verir
def cloudflare(model, govde):
    hesap, anahtar = anahtari_oku()
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{model}"
    try:
        cevap = requests.post(adres, headers={"Authorization": f"Bearer {anahtar}"}, json=govde, timeout=120)
    except requests.exceptions.RequestException:
        print("Bağlanamadım ya da cevap gelmedi")
        return None
    if cevap.status_code != 200:
        print("İstek başarısız, durum kodu:", cevap.status_code)
        return None
    return cevap.json()["result"]

# Konu 10'daki görsel okuma: gemma-4 afişe bakar, yazıları gördüğü gibi ve renkleri yazar
def gorseldeki_yazi(yol):
    if not os.path.exists(yol):
        return "Böyle bir dosya yok: " + yol
    with open(yol, "rb") as dosya:
        metin = base64.b64encode(dosya.read()).decode()
    soru = ("Bu bir afiş. Üzerindeki bütün yazıları satır satır, gördüğün gibi yaz; yazım hatalarını düzeltme. "
            "Sonra afişte kullanılan renkleri kısa bir liste olarak yaz: hangi yazı ya da şekil, hangi renk.")
    icerik = [{"type": "text", "text": soru},
              {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + metin}}]
    govde = {"messages": [{"role": "user", "content": icerik}], "temperature": 0, "max_completion_tokens": 2000}
    sonuc = cloudflare(AJAN_MODELI, govde)
    if sonuc is None:
        return "Afişi okuyamadım: istek başarısız oldu."
    return sonuc["choices"][0]["message"]["content"]

# Konu 10'daki gün hesabı: "14 Kasım 2026" (ya da "14.11.2026") → "Cumartesi". Model takvimi tahmin eder, Python hesaplar.
# Okuyamazsa Konu 10'daki gibi "?" değil, nasıl yazılacağını söyler: model tarihi düzeltip yeniden dener.
def gun_adi(tarih):
    parcalar = tarih.lower().translate(SADE).split()
    while len(parcalar) > 0 and not parcalar[0].isdigit():     # "Cumartesi, 14 Kasım 2026": baştaki sözcüğü at
        parcalar = parcalar[1:]
    try:
        gun, ay, yil = parcalar[:3]
        if len(gun) == 4:                                       # "2026-11-14" biçimi
            gun, yil = yil, gun
        ay_no = int(ay) if ay.isdigit() else AYLAR.index(ay) + 1
        return GUNLER[datetime.date(int(yil), ay_no, int(gun)).weekday()]
    except ValueError:
        return "Bu tarihi anlayamadım; '14 Kasım 2026' biçiminde yaz."

# Bir metin dosyasının boş olmayan satırlarını liste olarak verir
def satirlar(yol):
    with open(yol, encoding="utf-8") as dosya:
        return [satir.strip() for satir in dosya if satir.strip() != ""]

# Müşteri hafızasını satır satır verir; dosya yoksa veri/kilavuz.txt ile veri/notlar.txt'yi birleştirip açar
def hafizayi_oku():
    if not os.path.exists(HAFIZA):
        os.makedirs("ciktilar", exist_ok=True)
        with open(HAFIZA, "w", encoding="utf-8") as dosya:
            for satir in satirlar("veri/kilavuz.txt") + satirlar("veri/notlar.txt"):
                dosya.write(satir + "\n")
    return satirlar(HAFIZA)

# Konu 11'deki arama: hafızada soruya anlamca en yakın `kac` kuralı tek bir metin olarak verir
def en_yakin_kurallar(soru, kac):
    kurallar = hafizayi_oku()
    sonuc = cloudflare(VEKTOR_MODELI, {"text": [soru] + kurallar})   # tek istek: önce soru, sonra bütün kurallar
    if sonuc is None:
        return "Hafızaya şu an ulaşılamadı."
    vektorler = sonuc["data"]
    skorlar = cosine_similarity([vektorler[0]], vektorler[1:])[0]
    sirali = sorted(zip(skorlar, kurallar), reverse=True)
    return "\n".join(kural for skor, kural in sirali[:kac])

# Hafızanın sonuna bugünün tarihiyle yeni bir not ekler; ajana ne yazdığını geri söyler
def hafizaya_ekle(metin):
    hafizayi_oku()
    satir = "Asistanın notu, " + datetime.date.today().strftime("%d.%m.%Y") + ": " + metin.replace("\n", " ").strip()
    with open(HAFIZA, "a", encoding="utf-8") as dosya:
        dosya.write(satir + "\n")
    return "Not edildi: " + satir

# Ücretsiz web araması (ddgs paketi, anahtar istemez): ilk 5 sonucun başlığı, adresi ve kısa özeti
def internette_ara(sorgu):
    from ddgs import DDGS
    try:
        sonuclar = DDGS().text(sorgu, region="tr-tr", max_results=5)
    except Exception:
        return "Arama şu an yapılamadı ya da sonuç çıkmadı."
    return "\n\n".join(s["title"] + "\n" + s["href"] + "\n" + s["body"] for s in sonuclar)

# Agno'nun bu fonksiyondan kurup modele göndereceği tarif: aracın adı, tarifi (docstring) ve bilgileri
def tarifi_goster(fonksiyon):
    from agno.tools.function import Function
    tarif = Function.from_callable(fonksiyon).to_dict()
    print("Araç adı :", tarif["name"])
    print("Tarifi   :", tarif["description"] or "(BOŞ: model bu aracın ne işe yaradığını bilemez)")
    print("Bilgiler :", ", ".join(tarif["parameters"]["properties"]))

# cevap.tools listesini sırayla yazar: aracın adı (tool_name), modelin verdiği bilgiler (tool_args), sonucun başı
def kararlari_goster(cevap):
    if cevap.status == "ERROR":
        print("Ajan çalışamadı:", cevap.content)
    elif not cevap.tools:
        print("Ajan hiç araç kullanmadı; cevabı kendisi yazdı.")
    else:
        for sira, arac in enumerate(cevap.tools, start=1):
            print(f"{sira}. {arac.tool_name}  {arac.tool_args}")
            print("   sonuç:", str(arac.result)[:160].replace("\n", " / "))
