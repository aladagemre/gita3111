# Konu 4 Ödevi — Kendi kelimelerinin haritası

**Puan yok.** Konu 5'in başında sıradaki arkadaşlar gösterecek.

## Yapılacak

`ders.ipynb`'yi aynı klasörde yeni bir adla kopyala (ör. `odev4-ayse.ipynb`), kopyayı aç.
Depodaki dosyaya dokunmazsan `git pull` çakışmaz. Bu ödev kendi `anahtar.txt` dosyanı
ister.

1. **Kelimelerini seç.** Kendi ilgi alanından **20 kelime**: tasarım, müzik, yemek,
   oyun, sinema — fark etmez. İpucu: iki ya da üç gruptan seç (ör. 10 müzik türü,
   10 duygu); harita okumak kolaylaşır. Birkaç tane de "nereye düşecek, merak ediyorum"
   dediğin kelime koy.
2. **Adım 5'teki listeyi değiştir.** `kelimeler = [...]` listesindeki 24 kelimeyi sil,
   yerine kendi 20 kelimeni yaz: her kelime tırnak içinde, aralarında virgül.
3. **Sırayla çalıştır.** Hücreleri baştan Adım 7'nin sonuna kadar sırayla çalıştır.
   Adım 6'da `hedef = "kafe"` satırındaki kelimeyi kendi listenden bir kelimeyle değiştir
   (yoksa `KeyError: 'kafe'` alırsın).
4. **Haritayı kaydet.** Adım 7'nin son hücresinde `plt.show()` satırının **üstüne** şu
   satırı ekle ve hücreyi yeniden çalıştır:

   ```py
   plt.savefig("harita.png")
   ```

   `harita.png` defterin yanına, konu klasörüne kaydedilir.

## Teslim edeceğin

- `harita.png`
- 20 kelimelik listen
- **Tek cümle:** beklemediğin hangi iki kelime yan yana düştü? Neden olabilir?

## Dikkat

Harita bir özet; yüzlerce sayıyı 2'ye indiriyor. Yan yana düşen iki kelimeyi gördüğünde
Adım 8'deki gibi `benzerlik` ile asıl sayıya da bak. Haritada yakın ama sayıda uzaksa
bunu da yaz — bu da bir bulgu.

`anahtar.txt`'yi gönderme.

## İstersen (zorunlu değil)

Listende iki zıt anlamlı kelime olsun (ör. "gürültü" ve "sessizlik"). Haritada uzak mı
düştüler, yakın mı? Ders notundaki "Benzer, eşanlamlı demek değil" bölümüne bak.
