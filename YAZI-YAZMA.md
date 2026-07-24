# Yazı yazma kılavuzu

Her blog yazısı `content/tr/rehber/` altında **tek bir dosyadır**. Başlık bloğu
(frontmatter) ve gövdeden oluşur. Head, menü, footer, breadcrumb, tarih, ilgili
yazılar, sitemap kaydı ve şema etiketleri otomatik eklenir — bunları yazmazsınız.

## 1. Dosyayı oluşturun

```bash
python3 _build/yeni-yazi.py "Hasar ihbarı nasıl yapılır" --kategori Hasar
```

Başlıktan adres türetilir: `/tr/rehber/hasar-ihbari-nasil-yapilir/`

## 2. Başlık bloğunu doldurun

```yaml
---
baslik: "Hasar ihbarı nasıl yapılır"      # <title> — site adı sonuna otomatik eklenir
h1: "Hasar ihbarı nasıl yapılır"          # sayfadaki büyük başlık
kisa_baslik: "Hasar ihbarı"               # breadcrumb'da görünen kısa ad (opsiyonel)
aciklama: "Arama sonucunda görünen açıklama, 150-160 karakter."
ozet: "Liste sayfasındaki kartta görünen 2-3 cümle."
giris: "Başlığın altındaki iri paragraf."
kategori: Hasar                           # konu sayfası bundan üretilir
tarih: 2026-07-24                         # sıralama bu alana göre
guncelleme: 2026-07-24                    # "Son güncelleme" ve sitemap lastmod
taslak: evet                              # varsa yazı üretilmez
---
```

Zorunlu olanlar: `baslik`, `aciklama`, `ozet`, `kategori`, `tarih`.

Opsiyonel alanlar: `og_baslik`, `og_aciklama`, `og_gorsel`, `menu`, `url`
(adresi elle belirlemek için), `ceviriler`.

### Kategori

`kategori` yeni bir değer aldığında konu sayfası **kendiliğinden** oluşur:
`Hasar` → `/tr/rehber/konu/hasar/`. Ayrıca bir şey yapmanız gerekmez. Bu yüzden
kategori adlarını tutarlı yazın — "Hasar" ve "hasar" iki ayrı konu sayfası üretir.

### Çeviriler

Yazının başka dillerdeki karşılığı varsa:

```yaml
ceviriler:
  en: /en/guides/how-to-file-a-claim/
  ru: /ru/rukovodstvo/podacha-zayavleniya/
```

Karşı taraftaki sayfa gerçekten üretilmediği sürece bağlantı gösterilmez.

## 3. Gövdeyi yazın

Gövde Markdown'dır:

```markdown
Giriş paragrafı.

## Ana başlık

Metin. **Kalın**, *italik*, [bağlantı](/tr/sigorta/trafik/).

- Madde
- Madde

1. Birinci adım
2. İkinci adım

| Sütun | Sütun |
|---|---|
| Değer | Değer |

> Alıntı ya da vurgulanmış not.
```

Markdown, tasarım sisteminin `.u-md` stillerine bağlanır — başlıklar, listeler,
tablolar, alıntılar ve kod otomatik olarak sitenin tipografisiyle uyumlu çıkar.

### Özel bölüm gerektiğinde: ham HTML

Satır başında `<section>` ile başlayıp satır başında `</section>` ile biten
bloklar Markdown'a girmeden olduğu gibi sayfaya geçer. Zengin, tam genişlikte
bölümler böyle yazılır:

```html
<section class="bg-paper border-t border-line">
  <div class="mx-auto max-w-shell px-[22px] py-12 sm:py-16">
    <div class="max-w-prose">
      <p class="u-eyebrow mb-4">Sıralı liste</p>
      <h2 class="u-display text-[1.75rem] sm:text-[2.25rem] leading-[1.1] mb-8">Olay yerinde</h2>
      <p class="text-[15px] text-muted leading-relaxed">Metin.</p>
    </div>
  </div>
</section>
```

Bir dosyada ikisini istediğiniz sırada karıştırabilirsiniz. Yazının tamamı ham
HTML olacaksa dosyayı `.md` yerine `.html` uzantısıyla kaydedin — mevcut üç yazı
böyle yazılmıştır.

### Sık kullanılan tasarım sınıfları

| Sınıf | Ne yapar |
|---|---|
| `u-display` | Başlık yazı tipi (Inter Tight) |
| `u-lead` | İri giriş paragrafı |
| `u-eyebrow` | Başlık üstündeki küçük etiket |
| `u-cap` | Küçük gri açıklama metni |
| `u-num` | Rakamlar için hizalı sürüm |
| `card` | Kart yüzeyi |
| `arrow` / `arrow--sm` | Ok işaretli bağlantı |
| `badge badge--zorunlu` | Turuncu "zorunlu" rozeti |
| `bg-paper` | Dönüşümlü bölüm zemini |
| `max-w-shell` / `max-w-prose` | Sayfa ve metin genişliği |

Renkler ve yüzeyler `assets/css/site.css` başındaki değişkenlerde tanımlıdır:
iki yüzey (beyaz + `--paper`), tek eylem rengi (`--accent`), tek uyarı rengi
(`--flag`). Yeni renk eklemeyin.

## 4. Sayfaya özel şema (opsiyonel)

Dosyanın herhangi bir yerine `<script type="application/ld+json">` bloğu
yazarsanız `<head>` bölümüne taşınır. `BlogPosting` şeması zaten otomatik
üretildiği için tekrar yazmayın; `FAQPage` gibi ek şemalar için kullanın.

## 5. Yayınlayın

```bash
./yayinla.sh
```

`taslak` satırı duran yazılar üretilmez; çıktıda kaç taslağın atlandığı yazar.

## Kurallar

- Doğrulayamadığınız rakamı yazmayın. Boş bırakın ve neden boş olduğunu söyleyin.
- Türkiye mevzuatını KKTC'ye taşımayın; sitenin ayırt edici yanı bu.
- İç bağlantı verin — ilgili sigorta türü ve metodoloji sayfasına.
- `guncelleme` alanını gerçekten güncellediğinizde değiştirin; sitemap onu kullanır.
