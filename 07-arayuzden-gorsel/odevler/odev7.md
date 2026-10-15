# Konu 7 Ödevi — Üç görsel dil

**Puan yok.** Konu 8'in başında sıradaki arkadaşlar gösterecek (Konu 6'nın ödeviyle birlikte).

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). Toplam 3–6 görsel üretir.

---

## Ne yapacaksın?

Seçtiğin bir **marka ya da etkinlik** için üç farklı görsel dil deneyeceksin. Gerçek bir
marka olabilir (bir kahve dükkânı, bir festival, bir kitabevi) ya da hayalî.

1. `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev7-ayse.ipynb`). Kopya
   `gorsel_araci.py` ile aynı klasörde durmalı.
2. Kopyada **Isınma** hücresindeki beş parçayı kendi brifine göre İngilizce yaz:
   `ozne`, `ortam`, `stil`, `isik`, `kompozisyon`. Hücreyi çalıştır.
3. Adım 1'in **ilk** hücresini çalıştır: yalnızca `from gorsel_araci import ciz, duzenle, yan_yana`
   satırı olan hücre (görsel üretmez).
4. Adım 4'ün ilk hücresinde `stiller` listesine **kendi seçtiğin üç stili** yaz ve `kaydet`
   adını değiştir: `kaydet="odev7_pano.png"`. Hücreyi çalıştır. Hücre her yönergeyi ekrana da yazar.
5. Tohumu (`tohum=42`) değiştirme: üç görsel arasındaki fark yalnızca stilden gelsin.

İstersen Adım 4'ün ikinci hücresiyle (ışık) aynısını dene.

**Kural:** yaşayan bir sanatçının ya da illüstratörün adını stil olarak yazma. Sevdiğin bir
üslup varsa onun **özelliklerini** yaz: renk paleti, çizgi, doku, teknik.

---

## Teslim edeceğin

1. **Pano:** `odev7_pano.png`
2. **İki cümle:** Hangi görsel dil bu marka için işe yaradı? Neden? (Öbür ikisinde ne eksikti?)
3. **Üretim günlüğü:** kopyanın en sonuna bir metin (Markdown) hücresi ekle; her görsel bir satır:
   `dosya adı | model | tohum | yönergenin tamamı`, örneğin
   `012.jpg | flux | 42 | a small bookshop ..., linocut print, ...`. Dosya adı ve yönerge Adım 4'ün
   hücresinin çıktısında yan yana yazıyor.

`anahtar.txt`'yi **gönderme**.

---

## İstersen (zorunlu değil)

En beğendiğin görseli Adım 8'deki gibi `duzenle` ile değiştir (Adım 4'ün çıktısında her görselin dosya adı yazıyor; ör. `duzenle("ciktilar/002.jpg", "...")`): renk paletini markanın
renklerine çek ya da arka planı sadeleştir. Önce ve sonra hâlini yan yana getir.
