# KKTC Sigorta Merkezi

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
| Menüye madde eklemek | `site.json` → `menu.tr` (EN için `menu.en`) |
| Footer bağlantısı | `site.json` → `footer.tr` |
| Şablondaki sabit metin | `site.json` → `metinler.<dil>` |
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

Yapı dört dili (`tr`, `en`, `ru`, `fa`) destekler; şu an **TR ve EN** üretiliyor.
RU ve FA'nın metin taslakları `copy/` altında hazır bekliyor.

Dil değiştirici ve `hreflang` etiketleri yalnızca **üretilmiş** adresleri gösterir —
var olmayan bir dile bağlantı verilmez, o dilin içeriği eklendiği anda bağlantılar
kendiliğinden belirir.

**Yeni bir dil açarken sıra şudur.** İlk üç adım atlanırsa üretici durur ya da
sayfa yanlış dilde çıkar:

1. `site.json` → `metinler.<dil>` — şablonların sabit arayüz metinleri (buton,
   `aria-label`, sayfalama, liste sayfasının alt blokları). **Eksikse üretim durur.**
2. `site.json` → `menu.<dil>`, `footer.<dil>` — yalnızca üretilmiş adresler yazılır.
3. `site.json` → `blog.<dil>` — o dilde rehber yazısı yayımlanacaksa gerekir.
4. `content/<dil>/sayfa/` ve `content/<dil>/rehber/` altına içerik.
5. Yazıların çeviri eşleri **tek yerde** durur: TR dosyasının `ceviriler` alanında.
   Karşı taraf yazmasa da hreflang iki yönlü kurulur.

Ayrıntılı gerekçe ve yayın sırası: `copy/04-dil-katmani.md`.
