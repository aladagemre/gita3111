# Konu 10 Ödevi — Görselin hareketlensin

**Puan yok.** Konu 11'in başında sıradaki arkadaşlar gösterecek.

Bu ödev `anahtar.txt`'deki `VIDEO_ADRES` ve `VIDEO_KOD` satırlarını ister (derste dağıtıldı). **Bir klip** üretir
(4 saniye, 720p, yaklaşık 0,40 dolar; hocanın hesabından). Klip hakkın sınırlı: hücreleri gereksiz yere yeniden çalıştırma.

---

## Ne yapacaksın?

Konu 9 ödevinde ürettiğin görsellerden birini (`../09-toplu-uretim/odev9/` klasöründe) videoya çevireceksin.

1. `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev10-ayse.ipynb`). Kopya `video.py`'nin yanında durmalı.
2. Görselini seç: kazananın ya da harekete en uygun olanı (derinliği, boşluğu, hareket edebilecek bir öğesi olan).
3. Kopyada şunları **sırayla** çalıştır:
   - Isınma, Adım 2 ve Adım 3'ün bütün hücreleri (ücretsiz; sahte iş ve video kodun).
   - **Adım 4'ü atla** (metinden video; ödevde gerek yok).
   - Adım 5'te yalnızca `def bekle` hücresini; Adım 6'da yalnızca klasör hücresini (`klasor = Path("videolar")`).
   - Adım 7'nin hücrelerini, şu değişikliklerle:
     - İlk hücrede yolu kendi görselinle değiştir: `Path("../09-toplu-uretim/odev9/DOSYA_ADIN.jpg")`.
       Defter "yedek görseli kullanıyorum" derse dosya adı yanlış: düzelt, yoksa yedek fincan videoya çevrilir.
     - Gövdedeki `"yonerge"`'yi kendi hareket yönergenle (İngilizce) yaz. Kameranın hareketini (ör. `slow pan to the left`)
       ve öznenin hareketini (ör. `leaves falling slowly`) ayrı ayrı anlat.
     - İstersen `"oran"`'ı `"9:16"` yap (telefon, hikâye). Süreye dokunma: `"4"`.
     - Son hücrede dosya adını `"gorselden.mp4"` yerine `"odev10.mp4"` yap.
   - Adım 8'in ilk hücresinde `metin_kaydi = {...}` bloğunu sil ve son satırı `kayitlar = [gorsel_kaydi]` yap
     (ödevde metinden video yok). İkinci hücrede günlük adını `"odev10_gunlugu.json"` yap.
4. `bekle` "Zaman aşımı" derse yeni iş başlatma: yalnızca `video_adresi = bekle(gorsel_is_no)` hücresini yeniden çalıştır.

Görselinde gerçek bir kişinin yüzü varsa istek reddedilebilir; o zaman başka bir görsel seç. Yaşayan bir sanatçının adını
yönergeye yazma.

---

## Teslim edeceğin

1. `videolar/odev10.mp4`
2. `odev10_gunlugu.json`
3. **İki cümle:** Görsel hareket edince ne korundu (kompozisyon, stil, renk), ne bozuldu? Bu görsel harekete uygun muydu, neden?
4. **Bir cümle:** Bu klibi 8 saniye isteseydin kaç dolar tutardı (Isınma'daki fiyatla)? Bu iş için o fazladan 4 saniyeye değer miydi?

`anahtar.txt`'yi ve video kodunu **gönderme**.

---

## İstersen (zorunlu değil, bir klip daha)

Aynı görseli **farklı bir kamera hareketiyle** (ör. yaklaşma yerine uzaklaşma) bir kez daha üret: Adım 7'nin gövde hücresini
yönergeyi değiştirerek yeniden çalıştır, sonraki iki hücreyi de; son hücrede dosya adı `odev10_b.mp4` olsun. Sonra Adım 8'in iki
hücresini yeniden çalıştır; günlük adını `odev10_b_gunlugu.json` yap. İki klipten hangisi görsele daha çok yakıştı?
