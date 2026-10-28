# Konu 12 — Ajan: Kararı Modele Bırakmak

Bu konuda bir isteğe hangi araçların, hangi sırayla gerektiğine **modelin** karar verdiği bir program kuruyorsun: bir
**ajan**. Modelin elinde üç araç var: görsel çizmek, fotoğraf düzenlemek ve Sayfa Kahve'nin marka kılavuzunda aramak
(Konu 11'deki arama). Önce bir turu çerçevesiz, elle yapacaksın: araç tarifi, istekte `tools`, cevapta `tool_calls`,
aracı çalıştıran program. Sonra aynı işi **Agno** adlı ajan çerçevesiyle kuracak, ajanın kararlarını yazdıracak, bir
tarifi bozup düzeltecek ve tarifini senin yazdığın dördüncü bir aracı (`slogan_yaz`) ajana ekleyeceksin. Sonunda
elinde ajanın çizdiği afişler olacak; kılavuza uyup uymadıklarına sen bakacaksın. Bonus'ta bir ajan çalıştırmasının
modele kaç istek gönderdiğini ve ne kadar kota harcadığını da hesaplayabilirsin.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–9 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar ve boşluklu sorular (anahtar istemez, internete çıkmaz) |
| `ajan_araclari.py` | Yardımcı dosya. Araçların içinde çalışan hazır fonksiyonlar: `ciz` (Konu 8), `duzenle` (Konu 7), `en_yakin_paragraflar` (Konu 11'deki `kilavuzda_ara`'nın içindeki arama), `modele_sor` (Konu 5) ve `tarifi_goster` |
| `veri/fincan.jpg` | Düzenlenecek fotoğraf |
| `veri/kilavuz.txt` | Sayfa Kahve'nin marka kılavuzu (Konu 11'deki belge): her satır bir paragraf |
| `veri/ajan_gunlugu.json` | Alıştırmanın el yapımı ajan kayıtları |
| `odevler/odev12.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu — adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Defterin ürettiği ve düzenlediği görseller bu klasörde `ciktilar/` içine yazılır: `afis.jpg`, `duzenlenmis.jpg`,
`elle_cizim.jpg` ya da `elle_duzenleme.jpg`. Kılavuzun vektörleri ilk aramada `ciktilar/kilavuz_vektorleri.json`'a
saklanır.

## Çalıştırma

Bu konunun iki yeni kütüphanesi var: `agno` (ajan çerçevesi) ve `openai` (Agno'nun istek gönderirken kullandığı paket;
istekler Cloudflare'e gider, OpenAI hesabı gerekmez). Yeni konuyu almak ve kütüphaneleri kurmak için **`gita3111`
klasöründe** bir kez:

```
git pull
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır.

Defterin kopyası `ajan_araclari.py` ve `veri/` klasörüyle **aynı klasörde** durmalı; yoksa
`ModuleNotFoundError: No module named 'ajan_araclari'` alırsın. `ModuleNotFoundError: No module named 'agno'` alırsan
`uv sync`'i çalıştırmamışsındır ya da çekirdek `.venv` değildir.

## Anahtar gerekiyor mu?

Isınma anahtarsız; alıştırma defteri de. Adım 1 ve sonrası `anahtar.txt` ister (bütün konular için tek dosya,
`gita3111` klasöründe). Defterin tamamı (Bonus dahil) metin ve arama modellerine yaklaşık 30 istek gönderir ve 10 kadar
görsel üretir ya da düzenler; günlük ücretsiz kotanın %10'undan az. Her ajanın bir araç çağrısı sınırı var
(`tool_call_limit`): bir çalıştırma en fazla 3–4 araç çalıştırır. Anahtarın yoksa yanındakiyle birlikte, onun ekranında izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı
değiştirmek istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece
`git pull` hiç çakışmaz.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Ajanı önce sen oyna: beş istek için hangi araçlar, hangi sırayla | gerekmez |
| Adım 1 | Hazır parçalar; fincan; kılavuzda bir arama | gerekir |
| Adım 2 | Araç tarifi, elle | gerekmez |
| Adım 3 | İstekte `tools`, cevapta `tool_calls` | gerekir |
| Adım 4 | Aracı çalıştıran program; ajan döngüsü nedir | gerekir |
| Adım 5 | Agno: model ve üç araç fonksiyonu (tür ipucu, docstring) | istek göndermez |
| Adım 6 | İlk ajan; kararları görmek (`cevap.tools`) | gerekir |
| Adım 7 | Çok adım: önce kılavuz, sonra çizim; bütün konuşma (`cevap.messages`) | gerekir |
| Adım 8 | Tarifi boz, düzelt | gerekir |
| Adım 9 | Kendi aracın: `slogan_yaz` | gerekir |
| Bonus 1 | Bir çalıştırma kaç istek, ne kadar kota | istek göndermez |
| Bonus 2 | Isınmadaki öbür istekler | gerekir |
| Bonus 3 | Ajanın genel brifi (`instructions`) | gerekir |
