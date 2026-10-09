# Konu 0 — Dersin Tanıtımı ve Kurulum

GİTA3111 · Üretken Yapay Zeka ve Programlama
Ahmet Emre Aladağ

-----

## Dönemin haritası

![Birinci yarıda 01–06 kavram konuları, ortada vize, ikinci yarıda 07–12 üretim konuları, sonda final projesi](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/donem_haritasi.png)

- Bu ders GİTA2112'nin devamı: orada kodun temelini attık, burada yapay zekayı **kendi kodumuzdan** kullanacağız
- **Birinci yarı:** bu şeyler nasıl çalışıyor? **İkinci yarı:** onlarla ne üretiyoruz?
- Her konunun sonunda elinde çalışan bir çıktı olacak; hiçbir derste sadece dinlemeyeceğiz

-----

## Her ders aynı sırayla akıyor

![Bir dersin altı bölümü: nabız yoklaması, ödev gösterimi, kavram, birlikte kodlama, kendi başına yazma, toparlama](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/bir_ders.png)

- Ders çevrimiçi: önce slaytlarla kavram, sonra defterde **birlikte** kod
- Ben ekranımda yazarım, sen aynısını **kendi bilgisayarında** yazarsın
- Takıldığında beklemeden **sohbete yaz**; başta küçük bir anket "çalıştırabildim mi?" diye sorar

Bugün farklı: bugün kod yok, kurulumu birlikte göreceğiz.

-----

## Nasıl değerlendirileceksin?

- **Vize %40** — take-home, evde yapılır, **yapay zeka yasak**, derste sözlü teyit var
- **Final projesi %60** — kendi kurduğun üretim aracı + üretim günlüğü + sunum
- **Konu ödevleri: puansız**

Ödevler puansız ama sıra listesi var: herkes dönem boyunca 2-3 kez ekranını paylaşıp
çıktısını gösterecek.

Çalışmayan kodla gelmek sorun değil. Hiç denememiş gelmek sorun.

-----

## Yapay zeka ile kod yazmak (vibecoding)

![Aynı dönem haritası: kavram konularında serbest ama anlamadan geçme, vizede yasak, üretim konularında ve finalde serbest ve bekleniyor](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/yapay_zeka_kurali.png)

- **Vizede yasak:** ölçtüğümüz şey senin kendi programlama becerin
- **Kavram konularında serbest:** ama vizede tek başına yazacaksın; aracın yazdığını anlamadan geçmek kendi ayağına sıkmak
- **Üretim konularında ve finalde serbest ve bekleniyor:** kullandığın her yeri üretim günlüğüne yaz

Sohbete yaz: geçen dönem Antigravity'yle ne ürettin? Tek cümle.

-----

## Bu dersten sonra evde: kurulum

![git, uv, VS Code ve Cloudflare'in gita3111 klasöründe buluşması](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/kurulum_haritasi.png)

- Gelecek dersten (Konu 01) itibaren her derste kod çalıştıracağız; önce bu dört şey kurulu olmalı
- Adımları şimdi **birlikte göreceğiz**; kurulumu **evde**, slaytlara değil **yazılı yönergeye** bakarak yapacaksın: `00-hazirlik/kurulum-yonergesi.md` (yaklaşık 30 dakika)
- Gelecek dersin başında herkesin kurulumunu **birlikte kontrol edeceğiz**

Sohbete yaz: Windows mu kullanıyorsun, macOS mu?

-----

## Önce terminal: üç komut yeter

![Klasör basamakları: gita3111'de duran terminal, cd ile aşağı, cd .. ile yukarı, pwd ile konumu yazdırma](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/terminal_klasor.png)

```text
cd klasor_adi      bir klasörün içine gir
cd ..              bir üst klasöre çık
pwd                neredeyim? (PowerShell'de de aynı)
```

- **Terminali açmak:** Windows'ta Başlat → `PowerShell`; macOS'ta Cmd+Boşluk → `Terminal`
- Bu dönemin en sık hatası "yanlış klasördeyim" olacak; `pwd` senin pusulan

-----

## Adım 1 — uv kurulumu

**uv ne?** Python'ı ve dersin **kütüphanelerini** (başkalarının yazdığı hazır kod paketleri,
örneğin kelime bulutu çizen `wordcloud`) senin yerine kuran araç. Python'ı ayrıca kurmana gerek yok.

**Windows** (PowerShell):

```text
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS** (Terminal):

```text
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Sonra **terminali kapat ve yeniden aç**, ve kontrol et:

```text
uv --version
```

Bir sürüm numarası görüyorsan tamam. "tanınmıyor" ya da "command not found" diyorsa
terminali gerçekten kapatıp açmamışsındır.

-----

## git ne işe yarıyor?

![1. derste git clone ile depo bir kez iner; sonraki derslerde git pull yalnızca yeni konuyu getirir](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/clone_pull.png)

Ders materyali bir **depoda** duruyor: github.com/aladagemre/gita3111

- `git clone` → dönemde **bir kez**: depoyu bilgisayarına indirir
- `git pull` → **her dersten önce**: yalnızca yeni ve değişen dosyaları getirir
- Yeni konular geldikçe depoya ekliyorum; klasörü baştan indirmen gerekmiyor

-----

## Adım 2 — git kurulumu

Önce kurulu mu diye bak: `git --version`. Sürüm numarası çıkarsa bu adımı atla.

**Windows:**

```text
winget install --id Git.Git -e
```

`winget` tanınmıyorsa git-scm.com/download/win adresinden indir; kurulum ekranlarında
hiçbir şeyi değiştirmeden **Next** de.

**macOS:** `git --version` yazınca "geliştirici araçlarını yüklemek ister misin?" diye
bir pencere açılır. **Yükle** de.

İkisinde de iş bitince **terminali kapat, yeniden aç.**

-----

## Adım 3 — Depoyu indir

Masaüstüne geç ve depoyu indir:

```text
cd Desktop
git clone https://github.com/aladagemre/gita3111.git
```

Masaüstünde artık `gita3111` adında bir klasör var.

**Klasör yolu uyarısı:**
- Yolda **Türkçe karakter** (ç, ğ, ı, ö, ş, ü) ve **boşluk** olmasın
- "Ders Notları/Yapay Zekâ" gibi bir yol ileride saatlerini yer
- OneDrive'lı Windows'larda Masaüstü yolu uzun olabilir; sorun çıkarsa `C:\gita3111` gibi kısa bir yer seç

-----

## Deponun içi

![gita3111 klasör ağacı: pyproject.toml, .venv, anahtar.txt ve konu klasörleri; 01 klasörünün içinde ders.ipynb, alistirma.ipynb, ders_notu.md, veri ve odevler](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/depo_agaci.png)

- Her konu **kendi klasöründe**; baştaki numara hafta değil **sıra**
- Her konu klasöründe aynı düzen: ders defteri, alıştırma defteri, konu notu, veri, ödev
- Turuncular depoda yok, **sende oluşur**: `git pull` onlara dokunmaz

-----

## Depo tek bir uv projesi

![pyproject.toml'daki Python sürümü ve kütüphane listesi, uv sync ile .venv ortamına dönüşür](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/uv_proje.png)

- `pyproject.toml` dersin **hangi Python'u** ve **hangi kütüphaneleri** kullandığını yazar
- `uv sync` bu listeyi okur, eksikleri kurar ve `gita3111` içinde **tek bir** `.venv` klasörü oluşturur
- `.venv` = **ortam**: dersin Python'unun ve kütüphanelerinin kurulu durduğu klasör
- Sen hiçbir zaman "şu kütüphaneyi kur" diye uğraşmazsın

Tek şart: komutu `gita3111` klasörünün ya da bir konu klasörünün **içinden** ver.

-----

## Adım 4 — Kurulumu test et

```text
cd gita3111/00-hazirlik
uv run ornekler/kurulum_testi.py
```

İlk çalıştırmada uv doğru Python sürümünü ve kütüphaneleri indirir; birkaç dakika
sürebilir. Ekranda şunu görmelisin:

```text
[OK  ] Doğru klasördesin — şu an: .../Desktop/gita3111/00-hazirlik
[OK  ] Python sürümü — bulunan: 3.13
[OK  ] matplotlib kurulu
[OK  ] wordcloud kurulu
[OK  ] ipykernel kurulu
[OK  ] Grafik üretimi — kurulum_testi_ciktisi.png oluştu
[ATLA] Cloudflare bağlantısı — anahtar.txt yok (Konu 02'ye, API dersine kadar sorun değil)
----------------------------------------
KURULUM TAMAM
```

**KURULUM TAMAM** görmüyorsan betik neyin eksik olduğunu zaten yazıyor. Çıktının ekran
görüntüsünü al, derse onunla gel.

Sohbete yaz: aynı komutu bir üstteki `gita3111` klasöründe yazsan ne olur?

-----

## Yanlış klasörden çalıştırırsan

`gita3111` klasöründe durup aynı komutu yazarsan:

```text
error: Failed to spawn: `ornekler/kurulum_testi.py`
  Caused by: No such file or directory (os error 2)
```

`ornekler` klasörü `00-hazirlik`'in içinde; `gita3111`'de öyle bir klasör yok.

- **"No such file or directory"** → büyük ihtimalle yanlış klasördesin
- **"No module named ..."** → `gita3111`'in dışındasın ya da defterde `.venv` seçili değil
- Önce `pwd` yaz, nerede olduğuna bak

Hatanın sebebi çoğu zaman kodda değil, **nerede durduğunda.**

-----

## Önemli kural: depo dosyasını değiştirmeden önce kopyala

Dönem boyunca kuralımız bu:

- Depodaki bir dosyayı değiştireceksen önce **aynı klasörde yeni bir adla kopyala**
- Örnek: `ilk_defter.ipynb` → `benim_defterim.ipynb`, `alistirma.ipynb` → `benim_alistirmam.ipynb`
- Sonra kopyada çalış

**Neden?** `git pull` senin adını verdiğin dosyalara hiç dokunmaz. Ama depodaki bir
dosyayı değiştirdiysen ve ben de o dosyayı güncellediysem, `git pull` durur (çözümü sondaki Ek slaytında).

-----

## Adım 5 — VS Code ve defterler

Bu dönem kodu **defterlerde** (notebook, `.ipynb`) çalıştıracağız: kod küçük kutulara
(**hücre**) bölünmüş; her hücreyi ayrı çalıştırıp sonucunu hemen altında görürsün.

- VS Code yoksa: code.visualstudio.com → indir → kur
- VS Code'da sol menüden **Extensions** → **Python** ve **Jupyter** eklentilerini kur (ikisi de Microsoft'un)
- **File → Open Folder** ile `gita3111` klasörünü aç

VS Code'un içinde terminal de var: **Terminal → New Terminal**. Bu terminal
**zaten `gita3111` klasöründe** açılır; dönem boyunca komutları buradan yazmak en kolayı.

-----

## İlk defterin

![ilk_defter.ipynb'deki grafik hücresi ve çalıştırınca altında çıkan çubuk grafik](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/ilk_defter.png)

- VS Code'un terminalinde `uv sync` yaz (ortam hazır olsun)
- `00-hazirlik/ilk_defter.ipynb`'i aç; sağ üstte **Select Kernel** → **Python Environments** → `.venv`
- **Çekirdek** (kernel) = defterin kodu çalıştırdığı Python; bu dönem her defterde `.venv`'i seçeceksin
- Önce defteri `benim_defterim.ipynb` adıyla kopyala; kopyada turuncu satırları kendi verinle değiştir, **Shift + Enter**

-----

## Adım 6 — Cloudflare hesabı

Konu 02'de kodumuzdan yapay zeka modellerine bağlanacağız. Hesabı **şimdi** açıyoruz
ki sorun çıkarsa çözmeye zamanımız olsun.

1. dash.cloudflare.com/sign-up/workers-and-pages adresinde ücretsiz hesap aç
2. E-postana gelen doğrulama bağlantısına tıkla
3. dash.cloudflare.com/?to=/:account/ai/workers-ai adresine git
4. **Use REST API** bölümünü aç:
   - **Account ID**'yi kopyala
   - **Create a Workers AI API Token** → hazır bilgileri değiştirmeden **Create API Token** → **Copy**

**Kredi kartı isterse dur ve bana yaz.** Bu dersin tamamı ücretsiz kullanımla
tasarlandı; kart bilgisi girme.

-----

## Anahtarı nereye kaydedeceksin?

`gita3111` klasörünün içinde, konu klasörlerinin **yanında**, `anahtar.txt` adlı tek
bir dosya:

```text
ACCOUNT_ID = buraya_account_id
API_TOKEN = buraya_anahtar
```

- Bütün konuların kodu anahtarı **buradan** okur
- Bu dosya depoya hiçbir zaman gönderilmez; `git pull` da ona dokunmaz

**Üç kural:**
- Anahtarı **kimseyle paylaşma**, arkadaşına da gönderme
- Anahtarı **ödev teslimine koyma**
- Anahtar ekranı **bir kez** görünür; kapatırsan yenisini üretirsin (sorun değil)

Anahtarı kaydettikten sonra kurulum testini bir kez daha çalıştır: Cloudflare satırı da
**OK** olmalı.

-----

## Güvenlik: komutu sen onayla

Yapay zeka destekli kod aracı (Antigravity gibi) terminalde kendi başına komut çalıştırabilir.

- Aracın komutları **onaysız çalıştırmasını kapat**
- Her komutu **okuyup sen onayla**
- Araç `anahtar.txt` dosyanı okuyup bir yere gönderebilir; bunu durduran şey senin onayın

-----

## Gelecek dersten önce kontrol listesi

- [ ] `uv --version` ve `git --version` birer sürüm numarası yazıyor
- [ ] `git clone` ile indirdiğim `gita3111` klasörüm var
- [ ] `00-hazirlik` içinde `uv run ornekler/kurulum_testi.py` → **KURULUM TAMAM**
- [ ] VS Code'da `ilk_defter.ipynb` defterini açıp `.venv` çekirdeğiyle çalıştırdım, kendi verimle grafik çizdim
- [ ] Cloudflare hesabım var; Account ID ve anahtarım `gita3111/anahtar.txt` dosyasında

Beşi de tamamsa hazırsın. Gelecek dersin başında kurulum testini birlikte bir kez
daha çalıştıracağız; herkesin ekranında **KURULUM TAMAM** görmeden kelime bulutuna
geçmeyeceğiz.

-----

## Her dersten önce: gir, çek, kur, aç

![Dört adım: VS Code'da gita3111'i açıp terminali aç, git pull, uv sync, ders.ipynb'i .venv çekirdeğiyle aç](https://raw.githubusercontent.com/aladagemre/gita3111/main/00-hazirlik/gorseller/ders_ritmi.png)

VS Code'un terminalinde:

```text
git pull
uv sync
```

Bu dönemin ritmi bu. Gelecek ders kelime bulutuyla başlıyoruz.

Sondaki iki **Ek** slaytı derste anlatılmaz; evde takılırsan bak.

-----

## Ek — git pull takılırsa

Şu hatayı görürsen:

```text
error: Your local changes to the following files would be overwritten by merge
```

bir depo dosyasını değiştirmişsin demektir. Çözüm üç adım:

1. Değiştirdiğin dosyayı **yeni bir adla kopyala** (emeğin kaybolmasın)
2. Depo dosyalarını ilk hâline döndür:

```text
git restore .
```

3. Tekrar dene:

```text
git pull
```

Senin oluşturduğun dosyalar (kopyalar, üretilen görseller, `anahtar.txt`) bu işlemden
etkilenmez.

-----

## Ek — Sık karşılaşılan sorunlar

| Belirti | Sebep | Çözüm |
|---|---|---|
| `uv` / `git` tanınmıyor | Kurulumdan sonra terminal yenilenmedi | Terminali kapat, yeniden aç |
| İnternet hatası (`uv sync`, `git clone`) | Üniversite ağı bazı adresleri kapatıyor | Telefon internetini paylaşıp tekrar dene |
| "No such file or directory" | Yanlış klasördesin | `pwd` ile bak, doğru klasöre `cd` ile gir |
| "Repository not found" | Depo adresi yanlış yazıldı | Adresi kopyala-yapıştır yap |
| Defterde **Select Kernel** listesinde `.venv` yok | `uv sync` çalıştırılmadı ya da VS Code'da alt klasör açıldı | `gita3111` klasöründe `uv sync`; VS Code'da `gita3111` klasörünü aç, listeyi yenile |
| Cloudflare satırı HTTP 401 | Token yanlış kopyalandı | Yeni token üret, `anahtar.txt`'ye yapıştır |
| Cloudflare satırı HTTP 403 | Token'ın izinleri eksik | Token'ı hazır bilgileri değiştirmeden yeniden üret |

Listede olmayan bir şey görürsen: ekran görüntüsü, bana mesaj.
