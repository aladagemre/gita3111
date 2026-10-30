# Konu 8 Ödevi — Kendi müşterinin haftası

**Puan yok.** Konu 9'un başında sıradaki arkadaşlar gösterecek.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). 5 görsel üretir; beğenmediğin bir günü yenilersen her
yenileme 1 görsel daha. Seçenek B (logo paketi) anahtar istemez.

Bu ödevde seçtiğin müşteriyle Konu 12'ye kadar çalışacaksın: bir öğrenci kulübü, ailenin dükkânı, kendi markan
ya da bir arkadaşının işletmesi. Gerçek bir müşteri olsun, ya da gerçek olabilecek bir müşteri. İş ilanları
yapay zekâ kullandığını söyleyen değil, onunla gerçekten iş üretmiş tasarımcı arıyor; bu set portfolyona girer.

---

## Seçenek A — Haftalık gönderi seti (asıl ödev)

1. **Müşterini tanımla.** Kopyanın en üstüne bir metin hücresi aç, üç satır yaz: müşterinin adı, ne iş yaptığı,
   iki-üç rengi (renk kodlarıyla).
2. **Takvimi yaz.** VS Code'da `08-koddan-toplu-uretim` içinde `odev8` adında bir klasör aç; içine
   `takvim.csv` dosyası oluştur. İlk satır aynen `gun,baslik,sahne`; altına **5 gün**.
   - Başlıklar kısa ve müşterinin sesiyle (sakin mi, coşkulu mu, resmî mi?).
   - Sahneler İngilizce, görselin içinde **yazı olmadan**; virgül içeriyorsa sahneyi tırnak içine al.
   - `gun` sütunu dosya adı olacak: içinde `/` olmasın (`Pazartesi` ya da `14 Kasım` olur, `14/11` olmaz).
   - Dosyayı Excel'de değil VS Code'da ya da Google E-Tablolar'da hazırla (İndir → CSV): Türkçe Excel noktalı
     virgül koyabilir.
3. **Defteri hazırla.** `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev8-ayse.ipynb`), içindeki
   bütün hücreleri sil ve aşağıdaki üç hücreyi yapıştır.
4. **Stil cümleni yaz.** İlk hücrede `STIL`'i kendi müşterinin görsel diline göre yeniden yaz: önce Türkçe üç-dört
   öbek (renk ve teknik; biçim ve doku; ne olmayacak), sonra her öbeği İngilizceye çevir. Sonunda
   `no text, no letters` kalsın. Yaşayan bir sanatçının adını stil olarak yazma; üslubun özelliklerini yaz.
5. Üç hücreyi sırayla çalıştır. Onay sayfasına müşterinin kurallarıyla bak (renkler, yüz, yazı). Uymayan bir gün varsa
   yalnızca onu, derste Adım 5'te yaptığın gibi yeni bir dosya adıyla (`_2`) yeniden üret; eskisinin üstüne yazma.
   Aynı yönerge her seferinde başka bir görsel verir.

```python
import csv
from uretim import sabirli_ciz, gonderi_yap, onay_sayfasi, goster, gunluge_ekle

with open("odev8/takvim.csv", encoding="utf-8-sig") as dosya:
    okuyucu = csv.DictReader(dosya)
    takvim = list(okuyucu)

STIL = "bold paper cut-out collage, deep green and cream, simple shapes"
STIL = STIL + ", plenty of empty space, no text, no letters"
```

```python
gonderiler = []
hikayeler = []
for satir in takvim:
    gun = satir["gun"]
    yonerge = satir["sahne"] + ", " + STIL
    gorsel = sabirli_ciz(yonerge, f"odev8/{gun}_gorsel.jpg")
    gonderi = gonderi_yap(gorsel, satir["baslik"], "gonderi", f"odev8/{gun}_gonderi.jpg")
    hikaye = gonderi_yap(gorsel, satir["baslik"], "hikaye", f"odev8/{gun}_hikaye.jpg")
    gunluge_ekle("odev8/gunluk.csv", gun, yonerge, gorsel)
    gonderiler.append(gonderi)
    hikayeler.append(hikaye)
```

```python
tum_dosyalar = gonderiler + hikayeler
onay_sayfasi(tum_dosyalar, "odev8/onay_sayfasi.jpg")
goster("odev8/onay_sayfasi.jpg")
```

Kendi müşterinin renkleri için iki `gonderi_yap` satırının sonuna `zemin="#FFFFFF", renk="#222222"` gibi iki bilgi
ekleyebilirsin (kendi renk kodlarınla). Varsayılan Sayfa Kahve'nin renkleri.

### Teslim edeceğin

1. `odev8/onay_sayfasi.jpg`
2. `odev8/takvim.csv`
3. `odev8/gunluk.csv`
4. **Üç cümle: "Stil cümlemi nasıl kurdum."** Müşterinin hangi özelliğinden hangi öbeği çıkardın? İlk denemede ne
   tutmadı, nasıl düzelttin? Beş gönderi bir aile gibi duruyor mu?

---

## Seçenek B — Logo teslim paketi (anahtarsız)

Logo tasarlayan herkes aynı işi yapar: logoyu müşterinin istediği her ölçüye ve hem açık hem koyu zemine
yerleştirip ayrı ayrı dosyalar hâlinde teslim eder. Yapay zekâ gerekmez; Python yeter.

1. Kendi logonu (ya da müşterinin logosunu) arka planı **saydam** bir PNG olarak `odev8/logo.png` adıyla kaydet.
2. `ders.ipynb`'yi yeni bir adla kopyala, hücreleri sil, aşağıdaki üç hücreyi yapıştır. `olculer` ve `zeminler`
   listelerini müşterinin ihtiyacına göre değiştir (ör. profil fotoğrafı, kapak görseli, kartvizit).
3. Çalıştır. Logo her zeminin ortasına, kenarlarda logonun boyu kadar boşluk kalacak büyüklükte yerleşir.

```python
from PIL import Image
from uretim import onay_sayfasi, goster

logo = Image.open("odev8/logo.png").convert("RGBA")
olculer = [[1080, 1080], [1500, 500], [400, 400]]
zeminler = [["acik", "#FFFFFF"], ["koyu", "#1F3A5F"]]
dosyalar = []
```

```python
for olcu in olculer:
    en = olcu[0]
    boy = olcu[1]
    for zemin in zeminler:
        sayfa = Image.new("RGB", (en, boy), zemin[1])
        kopya = logo.copy()
        kopya.thumbnail((en // 3, boy // 3))
        x = (en - kopya.width) // 2
        y = (boy - kopya.height) // 2
        sayfa.paste(kopya, (x, y), kopya)
        yol = f"odev8/logo_{en}x{boy}_{zemin[0]}.jpg"
        sayfa.save(yol, quality=95)
        dosyalar.append(yol)
```

```python
onay_sayfasi(dosyalar, "odev8/logo_paketi.jpg")
goster("odev8/logo_paketi.jpg")
```

Satır satır: her ölçü için, her zemin için boş bir sayfa aç; logonun bir kopyasını sayfanın üçte birine sığacak kadar
küçült (`//` bölmenin tam sayı hâli); ortalayıp yapıştır (sondaki `kopya`, saydam yerlerin saydam kalmasını sağlar);
ölçüyü ve zemini dosya adına yazıp kaydet.

### Teslim edeceğin

1. `odev8/logo_paketi.jpg` (bütün dosyalar tek sayfada)
2. **Üç cümle:** Hangi ölçüleri neden seçtin? Logon koyu zeminde de okunuyor mu? Okunmuyorsa ne yapardın (ör. logonun
   açık renkli ikinci bir hâli)?

---

`anahtar.txt`'yi **gönderme**. `odev8/` klasöründeki görselleri **silme**: Konu 9'da birini videoya çevireceğiz.
