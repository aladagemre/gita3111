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
| `git` | Ders deposunu bilgisayarına indiren ve her yeni konu eklendiğinde güncelleyen araç |
| `gita3111` klasörü | Ders deposunun bilgisayarındaki kopyası; dersin tüm dosyaları burada |
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

## Adım 2 — `git` kurulumu

Önce kurulu mu diye bak:

```
git --version
```

Bir sürüm numarası görüyorsan bu adımı atla.

- **Windows:** PowerShell'e şunu yapıştır, sonra **terminali kapatıp yeniden aç**:
  ```
  winget install --id Git.Git -e
  ```
  `winget` tanınmıyorsa https://git-scm.com/download/win adresinden indirip kur; kurulum
  ekranlarındaki hazır seçenekleri değiştirmeden **Next** de.
- **macOS:** `git --version` yazınca "komut satırı geliştirici araçlarını yüklemek ister
  misin?" diye bir pencere açılır. **Yükle** de, bitince terminali kapatıp yeniden aç.

---

## Adım 3 — Ders deposunu indir

Deponun duracağı yere geç (Masaüstü uygundur) ve depoyu indir:

```
cd Desktop
git clone https://github.com/aladagemre/gita3111.git
```

Artık Masaüstünde `gita3111` adında bir klasör var. Dersin tüm dosyaları burada; her konu
kendi klasöründe (`00-hazirlik`, `01-veri-ve-kelime-bulutu`, …).

> **Klasör yolu uyarısı:** Depoyu Türkçe karakter (ç, ğ, ı, ö, ş, ü) ve boşluk içermeyen bir
> klasöre indir. Masaüstü genelde uygundur; "Ders Notları/Yapay Zekâ" gibi bir yol ilerde sana
> saatler kaybettirir. (OneDrive kullanan Windows'larda Masaüstü yolu uzun olabilir; sorun
> çıkarsa `C:\gita3111` gibi kısa bir yer seç.)

### Dönem boyunca: depoyu güncel tut

Yeni konular geldikçe depoya ekleyeceğim. Her dersten önce `gita3111` klasörünün içinde:

```
git pull
```

Bu komut yalnızca yeni ve değişen dosyaları indirir.

> **Depodaki bir dosyayı değiştireceksen önce kopyala.** Örneğin alıştırmayı doldurmadan önce
> `sinif_alistirmasi.py` dosyasını aynı klasörde `benim_alistirmam.py` adıyla kopyala ve
> kopyada çalış. Kendi adını verdiğin dosyalara `git pull` hiç dokunmaz.
>
> `git pull` "your local changes would be overwritten" diye hata verirse bir depo dosyasını
> değiştirmişsin demektir. O dosyayı yeni bir adla kopyala, sonra şunları çalıştır:
> ```
> git restore .
> git pull
> ```

---

## Adım 4 — Kurulumu test et

Her konu klasörü kendi başına bir **uv projesi**: içindeki `pyproject.toml` dosyası o konunun
hangi Python sürümünü ve hangi kütüphaneleri kullandığını yazar. Komutları hep **konunun
klasörünün içinden** çalıştırırız:

```
cd gita3111/00-hazirlik
uv run ornekler/kurulum_testi.py
```

İlk çalıştırmada `uv` doğru Python sürümünü ve kütüphaneleri kendisi indirir; bu birkaç
dakika sürebilir. Ekranda şunu görmelisin:

```
KURULUM TAMAM
```

Görmüyorsan betik zaten sana neyin eksik olduğunu yazacak. Çıktının tamamının ekran
görüntüsünü al, derse onunla gel.

> **Yeni bir konuya başlarken:** o konunun klasörüne gir ve dersten önce bir kez `uv sync`
> çalıştır. Kütüphaneler önceden inmiş olur, derste beklemezsin.
> ```
> cd ../01-veri-ve-kelime-bulutu
> uv sync
> ```

---

## Adım 5 — VS Code

Geçen dönemden kuruluysa bir şey yapma. Değilse: https://code.visualstudio.com adresinden indir,
kur, `gita3111` klasörünü aç (File → Open Folder).

---

## Adım 6 — Cloudflare hesabı ve anahtarı

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

**5.** İkisini birden `gita3111` klasörünün içinde (konu klasörlerinin yanında, tek bir
tane) `anahtar.txt` adlı bir metin dosyasına kaydet. Bütün konuların kodu anahtarı buradan
okur. Bu dosya depoya hiçbir zaman gönderilmez; `git pull` da ona dokunmaz.

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

- [ ] `uv --version` ve `git --version` birer sürüm numarası yazıyor
- [ ] `git clone` ile indirdiğim `gita3111` klasörüm var
- [ ] `00-hazirlik` klasörünün içinde `uv run ornekler/kurulum_testi.py` → **KURULUM TAMAM** yazdı
- [ ] VS Code kurulu ve `gita3111` klasörünü açabiliyorum
- [ ] Cloudflare hesabım var, Account ID ve anahtarım `gita3111/anahtar.txt` dosyasında

Beş maddeyi de işaretlediysen hazırsın.

---

## Sık karşılaşılan sorunlar

**"uv tanınmıyor / command not found"**
Terminali kapatıp yeniden açmadın. Aç-kapat, tekrar dene.

**`uv run` / `uv sync` ya da `git clone` hata veriyor, internet hatası gibi görünüyor**
Üniversite ağındaysan bazı adresler kapalı olabilir. Telefon internetini paylaşıp tekrar dene.

**Komutlar çalışıyor ama dosyayı bulamıyor diyor**
Muhtemelen yanlış klasördesin. Komutları konunun klasörünün **içinden** çalıştırıyoruz:
`cd gita3111/00-hazirlik` yazdığından emin ol. Nerede olduğunu görmek için Windows'ta `cd`,
macOS'ta `pwd` yaz.

**`git clone` "Repository not found" ya da kullanıcı adı/şifre soruyor**
Depo adresini yanlış yazmış olabilirsin; yukarıdan kopyala-yapıştır yap. Yine olmuyorsa bana yaz.
