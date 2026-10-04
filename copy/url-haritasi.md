# URL haritası — TR · EN

Bu tablo hreflang etiketlerinin, dil değiştiricinin ve sitemap'in tek kaynağıdır.
Şema, mevcut `/tr/sigorta/trafik/index.html` sayfasındaki hreflang'lerden alındı.

Alan adı henüz belli değil: her yerde `https://ORNEK-ALAN-ADI.com` placeholder'ı kullanılır.

| Sayfa | TR | EN |
|---|---|---|
| Ana sayfa | `/tr/` | `/en/` |
| Şirketler | `/tr/sirketler/` | `/en/companies/` |
| Metodoloji | `/tr/metodoloji/` | `/en/methodology/` |
| Trafik | `/tr/sigorta/trafik/` | `/en/insurance/motor-third-party/` |
| Kasko | `/tr/sigorta/kasko/` | `/en/insurance/comprehensive/` |
| Sağlık | `/tr/sigorta/saglik/` | `/en/insurance/health/` |
| Konut | `/tr/sigorta/konut/` | `/en/insurance/home/` |
| Seyahat | `/tr/sigorta/seyahat/` | `/en/insurance/travel/` |
| İşyeri | `/tr/sigorta/isyeri/` | `/en/insurance/business/` |
| Rehber (blog) | `/tr/rehber/` | `/en/guides/` |
| — Kaza sonrası | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | `/en/guides/first-48-hours-after-an-accident/` |
| — Sınır geçişi | `/tr/rehber/sinir-gecisi-sigortasi/` | `/en/guides/border-crossing-insurance/` |
| — Öğrenci sağlık | `/tr/rehber/ogrenci-saglik-sigortasi/` | `/en/guides/student-health-insurance/` |

## Henüz metni yazılmamış sayfalar

Footer bu sayfalara bağlantı veriyor ama sayfalar yok. Yayına almadan önce ya
üretilmeli ya da footer bağlantıları kaldırılmalı:

`/tr/hakkimizda/` · `/tr/iletisim/` · `/tr/yasal-uyari/` · `/tr/gizlilik/` · `/tr/duzeltme/`

Ayrıca şirket profil sayfaları (`/tr/sirketler/<sirket-adi>/`) henüz yok —
ana sayfadaki ve şirketler listesindeki adlar bu adreslere bağlanıyor.

## hreflang kuralı

Her sayfanın `<head>`'inde üç etiket bulunur: iki dil + `x-default`.
`x-default` her zaman **TR** sürümünü gösterir.

```html
<link rel="canonical" href="https://ORNEK-ALAN-ADI.com{KENDİ_URL}">
<link rel="alternate" hreflang="tr" href="https://ORNEK-ALAN-ADI.com{TR_URL}">
<link rel="alternate" hreflang="en" href="https://ORNEK-ALAN-ADI.com{EN_URL}">
<link rel="alternate" hreflang="x-default" href="https://ORNEK-ALAN-ADI.com{TR_URL}">
```

Header ve footer'daki dil değiştirici de **aynı sayfanın** diğer dildeki adresine
gitmelidir — dil ana sayfasına değil.

## Dil kodları

`lang` özniteliği: `tr`, `en`.
OG locale: `tr_TR`, `en_GB`.
