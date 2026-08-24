# Marka sorguları planı — şirket adıyla arayanı karşılamak

**Tarih:** 24 Ağustos 2026
**Hedef (kullanıcı ifadesiyle):** "Sigorta şirketlerinin ismiyle arama yapıldığında bu sitenin ilk sırada çıkması."
**Dayanak:** `copy/00-brief.md` ⛔ tablosu · `copy/01-icerik-stratejisi.md` P2 sütunu ·
`copy/02-programatik-seo.md` Set A · `data/sirketler.json` (39 şirket, 30 alan)
**Kapsam:** TR birincil. EN türetimi §12'de.

---

## 0. Bu planın tek kuralı

> **Şirketin kendi sayfasını, şirket hakkında olmayan bir sayfa geçemez.**
> Bu plandaki her sayfa, o şirket hakkında **şirketin kendi sitesinde bulunmayan**
> en az bir doğrulanmış gözlem taşır. Taşımayan sayfa üretilmez.

Elimizdeki `notlar` alanı tam olarak budur. Örnek:

> *"Türk Sigorta — teklif formunda doğum yılı seçenekleri 2003'te bitiyor. Genel Şartlar
> sayfası boş: 'Bu bölüm güncellenmektedir'. Sayfa memnuniyet oylaması 1.7/5."*

Bu üç cümle internette başka hiçbir yerde yok ve şirket bunu kendi sitesine yazmaz.
Marka sorgusunu kazandıracak olan şey budur — anahtar kelime yerleşimi değil.

---

## 1. Gerçeklik denetimi — neyi kazanabiliriz, neyi kazanamayız

Hedefi olduğu gibi kabul edip planlamak yanlış olur. **Çıplak marka sorgusu
(`"dağlı sigorta"`) navigasyonel bir sorgudur;** arayan kişi zaten o şirketin sitesine
gitmek istiyor ve Google bunu bilir. Çalışan bir siteye sahip bir şirketin adında
1. sırayı üçüncü taraf bir sitenin alması istisnadır.

**Ölçtüğümüz durum** (24 Ağustos 2026, iki örnek sorgu):

| Sorgu | 1–3. sıra | Sonraki sıralar |
|---|---|---|
| `"Dağlı Sigorta" KKTC` | daglisigorta.com (3 ayrı iç sayfa) | kktc-sigorta.com · kksrsb.org üye listesi |
| `"Limasol Sigorta" Kıbrıs` | limasolsigorta.com (4 ayrı iç sayfa) | yeniduzen.com · kibrismanset.com · kimibilin.com · rocketreach.co |

> ⚠ **Bu gözlem ABD çıkışlı bir arama üzerinden alındı.** KKTC/TR çıkışlı sonuçlar
> farklılaşır. GSC bağlandıktan sonra bu tablo gerçek konum verisiyle değiştirilmelidir.
> Sitenin kendi kuralı gereği: doğrulayamadığımızı doğrulanmış gibi yazmıyoruz — bu belge de dahil.

**Okunan şey:** şirketin kendi alan adı ilk 2–4 sırayı iç sayfalarıyla dolduruyor.
Geriye kalan sıralar **içerik boşluğu:** rehber dizinleri (kimibilin, rocketreach),
haber siteleri ve Birlik'in üye listesi. Bunların hiçbiri şirket hakkında
**karşılaştırılabilir** bir şey söylemiyor.

### Bu planın kabul ettiği hedef

| Sorgu tipi | Gerçekçi hedef | Gerekçe |
|---|---|---|
| Çıplak marka — **çalışan siteli 34 şirket** | **2–4. sıra** (dizinleri ve haberleri geçmek) | Navigasyonel niyet resmî siteye ait |
| Çıplak marka — **sitesi olmayan/ölü 5 şirket** | **1. sıra** | Rakip yok; ortada doğru bilgi veren tek sayfa biziz |
| Marka + nitelik (`güvenilir mi`, `yorum`, `şikayet`, `kimin`) | **1. sıra, 39 şirketin çoğunda** | Şirket kendi sitesinde bu soruları cevaplamaz |
| Karıştırılan ad çiftleri (`x mi y mi`, `aynı şirket mi`) | **1. sıra** | Bu soruyu cevaplayan sayfa hiç yok |
| LLM cevapları (ChatGPT/Claude/Perplexity/AI Overviews) | **Alıntı kaynağı** | Navigasyon önyargısı yok; yapılandırılmış + kaynaklı metin kazanır |

**Sonuç:** "her şirket adında 1. sıra" gerçekçi değil. **"Her şirket adında görünmek,
niteleyicili her sorguda 1. sıra, ve şirket hakkında bir soru sorulduğunda alıntılanan
kaynak olmak"** gerçekçi — ve ticari değeri daha yüksek. Şirketin adını çıplak arayan
zaten müşterisi; niteleyici ekleyen kişi **karar aşamasında.**

---

## 2. Marka sorgu aileleri

39 şirketin her biri için sekiz aile. Sütunlar: nerede cevaplanır, 1. sıra şansı.

| № | Aile | Desen | Niyet | Nerede cevaplanır | Şans |
|---|---|---|---|---|---|
| B1 | Çıplak marka | `dağlı sigorta` | navigasyon | Profil sayfası | düşük / 5 şirkette yüksek |
| B2 | Güvenilirlik | `x sigorta güvenilir mi`, `x sigorta nasıl bir şirket` | araştırma | Profil → **yeni bölüm** | **yüksek** |
| B3 | Yorum ve şikâyet | `x sigorta yorumları`, `x sigorta şikayet`, `x sigorta hasar ödemiyor` | araştırma | Profil → **yeni bölüm** | **yüksek** |
| B4 | Erişim | `x sigorta telefon`, `x sigorta girne şube`, `x sigorta acenteleri` | navigasyon-alt | Profil iletişim bloğu | orta |
| B5 | Ürün × marka | `x sigorta trafik`, `x sigorta kasko fiyat` | ticari | Profil branş bölümü (çıpalı) | orta |
| B6 | Hasar × marka | `x sigorta hasar ihbarı nasıl yapılır` | acil | Profil → **yeni bölüm** → P3 rehberi | **yüksek** |
| B7 | Karşılaştırma | `x mı y mi`, `x sigorta vs y sigorta` | karar | **Set I** (yeni) | **yüksek** |
| B8 | Kurumsal kimlik | `x sigorta kimin`, `x sigorta türkiye'nin mi`, `x sigorta hangi bankanın` | araştırma | Profil → **yeni bölüm** · **Set H** | **yüksek** |

**B2, B3, B6 ve B8 bu planın merkezidir.** Dördü de şirketin kendi sitesinin
yapısal olarak cevaplayamadığı sorulardır: hiçbir şirket kendi sitesine
"güvenilir miyiz" ya da "bizden şikâyetçiyseniz nereye gidin" yazmaz.

### ⛔ Bu ailelerde brief'in sınırı

B2 ve B3 en riskli ailelerdir. ⛔ tablosu gereği **hiçbir sayfada** şunlar olamaz:

- Şirket bazında hasar ödeme performansı, prim, pazar payı, özkaynak, mali güç
- "En çok ödeyen", "en güvenilir", "tavsiye edilen" gibi sıralama iddiası
- Kullanıcı yorumu, yıldız, `AggregateRating` şeması

**"Güvenilir mi" sorusunun bu sitedeki cevabı bir not değil, bir açıklamadır:**

> *"Bu soruyu KKTC'de hiç kimse veriyle cevaplayamıyor — şirket bazında mali veri
> 2016'dan beri yayımlanmıyor. Doğrulayabildiğimiz altı şey şunlar: […]. Doğrulayamadığımız
> şeyler bunlar: […]. Karar sizin."*

Bu cevap hem doğru, hem sitenin tezi, hem de arama sonucunda rakiplerin veremediği cevap.
B2 ailesini kazandıracak olan tam olarak budur.

---

## 3. Kazanılabilirlik katmanları — 39 şirket

Şirketin kendi web varlığı ne kadar zayıfsa, o markanın adında bizim şansımız o kadar yüksek.

| Katman | Şirket | Durum | B1 hedefi | Öncelik |
|---|---|---|---|---|
| **K1 — rakipsiz** | 5 | Sitesi yok ya da ölü | **1. sıra** | 1 |
| **K2 — kartvizit** | 6 | Tek sayfalık site, SSL/HTTPS sorunlu | **2–3. sıra** | 2 |
| **K3 — vekil site** | 5 | KKTC'ye özel site yok; TR sitesinin alt sayfası | **2–4. sıra** | 3 |
| **K4 — kurulu** | 23 | Çok sayfalı çalışan site | 3–6. sıra + niteleyicilerde 1. | 4 |

### K1 — sitesi olmayan ya da ölü beş şirket

| Şirket | Bulgu |
|---|---|
| UNIVERSAL SİGORTA LTD. | Site yok. Birlik listesindeki resmî e-posta bir gmail adresi. |
| ZURICH SİGORTA A.Ş. | KKTC sitesi yok; zurichsigorta.com.tr bölge listesinde KKTC geçmiyor. |
| CORRECT CHOICE INSURANCE LTD. | DNS'te hiç çözülmüyor — alan adı süresi dolmuş görünüyor. |
| EAGER INSURANCE LTD. | Alan adı Plesk varsayılan paneline yönleniyor. |
| SEGURE INSURANCE LTD. | DNS çözülüyor (212.68.34.70), HTTP/HTTPS yanıt vermiyor. |

**Bu beş isim arandığında internette hiçbir şey yok.** Ruhsatlı bir şirketin adını arayıp
sonuç bulamayan insan bunu "şirket yok" diye okuyor. Doğru cevabı verecek tek sayfa bizimki.
Bu, planın **en yüksek getirili beş sayfasıdır** ve §5'te bir kural değişikliği gerektirir.

### K2 — kartvizit siteliler

EUROCITY · EIG · TOWER · LONDON · MAPFREE · AS-CAN.
Her birinin taşıyıcı bulgusu hazır: aynı IP'de iki şirket, hotmail/outlook e-postası,
tema geliştiricisinin Facebook linki, ödenmemiş şablonun "Buy Pro Version" metni,
sayfa başlığında duran `***TEST YAYINIDIR***` ibaresi.

### K3 — KKTC'ye özel varlığı olmayanlar

ANADOLU · AXA · GIG · TÜRKİYE SİGORTA · ZURICH.
Ortak bulgu ve ortak arama sorusu: *"Bu şirketin KKTC'de gerçekten şubesi var mı,
poliçemi kim düzenliyor?"* Dördünde de KKTC'ye özel ürün/teklif/hasar akışı **yok.**
GIG'de KKTC adresi, telefonu ya da e-postası sitede hiç bulunmuyor.

---

## 4. İP-1 — Profil sayfası derinleştirme (35 sayfa, tek şablon)

**Bu planın tek en yüksek kaldıraçlı işi.** `_build/sablon/sirket-profil.html` dosyasına
dört bölüm eklenir; 35 sayfa aynı anda B2, B3, B6 ve B8 ailelerini cevaplamaya başlar.

**Mevcut durum:** sayfa başına ~600 kelime, bunun ~350'si özgün gövde.
Bir markanın adında dizinleri geçmek için yeterli değil.
**Hedef:** özgün gövdeyi ~650 kelimeye çıkarmak — tamamı **mevcut veriden türetilir,
yeni araştırma gerektirmez.**

### Eklenecek dört bölüm

#### 4.1 Cevap-önce özeti (H1'in hemen altı, ~55 kelime)

LLM'lerin ve AI Overviews'un çıkarıp alıntıladığı blok budur. Sabit iskelet:

```
{ad}, Kuzey Kıbrıs Sigorta ve Reasürans Şirketleri Birliği'ne üye ruhsatlı bir sigorta
şirketidir — acente değil. {sehir} merkezli, {kurulus_yili}'den beri faaliyette.
{brans_sayisi} branşta ürünü doğrulandı, {sehir_sayisi} şehirde ofisi var.
{online_cumlesi}. Hasar ödeme performansı ve mali gücü — KKTC'deki hiçbir şirkette
olduğu gibi — ölçülemiyor; nedeni aşağıda.
```

Kural: bu blokta puan geçmez, sıfat geçmez, bağlantı geçmez. Yalnız olgu.

#### 4.2 "{ad} güvenilir mi?" — B2

H2 tam olarak arama sorgusudur. Altında 40–60 kelimelik doğrudan cevap, sonra iki liste:

- **Doğrulayabildiklerimiz:** altı ölçütün `var` maddeleri, düz cümleyle
- **Hiç kimsenin doğrulayamadıkları:** mali güç · hasar ödeme oranı · ödenmiş sermaye
  — ve **bunun bu şirkete özgü olmadığı**, 2016'dan beri şirket bazında yayımlanmadığı

⛔ Bu bölümde "evet" ya da "hayır" cevabı verilmez. Verilirse site tezini çürütür.

#### 4.3 "{ad} ile ilgili sorununuzu nereye götürürsünüz" — B3 + B6

Üç basamak, şirkete göre değişkenli:

1. **Şirkete:** `{email}` · `{whatsapp}` · online hasar ihbarı var/yok (veriden)
2. **KKSRSB Sigorta Tahkim Komisyonu:** ne olduğu ⚠ *ücreti, limiti ve süresi tüzük
   metni okunmadığı için yazılmaz*
3. **Para, Kambiyo ve İnkişaf Sandığı İşleri Dairesi:** düzenleyici mercii
   ⚠ *merkezî tüketici şikâyet mercii belirsiz — öyle yazılır*

Sonunda `/tr/rehber/kaza-sonrasi-ilk-48-saat/` ve (üretildiğinde) hasar reddi yazısına bağlantı.

**Bu bölüm 35 sayfada aynı üç mercii anlatır ama şirkete özgü kanalları farklıdır.**
Şablon tekrarını kırmak için: online hasar ihbarı **olmayan** 30 şirkette
"bu şirkette online hasar ihbarı yok; ihbar telefon ya da WhatsApp ile yapılıyor"
cümlesi girer — ki bu, o şirkete özgü doğrulanmış bir olgudur.

#### 4.4 "{ad} kimin şirketi" — B8

`sirket_turu` alanı dört değer alıyor; dördü dört ayrı cevap üretir:

| `sirket_turu` | Cevap iskeleti |
|---|---|
| `yerel` | KKTC'de kurulmuş, KKTC yasalarına tabi ayrı tüzel kişi. Türkiye'deki aynı adlı şirketle ilgisi yok. |
| `banka_bagli` | Ana hissedar {banka}. Şube ağı bankanın şubeleriyle örtüşüyor. Poliçe yine sigorta şirketinin. |
| `tr_subesi` | Türkiye merkezli şirketin KKTC şubesi. **KKTC şubesine hangi mevzuatın uygulandığı doğrulanmadı** — öyle yazılır. |
| `bilinmiyor` | Şirket türü Birlik listesinden ve siteden çıkarılamadı. Bu, boşluğun kendisidir. |

`bilinmiyor` **11 şirkette** geçerli — bu tek başına bir şeffaflık bulgusudur ve
P5 sütununa da gider.

#### 4.5 SSS bloğu — beş soru, `FAQPage` şeması

Her soru bir marka sorgusudur, her cevap 40–70 kelimedir, hepsi veriden üretilir:

1. `{ad} ruhsatlı bir sigorta şirketi mi?`
2. `{ad} güvenilir mi?` → 4.2'nin özeti
3. `{ad} hangi sigortaları yapıyor?` → `branslar[]`
4. `{ad}'a nasıl ulaşılır?` → `ofis_sehirler[]` + iletişim
5. `{ad} ile ilgili şikâyetimi nereye götürürüm?` → 4.3'ün özeti

Koşullu altıncı soru — yalnız §6'daki 16 şirkette:
`{ad}, {karıştırılan ad} ile aynı şirket mi?`

> ⚠ **`FAQPage` zengin sonuç beklentisi kurulmaz.** Google 2023'ten beri FAQ zengin
> sonucunu yalnız kamu ve sağlık sitelerinde gösteriyor. Bu şema burada **zengin sonuç
> için değil, LLM ve AI Overviews çıkarımı için** konuyor. Plan bunu vaat olarak yazmaz.

### İP-1 çıktısı

| Ölçü | Önce | Sonra |
|---|---|---|
| Özgün gövde kelime | ~350 | ~650 |
| Cevaplanan sorgu ailesi | B1, B4, B5 | B1–B6, B8 |
| Sayfada H2 olarak duran arama sorgusu | 0 | 3 |
| Dosya değişikliği | — | **1 şablon + `uret.py`'de bir üretici fonksiyon** |

---

## 5. İP-2 — K1'deki beş şirket ve eşik kuralının revizyonu

`02-programatik-seo.md` §2, dört şirketi ayrı URL'den **dışlıyor:**
`zurich-sigorta` · `correct-choice-insurance` · `eager-insurance` · `segure-insurance`.
Gerekçe: adres, e-posta, branş ve dil verisinin dördü de boş.

**Bu kural, kullanıcının hedefiyle doğrudan çelişiyor** — dışlanan dört şirket,
marka adında 1. sıranın **tek gerçekçi olduğu** şirketler.

### Önerilen revizyon

Eşik "veri var mı" değil, **"özgün ve doğrulanmış bir şey söyleyebiliyor muyuz"** olur.
Dördünde de söyleyebiliyoruz:

| Şirket | Sayfanın taşıyıcı olgusu |
|---|---|
| ZURICH SİGORTA A.Ş. | Birlik listesinde ruhsatlı; **Türkiye'deki Zurich Sigorta'nın bölge müdürlükleri listesinde KKTC yok.** İlişkinin niteliği doğrulanamadı. |
| CORRECT CHOICE | Alan adı DNS'te hiç çözülmüyor — A ve NS kaydı yok. |
| EAGER INSURANCE | Alan adı Plesk Obsidian 18.0.78 varsayılan paneline yönleniyor; SSL geçersiz. |
| SEGURE INSURANCE | DNS çözülüyor, ne HTTP ne HTTPS yanıt veriyor (curl 000). |

**Sayfa iskeleti (kısa, dört bölüm):**

1. `{ad} ruhsatlı mı?` → Evet, Birlik üye listesinde. Ruhsat ≠ çalışan web sitesi.
2. `Neden hiçbir bilgi bulunamıyor?` → yukarıdaki teknik bulgu, tarih ve yöntemle
3. `Bu şirketten poliçeniz varsa` → poliçe geçerliliği hakkında **iddia yok**;
   Birlik ve Daire iletişimi verilir
4. `Bu sayfayı düzeltme` → şirket bilgi gönderirse yayımlarız, düzeltme tarihi yazılır

⛔ Yazılmayacak: "faaliyette değil", "kapandı", "tasfiye", "dikkat". Elimizde
yalnızca **web varlığı gözlemi** var; faaliyet durumu gözlemi yok. Bu ayrım her sayfada
açıkça yazılır.

**5 sayfa. Yayın sırasında 1. iş.** İP-1'den bile önce yayımlanabilir, çünkü şablon
değişikliği beklemiyor.

> **Yasal not:** Bu beş sayfa planın hukuken en hassas parçasıdır. Kural: yalnız
> ölçülen teknik durum yazılır, tarihiyle ve yöntemiyle; şirketin durumu hakkında
> çıkarım yazılmaz. §13'e bakınız.

---

## 6. Set H — Karıştırılan adlar (16 sayfa)

**URL:** `/tr/sirketler/karsilastirma/<a>-<b>/`
**Hedef desen:** `x sigorta ile y sigorta aynı mı`, `x sigorta türkiye'nin mi`,
`x sigorta hangi bankanın`
**1. sıra şansı: yüksek.** Bu soruyu cevaplayan hiçbir sayfa yok.

Bu, planın **en özgün** setidir. Veriden çıkan ad karışıklıkları:

### H-a · Türkiye'deki aynı adlı şirketle karışanlar (5)

| Sayfa | Cevabın çekirdeği |
|---|---|
| Türk Sigorta ↔ Türkiye Sigorta (KKTC) | **İki ayrı KKTC şirketi.** Türk Sigorta = TurkishBank Group, yerel; Türkiye Sigorta = TR şubesi. Adları bir harf farklı. |
| Şeker Sigorta (Kıbrıs) ↔ Şeker Sigorta (TR) | Bağın niteliği **doğrulanmadı** — öyle yazılır. |
| Güven Sigorta (Kıbrıs) ↔ Güven Sigorta (TR) | `tr_ortakligi` olarak kayıtlı; ortaklık payı doğrulanmadı. |
| Anadolu Sigorta KKTC ↔ Anadolu Sigorta (TR) | Şube. KKTC'ye özel teklif/satın alma ekranı yok. |
| AXA Sigorta KKTC ↔ AXA | Bağımsız KKTC sitesi yok; TR sitesi içinde "Kıbrıs Şubemiz" bölümü. KKTC'ye özel ürün **var** (Kıbrıs Özel Sağlık Sigortası). |

### H-b · Küresel markayla karışanlar (4)

| Sayfa | Cevabın çekirdeği |
|---|---|
| MAPFREE Insurance ↔ MAPFRE | ⛔ **Bağlantı iddiası yazılmaz.** Sayfa: MAPFREE 2011'de %100 yerel sermaye ile kurulmuş; yazımı da farklı; bir bağ **bulunamadı.** |
| Zurich Sigorta (KKTC) ↔ Zurich Insurance Group | Bağ doğrulanamadı; TR bölge listesinde KKTC yok. |
| London Insurance ↔ Birleşik Krallık | Alan adı `.com.tr`. Hazır WordPress teması, footer Facebook linki tema geliştiricisine gidiyor. Bir UK bağı **bulunamadı.** |
| GİG Sigorta ↔ gig.com.tr | Site tamamen Türkiye merkezli; KKTC adresi/telefonu/e-postası sitede yok. |

### H-c · Bankayla karışanlar (4)

Limasol Sigorta ↔ Limasol Türk Kooperatif Bankası · Creditwest Sigorta ↔ Creditwest Bank ·
Akfinans Sigorta ↔ Akfinans Bank · Kıbrıs İktisat Sigorta ↔ İktisatbank.

Ortak cevap: *"Banka ile aynı grup, ama poliçenizi düzenleyen ayrı tüzel kişi;
şikâyet yolu banka değil sigorta şirketi ve KKSRSB."* Akfinans'ta ek bulgu:
site `akfinans.one`, e-posta `akfinans.com`, Facebook linki bankaya gidiyor.

### H-d · Birbirine benzeyen yerel adlar (3)

| Sayfa | Cevabın çekirdeği |
|---|---|
| Can Sigorta ↔ As-Can Sigorta | İki ayrı ruhsatlı şirket. Can 1958'den beri, çalışan online poliçe; As-Can'ın sitesi SSL'siz ve başlıkta `***TEST YAYINIDIR***` yazıyor. |
| Kıbrıs Sigorta ↔ Kıbrıs İktisat ↔ Kıbrıs Kapital | Üç ayrı şirket, üç ayrı hissedar yapısı. Kıbrıs Sigorta KKTC'nin ilk yerel şirketi (01.09.1995). |
| Eurocity ↔ EIG | **İkisi de ayrı ayrı ruhsatlı; siteleri aynı IP'de (104.247.162.35) ve aynı şablonda.** Gözlem yazılır, yorum yazılmaz. |

> Eurocity–EIG sayfası bu setin en dikkatli yazılacak sayfasıdır. Cümle şudur:
> *"İki alan adı aynı IP adresinde ve aynı şablonda yayınlanıyor. Bu bir mülkiyet
> ilişkisi kanıtı değildir — ortak barındırma da aynı sonucu verir. İki şirkete
> sorduk / soracağız; cevap gelirse buraya yazılır."*

### Şablon (16 sayfa ortak)

1. **Tek cümlelik cevap** — "Hayır, ayrı iki şirket" / "Aynı grup, ayrı tüzel kişi" /
   "Bir bağ bulunamadı"
2. Yan yana tablo: ruhsat · tür · kuruluş · merkez · branş sayısı · alan adı
3. **Karışıklık nereden geliyor** — adın kaynağı
4. **Sizin için pratik farkı ne** — poliçe kimden, hasar kime, şikâyet nereye
5. Doğrulayamadıklarımız
6. İki profile bağlantı + kaynak

Şema: `FAQPage` + `BreadcrumbList`. Ana soru H1'de, aynen sorgu biçiminde.

---

## 7. Set I — Karşılaştırma sayfaları (28 çift)

**URL:** `/tr/sirketler/karsilastirma/<a>-<b>/` (Set H ile aynı desen, aynı şablon)
**Hedef desen:** `x sigorta mı y sigorta mı`, `kktc en iyi sigorta şirketi hangisi`

### Çift seçme kuralı — sayıyı bu kural belirler, biz değil

> Bir çift sayfa olur ancak **genel puanı 5,0 ve üstü** olan iki şirketse **ve**
> altı ölçütün **en az beşinde** puanları 1,5 puan ya da daha fazla ayrışıyorsa.

Ayrışmayan iki şirketin karşılaştırma sayfası hiçbir şey söylemez ve ince sayfadır.

Veriden hesaplanan dağılım (15 şirket, 105 olası çift):

| Ayrışan ölçüt | Çift sayısı | Sayfa? |
|---|---|---|
| 6 | 4 | ✓ |
| 5 | 24 | ✓ |
| 4 | 35 | ✗ |
| 3 | 30 | ✗ |
| 0–2 | 12 | ✗ |

**28 sayfa.** 105 değil. Alınmayan 77 çift bilinçli olarak alınmıyor —
`02-programatik-seo.md` §6'daki branş × şehir matrisi kararıyla aynı gerekçe.

En güçlü dördü: `dağlı × kıbrıs iktisat` · `limasol × anadolu` · `can × bicare` ·
`creditwest × commercial`.

### ⛔ Bu sette yazılmayacaklar

- "Hangisi daha iyi" cevabı. Sayfa **ayrışmayı** gösterir, seçimi göstermez.
- Fiyat karşılaştırması. Taban tarife rejimi nedeniyle prim farkı zaten sınırlı ve
  şirket bazında prim verisi yok.
- Hasar ödeme karşılaştırması. Veri yok.
- `AggregateRating`, `Review`, yıldız.

Her sayfanın kapanışı sabittir: *"Bu tablo iki şirketin **yayımladıklarını**
karşılaştırır. Hangisinin hasarınızı daha iyi ödediğini göstermez — o veri KKTC'de
yayımlanmıyor."*

---

## 8. ⛔ Üretilmeyecekler

Marka sorgularında hacim kolayca elde edilir; bu plan üçünü bilinçle almıyor.

| Üretilmeyecek | Hacim | Gerekçe |
|---|---|---|
| **Marka × branş** (`/tr/sirketler/dagli-sigorta/trafik/`) | 39 × 12 = **468** | Aynı profil verisinin permütasyonu. Profil sayfasında çıpalı bölüm (`#trafik`) aynı sorguyu karşılar ve tek güçlü sayfa 12 ince sayfayı yener. |
| **Marka × şehir** (`dağlı sigorta girne`) | 39 × 5 = **195** | Aynı gerekçe. Profilin "Nereden ulaşılıyor" bölümü karşılar. |
| **Yorum/puan sayfaları** (`x sigorta yorumları`) — kullanıcı yorumu toplayan | 39 | Brief'in tek iddiasını çürütür: elimizde doğrulanmış müşteri deneyimi yok. B3 ailesi **doğrulanabilir gözlemle** karşılanır, yorumla değil. |
| **Tüm 105 çift** için karşılaştırma | 77 fazla | §7'deki ayrışma kuralı. |

Toplam alınmayan hacim: **739 sayfa.** 35 iyi profilin güvenilirliği, 739 ince sayfadan
daha değerli — ve marka sorgusunu kazandıracak olan güvenilirliktir.

---

## 9. Varlık (entity) ve şema işleri

Bir markanın adında görünmek için Google'ın sayfayı **o varlıkla ilişkilendirmesi** gerekir.
Şu anda profil sayfaları çıplak bir `Organization` düğümü basıyor — bu, sayfanın
şirketin **kendisi** olduğunu ima ediyor. Üçüncü taraf profil sayfası için doğru işaretleme
bu değil.

### 9.1 Şema düzeltmesi (`sirket-profil.html`)

```jsonld
{
  "@type": "ProfilePage",
  "dateModified": "{tarama_tarihi}",
  "mainEntity": {
    "@type": "Organization",
    "name": "{ad}",
    "url": "{kaynak_url}",
    "sameAs": ["{web}", "{instagram}", "{facebook}"],
    "foundingDate": "{kurulus_yili}",
    "email": "{email}",
    "address": { "@type": "PostalAddress", ... },
    "areaServed": "Cyprus",
    "parentOrganization": { "@type": "Organization", "name": "{ana_kurulus}" }
  }
}
```

- `sameAs` **varlık eşleşmesinin ana sinyalidir** — resmî site ve doğrulanmış sosyal
  hesaplar. Veride hazır, şu anda kullanılmıyor.
- `parentOrganization` yalnız `banka_bagli` ve `tr_subesi` şirketlerde, **yalnız
  doğrulanmışsa** basılır. `bilinmiyor` olan 11 şirkette basılmaz.
- `ProfilePage` + `mainEntity`, sayfanın şirket **hakkında** olduğunu söyler; sayfanın
  şirket olduğunu değil.
- ⛔ `AggregateRating` yok, `Review` yok. (Zaten kural.)

### 9.2 Otomatik marka bağlama — `uret.py`

Bir rehber yazısı içinde bir şirket adı geçtiğinde, **ilk geçişte** o şirketin profiline
otomatik bağlanır. `sirketler.json`'daki `ad` ve yaygın kısa adlar (Dağlı, Limasol,
Türk Sigorta …) bir eşleme tablosundan taranır.

Kazanç: 78 yazılık kuyruk tamamlandığında her profil sayfası, konusuyla ilgili
onlarca yazıdan bağlantı alır. Marka sorgusunda iç bağlantı derinliği belirleyicidir
ve bu, elle bağlantı koymadan elde edilir.

Kural: bir yazıda aynı şirkete en fazla bir bağlantı; başlıklarda bağlama yok.

### 9.3 Marka sorguları için iç bağlantı hattı

```
/tr/sirketler/  (39 şirket dizini)
   ├→ profil ×35            ← B1, B2, B3, B4, B5, B6, B8
   │    ├→ karsilastirma/   ← B7 · her profil kendi 2–3 çiftine bağlanır
   │    ├→ /tr/sirketler/<brans>/   ← branş listeleri (Set B)
   │    └→ /tr/rehber/…     ← hasar ve şikâyet yolu yazıları
   └→ "Veri toplayamadığımız şirketler" → K1 sayfaları ×5
```

Her karşılaştırma sayfası iki profile, her profil en az iki karşılaştırmaya bağlanır.
Öksüz sayfa kalmaz — `_build/uret.py --kontrol` bunu denetler.

---

## 10. Rehber kuyruğuna eklenecek yazılar

Marka sorgularını **hub** olarak besleyen yazılar. `copy/yayin-kuyrugu.md` biçiminde,
oraya doğrudan yapıştırılabilir. Ağustos–Eylül bloklarının **sonuna** eklenir;
mevcut sıra bozulmaz (kuyruk kuralı 1).

| № | Durum | Başlık | Kategori | Hedef sorgu | Zorunlu bağlantı | İlan edilecek boşluk |
|---|---|---|---|---|---|---|
| M1 | ⬜ | KKTC'de ruhsatlı 39 sigorta şirketinin tam listesi | Şirket seçimi | kktc sigorta şirketleri listesi | `/tr/sirketler/` · `/tr/metodoloji/` | Birlik listesi dışında resmî bir güncel kayıt bulunamadı |
| M2 | ⬜ | Adında "Kıbrıs" ya da Türkiye'nin markası geçen şirketler aynı mı | Ayrım | kktc sigorta şirketi türkiyenin mi | `/tr/sirketler/` · Set H sayfaları | Beş şirkette TR bağının niteliği doğrulanamadı |
| M3 | ⬜ | Sigorta şirketiniz hakkındaki şikâyetinizi nereye götürürsünüz | Hasar | kktc sigorta şikayet nereye | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` · `/tr/duzeltme/` | Merkezî tüketici şikâyet mercii belirsiz; tahkim ücreti ve süresi okunmadı |
| M4 | ⬜ | Web sitesi olmayan beş ruhsatlı sigorta şirketi | Şeffaflık | kktc sigorta şirketi sitesi yok | K1 sayfaları ×5 · `/tr/sirketler/` | Faaliyet durumları gözlenmedi — yalnız web varlığı ölçüldü |
| M5 | ⬜ | Bankaya bağlı sigorta şirketinden poliçe almak ne değiştirir | Şirket seçimi | kktc banka sigorta şirketi | Set H-c sayfaları · `/tr/sirketler/` | Grup içi yükümlülük yapısı doğrulanmadı |
| M6 | ⬜ | Bir sigorta şirketinin güvenilirliğini KKTC'de neye bakarak ölçebilirsiniz | Şeffaflık | kktc sigorta şirketi güvenilir mi | `/tr/metodoloji/` · `/tr/sirketler/` | Mali güç ve hasar ödemesi hiçbir şirkette ölçülemiyor |
| M7 | ⬜ | İki sigorta şirketinin sitesi aynı IP'de: Eurocity ve EIG | Şeffaflık | eurocity eig sigorta | Set H-d Eurocity–EIG · iki profil | Ortak barındırma mı ortak mülkiyet mi — ayırt edilemedi |
| M8 | ⬜ | Türkiye'deki sigorta şubesinden KKTC'de poliçe almak | Ayrım | kktc türkiye sigorta şubesi | Set H-a sayfaları · `/tr/sigorta/trafik/` | KKTC şubelerine hangi mevzuatın uygulandığı doğrulanmadı |

M6, kuyruktaki mevcut **№24** ("Puanlama modelimiz neden mali gücü içermiyor") ile
komşu konudadır. İkisi birleştirilmez: №24 yöntemi anlatır, M6 okurun kendi
kontrol listesini verir ve `x sigorta güvenilir mi` desenini hedefler.

---

## 11. Site dışı — varlık sinyalleri

Marka sorgusunda sıralamanın site içi olmayan tek bileşeni budur.

| İş | Neden | Not |
|---|---|---|
| **Haber sitelerine bulgu vermek** | `yeniduzen.com` ve `kibrismanset.com` şirket adlarında **zaten sıralanıyor.** Bu domainlerden gelen bir bağlantı marka sorgularında doğrudan işe yarar. | Verilecek üç bulgu hazır: 39 şirketin 3'ü genel şartları yayımlıyor · 5 şirketin çalışan sitesi yok · 2024→2025 taban primlerde ~%60–65 artış. Haber değeri gerçek, satın alınmış bağlantı değil. |
| **KKSRSB ile temas** | Birlik'in üye listesi her marka sorgusunda çıkıyor. Veri düzeltmelerimizi Birlik'e bildirmek hem doğru, hem ilişki kurar. | Bağlantı talep edilmez, düzeltme bildirilir. |
| **Wikidata varlıkları** | KKTC sigorta şirketlerinin çoğunun Wikidata kaydı yok. Kayıt, Google'ın varlık grafiğini besler. | Yalnız doğrulanmış alanlar girilir; kendi sitemiz kaynak olarak **gösterilmez** — birincil kaynak gösterilir. |
| **Şirketlere düzeltme daveti** | `/tr/duzeltme/` bağlantısını 35 profilden şirkete bildirmek | Yanıt gelirse sayfa güçlenir, gelmezse "sorduk, yanıt gelmedi" satırı yazılır — ikisi de içerik. |

⛔ Yapılmayacak: dizin sitelerine toplu kayıt, bağlantı satın alma, şirket adlarıyla
reklam. Site poliçe satmıyor; ölçü trafik değil alıntılanabilirlik.

---

## 12. EN sürümü

`02-programatik-seo.md` §9 Set A'nın EN açılımını zaten öneriyor. Marka sorgularında
EN'in kendi gerekçesi var: **17 şirket İngilizce hizmet verdiğini beyan ediyor** ve
expat kitlesi şirket adını İngilizce niteleyicilerle arıyor
(`is x insurance reliable`, `x insurance cyprus reviews`).

| Set | TR | EN | Gerekçe |
|---|---|---|---|
| İP-1 derinleştirme | ✓ 35 | ✓ 35 | Aynı veriden üretilir |
| İP-2 K1 sayfaları | ✓ 5 | ✓ 5 | Expat için de rakipsiz |
| Set H karıştırılan adlar | ✓ 16 | ✓ 9 | Yalnız H-a ve H-b; banka karışıklığı yerel bir sorun |
| Set I karşılaştırma | ✓ 28 | ✗ | Önce TR'de indekslenme ölçülür |

RU ve FA bu planda **yok.** Şirket profilini Rusça ya da Farsça arayan bir kitle
varsayımı doğrulanmadı — veri yok, sayfa yok.

---

## 13. Risk ve sınırlar

Bu plan, adları geçen **gerçek şirketler** hakkında sayfa üretiyor. Üç kural bağlayıcıdır.

**1. Yalnız ölçülen yazılır, çıkarım yazılmaz.**
"Sitesi yanıt vermiyor" ölçümdür. "Şirket faaliyette değil" çıkarımdır ve yazılmaz.
"İki alan adı aynı IP'de" ölçümdür. "Aynı şirket" çıkarımdır ve yazılmaz.

**2. Her ölçüm tarihli ve yöntemlidir.**
Her sayfada: neyin, ne zaman, nasıl ölçüldüğü. "Temmuz 2026'da tarandı" yeterli değil —
K1 ve K2 sayfalarında yöntem de yazılır (DNS sorgusu, HTTP durum kodu, SSL zinciri).

**3. Düzeltme yolu her sayfada görünür ve gerçekten işler.**
`/tr/duzeltme/` bağlantısı her profilde ve her karşılaştırma sayfasında. Bir şirket
düzeltme gönderdiğinde **48 saat içinde** incelenir; kabul edilirse sayfa güncellenir
ve düzeltme tarihi sayfaya yazılır. Bu, hem doğru davranıştır hem de itiraz karşısındaki
tek savunmadır.

**Ölçek riski:** 35 profil + 5 K1 + 44 karşılaştırma = **84 sayfa, 39 gerçek şirket
hakkında.** Bu, sitenin sorumluluğunu artırır. Yayın öncesi §14'teki kapılar
istisnasız uygulanır.

---

## 14. Kalite kapıları

- [ ] Hiçbir sayfada şirket bazında prim, hasar, pazar payı, özkaynak, mali güç yok
- [ ] Hiçbir sayfada "en iyi", "en güvenilir", "tavsiye" yok
- [ ] `AggregateRating` ve `Review` şeması hiçbir yerde yok
- [ ] "Güvenilir mi" bölümlerinin hiçbirinde evet/hayır cevabı yok
- [ ] K1 sayfalarında faaliyet durumu hakkında tek çıkarım cümlesi yok
- [ ] Eurocity–EIG sayfasında mülkiyet iması yok, ortak barındırma alternatifi yazılı
- [ ] MAPFREE ↔ MAPFRE ve Zurich sayfalarında bağ **iddiası** değil, bağ **bulunamadığı** yazılı
- [ ] Her sayfada en az bir "bunu doğrulayamadık" cümlesi
- [ ] Her sayfada ölçüm tarihi ve yöntemi
- [ ] Her sayfada `/tr/duzeltme/` bağlantısı
- [ ] Title'lar benzersiz, 60 karakter altı, şirket adı geçen title'da puan yok
- [ ] `ProfilePage` + `mainEntity` yapısı 35 profilde kurulu, `sameAs` dolu
- [ ] Marka × branş ve marka × şehir sayfaları üretilmemiş
- [ ] Öksüz sayfa yok — `python3 _build/uret.py --kontrol` temiz

---

## 15. Yayın sırası

| Sıra | İş | Sayfa | Emek | Neden bu sırada |
|---|---|---|---|---|
| 1 | **İP-2** — K1 beş şirket | 5 | düşük | Tek gerçek 1. sıra fırsatı; şablon değişikliği beklemiyor |
| 2 | **İP-1** — profil derinleştirme | 35 (mevcut) | orta, tek şablon | Tek dosya değişikliğiyle 35 sayfa B2/B3/B6/B8'i cevaplamaya başlar |
| 3 | **§9.1** — şema düzeltmesi | 35 (mevcut) | düşük | İP-1 ile aynı dosya, aynı üretimde |
| 4 | **Set H** — karıştırılan adlar | 16 | orta | En yüksek 1. sıra şansı, en özgün içerik |
| 5 | **§9.2** — otomatik marka bağlama | — | düşük | Kuyruk ilerledikçe kendiliğinden birikir; erken kurulmalı |
| 6 | **M1–M8** kuyruk yazıları | 8 | kuyruk hızında | Hub'lar; Set H ve profilleri besler |
| 7 | **Set I** — karşılaştırma | 28 | yüksek | İP-1 ve Set H indekslendikten sonra |
| 8 | **§11** — site dışı | — | sürekli | 1–4 yayında olmadan bulgu paylaşılmaz |
| 9 | **EN açılımı** | 49 | yüksek | TR'de indekslenme ölçüldükten sonra |

**Toplam yeni sayfa: 49 TR** (5 + 16 + 28) **+ 35 mevcut sayfanın derinleştirilmesi.**

**İP-1 yayımlanmadan Set H ve Set I yayımlanmaz** — ikisi de derinleşmiş profillere bağlanıyor.

---

## 16. Ölçüm

> **Şu anda ölçüm yok.** Site 5 Ağustos 2026'da aramaya açıldı; GSC verisi henüz
> anlamlı bir pencere oluşturmadı. Aşağıdaki hedefler **gerekçeli beklentidir**,
> taahhüt değil — ve GSC'den gerçek veri geldiğinde bu bölüm değiştirilir.

### İzlenecek sorgu kümesi

39 şirket adı × 8 sorgu ailesi. GSC'de sorgu filtresi olarak şirket adları listesi
kurulur; her ay dört bant raporlanır: **1 · 2–3 · 4–10 · 10+**.

### Beklenti

| | 3. ay | 6. ay | 12. ay |
|---|---|---|---|
| İndekslenen profil | 35/35 | 35/35 | 35/35 |
| Çıplak marka — ilk 10'da | 25/39 | 34/39 | 37/39 |
| Çıplak marka — 1. sıra | 2/39 (K1) | 5/39 (K1) | 5/39 |
| B2/B3 niteleyicili — 1. sıra | 5/39 | 20/39 | 30/39 |
| Karıştırılan ad sorguları — 1. sıra | — | 10/16 | 14/16 |
| LLM'de alıntılanma (elle örnekleme, 10 sorgu) | 2/10 | 5/10 | 7/10 |

**Çıplak markada 1. sıra hedefi 5'te kalıyor.** Bu bir eksiklik değil, §1'deki
gerçekliğin kabulü. Ticari değer 2. satırda değil, 4. ve 5. satırlarda.

### Ölçüm ayrımı

`02-programatik-seo.md` §10'daki sitemap ayrımı korunur ve genişletilir:
`sitemap-sirketler.xml` (profiller + K1) · `sitemap-karsilastirma.xml` (Set H + I) ·
`sitemap-rehber.xml` · `sitemap-sayfalar.xml`. Dört setin indekslenme oranı ayrı ölçülür.
