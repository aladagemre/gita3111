# Konu 12 Ödevi — Ajanına yeni bir yetenek

**Puan yok.** Konu 13'ün başında sıradaki arkadaşlar gösterecek. Ajan final projesi için **zorunlu değil**; bu ödev,
projende kullanmak istersen elinde çalışan bir örnek olsun diye.

Bu ödev kendi `anahtar.txt` dosyanı ister (Konu 2). Bir ajan çalıştırması modele yaklaşık 2–4 istek gönderir; görsel
çizen her araç çağrısı ayrıca bir görsel (yaklaşık 58 neuron). Aşağıdaki adımların tamamı yaklaşık 20 model isteği ve en
fazla 6 görsel; günlük ücretsiz kotanın %10'undan az.

---

## Ne yapacaksın?

1. `ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev12-ayse.ipynb`). Adım 1'in ve Adım 5'in bütün
   hücrelerini, sonra Adım 6'nın ilk üç kod hücresini çalıştır (ajanı kurar, bir afiş çizer, `kararlari_goster`'i
   tanımlar). Adım 2–4'ü atlayabilirsin.
2. **Kendi aracın.** Defterin sonuna yeni bir hücre aç ve kendi tasarladığın bir araç yaz. Fikirler:
   - `yasak_sozcuk_bul(metin: str) -> str`: alıştırmanın Ek sorusu 1; bir metinde kılavuzun yasakladığı sözcükleri bulur.
   - `renk_kontrol(yonerge: str) -> str`: bir görsel yönergesinde kılavuzun yasakladığı renkler (`red`, `orange`) geçiyor mu?
   - `slogan_yaz`'ın başka bir hâli: İngilizce slogan, iki satırlık açıklama, bir gönderi metni.
   - Kendi final projene uygun bir araç.

   Aracın üç parçası eksiksiz olsun: **tür ipuçları** (`: str`, `-> str`), **docstring** (ne yapar, içinde ne var, ne
   zaman seçilmeli, bilgilere ne yazılmalı) ve **`return`** (modele giden sonuç). `tarifi_goster(araci_adi)` ile
   modelin göreceği tarife bak.
3. **Ajan.** Aracını listeye ekleyip ajanı kur. Sınırı işin büyüklüğüne göre seç (ör. 4):
   ```
   araclar = [afis_ciz, fotograf_duzenle, kilavuzda_ara, senin_aracin]
   ajan = Agent(model=model, tools=araclar, tool_call_limit=4, telemetry=False)
   ```
4. **Plan, sonra çalıştır.** En az **dört** istek yaz: en az biri senin aracını gerektirsin, en az biri iki ya da daha
   çok aracı bir sırayla gerektirsin, en az biri bilerek muğlak olsun. Çalıştırmadan **önce** her istek için planını yaz
   (Isınma'daki gibi: hangi araçlar, hangi sırayla). Sonra her isteği ayrı bir hücrede çalıştır:
   ```
   cevap = ajan.run("...")
   kararlari_goster(cevap)
   ```
5. **Tarifi boz, düzelt.** Senin aracını gerektiren isteği seç. Aracının docstring'ini bilerek tembel bir tek cümleye
   indir; fonksiyonu, araç listesini ve ajanı yeniden kur; isteği yeniden çalıştır. Sonra tarifi düzelt ve bir kez daha
   çalıştır. Üç sonucu (ilk, bozuk, düzeltilmiş) not et.
6. **Kota.** Bir çalıştırma için Bonus 1'deki iki hücreyi çalıştır: kaç istek, kaç belirteç, yaklaşık kaç neuron?

**İpucu (kotanı korumak için):** görsel çizdirmeden yalnızca kararları denemek istersen `afis_ciz`'in içini geçici
olarak değiştir: `print` satırından sonra yalnızca `return "Prova: görsel çizilmedi."` kalsın, docstring aynı kalsın.
Model aracın içini görmez: ilk kararını yalnızca istek ve tarifler belirler, aracın sonucunu ise farklı görür. Denemeler bitince asıl
hâline döndür.

---

## Teslim edeceğin

1. Defterinin kopyası (`odev12-ayse.ipynb`), çıktılarıyla.
2. Bir tablo: her istek, senin planın, modelin çağırdığı araçlar (sırayla).

   | İstek | Benim planım | Modelin kararı |
   |---|---|---|
   | ... | ... | ... |

3. Aracının üç tarifi (ilk, bozuk, düzeltilmiş) ve her biriyle model ne yaptı.
4. **İki cümle:** Model nerede senin planından ayrıştı? Tarifte neyi değiştirdin ve işe yaradı mı?
5. **Bir cümle:** Kendi final projende sırası baştan belli olmayan bir iş var mı, yoksa Konu 10'daki gibi bir hat yeter mi?

`anahtar.txt`'yi **gönderme**; defterin içine de anahtar yazma.

---

## İstersen (zorunlu değil)

- Bonus'taki `instructions`'ı kendi aracın için dene: kuralı aracın tarifinden çıkarıp ajanın genel brifine yaz. Model
  aynı kararı veriyor mu?
- Sınırı bilerek 1 yap ve iki araç isteyen bir isteği çalıştır. `kararlari_goster` ve `cevap.content` ne diyor?
