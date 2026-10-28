# Konu 11 — RAG: Belgeye Dayalı Cevap

Dil modeli senin belgeni bilmez: müşterinin marka kılavuzu, ajansın brif arşivi onun eğitim verisinde yok. Bu konuda
modele soru sormadan önce belgede soruya en yakın paragrafları bulup soruyla birlikte gönderiyoruz; model cevabı
belgeye bakarak veriyor. Bu yöntemin adı **RAG** (İngilizce *retrieval-augmented generation*: "bulup getirerek üretmek").
Örnek belge, sessiz çalışma kafemiz **Sayfa Kahve**'nin marka kılavuzu. Aynı soruyu kılavuzsuz ve kılavuzlu soruyor,
cevabı kılavuzda olmayan bir soruda modelin "bilmiyorum" deyip demediğine bakıyor ve sonunda kılavuza göre bir afiş
çizdiriyoruz.

| Klasör / dosya | Ne işe yarıyor |
|---|---|
| `slaytlar.md` | Kavram slaytları; dersin başında gösterilir |
| `ders.ipynb` | Derste birlikte çalıştıracağımız defter: Isınma, Adım 1–7 ve Bonus |
| `alistirma.ipynb` | Derste kendi başına çözeceğin defter: bozuk kodlar, kod okuma ve boşluklu sorular (anahtar istemez, internete çıkmaz) |
| `veri/kilavuz.txt` | Sayfa Kahve'nin marka kılavuzu: her satır bir paragraf, 14 paragraf |
| `rag_araclari.py` | Yardımcı dosya: `vektor_al` (Konu 4), `vektorleri_al` (yeni), `modele_sor` (Konu 5) ve `ciz` (Konu 8) hazır |
| `odevler/odev11.md` | Bu konunun ödevi |
| `ders_notu.md` | Konu notu: adım adım açıklamalar, sık hatalar, kendini dene soruları, sözlükçe |

Defterin çıktıları `ciktilar/` klasörüne yazılır: kılavuzun vektörleri (`kilavuz_vektorleri.json`) ve afişler
(`afis_kilavuzlu.jpg`, Bonus'ta `afis_kilavuzsuz.jpg`). `ciktilar/` depoya girmez.

## Çalıştırma

Yeni kütüphane yok. Yeni konuyu almak için **`gita3111` klasöründe** bir kez:

```
git pull
uv sync
```

Sonra:

1. VS Code'da `ders.ipynb`'yi aç.
2. Sağ üstten çekirdek (kernel) olarak **`.venv`**'i seç.
3. Hücreleri yukarıdan aşağı, **Shift + Enter** ile sırayla çalıştır.

Defterin kopyası `rag_araclari.py` ve `veri/` klasörüyle **aynı klasörde** durmalı; yoksa
`ModuleNotFoundError: No module named 'rag_araclari'` ya da `FileNotFoundError: ... 'veri/kilavuz.txt'` alırsın.

## Anahtar gerekiyor mu?

Isınma anahtarsız; alıştırma defteri de. Adım 1'den sonrası `anahtar.txt` ister (bütün konular için tek dosya, `gita3111`
klasöründe). Defterin tamamı (Bonus hariç) 5 vektör isteği, 4 metin isteği ve 1 görsel isteği gönderir; Bonus'un üç
maddesi birer kez çalıştırılınca 3 vektör, 3 metin ve 1 görsel isteği daha gider. Kılavuzun vektörleri ilk çalıştırmada kaydedilir;
defteri yeniden çalıştırdığında o istek gitmez. Hepsi ücretsiz günlük kotanın küçük bir kısmı. Anahtarın yoksa Adım 1'den
sonrasını hocanın paylaştığı ekrandan izle.

## Güncel kalmak

Yeni materyal geldiğinde `gita3111` klasöründe `git pull` çalıştır. Depodaki bir dosyayı (defter ya da kılavuz) değiştirmek
istersen önce aynı klasörde **yeni bir adla kopyala**, kopyada çalış; böylece `git pull` hiç çakışmaz.
`veri/kilavuz.txt`'yi değiştirdiysen `ciktilar/kilavuz_vektorleri.json`'u da sil: vektörler eski kılavuzdan kalır.

## Defterin bölümleri

| Bölüm | Ne yapılıyor | Anahtar |
|---|---|---|
| Isınma | Elle vektörlerle RAG'in üç adımı, kâğıt üstünde | gerekmez |
| Adım 1 | Hazır araçlar; kılavuzsuz soru: model Sayfa Kahve'yi tanıyor mu? | gerekir |
| Adım 2 | Kılavuzu paragraflara bölmek | gerekmez |
| Adım 3 | 14 paragrafı tek istekte vektöre çevirmek; vektörleri saklamak | gerekir (ilk çalıştırmada) |
| Adım 4 | Soruya en yakın üç paragraf (sen yazarsın) | gerekir |
| Adım 5 | Yönerge şablonu (sen yazarsın); kılavuzsuz ve kılavuzlu cevap | gerekir |
| Adım 6 | `kilavuzda_ara` fonksiyonu; cevabı kılavuzda olmayan bir soru | gerekir |
| Adım 7 | Kılavuzun görsel kuralları; görsel yönergesi; afiş | gerekir |
| Bonus | Kılavuzsuz afiş; kaç paragraf alınmalı; yarım bilgi | gerekir |
