# Konu 6 Ödevi — İki parça

**Puan yok.** Konu 7'nin ilk oturumu vizenin sözlü teyidine ayrıldığı için bu ödev Konu 8'in
başında, Konu 7'nin ödeviyle birlikte gösterilecek.

---

## Parça 1 — Kendi harfinin haritası

`ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev6-ayse.ipynb`). Depodaki
dosyaya dokunmazsan `git pull` çakışmaz.

1. Kopyada Adım 1'in ilk hücresinde `veri["A"]` yazan yeri `veri["g"]`, `veri["a"]` ya da
   `veri["R"]` yap: harfi sen seç.
2. Hücreleri **Isınma'dan** Adım 8'in sonuna kadar sırayla çalıştır (`plt` Isınma'da alınıyor).
3. Dört görselin ekran görüntüsünü al: **harita** (Adım 5), **soldan sağa yürüyüş** ve
   **yukarıdan aşağı yürüyüş** (Adım 7), **iki font arasındaki yürüyüş** (Adım 8).

**Teslim edeceğin:**

- Dört ekran görüntüsü
- **İki cümle:** Soldan sağa ve yukarıdan aşağı yürürken harfte ne değişiyor? Harita bu
  harfte neyi "en önemli fark" diye seçmiş?

İpucu: g ve a harflerinin **iki katlı** ve **tek katlı** biçimleri var. g'de iki katlı biçimin
altında ikinci bir halka var, tek katlıda açık bir kanca; a'da iki katlı biçimin üstünde bir kemer var.

---

## Parça 2 — En garip A

Bu parça **A** ile: ikinci bir kopya aç ya da Parça 1'deki kopyada harfi yeniden `veri["A"]`
yap; sonra Isınma'yı ve Adım 1–2'yi yeniden çalıştır. Sonra Adım 6'daki noktayı değiştirerek
(`nokta = [[x, y]]`) en garip görünen A'yı bul. Haritanın içinde de dışında da deneyebilirsin.

**Teslim edeceğin:**

- Seçtiğin nokta (iki sayı) ve A'nın ekran görüntüsü
- **İki cümle:** Neden garip? O nokta haritada nerede (A'ların arasında mı, dışında mı)?

---

## İstersen (zorunlu değil)

Adım 8'de iki fontu değiştir: `for ad in fontlar: print(ad)` ile adları alt alta yazdır, iki adı birebir kopyala.
Birbirine en **benzemeyen** iki font hangileri olabilir? Yürüyüşleri ilginç mi?
