# Konu 11 Ödevi — Kendi kılavuzun, kendi RAG'in

**Puan yok.** Konu 12'nin başında sıradaki arkadaşlar gösterecek.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). Yaklaşık 7 vektör isteği, 5 metin isteği ve 1 görsel isteği gönderir;
afişi yeniden ürettiğin her seferde bir görsel daha. Hepsi günlük kotanın küçük bir kısmı.

Bu ödevde Sayfa Kahve'nin yerine **kendi** markanı koyuyorsun: kısa bir kılavuz yazıp modele ona bakarak cevap verdiriyorsun.
Final projen için bir marka ya da kampanya düşünüyorsan onu seç; kılavuz final projesinde de işine yarar.

---

## Ne yapacaksın?

### 1. Kılavuzunu yaz

`11-rag` klasöründe yeni bir metin dosyası aç: `odev11_kilavuz.txt` (VS Code'da **New File**). İçine kendi markanın
kılavuzunu yaz:

- **8–12 paragraf**, her paragraf **tek satırda** (paragrafın içinde Enter'a basma; satır sonu yeni paragraf demek).
  Paragrafların arasında boş satır bırakabilirsin; kod boş satırları atlar.
- Her paragraf **tek bir konu**: ana renkler, kullanılmayan renkler, yazı tipi, logo, ses tonu, yasak sözcükler, görsel tarzı,
  ne gösterilir / ne gösterilmez, bir pratik bilgi (açılış saati, teslim süresi...).
- Her paragraf kendi başına okununca anlaşılsın: "Bu renk" yerine rengin adını yaz.
- Somut ol: "sıcak renkler" yerine "kiremit (#B5543C) ve krem (#F2E8D5)".
- Marka uydurma olabilir. Gerçek bir müşterinin gizli belgesini, kişisel bilgileri yazma: bu metin modelin sunucusuna gider.

Örnek için `veri/kilavuz.txt`'ye bak; ama kopyalama.

### 2. Defteri kendi kılavuzuna çevir

`ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev11-ayse.ipynb`). Kopyada yalnızca şu satırları değiştir:

| Adım | Satır | Yerine |
|---|---|---|
| 1 | `soru = "Sayfa Kahve'nin afişinde ..."` | Kendi markan hakkında, **cevabı kılavuzunda olan** bir soru |
| 2 | `open("veri/kilavuz.txt", ...)` | `open("odev11_kilavuz.txt", ...)` |
| 3 | `vektor_dosyasi = klasor + "kilavuz_vektorleri.json"` | `vektor_dosyasi = klasor + "odev11_vektorleri.json"` |
| 6 | `fiyat_sorusu = "..."` | Cevabı kılavuzunda **hiç olmayan** bir soru |
| 7 | `brif = "..."` ve `arama = "..."` | Kendi afişinin konusu; kılavuzunun görsel kurallarını arayan bir soru |
| 7 | `ciz(..., "ciktilar/afis_kilavuzlu.jpg")` | `"ciktilar/odev11_afis.jpg"` |
| Bonus 3 | `yazi_sorusu = "..."` | Cevabı kılavuzunda **yarım** olan bir soru (kılavuz bir şeyi tarif ediyor ama tam söylemiyor) |

Vektör dosyasının adını değiştirmen önemli: değiştirmezsen Adım 3 dersteki dosyayı görür ve Sayfa Kahve'nin vektörlerini
okur; senin kılavuzun hiç aranmaz.

Isınmadan başlayıp **Adım 7'nin sonuna kadar** sırayla çalıştır, sonra yalnızca Bonus 3'ün iki hücresini. Kılavuzunda sonradan
bir şey değiştirirsen `ciktilar/odev11_vektorleri.json`'u sil ve Adım 2'den yeniden çalıştır.

### 3. Oku ve karşılaştır

Her soruda iki şeye bak: hangi paragraflar geldi (Adım 4'ün, Adım 6'nın ve Bonus 3'ün ilk çıktısı), model bunlarla ne yaptı?

---

## Teslim edeceğin

1. Kılavuzun: `odev11_kilavuz.txt`
2. Defter kopyan, **çıktılarıyla birlikte kaydedilmiş** hâlde (anahtarın defterde görünmez; `rag_araclari.py` onu kendisi okur)
3. Afişin: `ciktilar/odev11_afis.jpg`
4. **Üç cümle:**
   - Model nerede kılavuzuna sadık kaldı, nerede uydurdu? (Üç sorudan birini örnek ver.)
   - Afişte kılavuzuna uymayan bir şey var mı? Kural aramada mı, yönergede mi, çizimde mi kayboldu?
   - Bu sonuçlardan sonra kılavuzunda neyi değiştirirdin (bir paragrafı böler miydin, bir kuralı daha açık mı yazardın)?

`anahtar.txt`'yi **gönderme**. Teslimden önce defter kopyanda anahtarını bir hücreye yazmadığından emin ol.

---

## İstersen (zorunlu değil)

Kılavuzuna aynı konuyu iki yerde anlatan iki paragraf ekle (ör. renkler hem genel bölümde hem "ambalaj" paragrafında).
Vektör dosyasını silip yeniden çalıştır ve renk sorusunu yeniden sor. İki paragraf birlikte geldi mi? Cevap daha mı iyi
oldu, daha mı karışık? Bir cümle.
