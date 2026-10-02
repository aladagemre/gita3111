# Konu 2 Ödevi — İki parça

**Puan yok.** İkincisi Konu 3'ün dersini besliyor, o yüzden atlanmasın.

---

## Parça 1 — Beş soru, tek dosya

`ders.ipynb` defterini aynı klasörde yeni bir adla kopyala (örneğin
`odev2-sorularim.ipynb`). Kopyada **Adım 7**'deki `sorular` listesini sil, yerine
**kendi beş sorunu** yaz: her soru tırnak içinde, sonunda virgül. Sonra hücreleri
yukarıdan aşağı, sırayla çalıştır (Adım 1'den başla; `modele_sor` Adım 6'da tanımlanıyor).
Adım 7 bitince klasörde `cevaplar.txt` oluşur. Depodaki `ders.ipynb`'yi değiştirmezsen
`git pull` çakışmaz.

Bu parça kendi `anahtar.txt` dosyanı ister (kurulum yönergesinin 6. adımı).

Sorular senin ilgi alanından olsun: tasarım, müzik, oyun, yemek — fark etmez.
Tek kural: hepsi aynı konudan olsun ki cevapları karşılaştırabilelim.

**Teslim edeceğin:** `cevaplar.txt` dosyan ve şu tek cümle:

> Beş cevaptan hangisi işe yaramazdı, sence neden?

İpucu: ders notundaki Adım 8'i hatırla. İşe yaramayan bir cevabın sebebi bazen
modelde değil, soruda eksik kalan bağlamdadır.

`cevaplar.txt` dosyasını gönderirken **`anahtar.txt`'yi gönderme**; defterin kopyasını
da göndermen gerekmiyor.

---

## Parça 2 — Renk etiketleme (Konu 3'ün verisi)

Konu 3'te makine öğrenmesine gireceğiz ve **sınıfın kendi ürettiği veriyle**
model eğiteceğiz. O veriyi şimdi üretiyoruz.

`veri/renkler.csv` dosyasında 20 renk var. Her renge, sana **hangi duyguyu
çağrıştırdığına** göre bir etiket ver:

```
sakin      — dinginlik, huzur, mesafe
enerjik    — hareket, dikkat, canlılık
ciddi      — kurumsal, ağır, güven
```

Dosyayı aynı klasörde **kendi adınla** kopyala (örneğin `ayse-yilmaz.csv`), kopyanın
`etiket` sütununu doldur ve kopyayı gönder.

**Doğru cevap yok.** Herkesin etiketi farklı olacak — zaten mesele bu. Konu 3'te
modelin bu kararsızlıkla ne yaptığını göreceğiz.

Renkleri görmek için hex kodunu bir tasarım aracına yapıştırabilir ya da
`coolors.co` gibi bir siteye girebilirsin.
