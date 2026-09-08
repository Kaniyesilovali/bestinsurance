# Dil katmanı stratejisi — EN · RU · FA

**Tarih:** 8 Eylül 2026
**Girdi:** `copy/00-brief.md` (Pazar kapsamı · ⛔ tablosu) · `copy/01-icerik-stratejisi.md` §3 P4 ·
`data/sirketler.json` (39 şirket, dil alanı) · `data/arastirma-kktc-sigorta.md` §2.6, §3.1, §6 ·
`site.json` (rotalar, menu, footer, blog) · `copy/en|ru|fa/` (34 taslak)
**Üstündeki belge:** `copy/00-brief.md`. Çatışma halinde brief kazanır.

> Bu belge `01-icerik-stratejisi.md`'yi değiştirmez, onun **P4 sütununu** açar.
> Sütunun kendisi orada tanımlı; burada hangi dilde, hangi sırayla ve hangi
> sınırla yayımlanacağı karara bağlanır.

---

## 1. Kararın tek cümlesi

Sitenin **tahmine dayanmayan tek talebi** yabancı dilde geliyor, ve o talebi
karşılayacak 34 taslak yazılmış olduğu halde tek bir sayfa canlı değil.
Bu katman açılır — ama üç dil eşit açılmaz: **şirket verisi hangi dili
taşıyorsa o dil o kadar açılır.**

---

## 2. Neden bu sütun, neden şimdi

Dört gerekçe. Üçü ölçülmüş, biri yapısal.

### 2.1 Ölçülmüş talep — sitedeki tek tanesi

`01-icerik-stratejisi.md` kendi arama potansiyeli sütununu **tahmin** olarak
etiketliyor; GSC bağlanana kadar bu sitede hacim verisi yok. Tek istisna P4:

**2024 sınır geçişi: 238.320 poliçe · 356.742.641,24 ₺ net prim (KKSBM, resmî).**
Metehan tek başına 109.695 poliçe — toplamın %46'sı.

Bu poliçeleri alanlar tanım gereği KKTC'de ikamet etmeyen sürücüler. Sitenin
başka hiçbir sayfası arkasında bu ağırlıkta bir sayıya yaslanmıyor.

### 2.2 Şirket verisi dil desteğini ölçmüş

`data/sirketler.json`, 39 ruhsatlı şirket:

| Dil | Hizmet veren şirket | Ne anlama geliyor |
|---|---|---|
| Türkçe | 33 | Temel |
| **İngilizce** | **17** | Arkasında gerçek bir arz var |
| **Rusça** | **2** | Dağlı Sigorta, Creditwest Sigorta |
| **Farsça** | **0** | Karşılaştırılacak şirket yok |

Bu tablo dil kapsamı kararını tahminden çıkarıp veriye bağlıyor. Ayrıntısı §5'te.

### 2.3 Resmî İngilizce birincil kaynak var

KKSRSB poliçe genel şartlarını **TR ve İngilizce** yayımlıyor
(`arastirma-kktc-sigorta.md` §2.6): Motorlu Araçlar 3. Şahıs Zorunlu Trafik ve
Kasko, ikisi de iki dilde.

EN sayfaları bu yüzden **çeviriye değil, resmî metne** dayanabilir. Sitenin
tamamında "dışarıdan doğrulanabilen" iddiası bu kadar temiz duran ikinci bir
yer yok. TR tarafında karşılığı olmayan bir üstünlük — çünkü TR okuru zaten
Türkiye'nin metnini bulup yanlış metne bakıyor.

### 2.4 Rekabet asimetrisi

TR'de her KKTC sorgusu Türkiye'nin SEO kütlesiyle dövüşüyor; stratejinin
birinci cümlesi bu. EN tarafında ise KKTC sigortası için bağımsız bir
karşılaştırma kaynağı yok — alan boş, ve dolduran taraf poliçe satan acenteler.

**Not:** Bu bir rakip sonuç sayfası gözlemidir, metin malzemesi değil
(`00-brief.md`, Pazar kapsamı). EN sayfaları rakiple değil kendi verimizle açılır.

---

## 3. Envanter — elde ne var

| | EN | RU | FA |
|---|---|---|---|
| `copy/` taslağı | **12** | 11 | 11 |
| `content/` sayfası | **4** (Blok A) | 0 | 0 |
| `dist/` canlı sayfa | **4** | 0 | 0 |
| `site.json` rotası | 10 adres tanımlı | yok | yok |
| `site.json` menu | var (3 madde) | yok | yok |
| `site.json` footer | var (AB uyarısı yazılı) | yok | yok |
| `site.json` blog | var (`/en/guides/`) | yok | yok |

**Taslakların kapsamı** (her dilde aynı iskelet): ana sayfa · metodoloji ·
şirketler · 6 sigorta türü · 3 rehber. Yani çekirdek sitenin tamamı.

**RU ve FA'da eksik olan tek taslak:** `sigorta-trafik`. Üç dilde birden
eksikti; 2 Eylül'de yalnızca EN'i yazıldı (commit `801b966`). Zorunlu trafik
sayfası diğer motor sayfalarının şablonu olduğu için bu eksik RU/FA'yı
kilitliyor.

---

## 4. Tek kapı: `/en/` ana sayfası

Yazılmış tek EN sayfası — `content/en/sayfa/insurance/motor-third-party/` —
`taslak: evet` ile bekliyor. Sebebi içerik değil, yapı:

- `_build/sablon/parca/header.html`: her sayfadaki logo `/{dil}/` adresine bağlanır.
- `_build/uret.py:1723`: dil değiştirici yalnızca `/{dil}/` üretilmiş dilleri listeler.

Yani **hiçbir EN sayfası `/en/` olmadan tek başına yayımlanamaz** — kırık
bağlantı doğar. Aynı kural RU ve FA için de geçerli.

> Bu, katmanın tamamını tek bir sayfanın arkasında bekleten bir bağımlılık.
> Yayın sırası (§6) bu kapıdan başlar; başka hiçbir sıralama tartışması
> bu maddenin önüne geçmez.

---

## 5. Dil kapsamı kararı — üç dil, üç ayrı sınır

Üç dili aynı genişlikte açmak, elde 34 taslak varken cazip görünüyor. Veri
buna izin vermiyor. Sitenin kuralı burada da işler: **karşılaştıramadığımız
yeri boş bırakırız.**

### EN — tam katman

17 şirket İngilizce hizmet veriyor; resmî İngilizce genel şartlar var; sınır
geçişi hacminin ana kitlesi burada. Beş sütunun beşi de EN'de kurulabilir:
`/en/companies/` gerçek bir karşılaştırma sunar, çünkü 17 şirketlik bir arz var.

### RU — çekirdek + ilan edilmiş sınır

2 şirket Rusça hizmet veriyor. Bu, rehber sayfalarını (P4) tamamen meşru
kılar — sınır geçişi, öğrenci sağlığı, kaza sonrası ilk 48 saat okurun
diliyle okunması gereken metinler ve şirketin dilinden bağımsız.

Ama **P2 (hangi şirket) sütunu RU'da tam kurulamaz.** `/ru/kompanii/` sayfası
39 şirketi listeler, okurun konuşabileceği ikisini gösterir ve bunu **açıkça
yazar.** Gizlenecek bir şey değil — sayfanın bulgusu bu.

> RU'da ilan edilecek boşluk: *"39 ruhsatlı şirketten yalnızca ikisinin Rusça
> hizmet verdiğini doğrulayabildik. Kalan 37'sinde Rusça hizmet olup olmadığı
> şirket sitelerinden ölçülemedi."*

### FA — yalnızca P4, ve boşluk ilanıyla

**Hiçbir şirket Farsça hizmet vermiyor.** FA katmanında bir şirket
karşılaştırması yayımlamak, okuru hiçbirinin kendisiyle konuşamayacağı 39
şirkete yönlendirmek olur. Bu, sitenin CTA kuralına da ters: eylem okumaktır,
ama okunacak şey yanlış yere çıkıyorsa eylem de yanlıştır.

FA'da açılan: ana sayfa · metodoloji · sınır geçişi · öğrenci sağlığı ·
kaza sonrası ilk 48 saat · sağlık. Yani **zarar anı ve ikamet** — dil desteği
gerektirmeyen, prosedürel bilgi.

FA'da açılmayan: `/fa/companies/` ve branş karşılaştırma sayfaları — ta ki
en az bir şirkette Farsça hizmet doğrulanana kadar.

> FA'da ilan edilecek boşluk: *"KKTC'de ruhsatlı 39 sigorta şirketinin
> hiçbirinde Farsça hizmet doğrulayamadık. Bu sayfalar bu yüzden şirket
> karşılaştırması içermiyor."*

### Karar tablosu

| | EN | RU | FA |
|---|---|---|---|
| P1 Ayrım | ✔ | ✔ | kısmi |
| P2 Hangi şirket | ✔ | **sınırlı + ilan** | **açılmaz** |
| P3 Bir şey oldu | ✔ | ✔ | ✔ |
| P4 Burada yabancıyım | ✔ | ✔ | ✔ |
| P5 Kimse söylemiyor | ✔ | kısmi | kısmi |
| Hedef sayfa sayısı | 12 | 8 | 6 |

---

## 6. Yayın sırası

Bağımlılık sırasıdır, önem sırası değil. Her adım bir öncekini gerektirir.

### Blok A — kapıyı aç (EN) · ✅ tamamlandı 8 Eylül 2026

| # | Sayfa | Kaynak taslak | Neden burada |
|---|---|---|---|
| A1 | ✅ `/en/` | `copy/en/ana-sayfa.md` | §4'teki kapı. Bu olmadan hiçbiri yayımlanamaz. |
| A2 | ✅ `/en/insurance/motor-third-party/` | *(yazılmıştı)* | `taslak: evet` ve breadcrumb notu silindi |
| A3 | ✅ `/en/methodology/` | `copy/en/metodoloji.md` | Sitenin kanıtı. Şirketler sayfasından önce gelmeli. |
| A4 | ✅ `/en/companies/` | `copy/en/sirketler.md` | 17 EN şirketi burada anlam kazanır. **Veriden üretiliyor**, elle yazılmadı. |

A4 bittiğinde EN katmanı **kendi başına ayakta duran bir site** olur:
giriş, yöntem, veri, ve bir ürün sayfası.

### Blok B — EN zarar anı ve ikamet (P3 + P4)

| # | Sayfa | Kaynak taslak |
|---|---|---|
| B1 | `/en/guides/border-crossing-insurance/` | `copy/en/rehber-sinir-gecisi.md` |
| B2 | `/en/insurance/travel/` | `copy/en/sigorta-seyahat.md` |
| B3 | `/en/guides/student-health-insurance/` | `copy/en/rehber-ogrenci-saglik.md` |
| B4 | `/en/insurance/health/` | `copy/en/sigorta-saglik.md` |
| B5 | `/en/guides/first-48-hours-after-an-accident/` | `copy/en/rehber-kaza-48-saat.md` |

B1 ve B2 önce: 238.320 poliçelik ölçülmüş talep bu ikisinin arkasında.

### Blok C — EN kalan branşlar

| # | Sayfa | Kaynak taslak |
|---|---|---|
| C1 | `/en/insurance/comprehensive/` | `copy/en/sigorta-kasko.md` |
| C2 | `/en/insurance/home/` | `copy/en/sigorta-konut.md` |
| C3 | `/en/insurance/business/` | `copy/en/sigorta-isyeri.md` |

### Blok D — RU

`copy/ru/sigorta-trafik.md` **önce yazılır** (§3'teki eksik). Sonra:
`/ru/` → `/ru/strahovanie/osago/` → `/ru/metodologiya/` → `/ru/kompanii/`
(sınır ilanıyla) → sınır geçişi → öğrenci sağlığı → kaza 48 saat.

### Blok E — FA

`copy/fa/sigorta-trafik.md` yazılır. Sonra: `/fa/` → metodoloji →
zorunlu trafik → sınır geçişi → öğrenci sağlığı → sağlık → kaza 48 saat.
**Şirket sayfası üretilmez** (§5).

---

## 7. Sorgu sahipliği — TR kuyruğundan devredilenler

`03-marka-sorgulari.md` §10: bir sorgunun bir sahibi olur. `sorgu-sec`
Kapı 4: hedef kitle TR konuşmuyorsa sorgu TR sayfayla karşılanamaz.

Kuyrukta hedef sorgusu **başka bir dilde yazılmış** üç satır var. Bunlar
TR yazıyla karşılanamaz:

| № | Başlık | Hedef sorgu | Karar |
|---|---|---|---|
| 41 | AB tüketici mekanizmaları KKTC'de neden işlemez | `north cyprus insurance complaint` | **EN'e devir.** Sahibi `/en/methodology/` + footer.en'deki AB uyarısı (A3). |
| 60 | İngilizce hizmet veren şirketler nasıl bulunur | `north cyprus english speaking insurance` | **EN'e devir.** Sahibi `/en/companies/` (A4) — 17 şirketlik filtre zaten orada. |
| 75 | Rusça hizmet: KKTC sigortasında gerçek durum | `северный кипр страхование` | **RU'ya devir.** Sahibi `/ru/kompanii/` (Blok D) — iki şirket bulgusu o sayfanın kendi içeriği. |

### Kuyrukta nasıl işaretlenir

Bu satırlar **`✅` yapılamaz** — hiçbir şey yayımlanmadı, öyle işaretlemek
sayacı yalanlar. **`⬜` de kalamaz** — `yazi-uret` sırası gelince TR yazı üretir
ve yanlış dilde bir sayfa doğar.

Kuyruk kuralı 2'deki `⛔` semantiği ("henüz yazılamaz, atlanır") bu duruma
uyar. Gerekçe metni değişir:

```
| 41 | ⛔ | AB tüketici mekanizmaları KKTC'de neden işlemez — **EN katmanına devredildi** (04-dil-katmani §7); TR yazıyla karşılanamaz | Yabancılar | north cyprus insurance complaint | `/en/methodology/` | KKTC şirketlerinin AB şema dışılığı resmî metinle doğrulanmadı |
| 60 | ⛔ | İngilizce hizmet veren şirketler nasıl bulunur — **EN katmanına devredildi** (04-dil-katmani §7) | Yabancılar | north cyprus english speaking insurance | `/en/companies/` | Hizmetin gerçekten İngilizce verildiği test edilmedi |
| 75 | ⛔ | Rusça hizmet: KKTC sigortasında gerçek durum — **RU katmanına devredildi** (04-dil-katmani §7) | Yabancılar | северный кипр страхование | `/ru/kompanii/` | İki şirket dışında Rusça hizmet doğrulanamadı |
```

Zorunlu bağlantı sütunu ilgili dil sayfası **üretildikten sonra** geçerlidir;
o zamana kadar satır zaten `⛔` olduğu için beceri dokunmaz.

### Devredilmeyen ama dil ikizi hak eden satırlar

Hedef sorgusu TR ama okur kitlesi ağırlıklı yabancı olan satırlar. Bunlar
TR'de kalır — Türkçe konuşan yabancı da gerçek bir okur (`00-brief.md`
okur tablosu). EN karşılığı Blok C sonrasında ayrı satır olarak açılır:

| № | Başlık | TR'de kalma gerekçesi |
|---|---|---|
| 29 | Kuzey'de alınan poliçe Güney'de neden geçmez | Çift yönlü kural TR okuru da ilgilendiriyor |
| 45 | KKTC'de ev satın alan yabancı için konut sigortası | Alıcıların bir kısmı TR konuşuyor |
| 63 | Emeklilikte KKTC'ye yerleşenler için sağlık | — |
| 67 | Turist olarak araç kiralarken sigorta | Türkiye'den gelen turist TR okuyor |

---

## 8. Çeviri değil, sürüm — metin kuralları

Taslaklar çeviri değil, o dilin okuru için yeniden yazılmış metinler. Yayına
dökülürken korunacaklar:

1. **Dördüncü ayrım daha görünür yerde.** Güney Kıbrıs'ın Financial
   Ombudsman'ı ve AB tüketici mekanizmaları KKTC'de geçmez. `00-brief.md`
   bunu EN/RU/FA'da TR'dekinden **daha görünür** yere koymayı şart koşuyor.
   `footer.en` bu uyarıyı zaten taşıyor; `footer.ru` ve `footer.fa` yazılırken
   aynı metin girer.
2. **Terim sözlüğü sabittir.** `00-brief.md` terim tablosu bağlayıcı.
   Kurum adları çevrilmez, ilk geçişte açıklanır: KKSRSB, KKSBM.
   Para birimi ondalık ayırıcısı EN'de **nokta**, TR'de virgül.
3. **⛔ tablosu dile bakmaz.** Türkiye'nin limitleri, sigortasız araç cezası,
   hasarsızlık oranları — hiçbir dilde yazılmaz.
4. **Her sayfa bir boşluk ifadesi taşır.** RU ve FA'da §5'teki dil boşluğu
   ifadeleri bu şartı kendiliğinden karşılamaz; sayfanın kendi konusuna ait
   bir boşluk ayrıca yazılır.
5. **FA sağdan sola.** `site.json` → `diller.fa.dir = "rtl"` tanımlı;
   şablonun bunu gerçekten uyguladığı ilk FA sayfasında kontrol edilir.

---

## 9. Kapatılacak yapılandırma boşlukları

Yayın sırası bunlara takılır. Sırası gelince kapatılır, önceden hepsi değil.

| Boşluk | Durum | Karar |
|---|---|---|
| `rotalar` → EN rehber adresleri | 3 rehberin rotası yok | Blok B'den önce eklenir |
| **`/en/guide/` mi `/en/guides/` mi** | Taslaklar tekil, `blog.en.kok` çoğul | **Çoğul kazanır** — liste sayfası `/en/guides/`, yazılar `/en/guides/<slug>/`. Taslaklardaki tekil adresler düzeltilir. |
| **`/en/insurance/kasko/` mi `comprehensive/` mi** | ✅ karara bağlandı | **Rota kazanır.** `00-brief.md` terim tablosu: "Comprehensive motor insurance", "Kasko" parantez içinde korunur. |
| `menu.en` | ✅ 3 madde (Blok A) | Her blok sonunda genişletilir |
| `menu.ru`, `menu.fa` | yok | Blok D / E başında |
| `footer.ru`, `footer.fa` | yok | Blok D / E başında, AB uyarısı dahil |
| `blog.ru`, `blog.fa` | yok | Rehber sayfası üretilecekse gerekir |
| `rotalar` → RU/FA rehber adresleri | yok | Blok D / E |

---

## 10. Ölçüm

`01-icerik-stratejisi.md` §8'e eklenir. İlk 90 günde hacim hedefi yok.

| Soru | Nasıl bakılır |
|---|---|
| EN katmanı indekslendi mi | GSC Sayfalar → `/en/` öneki |
| Doğru kitle mi geliyor | GSC → `/en/` sorgularında "north cyprus" / "trnc" payı |
| Sınır geçişi talebi karşılanıyor mu | `/en/insurance/travel/` + `/en/guides/border-crossing-insurance/` tıklaması |
| RU sınır ilanı işe yarıyor mu | `/ru/kompanii/` çıkış oranı — okur ikinci sayfaya geçiyor mu |
| FA kararı doğru muydu | FA sayfalarında şirket sorgusu geliyorsa karar gözden geçirilir |
| LLM alıntısı | 10 sabit sorgunun EN karşılıkları aylık kontrol |

**Kararı değiştirecek tek bulgu:** bir şirkette Farsça ya da üçüncü bir
şirkette Rusça hizmet doğrulanırsa §5 tablosu güncellenir. Karar veriye
bağlı, dolayısıyla veri değişince karar da değişir.

---

## 11. Yan onarımlar

Bu turun kapsamı değil ama katman açılmadan önce kapanmalı — ikisi de
şu an yayındaki siteyi bozuyor:

1. ✅ **Kategori bütünlüğü.** `can-sigorta-lefkosa.md` → `Şirket seçimi`;
   öksüz `/tr/rehber/konu/sirket/` konu sayfası kalktı.
2. ✅ **Kuyruk sayacı.** 7 `✅` · 77 `⬜` · 3 `⛔`; kapsam 87 satır olarak düzeltildi.
3. ✅ **Üretici onarımı** — planlanmamıştı, Blok A sırasında çıktı. Ayrıntı §12.

Ayrıca not: `Ürün` kategorisinde hiç yayın yok, bu yüzden o sütunun konu
sayfası hâlâ doğmadı. Kuyrukta 10 `Ürün` satırı bekliyor — kendiliğinden
kapanacak, işlem gerekmiyor.

---

## 12. Yol üstünde çıkan: üretici onarımı

Blok A sırasında `data/uret-sirketler.py` içinde sessiz bir veri hatası bulundu.
Dil katmanının parçası değildi ama önce onarılması gerekti: EN şirketler sayfası
aynı üreticiden çıkıyor.

**Hata.** Betik ana sayfanın sıralama tablosunu 10 boşluk girintili `<tbody>`
deseniyle arıyordu; ana sayfada girinti 6 boşluk. `re.subn` eşleşme bulmuyor,
`n = 0` dönüyor ve blok **hata vermeden** atlanıyordu. Şirketler sayfası
güncelleniyor, ana sayfa eski puanlarla kalıyordu. Kanıtı: `can-sigorta`
erişilebilirlik puanı veride `4`, yayındaki ana sayfada `4,0` — ana sayfa bir
veri değişikliğinden beri bayattı.

**Neden önemli.** Puanlar bir sonraki puanlamada değişseydi ana sayfa ile
şirketler sayfası aynı beş şirket için farklı puan gösterecekti. Verisini iddia
edinmiş bir sitede iki sayfanın aynı şirkete farklı puan vermesi, brief'in
tamamını çürütür.

**Onarım.**

| Ne | Nasıl |
|---|---|
| Sessiz atlama | Girinti duyarsız eşleşme; bulunamazsa `SystemExit` ile **durur** |
| `satir_html_koyu` | Koyu bant markup'ı basıyordu — ana sayfa açık yüzeye geçtiğinde geride kalmış. Regex düzelseydi reddedilen koyu yönü ana sayfaya geri enjekte edecekti. `satir_html_ana` olarak yayındaki açık tasarıma hizalandı. |
| Kısa ad türetimi | Algoritmik büyük/küçük harf çevrimi 35 addan en az onunu bozuyordu (`CREDITWEST → Credıtwest`, ve `AS-CAN SİGORTA → Ascan Sigorta`). Adlar artık `data/marka-adlari.json` → `gorunen_adlar` içinde elle yazılı; listede olmayan şirket ilk beşe girerse betik durur. |
| Puan biçimi | Veride 65 int / 141 float karışık; aynı `aria-label` içinde "Şeffaflık 8" ile "Dijital hizmet 8,0" yan yana düşüyordu. Biçim veriye değil ölçeğe bağlandı. |

**Doğrulama.** Onarılan üretici, yayındaki TR ana sayfasını markup düzeyinde
birebir yeniden üretiyor — tek fark yukarıdaki bayat puan. Yani onarım tasarımı
değiştirmedi, yalnızca kopan bağı kurdu.

**EN'e etkisi.** `serit()` artık dile bağlı (`dil="en"` İngilizce etiket ve
**nokta** ondalık üretir — brief'in terim tablosu gereği). `/en/companies/` ve
EN ana sayfasının ilk beş satırı aynı veriden üretiliyor; elle yazılsaydı
puanlar güncellendiğinde iki dil aynı şirkete farklı puan gösterirdi — az önce
onarılan hatanın aynısı.

---

## 13. Bu belgenin yazmadıkları

- **Metin yazmaz.** Taslaklar `copy/en|ru|fa/` altında hazır; bu belge
  hangisinin ne zaman ve hangi sınırla sayfaya döküleceğine karar verir.
- **Arama hacmi tahmini üretmez.** 238.320 rakamı ölçümdür ve kaynağı
  yazılıdır; onun dışında bu belgede hacim iddiası yok.
- **TR kuyruğunun sırasını değiştirmez.** §7'deki üç satır dışında hiçbir
  satıra dokunulmaz; ilk `⬜` kuralı işlemeye devam eder.
- **FA'yı kapatmaz.** FA katmanı açılır, yalnızca şirket karşılaştırması
  içermez. Bu bir kapsam kararıdır, bir vazgeçiş değil.
