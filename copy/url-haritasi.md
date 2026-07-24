# URL haritası — dört dil

Bu tablo hreflang etiketlerinin, dil değiştiricinin ve sitemap'in tek kaynağıdır.
Şema, mevcut `/tr/sigorta/trafik/index.html` sayfasındaki hreflang'lerden alındı.

Alan adı henüz belli değil: her yerde `https://ORNEK-ALAN-ADI.com` placeholder'ı kullanılır.

| Sayfa | TR | EN | RU | FA |
|---|---|---|---|---|
| Ana sayfa | `/tr/` | `/en/` | `/ru/` | `/fa/` |
| Şirketler | `/tr/sirketler/` | `/en/companies/` | `/ru/kompanii/` | `/fa/companies/` |
| Metodoloji | `/tr/metodoloji/` | `/en/methodology/` | `/ru/metodologiya/` | `/fa/methodology/` |
| Trafik | `/tr/sigorta/trafik/` | `/en/insurance/motor-third-party/` | `/ru/strahovanie/osago/` | `/fa/insurance/motor-third-party/` |
| Kasko | `/tr/sigorta/kasko/` | `/en/insurance/comprehensive/` | `/ru/strahovanie/kasko/` | `/fa/insurance/comprehensive/` |
| Sağlık | `/tr/sigorta/saglik/` | `/en/insurance/health/` | `/ru/strahovanie/zdorove/` | `/fa/insurance/health/` |
| Konut | `/tr/sigorta/konut/` | `/en/insurance/home/` | `/ru/strahovanie/zhilje/` | `/fa/insurance/home/` |
| Seyahat | `/tr/sigorta/seyahat/` | `/en/insurance/travel/` | `/ru/strahovanie/puteshestvie/` | `/fa/insurance/travel/` |
| İşyeri | `/tr/sigorta/isyeri/` | `/en/insurance/business/` | `/ru/strahovanie/biznes/` | `/fa/insurance/business/` |
| Rehber (blog) | `/tr/rehber/` | `/en/guides/` | `/ru/rukovodstvo/` | `/fa/guides/` |
| — Kaza sonrası | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | `/en/guides/after-an-accident/` | `/ru/rukovodstvo/posle-dtp/` | `/fa/guides/after-an-accident/` |
| — Sınır geçişi | `/tr/rehber/sinir-gecisi-sigortasi/` | `/en/guides/crossing-the-border/` | `/ru/rukovodstvo/perehod-granicy/` | `/fa/guides/crossing-the-border/` |
| — Öğrenci sağlık | `/tr/rehber/ogrenci-saglik-sigortasi/` | `/en/guides/student-health-cover/` | `/ru/rukovodstvo/studencheskaya-strahovka/` | `/fa/guides/student-health-cover/` |

## Henüz metni yazılmamış sayfalar

Footer bu sayfalara bağlantı veriyor ama sayfalar yok. Yayına almadan önce ya
üretilmeli ya da footer bağlantıları kaldırılmalı:

`/tr/hakkimizda/` · `/tr/iletisim/` · `/tr/yasal-uyari/` · `/tr/gizlilik/` · `/tr/duzeltme/`

Ayrıca şirket profil sayfaları (`/tr/sirketler/<sirket-adi>/`) henüz yok —
ana sayfadaki ve şirketler listesindeki adlar bu adreslere bağlanıyor.

## hreflang kuralı

Her sayfanın `<head>`'inde beş etiket bulunur: dört dil + `x-default`.
`x-default` her zaman **TR** sürümünü gösterir.

```html
<link rel="canonical" href="https://ORNEK-ALAN-ADI.com{KENDİ_URL}">
<link rel="alternate" hreflang="tr" href="https://ORNEK-ALAN-ADI.com{TR_URL}">
<link rel="alternate" hreflang="en" href="https://ORNEK-ALAN-ADI.com{EN_URL}">
<link rel="alternate" hreflang="ru" href="https://ORNEK-ALAN-ADI.com{RU_URL}">
<link rel="alternate" hreflang="fa" href="https://ORNEK-ALAN-ADI.com{FA_URL}">
<link rel="alternate" hreflang="x-default" href="https://ORNEK-ALAN-ADI.com{TR_URL}">
```

Header ve footer'daki dil değiştirici de **aynı sayfanın** diğer dildeki adresine
gitmelidir — dil ana sayfasına değil.

## Dil kodları

`lang` özniteliği: `tr`, `en`, `ru`, `fa`.
FA sayfalarında ayrıca `dir="rtl"` gerekir: `<html lang="fa" dir="rtl">`.
OG locale: `tr_TR`, `en_GB`, `ru_RU`, `fa_IR`.
