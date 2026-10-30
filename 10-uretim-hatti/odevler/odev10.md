# Konu 10 Ödevi — Kendi müşterinin afişi için son kontrol

**Puan yok.** Konu 11'in başında birkaç arkadaşımız raporunu gösterecek.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). Bir afiş için 1 görsel okuma ve 1 metin isteği gönderir;
düzelttiğin hâli de hattan geçirirsen bu iki katına çıkar. Hepsi günlük kotanın küçük bir kısmıdır. Anahtarını kimseyle
paylaşma, teslim ettiğin dosyalara koyma.

## Ne yapacaksın?

1. Konu 8'de seçtiğin müşterinin (öğrenci kulübü, ailenin dükkânı, kendi markan, bir arkadaşının işletmesi) bir
   **afişini** ya da Konu 8 setinden bir **gönderiyi** seç. Afiş yoksa o müşteri için yazılı bilgileri olan bir afiş
   tasarla: etkinlik adı, tarih, gün, saat, yer. Görseli `.jpg` olarak `10-uretim-hatti/veri/` içine koy
   (ör. `odev10_afis.jpg` adıyla).
2. `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev10-ayse.ipynb`). Kopyada Adım 1'in ilk hücresindeki
   iki satırı değiştir:
   - `afis = "veri/odev10_afis.jpg"`
   - `klasor = "ciktilar/odev10"` (Sayfa Kahve'nin klasörü olmasın; yoksa hat eski okumayı kullanır)
3. Menüden Restart'a bas ve hücreleri baştan sırayla çalıştır. "Model cevap vermezse?" hücresini ve Bonus'u
   atlayabilirsin.
4. **Kendi kontrolünü ekle:** Adım 5'teki boş hücreye müşterine özgü en az bir kontrol yaz (ör. "Instagram adresi
   doğru mu", "ünlem var mı", "semt adı geçiyor mu") ve rapora ekle.
5. `ciktilar/odev10/rapor.md`'yi oku. Her bulgunun (modelin yazım önerileri dahil) yanına kısa bir not düş: **doğru mu** (gerçekten bir sorun mu),
   **yanlış alarm mı** (ör. süs rengi), **eksik mi** (hattın bulamadığı ama senin gördüğün bir sorun).
6. Afişi düzelt ve düzelttiğin hâli de hattan geçir (yeni bir `klasor` adıyla, ör. `ciktilar/odev10_duzeltilmis`).

## Ne teslim edeceksin?

- İlk afiş ve düzelttiğin afiş (`.jpg`).
- İki rapor (`rapor.md`), ilkinde 5. maddedeki notlarınla.
- Kendi kontrol hücrenin kodu (raporun sonuna da yapıştırabilirsin).
- Üç cümle: hattın en çok işine yarayan kontrolü hangisiydi, hangi sorunu yalnızca sen gördün, bir sonraki afişte
  hatta hangi kontrolü eklerdin?

## İpuçları

- Model afişteki bir satırı yanlış okuduysa `ciktilar/odev10/okunan.txt` dosyasını elle düzelt, kaydet ve Adım 1'den
  yeniden çalıştır. Bu bir hile değil, hattın tasarımı böyle.
- Raporda bir renk "zor okunur" çıktıysa afişte bul: yazıysa düzelt, süsse notuna "süs" yaz.
- Afişinde gün adı yoksa Adım 3 `yok` der; bu bir hata değil.
- Kişisel bilgi (telefon numarası, ev adresi) içeren bir afişi modele göndermeden önce müşterine sor ya da o satırı
  çıkar.
