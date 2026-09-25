# GİTA3111 — Ders Öncesi Kurulum Yönergesi

**Bunu ilk dersten ÖNCE yap.** Ders saatinde kurulumla uğraşmayacağız; sadece çalıştığını
kontrol edeceğiz. Toplam süre yaklaşık 30 dakika.

Takıldığın yerde dur, ekran görüntüsü al ve bana yaz. Yarım kalmış kurulumla derse gelmek
sorun değil — hiç denememiş olarak gelmek sorun.

---

## Ne kuracağız?

| Ne | Ne işe yarıyor |
|---|---|
| `uv` | Python'ı ve kullanacağımız kütüphaneleri senin yerine kuran araç |
| Proje klasörü | Dersin tüm dosyalarının duracağı yer |
| VS Code | Kod yazacağın editör (geçen dönemden duruyorsa yeniden kurma) |
| Cloudflare hesabı | Konu 02'den (API ile konuşmak) itibaren kod içinden yapay zekaya bağlanmak için. **Ücretsiz.** |

Python'ı ayrıca kurmana gerek yok — `uv` onu da hallediyor.

---

## Adım 1 — `uv` kurulumu

### Windows

Başlat menüsüne `PowerShell` yaz, aç. Şunu yapıştır ve Enter'a bas:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS

Spotlight'ta (Cmd+Boşluk) `Terminal` yaz, aç. Şunu yapıştır ve Enter'a bas:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Sonra (ikisinde de)

**Terminali kapat, yeniden aç.** Bu önemli — kapatıp açmazsan bilgisayar yeni aracı göremez.

Kontrol et:

```
uv --version
```

Bir sürüm numarası görüyorsan tamam. "command not found" ya da "tanınmıyor" diyorsa:
terminali gerçekten kapatıp açtığından emin ol, olmuyorsa bana yaz.

---

## Adım 2 — Python'ı kur ve proje klasörünü oluştur

Sırayla:

```
uv python install 3.13
uv init gita3111
cd gita3111
uv add matplotlib wordcloud
```

Son komut biraz sürebilir, indirme yapıyor.

> **Klasör yolu uyarısı:** Bu komutları Türkçe karakter (ç, ğ, ı, ö, ş, ü) ve boşluk içermeyen
> bir klasörde çalıştır. Masaüstü genelde uygundur; "Ders Notları/Yapay Zekâ" gibi bir yol
> ilerde sana saatler kaybettirir.

---

## Adım 3 — Test betiğini çalıştır

Ders deposundan `00-hazirlik/ornekler/kurulum_testi.py` dosyasını indir ve `gita3111` klasörünün
içine koy. Sonra:

```
uv run kurulum_testi.py
```

Ekranda şunu görmelisin:

```
KURULUM TAMAM
```

Görmüyorsan betik zaten sana neyin eksik olduğunu yazacak. Çıktının tamamının ekran
görüntüsünü al, derse onunla gel.

---

## Adım 4 — VS Code

Geçen dönemden kuruluysa bir şey yapma. Değilse: https://code.visualstudio.com adresinden indir,
kur, `gita3111` klasörünü aç (File → Open Folder).

---

## Adım 5 — Cloudflare hesabı ve anahtarı

Bunu Konu 02'de (API ile konuşmak) kullanacağız ama şimdi açıyoruz ki sorun çıkarsa çözmek için zamanımız olsun.

**1.** Şu adrese git ve ücretsiz hesap aç:
https://dash.cloudflare.com/sign-up/workers-and-pages

**2.** E-postana gelen doğrulama bağlantısına tıkla.

**3.** Şu adrese git:
https://dash.cloudflare.com/?to=/:account/ai/workers-ai

**4.** **Use REST API** bölümünü aç. Burada iki şey var:
   - **Account ID** — kopyala
   - **Create a Workers AI API Token** düğmesi — tıkla, açılan ekrandaki hazır bilgileri
     değiştirmeden **Create API Token** de, çıkan anahtarı **Copy** ile kopyala

**5.** İkisini birden bilgisayarında bir metin dosyasına kaydet. Örneğin `gita3111` klasörünün
içinde `anahtar.txt`:

```
ACCOUNT_ID = buraya_account_id
API_TOKEN = buraya_anahtar
```

> ### Üç kural
> - Anahtarı **kimseyle paylaşma.** Arkadaşına da gönderme.
> - Anahtarı **ödev teslimine koyma.**
> - Anahtar ekranını **bir kez** gösteriyor; kapatırsan yenisini üretmen gerekir (sorun değil).

> ### Kayıt sırasında kredi kartı isterse
> **Dur ve bana yaz.** Bu dersin tamamı ücretsiz kullanımla tasarlandı; kart istenmesi
> beklenmiyor. İstenirse kurguyu ben değiştiririm — sen kart bilgisi girme.

---

## Derse gelmeden önce kontrol listesi

- [ ] `uv --version` bir sürüm numarası yazıyor
- [ ] `gita3111` klasörüm var, içinde `uv add` ile kütüphaneler kurulu
- [ ] `uv run kurulum_testi.py` → **KURULUM TAMAM** yazdı
- [ ] VS Code kurulu ve `gita3111` klasörünü açabiliyorum
- [ ] Cloudflare hesabım var, Account ID ve anahtarımı bir dosyaya kaydettim

Beş maddeyi de işaretlediysen hazırsın.

---

## Sık karşılaşılan üç sorun

**"uv tanınmıyor / command not found"**
Terminali kapatıp yeniden açmadın. Aç-kapat, tekrar dene.

**`uv add` hata veriyor, internet hatası gibi görünüyor**
Üniversite ağındaysan bazı adresler kapalı olabilir. Telefon internetini paylaşıp tekrar dene.

**Komutlar çalışıyor ama dosyayı bulamıyor diyor**
Muhtemelen yanlış klasördesin. `cd gita3111` yazdığından ve test dosyasını o klasörün **içine**
koyduğundan emin ol.
