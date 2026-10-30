# Konu 11 — Müşterinin söylediklerini unutmayan bir hafıza

Müşterinin WhatsApp'tan, e-postayla, toplantıda söyledikleri ve jüride aldığın eleştiriler dağınık durur; yeni bir
iş yaparken yarısı unutulur. Bu konuda Sayfa Kahve için bir **müşteri hafızası** kuruyorsun: marka kılavuzu ve
notlar tek yerde, soruna anlamca en yakın notları bulan ve cevabını yalnız o notlara dayandıran bir yardımcı. Konu
10'daki afişin metnini müşterinin kurallarına göre kontrol ettiriyor, sonra hafızaya yeni bir not ekleyip aynı
sorunun cevabının değiştiğini görüyorsun. En sonda kendi müşterin için küçük bir hafıza kuruyorsun.

| Dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Dersin başındaki slaytlar |
| `ders.ipynb` | Birlikte çalıştırdığımız defter: Isınma, 4 adım, Bonus |
| `alistirma.ipynb` | Kendi başına çözeceğin defter (anahtar istemez, internete çıkmaz) |
| `ders_notu.md` | Adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |
| `rag_araclari.py` | Yardımcı dosya: `vektor_al`, `benzerlik` (Konu 4), `modele_sor` (Konu 5), `hafizayi_kur`, `hafizada_ara`, `not_ekle` |
| `veri/kilavuz.txt` | Sayfa Kahve'nin marka kılavuzu: her satır bir kural |
| `veri/notlar.txt` | Hafızanın notları: her satır `Kaynak, kanal, tarih: not`. Defter yeni notları bu dosyanın sonuna ekler |
| `veri/afis_metni.txt` | Konu 10'daki afişin üstündeki yazılar |
| `odevler/odev11.md` | Bu konunun ödevi |

## Çalıştırma

Yeni kütüphane yok. Yeni konuyu almak için `gita3111` klasöründe:

```
git pull
uv sync
```

Sonra VS Code'da `ders.ipynb`'yi aç, sağ üstten çekirdek olarak **`.venv`**'i seç ve hücreleri yukarıdan aşağı
**Shift + Enter** ile çalıştır. Defter `rag_araclari.py` ve `veri/` ile aynı klasörde durmalı.

Defter, Adım 4'te `veri/notlar.txt`'nin sonuna not ekler; hafızanın büyümesi budur. Defteri ikinci kez çalıştırırsan
aynı not bir kez daha eklenir: dosyayı aç, fazla satırı sil. Bir gün `git pull` bu dosya
yüzünden "your local changes would be overwritten" derse eklediğin notları bir kenara kopyala, `gita3111`
klasöründe `git checkout 11-rag/veri/notlar.txt` çalıştır, sonra yeniden `git pull`.

## Anahtar gerekiyor mu?

Isınma ve alıştırma defteri anahtarsız. Ders defterinde Adım 1'den sonrası `anahtar.txt` ister (Konu 2'deki dosya,
`gita3111` klasöründe). Defterin tamamı 12 istek gönderir (10 vektör, 2 metin); Bonus 3 istek daha. Hepsi günlük
ücretsiz kotanın küçük bir parçası. Anahtarın yoksa Adım 1'den sonrasını hocanın ekranından izle.
