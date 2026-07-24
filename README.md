# Kıbrıs Sigorta Rehberi

Kuzey Kıbrıs'taki sigorta şirketlerini karşılaştıran çok dilli statik bilgi sitesi.
Sayfalar `content/` içindeki kaynaklardan üretilir; çıktı `dist/` klasörüne yazılır
ve olduğu gibi sunucuya yüklenir. Sitede çalışma anında hiçbir şablon motoru,
veritabanı ya da JavaScript bağımlılığı yoktur.

## Hızlı başlangıç

```bash
pip3 install --user markdown jinja2   # tek seferlik
./yayinla.sh                          # CSS + sayfalar + bağlantı denetimi
```

Çıktı: `dist/`. Yayın adımları için [YAYIN.md](YAYIN.md).

## Yeni blog yazısı

```bash
python3 _build/yeni-yazi.py "Hasar ihbarı nasıl yapılır" --kategori Hasar
```

Dosyayı doldurun, `taslak: evet` satırını silin, `./yayinla.sh` çalıştırın.
Ayrıntı: [YAZI-YAZMA.md](YAZI-YAZMA.md).

## Klasörler

| Yol | Ne işe yarar |
|---|---|
| `site.json` | **Tek yapılandırma.** Alan adı, menü, footer, dil rotaları, sayfa başına yazı. |
| `content/tr/rehber/` | Blog yazıları (`.md` veya `.html`). Her dosya bir yazı. |
| `content/tr/sayfa/` | Statik sayfalar. Klasör yapısı adres yapısıdır. |
| `_build/sablon/` | Sayfa iskeleti, header, footer, yazı ve liste şablonları. |
| `_build/uret.py` | Üretici. `content/` + şablon → `dist/`. |
| `_build/yeni-yazi.py` | Yeni yazı iskeleti oluşturur. |
| `assets/` | CSS ve JS. `tailwind.css` derlenir, `site.css` elle yazılır. |
| `data/` | Şirket verisi ve puanlama betikleri. Siteye yüklenmez. |
| `copy/` | Dört dildeki metin taslakları. Siteye yüklenmez. |
| `dist/` | **Üretilen çıktı.** Elle düzenlenmez, her üretimde silinip yeniden yazılır. |

## Neyi nerede değiştirirsiniz

| İstediğiniz | Dokunacağınız yer |
|---|---|
| Alan adını değiştirmek | `site.json` → `alan_adi` |
| Siteyi aramaya açmak | `site.json` → `yayin.noindex` → `false` |
| Menüye madde eklemek | `site.json` → `menu.tr` |
| Footer bağlantısı | `site.json` → `footer.tr` |
| Sayfa başına yazı sayısı | `site.json` → `yayin.sayfa_basina_yazi` |
| Tüm sayfaların üst/alt bölümü | `_build/sablon/parca/` |
| Blog liste sayfasının düzeni | `_build/sablon/liste.html` |
| Yazı sayfasının düzeni | `_build/sablon/yazi.html` |
| Renk, tipografi, bileşenler | `assets/css/site.css` |
| Şirket tablosu | `data/sirketler.json`, sonra `python3 data/uret-sirketler.py` |

Menüyü, footer'ı veya sayfa iskeletini değiştirdiğinizde **tüm** sayfalar bir sonraki
üretimde güncellenir — kaç yazı olduğu fark etmez.

## Otomatik üretilenler

Bunları elle yazmayın; her üretimde yeniden oluşturulurlar:

- Blog liste sayfası ve sayfalama (`/tr/rehber/`, `/tr/rehber/sayfa/2/` …)
- Konu sayfaları (`/tr/rehber/konu/hasar/`) ve kendi sayfalamaları
- `sitemap.xml`, `robots.txt`, RSS beslemesi (`/tr/rehber/feed.xml`)
- `404.html` ve kök dil yönlendirmesi (`/index.html`)
- Her sayfanın `canonical`, `hreflang`, Open Graph etiketleri
- Yazıların `BlogPosting` şeması ve liste sayfasının `Blog` şeması

## Diller

Yapı dört dili (`tr`, `en`, `ru`, `fa`) destekler; şu an yalnızca **TR** üretiliyor.
`content/en/…` altına içerik eklendiğinde dil değiştirici ve `hreflang` etiketleri
kendiliğinden belirir — var olmayan bir dile bağlantı verilmez. Metin taslakları
`copy/` altında hazır bekliyor.
