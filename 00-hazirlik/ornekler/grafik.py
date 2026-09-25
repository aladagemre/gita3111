"""GİTA3111 — Konu 00 (kurulum): verilen grafik betiği.

Çalıştırma (00-hazirlik klasörünün içinden):  uv run ornekler/grafik.py

Buradaki işin: bu dosyayı benim_grafigim.py adıyla kopyalamak, kopyadaki iki listeyi
kendi verinle değiştirip çalıştırmak.
Grafik kodunun nasıl yazıldığını Konu 01'de (kelime bulutu) öğreneceğiz.
"""

import matplotlib
matplotlib.use("Agg")          # ekran yerine dosyaya çizer
import matplotlib.pyplot as plt

# ---- DEĞİŞTİRECEĞİN YER ----------------------------------------------------
etiketler = ["Pzt", "Sal", "Çar", "Per", "Cum"]
degerler = [3, 7, 2, 8, 5]
baslik = "Haftalık bir şey"
# ---------------------------------------------------------------------------


def grafik_ciz(etiketler, degerler, baslik, dosya_adi="grafik.png"):
    """Çubuk grafiği çizer ve PNG olarak kaydeder. Kaydedilen dosyanın adını döndürür."""
    plt.figure(figsize=(6, 4))
    plt.bar(etiketler, degerler)
    plt.title(baslik)
    plt.tight_layout()
    plt.savefig(dosya_adi, dpi=150)
    plt.close()
    return dosya_adi


kaydedilen = grafik_ciz(etiketler, degerler, baslik)
print(f"Grafik kaydedildi: {kaydedilen}")
