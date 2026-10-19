# Konu 9 Ödevi — Kendi ızgaran

**Puan yok.** Konu 10'un başında sıradaki arkadaşlar gösterecek.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). En fazla 12 görsel (İstersen bölümüyle 15) üretir ve en fazla 13 kez
görsel anlayan modele soru sorar.

---

## Ne yapacaksın?

Kendi seçtiğin bir konuda (bir marka, bir etkinlik, bir kitap kapağı...) bir şablon kur ve bir ızgara üret.

1. `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev9-ayse.ipynb`).
2. Kopyada şablonu kendi konuna göre değiştir:
   - Isınma hücresindeki `stiller` listesine **en az 2**, `renkler` listesine **en az 3** kısa ad yaz.
     Kısa adlarda boşluk ve Türkçe karakter olmasın (dosya adı olacaklar): `"kolaj"`, `"neon"`.
   - Adım 1'in ilk hücresinde `ozne` (sabit kısım, İngilizce), `brif` (Türkçe notun) ve iki yönerge sözlüğünü
     yaz: sözlüğün anahtarı listedeki kısa ad, değeri İngilizce açıklama (`"kolaj": "paper collage"`). Her kısa
     adın sözlükte bir karşılığı olmalı.
   - Adım 1'deki elle yazılmış tek kart hücresi yalnızca örnek; ona dokunma.
   - Toplam en fazla 12 kart (ör. 2 × 3, 3 × 4).
3. Adım 4'ün ilk hücresinde `Path("izgara")` yerine `Path("odev9")` yaz: ödevin görselleri dersten kalanlarla karışmasın.
4. Adım 7'deki `brif_ingilizce = "..."` satırını kendi brifine göre İngilizce yaz.
5. Isınma'dan başlayıp **Adım 7'nin sonuna kadar** sırayla çalıştır. Bonus 2'yi çalıştırma. Bir listeyi ya da
   sözlüğü sonradan değiştirirsen yine Isınma'dan itibaren sırayla çalıştır; yoksa kartlar eski kalır. Adım 6'daki
   `benim_secimim` satırına kendi kazananının dosya adını yaz.
   Kontak sayfasının ızgarası liste uzunluklarına göre kendini ayarlar (`satir = len(stiller)`).
   `kontak_sayfasi.png` ve `uretim_gunlugu.json` dersteki dosyaların üzerine yazılır; dersinkini saklamak
   istersen önce başka bir ada kopyala.

Yaşayan bir sanatçının adını stil olarak yazma.

---

## Teslim edeceğin

1. `kontak_sayfasi.png`
2. `uretim_gunlugu.json` (model puanlarıyla birlikte)
3. **İki cümle:** Hangi kombinasyon kazandı, neden? Bir satırda ya da sütunda bir eğilim var mı (bir stil ya da renk hep iyi ya da hep kötü mü)?
4. **Bir cümle:** Görsel anlayan model de aynı kombinasyonu mu öne çıkardı? Çıkarmadıysa sence neden?

`anahtar.txt`'yi **gönderme**. `odev9/` klasöründeki görselleri **silme**: Konu 10'da birini videoya çevireceğiz.

---

## İstersen (zorunlu değil)

Bonus 1'i çalıştır: `benim_secimim`'deki kazananı üç tohumla üretir (3 görsel daha). Üç kompozisyondan hangisini seçerdin?
