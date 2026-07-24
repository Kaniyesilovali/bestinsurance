# Yayın kılavuzu

Site statik HTML'dir. Sunucuda PHP, Node ya da veritabanı gerekmez —
`dist/` klasörünün **içindekiler** sunucunun kök dizinine kopyalanır.

## Her yayında

```bash
./yayinla.sh
```

Bu komut sırayla: Tailwind CSS'i derler, şirket tablosunu verisinden yeniler,
sayfaları üretir ve kırık iç bağlantı raporu verir. Çıktı `dist/`.

Rapor "kırık iç bağlantı yok" demeden yüklemeyin.

## İlk yayın öncesi kontrol listesi

### 1. Alan adını yazın

`site.json` → `alan_adi`. Placeholder olan `https://ORNEK-ALAN-ADI.com` değerini
gerçek adresle değiştirin (sonda eğik çizgi olmadan):

```json
"alan_adi": "https://kibrissigortarehberi.com",
```

Bu tek satır `canonical`, `hreflang`, Open Graph, `sitemap.xml` ve `robots.txt`
içindeki tüm adresleri düzeltir.

### 2. Aramaya açın

`site.json` → `yayin.noindex` değerini `false` yapın.

`true` iken her sayfaya `noindex` eklenir, `robots.txt` her şeyi kapatır ve
`sitemap.xml` üretilmez. Alan adı gerçek değerini almadan bunu açmayın —
yanlış adresle indekslenen sayfaları geri almak zordur.

### 3. Eksik metinleri tamamlayın

Şu sayfalarda `<!-- DOLDURULACAK: … -->` notları var:

- `content/tr/sayfa/hakkimizda.md` — yayıncı kimliği, gelir modeli
- `content/tr/sayfa/iletisim.md` — e-posta adresleri, yanıt süresi
- `content/tr/sayfa/yasal-uyari.md` — yayıncı unvanı, güncelleme tarihi
- `content/tr/sayfa/gizlilik.md` — ölçümleme aracı, çerez durumu, tarih

Kalan notları bulmak için:

```bash
grep -rn "DOLDURULACAK" content/
```

Bu notlar HTML yorumu olduğu için sayfada görünmez, ama kaynak koda bakan
herkes görür. Yayından önce hepsini temizleyin.

### 4. Şirket profil sayfaları

Şirket tablosundaki 39 ad `/tr/sirketler/<slug>/` adresine bağlanıyor ama bu
sayfalar henüz yok — `./yayinla.sh` çıktısındaki kırık bağlantılar bunlar.
Ya sayfalar üretilmeli ya da tablodaki bağlantılar kaldırılmalı.

### 5. Favicon

Kök dizine `favicon.ico` veya `favicon.svg` koyun; üretim sırasında `dist/`
içine kopyalanır.

## Yükleme

### FTP / cPanel Dosya Yöneticisi

`dist/` klasörünün **içeriğini** (klasörün kendisini değil) `public_html`
veya `www` dizinine yükleyin. Eski dosyaların üzerine yazın.

Yapı şöyle olmalı:

```
public_html/
  index.html
  404.html
  robots.txt
  sitemap.xml
  assets/
  tr/
```

### rsync (SSH varsa)

```bash
rsync -avz --delete dist/ kullanici@sunucu:/var/www/html/
```

`--delete` sunucudaki artık dosyaları da temizler — ilk seferde `--dry-run`
ekleyerek ne olacağını görün.

### Netlify / Cloudflare Pages

`dist/` klasörünü panele sürükleyin. Bir depo bağlıyorsanız:
build komutu `./yayinla.sh`, yayın dizini `dist`.

## Sunucu ayarları

**404 sayfası.** Apache için `dist/` içine bir `.htaccess` koyun:

```apache
ErrorDocument 404 /404.html
```

Nginx: `error_page 404 /404.html;`

Netlify ve Cloudflare Pages `404.html` dosyasını kendiliğinden kullanır.

**Adres sonundaki eğik çizgi.** Tüm iç bağlantılar `/tr/rehber/x/` biçimindedir
ve klasör içinde `index.html` bulunur; standart kurulumlar bunu sorunsuz sunar.

## Yayın sonrası

1. `https://alan-adiniz.com/sitemap.xml` açılıyor mu?
2. `robots.txt` içinde `Disallow: /` **kalmamış** olmalı.
3. Google Search Console'a siteyi ekleyip sitemap'i gönderin.
4. Birkaç sayfanın kaynağında `ORNEK-ALAN-ADI` kalmadığını doğrulayın:

```bash
grep -rl "ORNEK-ALAN-ADI" dist/ || echo "temiz"
```

## Sorun giderme

| Belirti | Nedeni |
|---|---|
| `Eksik paket: markdown` | `pip3 install --user markdown jinja2` |
| Sayfalar biçimsiz görünüyor | `assets/css/tailwind.css` derlenmemiş — `./yayinla.sh` çalıştırın |
| Yeni yazı görünmüyor | Frontmatter'da `taslak` satırı duruyor olabilir |
| Bir sayfa hiç üretilmiyor | `content/` altında `.md` veya `.html` uzantısı olmalı |
| Değişiklik yansımıyor | `dist/` yerine kaynak dosyayı düzenlediğinizden emin olun; `dist/` her üretimde silinir |
