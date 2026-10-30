# Konu 8 — Bir haftalık gönderi seti

Bu konuda bir sosyal medya tasarımcısının en sık yaptığı işi yapıyorsun: müşteri (Sayfa Kahve, sessiz bir çalışma
kafesi) haftalık içerik takvimini gönderiyor; sen her gün için bir gönderi (4:5) ve aynı görselden bir hikâye (9:16)
hazırlıyor, hepsini müşteriye tek bir onay sayfasıyla yolluyorsun. Arayüzde aynı işi on kez elle yapardın; burada
bir tablo ve bir döngüyle yapıyorsun. Görselleri yapay zekâ üretiyor, marka dilinin tutarlı kalması için kılavuzdan
kurduğun bir stil cümlesi kullanıyorsun; başlığı görselin altına, ölçüleri, onay sayfasını ve üretim günlüğünü
Python hazırlıyor. Sonra onay sayfasına kılavuzun gözüyle sen bakıyorsun; uymayan bir gün varsa (model bazen yasak
bir renk ekler) yalnızca onu kendi yazdığın birkaç satırla yeniliyorsun.
Ödevde aynısını kendi seçtiğin bir müşteri için yapacaksın; o müşteriyle Konu 12'ye kadar çalışacaksın.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–5 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar, boşluklu sorular, bir "kendin yaz" (anahtar istemez, internete çıkmaz) |
| `uretim.py` | Yardımcı dosya: `ciz`, `sabirli_ciz` (görsel üretir), `gonderi_yap`, `onay_sayfasi`, `gunluge_ekle`, `goster` (Python işleri). İçini okuman gerekmiyor |
| `veri/takvim.csv` | Sayfa Kahve'nin haftalık takvimi: `gun`, `baslik`, `sahne` |
| `veri/benim_takvimim.csv` | Bonus için örnek üç satır; kendi müşterinle değiştir |
| `veri/hazir/` | Alıştırmada model yerine kullanılan beş hazır görsel |
| `veri/DejaVuSerif.ttf` | Başlıkların yazı tipi (Türkçe harfli, serbest lisanslı; lisansı `veri/DejaVu_LISANS.txt`) |
| `odevler/odev8.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu: adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Defterin çıktıları `ciktilar/` içine yazılır (`Pazartesi_gonderi.jpg`, `Pazartesi_hikaye.jpg`, `onay_sayfasi.jpg`,
`gunluk.csv`...); alıştırmanınkiler `alistirma_ciktilari/`, ödevinkiler `odev8/` içine. Bu klasörler depoya girmez.

## Çalıştırma

Yeni kütüphane yok. Yeni konuyu almak için **`gita3111` klasöründe** bir kez:

```
git pull
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır.

Defter `uretim.py` ile **aynı klasörde** durmalı; yoksa `ModuleNotFoundError: No module named 'uretim'` alırsın.

## Anahtar gerekiyor mu?

Isınma anahtarsız; alıştırma defteri de. Adım 1'den itibaren ders defteri `anahtar.txt` ister (bütün konular için tek
dosya, `gita3111` klasöründe; Konu 2). Ana akış 7 görsel üretir, Bonus'la 10; her görsel ücretsiz günlük kotadan yer.
Yazı, ölçü, onay sayfası ve günlük kota yemez. Anahtarın yoksa hocanın paylaştığı ekrandan izle; alıştırmayı yine
kendin çözebilirsin.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Defteri değiştirip saklamak istersen önce aynı
klasörde **yeni bir adla kopyala** (ör. `ders-ayse.ipynb`), kopyada çalış. `veri/benim_takvimim.csv` senin: içini
istediğin gibi değiştir. `ciktilar/` ve `odev8/` depoya girmez.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Kim yapıyor | Anahtar |
|---|---|---|---|
| Isınma | Takvimi oku; kaç görsel üretilecek, kaç dosya hazırlanacak | Python | gerekmez |
| Adım 1 | Pazartesi'nin gönderisi: görsel + başlık | yapay zekâ (1 görsel) + Python | gerekir |
| Adım 2 | Marka dili: kılavuzdan stil cümlesi; günlüğü başlat | yapay zekâ (1 görsel) + Python | gerekir |
| Adım 3 | Bütün hafta: kalan dört gün için döngü, günlük | yapay zekâ (4 görsel) + Python | gerekir |
| Adım 4 | Aynı görsellerden hikâyeler ve onay sayfası | Python | istek yok |
| Adım 5 | Kılavuza uymayan günü sen seç; yalnızca onu, yeni bir dosya adıyla yenile (kendin yazıyorsun) | yapay zekâ (1 görsel) + Python | gerekir |
| Bonus | Kendi müşterinin üç günü | yapay zekâ (3 görsel) + Python | gerekir |
