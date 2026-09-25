"""9. adım (ek) — Soruya bağlam koymak cevabı değiştiriyor mu?

Çalıştırma (önce konunun klasörüne gir: cd 02-api-ile-konusmak):
    uv run ornekler/09_baglam_farki.py

Konu 1'deki bulgu: müşteriler kafeyi kahvesiyle değil, SESSİZ BİR ÇALIŞMA YERİ
olarak anlatıyordu. Bu dosya aynı isteği iki biçimde soruyor:

  bağlamsız : "Bir kafe için üç kısa slogan yaz."
  bağlamlı  : bulguyu da soruya yazıyoruz

Her soru 3 kez soruluyor (model her seferinde başka cümle kurar), sonra
cevaplarda kaç kez "kahve klişesi", kaç kez "çalışma yeri" kelimesi geçtiği
sayılıyor. Soru: bulguyu söylemezsen model senin kafeni mi anlatıyor, yoksa
"ortalama bir kafe"yi mi?

anahtar.txt yoksa DEMO modunda çalışır: kayıtlı örnek cevaplar kullanılır.
"""

import json
import time

import requests

MODEL = "@cf/google/gemma-4-26b-a4b-it"
ANAHTAR_DOSYASI = "../anahtar.txt"
DEMO_CEVAPLAR = "veri/baglam_ornek_cevaplar.json"
TEKRAR = 3
BEKLEME = 1  # istekler arasında saniye

SORULAR = {
    "baglamsiz": "Bir kafe için üç kısa slogan yaz.",
    "baglamli": "Müşterilerinin sessiz bir çalışma yeri olarak anlattığı bir kafe için üç kısa slogan yaz.",
}

ETIKET = {"baglamsiz": "bağlamsız", "baglamli": "bağlamlı"}

# Kelimenin başını yazıyoruz: "kahve" hem "kahve"yi hem "kahvenin"i yakalar.
# "köpü" yazdık ki hem "köpük" hem "köpüğü" sayılsın (k → ğ yumuşaması).
KLISE = ["kahve", "fincan", "çekirdek", "aroma", "espresso", "latte", "köpü", "yudum"]
CALISMA = ["sessiz", "odak", "çalış", "priz", "sakin", "masa"]


def anahtarlari_oku(yol=ANAHTAR_DOSYASI):
    degerler = {}
    with open(yol, encoding="utf-8") as dosya:
        for satir in dosya:
            if "=" in satir:
                ad, _, deger = satir.partition("=")
                degerler[ad.strip().upper()] = deger.strip()
    return degerler


def anahtar_durumu(yol=ANAHTAR_DOSYASI):
    """'tamam', 'yok' ya da 'bozuk' ve okunan değerleri döndürür."""
    try:
        degerler = anahtarlari_oku(yol)
    except FileNotFoundError:
        return "yok", {}
    if degerler.get("ACCOUNT_ID") and degerler.get("API_TOKEN"):
        return "tamam", degerler
    return "bozuk", degerler


def modele_sor(soru, hesap, anahtar):
    adres = f"https://api.cloudflare.com/client/v4/accounts/{hesap}/ai/run/{MODEL}"
    basliklar = {"Authorization": f"Bearer {anahtar}"}
    cevap = requests.post(adres, headers=basliklar, json={"prompt": soru}, timeout=60)
    if cevap.status_code != 200:
        return f"[HATA {cevap.status_code}]"
    return cevap.json()["result"]["response"]


def turkce_kucult(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()


def kelime_say(cevaplar, kelimeler):
    """Cevaplarda, listedeki kelimelerin toplam kaç kez geçtiğini sayar."""
    toplam = 0
    for cevap in cevaplar:
        kucuk = turkce_kucult(cevap)
        for kelime in kelimeler:
            toplam = toplam + kucuk.count(kelime)
    return toplam


durum, anahtarlar = anahtar_durumu()

if durum == "tamam":
    hesap, anahtar = anahtarlar["ACCOUNT_ID"], anahtarlar["API_TOKEN"]
    cevaplar = {}
    for tur in SORULAR:
        cevaplar[tur] = []
        for _ in range(TEKRAR):
            print(f"Soruluyor ({ETIKET[tur]})...")
            cevaplar[tur].append(modele_sor(SORULAR[tur], hesap, anahtar))
            time.sleep(BEKLEME)
else:
    if durum == "bozuk":
        print("[UYARI] anahtar.txt var ama ACCOUNT_ID / API_TOKEN okunamadı — düzeltmen gerek.")
    print("[DEMO MODU] Kayıtlı örnek cevaplar kullanılıyor. Kendi sonucun farklı olabilir.\n")
    with open(DEMO_CEVAPLAR, encoding="utf-8") as dosya:
        kayitli = json.load(dosya)
    cevaplar = {"baglamsiz": kayitli["baglamsiz"], "baglamli": kayitli["baglamli"]}

for tur in SORULAR:
    print(f"=== {ETIKET[tur]}: {SORULAR[tur]}")
    for cevap in cevaplar[tur]:
        print("  -", cevap.replace("\n", " ")[:110])
    print()

klise_siz = kelime_say(cevaplar["baglamsiz"], KLISE)
klise_li = kelime_say(cevaplar["baglamli"], KLISE)
calisma_siz = kelime_say(cevaplar["baglamsiz"], CALISMA)
calisma_li = kelime_say(cevaplar["baglamli"], CALISMA)

print("--- Sayım (3'er cevapta) ---")
print(f"{'':12}{'kahve klişesi':>16}{'çalışma yeri':>16}")
print(f"{'bağlamsız':12}{klise_siz:>16}{calisma_siz:>16}")
print(f"{'bağlamlı':12}{klise_li:>16}{calisma_li:>16}")
print()

if klise_siz > klise_li and calisma_li > calisma_siz:
    print("Bulguyu söylemeyince model 'ortalama bir kafe'yi anlattı: kahve, fincan, aroma.")
    print("Müşterinin gerçekten önemsediği şey (sessizlik, çalışmak) ancak soruya")
    print("yazınca cevaba girdi. Soruyu yazmak da bir tasarım kararı.")
else:
    print("Senin sonucunda fark net değil. Cevapları oku: sayım neyi kaçırıyor?")
    print("Kelime listelerine (KLISE, CALISMA) kendi gözlediğin kelimeleri ekleyip tekrar dene.")
