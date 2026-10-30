# Konu 11 Ödevi — Kendi müşterinin hafızası

**Puan yok.** Konu 12'nin başında birkaç arkadaş gösterecek.

Konu 8'de seçtiğin müşteri (öğrenci kulübü, ailenin dükkânı, kendi markan, bir arkadaşının işletmesi) için bir
müşteri hafızası kuruyorsun. Final projende küçük bir RAG adımı zorunlu: bu hafıza o adımın temeli olacak, o yüzden
gerçekten kullanacağın bir müşteri seç.

Bu ödev kendi `anahtar.txt` dosyanı ister. Yaklaşık 10 istek gönderir; günlük ücretsiz kotanın küçük bir parçası.

## 1. Notlarını yaz

`11-rag` klasöründe yeni bir metin dosyası aç: `odev11_notlar.txt`. İçine **en az 8 not** yaz, her not tek satırda,
Sayfa Kahve'nin notlarıyla aynı biçimde: `Kaynak, kanal, tarih: not`.

- Müşterinin istekleri (en az 4): renk, yazı, fotoğraf, yasak sözcükler, teslim biçimi...
- Aldığın eleştiriler (en az 2): jüri, hoca, bir arkadaşın ya da müşterinin kendisi.
- İşle doğrudan ilgisi olmayan bir not (en az 1): ödeme günü, matbaa saati, teslim yeri.
- Her not tek bir şey söylesin. "Bu renk" yerine rengin adını yaz.
- Gerçek bir müşteriyse telefon, adres, fatura bilgisi yazma; notlar modelin sunucusuna gider.

## 2. Hafızanı kur ve soru sor

`ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev11-ayse.ipynb`). Kopyada:

- Isınmadaki `veri/notlar.txt`'yi `odev11_notlar.txt` yap.
- Kendi kılavuzun yoksa Adım 1'de `hafizayi_kur(kilavuz + notlar)` yerine `hafizayi_kur(notlar)` yaz.
- Adım 2'nin ve Adım 3'ün sorularını kendi müşterinin sorularıyla değiştir.

**3 soru** sor: biri cevabı notlarında açıkça olan, biri iki notu birlikte gerektiren, biri cevabı notlarında
**hiç olmayan** bir soru. Her soru için gelen notları ve modelin cevabını kaydet.

## 3. Bir not ekle, cevap değişsin

Müşterinden yeni bir mesaj gelmiş gibi bir not ekle (Adım 4'teki gibi, dosya `odev11_notlar.txt`). Üç sorudan
birini yeniden sor ve cevabın değiştiğini göster.

## Teslim edeceğin

1. `odev11_notlar.txt` (eklediğin not dahil)
2. Defter kopyan, **çıktılarıyla birlikte kaydedilmiş** hâlde
3. **Üç cümle:**
   - Hangi soruda arama doğru notları getirdi, hangisinde kaçırdı?
   - Cevabı notlarında olmayan soruda model "notlarda yok" dedi mi?
   - Not ekleyince cevap nasıl değişti?

`anahtar.txt`'yi **gönderme**; defter kopyanda anahtarını bir hücreye yazmadığından emin ol.

## İstersen (zorunlu değil)

Notlarına bir öncekiyle çelişen bir not ekle (ör. önce "yeşil kullanalım", sonra "yeşili bırakalım"). Aynı soruyu
sor: model hangisine uydu, çelişkiyi fark etti mi? Bir cümle.
