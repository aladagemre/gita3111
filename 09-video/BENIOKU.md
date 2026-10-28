# Konu 9 — Video Üretimi

Bu konuda görsele zaman ekliyoruz: kısa video klipler. Videoyu **arayüzde** üreteceksin (Google Flow, ücretsiz günlük kredi):
önce bir yönergeden, sonra Konu 8'de ürettiğin bir görselden. Defterde iki iş yapacaksın: aynı klip ücretli bir API'yle
koddan üretilseydi kaça mal olurdu, süre ve çözünürlük bedeli nasıl değiştirirdi; ve ürettiğin her klibin yönergesini ve
ayarlarını bir JSON günlüğüne yazmak.

Konu yarım oturum sürüyor: aynı oturumun ikinci yarısı Konu 10 (üretim hattı).

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; konunun başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–6 ve Bonus (Adım 1, 4 ve 5 arayüzde) |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular |
| `ders_notu.md` | Konu notu — arayüz adımları, adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |
| `veri/yedek_fincan.jpg` | Konu 8'in görseli yoksa görselden video için kullanılan yedek görsel |
| `odevler/odev9.md` | Bu konunun ödevi |

İndirdiğin videoları bu klasörde `videolar/` içine koyarsın (`metinden.mp4`, `gorselden.mp4`); günlük `video_gunlugu.json`'a
yazılır. Alıştırma defteri `alistirma_gunlugu.json`'u kullanır. Bunların hiçbiri depoya girmez.

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

Arayüz için bilgisayarda Chrome ya da Edge ile `labs.google/fx/tools/flow` adresini aç ve kişisel Google hesabınla gir
(18 yaş ve üstü). Adımlar
`ders_notu.md`'de.

## Anahtar gerekiyor mu?

Hayır. İki defter de anahtar istemez, internete çıkmaz. Video arayüzde, kendi Google hesabının ücretsiz günlük kredisiyle
üretilir (abonelik almamış her kullanıcıya her gün 50 kredi; derste iki klip 22 kredi). Hesap açarken ya da üretirken kart bilgisi
istenirse ya da abone olman istenirse girme, abone olma, hocaya yaz.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece
`git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Nerede |
|---|---|---|
| Isınma | Bir klip kaç kare | defter |
| Adım 1 | Metinden ilk klibi başlatmak; uzun süren iş | arayüz |
| Adım 2 | Fiyat sözlüğü; 4K ile 1080p | defter |
| Adım 3 | 20 saniyelik tanıtım: hangi ayar yarısına indirir | defter |
| Adım 4 | Klibi izlemek, indirmek, değerlendirmek | arayüz |
| Adım 5 | Görselden klip | arayüz |
| Adım 6 | Video günlüğü ve "API'yle olsaydı" hesabı | defter |
| Bonus | Ücretsiz krediyi planlamak; dikey video | defter, arayüz |
