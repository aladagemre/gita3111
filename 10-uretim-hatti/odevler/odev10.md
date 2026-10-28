# Konu 10 Ödevi — Kendi hattının iskeleti

**Puan yok.** Konu 11'in başında sıradaki arkadaşlar gösterecek.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). En fazla 5 metin isteği (bir deneme + en fazla 4 slogan) gönderir ve
en fazla 4 görsel üretir. Bir sloganı değiştirip görselini yeniden ürettiğinde her değişiklik bir görsel isteği daha
demek. Hepsi günlük kotanın küçük bir kısmını tutar.

Bu ödev final projesinin ilk taslağı: kendi konunda, kendi brifinle çalışan bir hat. **Güzel olması gerekmiyor**;
halkaların birbirine bağlı ve kayıtlı çalışması yeter. Final projeni bu iskeletin üstüne kuracaksın.

---

## Ne yapacaksın?

1. `10-uretim-hatti` klasöründe iki dosyayı yeni adlarla kopyala (kopyalar aynı klasörde, `halkalar.py`'nin yanında kalsın):
   - `ders.ipynb` → ör. `odev10-ayse.ipynb`
   - `ayarlar.json` → ör. `odev10_ayarlar.json`
2. Kendi ayarlar dosyanı doldur. Final projen için bir konu seç (bir marka, bir etkinlik, bir kampanya). Final brifi
   elindeyse konuyu oradan seç.
   - `calisma`: kısa, boşluksuz, Türkçe karaktersiz bir ad (ör. `"odev10_cicekci"`). Dersteki `kafe_afisi_1` olmasın:
     çıktıların dersinkilerle karışmasın.
   - `konu`: Türkçe, slogan sorusuna gidecek (ör. `"mahallede yeni açılan bir çiçekçi"`).
   - `stil`: İngilizce, görsel yönergesine gidecek (ör. `"paper collage poster, warm colors"`).
   - `slogan_sayisi`: en fazla `4`.
   - `sicaklik`, `tohum`: istersen değiştir.
   - JSON kuralları: metinler çift tırnakta, ayarlar arasında virgül, son satırdan sonra virgül yok.
3. Defter kopyasında Adım 1'in ilk hücresinde `open("ayarlar.json", ...)` yerine kendi dosyanın adını yaz:
   `open("odev10_ayarlar.json", ...)`. Başka bir hücreyi değiştirmen gerekmiyor.
4. Isınma'dan başlayıp **Adım 7'nin sonuna kadar** sırayla çalıştır, yalnızca **Adım 6'yı atla** (bilerek koparma). O hücre
   4 numaralı görseli boş yönergeyle ister; 4 slogan seçtiysen `gorsel_4.jpg` zaten var ve kayda yanlış bir satır girer.
   Sonra Bonus 1'in pano hücresini çalıştır.
5. Panoya bak. Beğenmediğin bir slogan varsa Bonus 2'deki gibi kendi çalışma klasöründeki `sloganlar.json`'da değiştir,
   o görseli sil, sonra Adım 4'ün ilk çağrı hücresinden (`sloganlar = slogan_halkasi()`) Adım 5'in sonuna kadar, ardından
   Adım 7'nin günlük hücresini ve panoyu yeniden çalıştır (Adım 6 yine hariç); böylece `uretim.json` ve pano da yenilenir.
   Ayarlar dosyasını değiştirdiysen Adım 1'den itibaren yeniden çalıştır; brifi (konu, stil, tohum) değiştirdiysen `calisma`
   adını da değiştir.

Yaşayan bir sanatçının adını stil olarak yazma.

---

## Teslim edeceğin

1. Kendi ayarlar dosyan (`odev10_ayarlar.json`)
2. Çalışma klasöründen (`ciktilar/` içinde, `calisma` adını verdiğin klasör) `pano.png` ve `uretim.json`
3. **Üç cümle:**
   - Hangi halkaya elle müdahale ettin (bir sloganı değiştirdin mi, bir görseli sildin mi), neden? Müdahale etmediysen neden gerek görmedin?
   - Hangi slogan–görsel eşleşmesi işe yaradı: aynı şeyi mi söylüyorlardı, birbirini mi tamamlıyordu?
   - Final projende bu hatta hangi halkayı eklemek istersin (başlık, ölçü uyarlaması, başka bir şey)?

`anahtar.txt`'yi **gönderme**. Çalışma klasörünü silme: final projesinde aynı hattı geliştireceksin.

---

## İstersen (zorunlu değil)

Hattın başına bir halka daha düşün: konuyu metin modeline verip **İngilizce bir sahne tarifi** yazdırmak ve görsel yönergesine
slogan yerine onu koymak. Ayarlar dosyana yeni bir alan, defterine yeni bir halka eklemen gerekir. Görseller daha mı iyi
oldu, daha mı kötü? Bir cümle.
