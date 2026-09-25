# Konu 2 Ödevi — İki parça

**Puan yok.** İkincisi Konu 3'ün dersini besliyor, o yüzden atlanmasın.

---

## Parça 1 — Beş soru, tek dosya

`06_coklu_soru.py` dosyasını `ornekler` klasöründe yeni bir adla kopyala (örneğin
`odev2_sorularim.py`) ve **kendi beş sorunla** çalıştır. Sorularını da
`veri/ornek_sorular.txt` dosyasının yeni adlı bir kopyasına yaz; kopyadaki
`SORULAR_DOSYASI` satırını o dosyaya çevir. Depodaki dosyaları değiştirmezsen
`git pull` çakışmaz.

Sorular senin ilgi alanından olsun: tasarım, müzik, oyun, yemek — fark etmez.
Tek kural: hepsi aynı konudan olsun ki cevapları karşılaştırabilelim.

**Teslim edeceğin:** `cevaplar.json` dosyan ve şu tek cümle:

> Beş cevaptan hangisi işe yaramazdı, sence neden?

İpucu: ders notundaki Adım 7'yi hatırla. İşe yaramayan bir cevabın sebebi bazen
modelde değil, soruda eksik kalan bağlamdadır.

**İstersen (zorunlu değil):** `08_cevap_raporu.py` ile cevaplarının kelime bulutunu da üret.

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
