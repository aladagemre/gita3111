"""GİTA3111 — kurulum testi.

Çalıştırma:  uv run kurulum_testi.py

Bu betik hiçbir şeyi değiştirmez; sadece kurulumun tamam olup olmadığına bakar.
"""

import sys
from pathlib import Path

sorunlar = []


def bildir(baslik, durum, aciklama=""):
    isaret = "OK  " if durum else "EKSİK"
    print(f"[{isaret}] {baslik}" + (f" — {aciklama}" if aciklama else ""))
    if not durum:
        sorunlar.append(baslik)


print("GİTA3111 kurulum testi")
print("-" * 40)

# 1) Python sürümü
surum = f"{sys.version_info.major}.{sys.version_info.minor}"
bildir("Python sürümü", sys.version_info[:2] in [(3, 13), (3, 14)], f"bulunan: {surum}")
if surum not in ("3.13", "3.14"):
    print("      -> Beklenen 3.13 veya 3.14. Bu sürümle devam edilebilir ama"
          " kelime bulutu kütüphanesi sorun çıkarabilir. Hocaya bildir.")

# 2) Kütüphaneler
for paket in ("matplotlib", "wordcloud"):
    try:
        __import__(paket)
        bildir(f"{paket} kurulu", True)
    except ImportError:
        bildir(f"{paket} kurulu", False, "`uv add " + paket + "` komutunu çalıştır")

# 3) Gerçekten bir görsel üretebiliyor muyuz?
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(3, 2))
    plt.bar(["a", "b", "c"], [3, 1, 2])
    cikti = Path("kurulum_testi_ciktisi.png")
    plt.savefig(cikti)
    plt.close()
    bildir("Grafik üretimi", cikti.exists(), f"{cikti.name} oluştu")
except Exception as hata:
    bildir("Grafik üretimi", False, str(hata))

# 4) Cloudflare anahtarı (isteğe bağlı — yoksa sorun değil)
anahtar_dosyasi = Path("anahtar.txt")
if anahtar_dosyasi.exists():
    metin = anahtar_dosyasi.read_text(encoding="utf-8")
    degerler = {}
    for satir in metin.splitlines():
        if "=" in satir:
            ad, _, deger = satir.partition("=")
            degerler[ad.strip().upper()] = deger.strip()

    hesap = degerler.get("ACCOUNT_ID", "")
    anahtar = degerler.get("API_TOKEN", "")

    if hesap and anahtar:
        import json
        import urllib.error
        import urllib.request

        adres = (f"https://api.cloudflare.com/client/v4/accounts/{hesap}"
                 "/ai/run/@cf/google/gemma-4-26b-a4b-it")
        govde = json.dumps({"prompt": "Merhaba de."}).encode("utf-8")
        istek = urllib.request.Request(
            adres,
            data=govde,
            headers={"Authorization": f"Bearer {anahtar}",
                     "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(istek, timeout=30) as yanit:
                bildir("Cloudflare bağlantısı", yanit.status == 200, f"HTTP {yanit.status}")
        except urllib.error.HTTPError as hata:
            bildir("Cloudflare bağlantısı", False,
                   f"HTTP {hata.code} — 401 ise anahtar yanlış, 403 ise izinler eksik")
        except Exception as hata:
            bildir("Cloudflare bağlantısı", False, str(hata))
    else:
        print("[ATLA] Cloudflare bağlantısı — anahtar.txt var ama içi eksik")
else:
    print("[ATLA] Cloudflare bağlantısı — anahtar.txt yok (Konu 02'ye, API dersine kadar sorun değil)")

print("-" * 40)
if sorunlar:
    print("EKSİKLER VAR:", ", ".join(sorunlar))
    print("Bu çıktının ekran görüntüsünü al ve hocana gönder.")
else:
    print("KURULUM TAMAM")
