# Konu 12 Ödevi — Kendi müşterin için bir asistan

**Puan yok.** Konu 13'ün başında birkaç arkadaşın gösterecek. Ajan final projesinde **isteğe bağlı bir ekstra**;
küçük bir hafıza (RAG) adımı ise finalde zorunlu. Bu ödev, ajanı projende kullanmak istersen elinde çalışan bir örnek
olsun diye.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). Her ajanda `tool_call_limit` kullan; denemelerin kotanı
tüketmesin.

---

## Ne yapacaksın?

1. **Hazırlık.** `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev12-ayse.ipynb`). Isınma'yı, Adım 1'in
   ilk kod hücresini ve kullanacağın araçların `def` hücrelerini (Adım 2–3) çalıştır.
2. **Hafıza.** Konu 11'de kendi müşterin için yazdığın notları (her satır bir kural ya da not) bu klasörde
   `ciktilar/hafiza.txt` dosyasına koy. Dosya derste Sayfa Kahve'nin notlarıyla açıldıysa içini kendi notlarınla
   değiştir. `kurallara_bak` ve `hatirla` araçları bu dosyayı kullanır.
3. **Araçlar.** Ajanın en az iki aracı olsun:
   - biri Adım 2–3'teki araçlardan (`kurallara_bak` ya da `hatirla`; müşterinin hafızası için),
   - biri **baştan sona senin yazdığın** yeni bir araç: kendi müşterinin işine yarayan, içi sıradan Python olan bir
     fonksiyon ve tarifi. Fikirler: müşterinin yasak sözcüklerini bulan bir araç; teslim ölçülerini veren bir araç
     (gönderi, hikâye, afiş); bir metnin karakter sayısını sosyal medya sınırına göre denetleyen bir araç.

   Aracını ajana vermeden önce kendin bir kez çağır; sonra `tarifi_goster` ile modelin göreceği tarife bak.
4. **İki istek.** Asistana kendi müşterinle ilgili iki gerçek istek ver; en az birinde senin aracın gereksin. Her
   isteği çalıştırmadan **önce** planını yaz (hangi araçlar, hangi sırayla), sonra `kararlari_goster` ile ajanın
   kararını oku.
5. **Bir brif düzeltmesi.** Aracının adını ve tarifini bilerek belirsiz yap (derste olduğu gibi: `metne_bak`,
   "Metne bakar."); araç listesini ve ajanı yeniden kurup aynı isteği çalıştır. Sonra adı ve tarifi düzelt, bir kez
   daha çalıştır. Model aracı adından da tanır; yalnız tarifi bozarsan fark görmeyebilirsin.

---

## Teslim edeceğin

1. Defterinin kopyası (`odev12-ayse.ipynb`), çıktılarıyla.
2. Bir tablo:

   | İstek | Benim planım | Ajanın seçtiği araçlar (sırayla) |
   |---|---|---|
   | ... | ... | ... |

3. Aracının iki hâli (belirsiz ad ve tarif / düzeltilmiş) ve her biriyle ajanın ne yaptığı, birer cümleyle.
4. **Bir cümle:** Bu asistan kendi müşterinin hangi işini senden alabilir, hangi kararı yine sen vermelisin?

`anahtar.txt`'yi **gönderme**; defterin içine de anahtar yazma.

---

## İstersen (zorunlu değil)

- Bonus'taki yarışma takipçisini kendi alanına göre değiştir: şehrindeki staj ilanları, illüstrasyon yarışmaları.
  Listedeki her bağlantıya tıkla, adı ve son tarihi sitesinden doğrula: model özetlerken uydurabilir. Kaçı gerçekten
  var ve güncel çıktı?
- Ajana bilerek `tool_call_limit=1` ver ve iki araç isteyen bir isteği çalıştır. Cevap neyi eksik bıraktı?
