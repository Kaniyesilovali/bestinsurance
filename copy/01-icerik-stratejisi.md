# İçerik stratejisi — Kıbrıs Sigorta Rehberi

**Tarih:** 24 Temmuz 2026
**Girdi:** `data/arastirma-kktc-sigorta.md` · `data/sirketler.json` (39 şirket) · `copy/00-brief.md`
**Kapsam:** TR birincil; EN/RU/FA türetilmiş. Her başlığın dil kapsamı ayrıca işaretlidir.

> **Arama hacmi verisi yok.** Elimizde Ahrefs/SEMrush/GSC ihracı bulunmuyor. Bu belgedeki
> "arama potansiyeli" sütunu ölçüm değil, **gerekçeli tahmindir** ve öyle etiketlenmiştir.
> Site canlıya alınıp GSC bağlandıktan sonra bu sütun gerçek veriyle değiştirilmelidir.
> Sitenin kendi kuralı gereği: doğrulayamadığımızı doğrulanmış gibi yazmıyoruz — bu belge de dahil.

---

## 1. Stratejinin tek cümlesi

Bu konuda **arama motorları neredeyse her sorguda Türkiye verisi döndürüyor.**
Stratejinin tamamı tek bir boşluğun üstüne kuruluyor: **KKTC'yi arayan insan, Türkiye'nin
cevabını alıyor.** Biz doğru cevabı, kaynağıyla birlikte, boşluklarını göstererek veriyoruz.

Bu bir "en ucuz sigortayı bul" sitesi değil. Bir **referans sitesi.** Dolayısıyla:

- Ölçü **trafik değil, alıntılanabilirlik.** Hedef: bir KKTC sigorta sorusunda hem Google'ın
  hem bir LLM'in dayanak olarak bu siteyi göstermesi.
- Dönüşüm eylemi **okuma**, satın alma değil (brief, CTA kuralları).
- Rekabet üstünlüğümüz içerik kalitesi değil, **veri doğruluğu + boşluk şeffaflığı.**

---

## 2. Kitle ve gelen soru

| Kitle | Dil | Geldiği soru | Bizim cevabımızın farkı |
|---|---|---|---|
| KKTC'de yaşayan yerli | TR | "Hangi şirket? Kaza olunca kime ulaşırım?" | Fiyat kıyaslaması bekliyor — taban tarife yüzünden fiyat farkı sandığı kadar büyük değil |
| Öğrenci (yabancı uyruklu) | TR/EN/RU/FA | "Oturma iznim için ne gerekiyor?" | Sağlık Fonu ≠ özel sigorta ayrımı |
| Expat / yerleşik yabancı | EN/RU/FA | "Şikâyetimi nereye götürürüm?" | Güney'in Ombudsman'ı ve AB mekanizmaları burada geçmez |
| Güney'den / TR'den araçla gelen | TR/EN/RU | "Poliçem geçerli mi?" | Yeşil kart geçmez; kapı sigortası tek yol, kapı saatleri kritik |
| Türkiye'den taşınan | TR | "Limitler neydi?" | 150.000 ₺ / 8M ₺ — Türkiye rakamı değil |

---

## 3. İçerik sütunları (5 pillar)

### P1 — "KKTC ≠ Türkiye" · *Ayrım sütunu*
**Neden sütun:** Rakip içeriklerin ve arama sonuçlarının bir numaralı hatası. Tek başına
sitenin varlık sebebi. Her sayfada tekrar eden bir motif, ayrıca kendi hub'ı var.

Küme:
- Limit karşılaştırması (mal 150.000 ₺ vs 400.000 ₺ · bedeni 8M/15M ₺ vs 3,6M ₺)
- Düzenleyici karşılaştırması (Para Kambiyo Dairesi ≠ SEDDK · KKSBM ≠ SBM · KKSRSB Tahkim ≠ TR Tahkim)
- Tarife rejimi (taban tarife + bildirim ≠ serbest tarife)
- Hasarsızlık indirimi (KKTC oranları **bilinmiyor** — bu sayfanın işi boşluğu ilan etmek)
- Yeşil kart (KKTC üye değil)
- Şirket ≠ acente (Azant, Espada, ESTA acentedir)

**Yayın kısıtı:** Sigortasız araç cezası ve hasarsızlık basamak oranları bu kümede
**boş bırakılır ve neden boş olduğu yazılır.** Fasıl 333 md. 17 okunana kadar rakam yazılmaz.

---

### P2 — "Hangi şirket" · *Karar sütunu*
**Neden sütun:** Sitenin ana varlığı 39 şirketlik veri seti. Ticari niyetin en yüksek olduğu yer.

Küme:
- Şirket profilleri (35 sayfa — bkz. `02-programatik-seo.md`)
- Şirket türü açıklayıcıları: yerel Ltd. · TR şubesi · banka bağlı · reasürans
- Branşa göre şirket listeleri (trafik / kasko / sağlık / konut / seyahat / işyeri / yat …)
- Şehre göre erişim (Lefkoşa dışında ofisi olan şirketler)
- Dil desteğine göre (İngilizce · Rusça hizmet veren şirketler)
- Puanlama metodolojisi (mevcut sayfa — bu kümenin güven çıpası)

**Yapısal avantaj:** 39 şirketin hiçbirinin kendi hakkında karşılaştırılabilir sayfası yok;
6 büyük şirketin sitesinde faaliyet raporu bile bulunmuyor. Bu alan **boş.**

---

### P3 — "Bir şey oldu" · *Zarar anı sütunu*
**Neden sütun:** En yüksek aciliyet, en yüksek paylaşılabilirlik, en düşük rekabet.
Kaza anında telefonda okunan içerik.

Küme:
- Kaza sonrası ilk 48 saat *(yazıldı)*
- Garanti Fonu: sigortasız/ehliyetsiz/kaçan araç — **avukat ücretini fon karşılıyor**
- Sigorta Tahkim Komisyonu'na başvuru (adres, form, üyeler biliniyor; limit/ücret **bilinmiyor**)
- Hasar dosyası reddedildiyse beş basamaklı başvuru yolu
- Eksper süreci ve polis raporunun rolü

**En güçlü tek kanca:** *"Başvuru avukat aracılığıyla yapılır ve avukat ücretini Fon öder."*
Bu cümle internette hiçbir yerde düzgün anlatılmıyor.

---

### P4 — "Burada yabancıyım" · *Expat sütunu*
**Neden sütun:** EN/RU/FA sürümlerinin varlık sebebi. Sınır sigortasında ölçülmüş talep var:
**2024'te 238.320 poliçe** (KKSBM). Bu, tahmin değil, resmî sayı.

Küme:
- Sınır geçişi sigortası *(yazıldı)* — kapı kapı saat/fiyat
- Öğrenci Sağlık Fonu *(yazıldı)* — özel sigorta DEĞİL
- 3 aydan uzun ikamette sağlık şartı (**hangi türün kabul edildiği net değil** — öyle yazılır)
- Yabancı plakayla KKTC'de araç kullanmak
- Güney ↔ Kuzey çift yönlü geçersizlik kuralı
- **AB tüketici mekanizmaları burada işlemez** — EN/RU/FA'da TR'dekinden daha görünür yerde

---

### P5 — "Kimse söylemiyor" · *Şeffaflık sütunu* — **paylaşılabilir ağırlıklı**
**Neden sütun:** Aramada değil, alıntıda kazanır. Sitenin tarafsızlık iddiasının kanıtı.
Diğer dört sütunun tamamına güven aktarır.

Küme:
- **KKTC'de şirket bazında mali veri 2016'dan beri yayımlanmıyor** ← özgün bulgu
- Puanlama modelimiz neden mali güç içermiyor
- 2024→2025 taban primlerde ~%60–65 artış (CX1: 2.505,56 → 4.000,00 ₺)
- 39 şirketin web varlığı denetimi: 3 ölü alan adı, 2 şirketin sitesi hiç yok
- **Eurocity Sigorta ile EIG Sigorta'nın siteleri aynı IP'de ve aynı şablonda** —
  ikisi de ayrı ayrı ruhsatlı üye
- 39 şirketin yalnızca 3'ü poliçe genel şartlarını yayımlıyor
- Kapatılması gereken 12 veri boşluğu — açık bir liste olarak yayımlanır
- 2024 raporundaki çelişkili prim rakamı (4,84 milyar ₺ vs 5,32 milyar ₺)

Bu sütun ayrıca **düzeltme talebi** sayfasının anlamını yaratır: veriyi kamuya açıp
düzeltilmesini istemek.

---

## 4. Öncelik tablosu

Puanlama: brief'teki ağırlıklar — Okur etkisi %40 · İçerik-ürün uyumu %30 ·
Arama potansiyeli %20 (**tahmin**) · Kaynak gereksinimi %10.

| # | Başlık | Sütun | Tür | Aşama | Okur | Uyum | Arama* | Kaynak | **Toplam** |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Şirket profilleri (35 sayfa) | P2 | Aranabilir · pSEO | Karar | 9 | 10 | 8 | 7 | **9,0** |
| 2 | KKTC trafik sigortası Türkiye'den ne kadar farklı | P1 | Aranabilir | Farkındalık | 10 | 9 | 8 | 8 | **9,1** |
| 3 | Sigortasız araç çarptı: Garanti Fonu | P3 | İkisi de | Uygulama | 10 | 8 | 7 | 8 | **8,8** |
| 4 | Mali veri 2016'dan beri yayımlanmıyor | P5 | Paylaşılabilir | Farkındalık | 7 | 10 | 4 | 9 | **7,6** |
| 5 | Branşa göre şirket listeleri (10 sayfa) | P2 | Aranabilir · pSEO | Değerlendirme | 8 | 10 | 8 | 8 | **8,6** |
| 6 | Hasar dosyanız reddedilirse: 5 basamak | P3 | Aranabilir | Uygulama | 9 | 8 | 6 | 7 | **8,1** |
| 7 | Taban tarife nedir, fiyatı nasıl belirler | P1 | Aranabilir | Değerlendirme | 8 | 9 | 7 | 8 | **8,1** |
| 8 | Şirket mi acente mi — 3 isim | P1 | Aranabilir | Değerlendirme | 7 | 9 | 6 | 9 | **7,6** |
| 9 | Araç tipine göre 2025 taban prim (12 sayfa) | P1 | Aranabilir · pSEO | Değerlendirme | 8 | 8 | 8 | 6 | **7,8** |
| 10 | Sınır kapısı kapı kapı (6 sayfa) | P4 | Aranabilir · pSEO | Uygulama | 9 | 7 | 8 | 7 | **8,0** |
| 11 | Tahkim Komisyonu'na başvuru | P3 | Aranabilir | Uygulama | 8 | 8 | 5 | 6 | **7,3** |
| 12 | 3 aydan uzun ikamet: sağlık şartı | P4 | Aranabilir | Farkındalık | 8 | 7 | 7 | 5 | **7,3** |
| 13 | Şehre göre şirket erişimi (4 sayfa) | P2 | Aranabilir · pSEO | Değerlendirme | 6 | 9 | 7 | 8 | **7,3** |
| 14 | 2024→2025'te taban primler neden %60 arttı | P5 | Paylaşılabilir | Farkındalık | 6 | 8 | 5 | 7 | **6,5** |
| 15 | Sözlük: 20 terim | P1 | Aranabilir · pSEO | Farkındalık | 5 | 7 | 6 | 9 | **6,2** |

\* **Arama potansiyeli sütunu tahmindir.** Hacim verisiyle doğrulanmamıştır.

**Yayın sırası:** 1 → 2 → 3 → 5 → 4 → 7 → 6 → 10 → 9 → 8 → 11/12 → 13 → 14 → 15

Gerekçe: (1) footer ve şirket listesi zaten var olmayan adreslere bağlanıyor — kırık iç
bağlantı en acil teknik borç. (2) ve (3) sitenin iki tez cümlesini kanıtlar. (4) o ikisi
yayında olmadan yayımlanırsa dayanaksız kalır.

---

## 5. Küme haritası

```
/tr/  (ana sayfa — beş sütunun tamamına açılan kapı)
│
├── P1  KKTC ≠ Türkiye              → /tr/rehber/kktc-turkiye-farki/   [HUB]
│   ├── Taban tarife nedir                /tr/rehber/taban-tarife/
│   ├── Araç tipine göre taban prim       /tr/tarife/<arac-tipi>/         ← pSEO ×12
│   ├── Şirket mi acente mi                /tr/rehber/sirket-mi-acente-mi/
│   ├── Hasarsızlık indirimi (boşluk ilanı)/tr/rehber/hasarsizlik-indirimi/
│   └── Sözlük                             /tr/sozluk/<terim>/             ← pSEO ×20
│
├── P2  Hangi şirket                 → /tr/sirketler/                  [HUB · var]
│   ├── Şirket profili                    /tr/sirketler/<slug>/           ← pSEO ×35
│   ├── Branşa göre                        /tr/sirketler/<brans>/          ← pSEO ×10
│   ├── Şehre göre                         /tr/sirketler/sehir/<sehir>/    ← pSEO ×4
│   ├── Dile göre                          /tr/sirketler/ozellik/<x>/      ← pSEO ×4
│   └── Nasıl puanlıyoruz                  /tr/metodoloji/                 [var]
│
├── P3  Bir şey oldu                 → /tr/rehber/ (Hasar kategorisi)
│   ├── Kaza sonrası ilk 48 saat          /tr/rehber/kaza-sonrasi-ilk-48-saat/  [var]
│   ├── Garanti Fonu                       /tr/rehber/garanti-fonu/
│   ├── Tahkim Komisyonu                   /tr/rehber/tahkim-komisyonu/
│   └── Dosyanız reddedilirse               /tr/rehber/hasar-reddi/
│
├── P4  Burada yabancıyım            → EN/RU/FA'da ana giriş
│   ├── Sınır geçişi sigortası            /tr/rehber/sinir-gecisi-sigortasi/    [var]
│   ├── Kapı kapı sınır sigortası          /tr/rehber/sinir/<kapi>/        ← pSEO ×6
│   ├── Öğrenci Sağlık Fonu                /tr/rehber/ogrenci-saglik-sigortasi/  [var]
│   └── İkamet ve sağlık şartı             /tr/rehber/ikamet-saglik-sarti/
│
├── P5  Kimse söylemiyor             → /tr/rehber/ (Şeffaflık kategorisi)
│   ├── Mali veri yayımlanmıyor           /tr/rehber/mali-veri-yok/
│   ├── 12 veri boşluğu (canlı liste)      /tr/veri-bosluklari/
│   └── Taban primlerde %60 artış          /tr/rehber/taban-prim-artisi/
│
└── Sigorta türü hub'ları (var)      /tr/sigorta/{trafik,kasko,saglik,konut,seyahat,isyeri}/
```

### İç bağlantı kuralları

1. Her **şirket profili** → puanlandığı 6 ölçütün metodoloji bölümüne, sunduğu her branşın
   `/tr/sigorta/<brans>/` sayfasına, bulunduğu şehrin listesine bağlanır.
2. Her **branş listesi** → o branşın tür hub'ına ve ilk 5 şirket profiline bağlanır.
3. Her **fiyat/limit içeren sayfa** → P1 hub'ına ("bu rakam Türkiye'nin değil") bağlanır.
4. Her **boşluk ifadesi** ("bu veriyi doğrulayamadık") → `/tr/veri-bosluklari/` sayfasına bağlanır.
   Bu, sitenin tek en ayırt edici iç bağlantı deseni.
5. Hiçbir sayfa öksüz kalmaz: 35 profil şirketler listesinden, 10 branş listesi tür
   hub'larından, 12 tarife sayfası taban tarife sayfasından erişilebilir.

> Set büyüklükleri `02-programatik-seo.md`'de veriye bakılarak kesinleştirildi; o belge
> bu haritanın üstündedir.

---

## 6. Eksik altyapı sayfaları (yayın öncesi zorunlu)

Footer bunlara bağlantı veriyor, sayfalar yok:

`/tr/hakkimizda/` · `/tr/iletisim/` · `/tr/yasal-uyari/` · `/tr/gizlilik/` · `/tr/duzeltme/`

Bunların üçü strateji açısından da işlevli:
- **Hakkımızda** → P5'in insan yüzü. Kim, neden, parayı kim ödüyor.
- **Düzeltme talebi** → şirketlerin veriyi düzeltmesi için kanal. Aynı zamanda E-E-A-T sinyali.
- **Yasal uyarı** → "sigorta tavsiyesi değildir" tek sayfada.

---

## 7. Yazılmayacaklar — hatırlatma

`00-brief.md` ⛔ tablosu bu stratejinin bağlayıcı ekidir. Öncelik listesindeki hiçbir başlık
o tablodaki bir rakamı yazma iznine sahip değil. Özellikle:

- **9 numaralı pSEO kümesi (araç tipi tarifeleri)** yalnızca **2025** etiketiyle yayımlanır.
  2026 tarifesi yayımlanmadı; sayfalarda bu açıkça yazılır. 2026 çıktığında güncellenir.
- **8 numaralı başlık** MAPFREE/MAPFRE veya London Insurance grup bağı iddiasına girmez.
- **6 ve 11 numaralı başlıklar** tahkim ücreti/limiti/süresi yazamaz — tüzük okunmadı.
- **3 numaralı başlık** Garanti Fonu ödeme limiti yazamaz — yalnızca kapsam ve süreç.

---

## 8. Ölçüm

Site canlıya alınınca (`site.json` → `yayin.noindex: false`) izlenecekler:

| Soru | Nasıl bakılır |
|---|---|
| Türkiye verisi arayan mı geliyor, KKTC arayan mı? | GSC sorguları: "kktc" / "kuzey kıbrıs" içeren pay |
| 39 profil indekslendi mi? | GSC Sayfalar → `/tr/sirketler/` öneki |
| Hangi sütun çalışıyor? | GSC'de URL öneki bazında tıklama |
| LLM'ler alıntılıyor mu? | ChatGPT/Perplexity/Claude'da 10 sabit sorgunun aylık kontrolü |
| Boşluk kapandı mı? | `/tr/veri-bosluklari/` — 12 maddeden kaçı kapandı |

İlk 90 günde **hacim hedefi konmaz.** Tek hedef: 12 veri boşluğundan en az 3'ünün
birincil kaynaktan kapatılması. Bu sitenin gerçek üretim işi.
