# Konu 9 Ödevi — Görselin hareketlensin

**Puan yok.** Konu 11'in başında sıradaki arkadaşlar gösterecek.

Bu ödev anahtar istemez. Arayüzde **bir klip** üretirsin (dersteki gibi Google Flow; ücretsiz günlük kredinden, 720p ve
6 saniyede 10 kredi). Kredin o gün yetmezse ertesi gün yap. Bir araç kart bilgisi ya da abonelik isterse kart girme,
abone olma; hocaya yaz.

---

## Ne yapacaksın?

Konu 8'de ürettiğin görsellerden birini (`08-koddan-toplu-uretim` klasöründe: `odev8/`, `izgara/` ya da `ciktilar/`) arayüzde
videoya çevireceksin.

1. **Görselini seç.** Harekete en uygun olanı: derinliği, boşluğu, hareket edebilecek bir öğesi (buhar, yaprak, su, kumaş) olanı.
   Gerçek bir kişinin yüzü olan görseli seçme; istek reddedilebilir.
2. **Hareket yönergeni yaz** (İngilizce). Kameranın hareketini ve öznenin hareketini **ayrı** cümlelerle anlat, tek bir kamera
   hareketi seç. Örnek: `leaves falling slowly from the tree. slow camera pull out.`
3. **Arayüzde üret.** `ders_notu.md` → Adım 5'in arayüz adımları: model adı → **Video** → **Frames**, görselini
   **+ Add start frame** kutusuna koy, yönergeni yaz. Ayar: Omni Flash 720p, 6 saniye, çıktı sayısı 1. Oranı sen seç: 16:9 ya da
   9:16. Üretmeden önce ayarlarda kredi değerine bak: 10 olmalı.
4. **İndir.** Ders notunun Adım 4'ündeki gibi indir ve `09-video/videolar/odev9.mp4` olarak kaydet.
5. **Günlüğe yaz.** `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev9-ayse.ipynb`). Kopyada:
   - Adım 2'nin ilk hücresini çalıştır (fiyat sözlüğü).
   - Adım 6'nın **ikinci** hücresinde (görselden klibin kaydı) değerleri kendi klibine göre değiştir: `"gorsel"` kendi
     görselinin yolu (ör. `"08-koddan-toplu-uretim/odev8/kolaj_mavi.jpg"`), `"sure"`, `"cozunurluk"` ve `"oran"` arayüzde
     seçtiğin, `"dosya"` `"videolar/odev9.mp4"`. Hücreyi çalıştır; `input` kutularına yönergeni ve beğenip
     beğenmediğini yaz.
   - Adım 6'nın üçüncü hücresinde `kayitlar = [metin_kaydi, gorsel_kaydi]` satırını `kayitlar = [gorsel_kaydi]` yap
     (ödevde metinden video yok) ve dosya adını iki yerde `"odev9_gunlugu.json"` yap. Çalıştır.
   - Adım 6'nın son hücresinde de dosya adını `"odev9_gunlugu.json"` yap ve çalıştır: klibin ücretli bir API'yle kaça mal
     olacağını yazar.

Yaşayan bir sanatçının adını yönergeye yazma.

---

## Teslim edeceğin

1. `videolar/odev9.mp4`
2. `odev9_gunlugu.json`
3. **İki cümle:** görsel hareket edince ne korundu (kompozisyon, stil, renk), ne bozuldu? Bu görsel harekete uygun muydu, neden?
4. **Bir cümle:** bu klip ücretli bir API'yle **1080p**'de koddan üretilseydi kaça mal olurdu (Adım 2'deki fiyat sözlüğüyle)?
   Daha ucuz hangi ayar (süre ya da çözünürlük) bu iş için yeterdi?

Arayüzdeki hesap bilgilerini ya da kart bilgisini **gönderme**.

---

## İstersen (zorunlu değil, bir klip daha)

Aynı görseli **farklı bir kamera hareketiyle** (ör. yaklaşma yerine uzaklaşma) bir kez daha üret, `videolar/odev9_b.mp4` olarak
kaydet. Günlüğe ikinci bir kayıt ekle: ikinci hücreyi yeni değerlerle bir kez daha çalıştırmadan önce sözlüğün adını
`gorsel_kaydi_b` yap, sonra üçüncü hücrede `kayitlar = [gorsel_kaydi, gorsel_kaydi_b]` yaz. İki klipten hangisi görsele daha
çok yakıştı? Bir cümle.
