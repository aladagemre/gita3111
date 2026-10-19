# Konu 8 Ödevi — 5 yönerge × 2 tohum

**Puan yok.** Konu 9'un başında sıradaki arkadaşlar gösterecek.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). Tam 10 istek gönderir; ücretsiz günlük
kotanın küçük bir kısmı.

---

## Ne yapacaksın?

Kendi seçtiğin bir konuda (bir marka, bir etkinlik, bir kitap kapağı...) **beş farklı yönerge**
yaz ve her birini **iki farklı tohumla** üret: 10 görsel. Hepsi ayrı bir `odev8/` klasörüne,
kendini anlatan adlarla kaydedilsin; hiçbiri üzerine yazılmasın.

1. `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev8-ayse.ipynb`).
2. Kopyada Adım 6'nın ilk hücresindeki `Path("ciktilar")` yazan yeri `Path("odev8")` yap: ödevin
   görselleri dersten kalanlarla karışmasın.
3. Kopyada **yalnızca şu beş hücreyi**, bu sırayla çalıştır (hiçbiri görsel üretmez):
   - Adım 1'in iki hücresi (anahtar; `base64`, `requests`, adres)
   - Adım 5'in `def ciz` hücresi
   - Adım 6'nın ilk hücresi (`klasor`, `datetime`)
   - Adım 7'nin `def kaydet` hücresi
4. Adım 7'nin altına yeni bir hücre aç ve şunu yaz; beş yönergeni tırnakların içine yaz
   (Konu 2'deki soru listesi gibi):

```python
yonergeler = ["...", "...", "...", "...", "..."]
tohum = 1

for yonerge in yonergeler:
    resim = ciz(yonerge, tohum)
    if resim is not None:
        print(kaydet(resim, yonerge, tohum))
```

5. Hücreyi çalıştır: beş görsel. Sonra `tohum = 1` satırını `tohum = 2` yapıp **bir kez daha** çalıştır:
   beş görsel daha. `odev8/` klasöründe 10 dosya olmalı.

Kurallar:

- Yönergeleri İngilizce yaz (Konu 7). İçlerine `/` koyma; Windows'ta `\ : ? * " < > |` da dosya adında
  hata verir.
- Yaşayan bir sanatçının adını stil olarak yazma.
- Bir yönerge `İstek başarısız` derse durum koduna bak; o görsel atlanır, diğerleri üretilir.

---

## Teslim edeceğin

1. `odev8/` klasöründeki **10 görsel** (klasörü sıkıştırıp gönderebilirsin)
2. `odev8/yonergeler.txt`: beş yönergenin tamamı, her satıra bir yönerge (dosya adında yalnızca
   ilk 20 karakteri var)
3. **İki cümle** (teslim mesajında): Aynı yönergenin iki tohumu arasındaki fark neydi (kompozisyon mu,
   renk mi, ayrıntı mı)? Hangi yönerge iki tohumda da en tutarlı kaldı, sence neden?

`anahtar.txt`'yi **gönderme**.

---

## İstersen (zorunlu değil)

En beğendiğin görseli Adım 9'daki gibi koddan düzenle. Önce Adım 9'un hücrelerini oku; sonra
`gorsel = Image.open("ilk.jpg")` satırındaki dosya adını kendi görselinin yoluyla değiştir ve talimatı
kendin yaz. Yolu `print`'in yazdığı gibi kopyala; Windows'ta da ters bölü (`\`) yerine düz bölü (`/`)
kullan: `"odev8/2026-10-19_..._1.jpg"`.
