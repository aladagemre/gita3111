# Konu 12 — Stüdyo asistanı

Bu konuda Sayfa Kahve için bir günün dört küçük işine bakan bir **stüdyo asistanı** kuruyorsun: 14 Kasım hangi
güne denk geliyor, afiş matbaaya gitmeden kurallara uyuyor mu, müşterinin yeni isteği ("artık hardal sarısı
istemiyoruz") unutulmasın, yeni gönderi metni olur mu. Asistana yalnızca hedefi söylüyorsun; afişi okumak, kurallara
bakmak, günü hesaplamak ve not almak için hangi aracı hangi sırayla kullanacağına kendisi karar veriyor. Araçları sen
yazıyorsun: her biri kısa bir Python fonksiyonu ve onun tarifi. Sonunda müşteriye gidecek bir kontrol notu taslağın ve
içini kendi yazdığın bir aracın oluyor. Bonus'ta aynı yolla yaklaşan tasarım yarışmalarını arıyorsun.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–4 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: araç tarifleri, bozuk araçlar, ajanın yerine karar vermek (anahtar istemez, internete çıkmaz) |
| `ajan_araclari.py` | Yardımcı dosya: araçların içinde çalışan hazır işler (afişteki yazıyı okumak, gün hesabı, hafızada arama ve not ekleme, web araması) ve ajanın modelini kuran `model_kur` |
| `veri/afis.jpg` | Kontrol edilecek afiş (Konu 10'daki, bilerek hatalı) |
| `veri/afis_temiz.jpg` | Aynı afişin düzeltilmiş hâli, karşılaştırma için |
| `veri/kilavuz.txt` | Sayfa Kahve'nin marka kılavuzu: her satır bir paragraf |
| `veri/notlar.txt` | Müşterinin mesajlarından ve jüriden notlar (Konu 11'deki): her satır bir not |
| `odevler/odev12.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu: adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Defter `ciktilar/` klasörüne yazar: `hafiza.txt` (asistanın müşteri hafızası; ilk aramada kılavuz ve notlardan açılır,
`veri/` içindeki dosyalar değişmez) ve `afis_kontrolu.txt` (kontrol notunun taslağı).

## Çalıştırma

Bu konunun kütüphaneleri `agno` (ajan kütüphanesi), `openai` ve `ddgs` (ücretsiz web araması). `openai` yalnızca
Agno'nun istek gönderirken kullandığı biçimin adı: istekler Cloudflare'e gider, OpenAI hesabı da ödeme de gerekmez.
Yeni konuyu almak ve kütüphaneleri kurmak için **`gita3111` klasöründe** bir kez:

```
git pull
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır.

Defter `ajan_araclari.py` ve `veri/` klasörüyle **aynı klasörde** durmalı; yoksa
`ModuleNotFoundError: No module named 'ajan_araclari'` alırsın. `No module named 'agno'` alırsan `uv sync`'i
çalıştırmamışsındır ya da çekirdek `.venv` değildir.

## Anahtar gerekiyor mu?

Isınma ve alıştırma defteri anahtarsız. Adım 1 ve sonrası `anahtar.txt` ister (bütün konular için tek dosya,
`gita3111` klasöründe). Her ajan çalıştırması modele birkaç istek gönderir; her ajanda bir araç sınırı
(`tool_call_limit`) var, bu yüzden bir çalıştırma kotanı tüketemez. Bonus'taki web araması anahtar istemez.
Anahtarın yoksa Isınma'dan sonrasını hocanın paylaştığı ekrandan izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı değiştirmek istersen önce
aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.
