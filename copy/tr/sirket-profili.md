# Şirket profili — şablon · /tr/sirketler/{slug}/

**Durum:** 33 sayfa üretecek tek şablon. Bu dosya o sayfaların **metnidir** —
değişkenler `{süslü parantez}` içinde, koşullu bloklar `EĞER` ile işaretli.

**Sayfa amacı:** Bir şirket hakkında dışarıdan doğrulanabilen her şeyi tek yerde vermek —
ve doğrulanamayanı ilan etmek.
**Okur:** Bir adı duymuş, "bu şirket ciddi mi" diye bakan kişi.
**Tek eylem:** Aynı branştaki başka bir şirketle karşılaştırmak.

**Kaynak veri:** `data/sirketler.json` · **Şablon:** `_build/sablon/sirket-profil.html`

> **Bu şablonun tek testi:** Sayfa, şirketin kendi sitesinden kopyalanmış gibi
> okunuyorsa başarısızdır. Şirketin **kendi sitesinde bulamayacağınız** şeyi
> söylemiyorsa yayımlanmaz.

---

## Meta

**Title:** `{ad} — KKTC sigorta şirketi profili`
*60 karakteri aşan adlarda "CO LTD.", "ŞTİ. LTD.", "A.Ş." kısaltmaları düşürülür.*

**Meta description (üç varyant — veri durumuna göre seçilir):**

| Koşul | Metin |
|---|---|
| Branş ≥ 8 | `{sehir} merkezli {ad}. {brans} branşta ürün, {sehir_sayisi} şehirde ofis. Şeffaflık, dijital hizmet ve dil desteğinde ne doğrulayabildiğimiz.` |
| Branş 4–7 | `{sehir} merkezli {ad}. {brans} branşta ürün doğrulandı. Hangi bilgileri yayımladığı, hangilerini yayımlamadığı.` |
| Boşluk var | `{sehir} merkezli {ad}. {brans} branş doğrulandı; {bosluk_sayisi} ölçütte veri toplanamadı. Neyi bulabildiğimiz, neyi bulamadığımız.` |

*Neden üç varyant: 33 sayfada aynı cümle iskeleti tekrarlarsa Google bunu tek şablon
sayar. Ayrıca veri fakiri bir şirketin description'ı zengin bir şirketinkiyle aynı
vaadi vermemeli — vermediğimiz şeyi vaat etmiş oluruz.*

**H1:** `{ad}`

*Neden sade: başlıkta puan yok. "8,6 puanlı sigorta şirketi" arama sonucunda bir
derecelendirme iddiası gibi görünür. Puan bir gözlem, unvan değil.*

---

## Bölüm 1 — Başlık bloğu

**Eyebrow:** `{sehir}` · `{sirket_turu_metni}`

**Şirket türü metni — sabit karşılıklar:**

| Veri | Ekranda |
|---|---|
| `yerel` | KKTC'de kurulmuş yerel şirket |
| `tr_subesi` | Türkiye şirketinin KKTC şubesi |
| `tr_ortakligi` | Türkiye sigortacısıyla yerel ortaklık |
| `banka_bagli` | Banka grubuna bağlı |
| `bilinmiyor` | Şirket yapısı doğrulanamadı |

**Alt satır:**
> Kuzey Kıbrıs Sigorta ve Reasürans Şirketleri Birliği üyesi. Ruhsatlı sigorta şirketi —
> acente değil.

*Neden bu cümle her profilde: sitenin üç ayrımından biri. Okur bir acente adını arayıp
buraya düştüğünde farkı burada görecek.*

**EĞER `kurulus_yili` varsa:** `{yil}'den beri faaliyette`
**EĞER yoksa:** satır **görünmez.** "Bilinmiyor" yazılmaz — başlık bloğunda boşluk
ilanı yapılmaz, o iş 4. bölümün.

---

## Bölüm 2 — Tek cümlelik özet

**Bu, sayfanın en önemli 30 kelimesi ve şablondan gelmez.** Her şirket için `notlar`
alanından elle yazılır.

**Yazım kuralı:** Şirketin kendi sitesinde bulunmayan, bizim gözlemlediğimiz bir şeyi
söyler. Övgü ya da suçlama değil, gözlem.

**Üç örnek — üçü de gerçek veriden:**

> **Dağlı Sigorta:** 1967'den beri faaliyette ve listedeki en geniş gerçek dil desteğine
> sahip: Türkçe, İngilizce, Rusça, Yunanca. Acente sayısı sitede iki farklı yerde iki
> farklı rakamla veriliyor — metinde 25, footer'da 22.

> **Creditwest Sigorta:** On branşta ürün, çalışan bir online poliçe akışı ve online hasar
> bildirim formu var — bu üçünü birden yapan şirket az. Buna karşılık tek ofisi var ve
> kuruluş yılını yayımlamıyor.

> **London Insurance:** Hazır bir WordPress teması varsayılan ayarlarıyla kullanılıyor;
> footer'daki Facebook bağlantısı şirkete değil, temanın geliştiricisine gidiyor.
> Sitede e-posta, adres ve telefon yayımlanmamış.

*Neden bu bölüm zorunlu: 33 sayfayı birbirinden ayıran şey bu. Bu cümle yazılamıyorsa
o şirket hakkında söyleyecek özgün bir şeyimiz yok demektir — sayfa üretilmez, şirket
listede kalır.*

---

## Bölüm 3 — Altı ölçüt

**H2:** Neyi ölçtük

**Giriş cümlesi (sabit):**
Altı ölçütün her birinde şirketin ne yayımladığına baktık. Aşağıda puanın yanında
**puanın dayandığı liste** var — böylece katılmadığınız yeri görebilirsiniz.

*Neden liste puanla birlikte: puan tek başına bir iddia. Yanındaki "var/yok" listesi
onu denetlenebilir bir ölçüme çeviriyor. Okur bizim hesabımıza değil, kendi gözüne bakar.*

**Her ölçüt kartı:**

```
{Ölçüt adı}                          ağırlık %{n}        {puan}/10
Bulduklarımız:   {var[] listesi}
Bulamadıklarımız: {yok[] listesi}
```

**Altı ölçüt ve sabit ağırlıkları** *(metodoloji sayfasıyla birebir aynı kalır)*:
Şeffaflık ve doğrulanabilirlik %25 · Ürün genişliği %20 · Erişilebilirlik %20 ·
Dijital hizmet %20 · Yabancı dil %10 · Kurumsal derinlik %5

**Bölüm sonu — sabit uyarı:**
> Bu altı ölçüt şirketin **görünürlüğünü** ölçer. Hasarınızı ödeyip ödemeyeceğini
> ölçmez; o veri KKTC'de yayımlanmıyor. [Nasıl puanlıyoruz →](/tr/metodoloji/)

---

## Bölüm 4 — Neyi doğrulayamadık

**Bu bölüm her profilde vardır. Boş geçilmez.**

**EĞER `veri_yok_olcutler` doluysa:**

**H2:** Doğrulayamadığımız ölçütler

> **{Ölçüt adı} puanlanmadı.** {sebep}
> Bu ölçütün ağırlığı diğerlerine dağıtıldı; şirketin genel puanı beş ölçüt üzerinden
> hesaplandı. Eksik bir puan, düşük bir puan değildir.

*Örnek — London Insurance:* "Kurumsal derinlik puanlanmadı. Kuruluş yılı ve şirket
yapısı doğrulanamadı."

**EĞER `veri_yok_olcutler` boşsa:**

**H2:** Bu sayfada eksik veri yok

> Altı ölçütün altısını da puanlayabildik. Bu, şirketin her bilgiyi yayımladığı anlamına
> gelmiyor — yayımlamadıkları yukarıda "bulamadıklarımız" satırlarında duruyor.

**Her iki durumda da sayfa altındaki sabit blok:**
> **Herkeste eksik olan iki şey:** mali güç ve hasar ödeme performansı. Bunlar bu
> şirkette değil, KKTC'de hiçbir şirkette ölçülemiyor — 2016'dan beri şirket bazında
> yayımlanmıyorlar. [Neyi doğrulayabildiğimizi görün →](/tr/veri-bosluklari/)

*Neden ayrı bir bölüm hak ediyor: bu sitenin tek satılık iddiası. Bir dipnota
gömülürse iddia da gömülür.*

---

## Bölüm 5 — Branş matrisi

**H2:** Hangi branşlarda ürünü var

12 satırlık liste. ✓ olanlar tür hub'ına bağlanır, — olanlar bağlanmaz.

**Liste altı — sabit:**
> Bu liste şirketin **kendi sitesindeki ürün sayfalarından** derlendi. Bir branşın
> işaretsiz olması şirketin o ürünü satmadığı anlamına gelmez; sitesinde bulamadığımız
> anlamına gelir. Merkezî bir "hangi şirket hangi branşı satıyor" kaydı KKTC'de yok.

*Neden bu uyarı: matris bir iddia gibi okunuyor. Kaynağını ve sınırını söylemek onu
gözleme çeviriyor. Aynı zamanda şirketlerin düzeltme göndermesini davet ediyor.*

**EĞER branş sayısı ≥ 8:** `{brans} branşta ürün doğrulandı — listedeki en geniş
yelpazelerden biri.`
**EĞER 4–7:** `{brans} branşta ürün doğrulandı. Ortalama {ort} branş.`
**EĞER ≤ 3:** `Yalnızca {brans} branşta ürün sayfası bulunabildi.`

---

## Bölüm 6 — Erişim

**H2:** Nereden ulaşılıyor

**Ofis şehirleri:** `{ofis_sehirler}` — her biri şehir listesine bağlanır.

**EĞER `acente_sayisi` varsa:**
> **{n} acente** — *şirket beyanı, bağımsız olarak doğrulanmadı*

*Etiket zorunlu. Bu rakamlar şirketlerin kendi sitelerinden geliyor ve en az bir
şirkette kendi sitesinde bile tutarsız.*

**EĞER tek şehir:**
> Yalnızca {sehir}'da ofisi var. Hasar anında yüz yüze görüşmeniz gerekirse mesafe
> bir maliyettir.

**Sabit bağlam cümlesi:**
> Karşılaştırma için: 39 ruhsatlı şirketin 36'sının merkezi Lefkoşa'da. Girne'de iki,
> Gazimağusa'da bir şirket merkezli; İskele ve Güzelyurt'ta merkezi olan hiç yok.

---

## Bölüm 7 — Dijital denetim

**H2:** Sitesi ve dijital hizmetleri

Dört satır, ✓ / — ile: online teklif · online poliçe · online hasar ihbarı · mobil uygulama

**Web sitesi durumu — `http_durum` alanında yalnızca üç değer var:**

| Veri | Ekranda |
|---|---|
| `200` | Site çalışıyor — Temmuz 2026'da test edildi |
| `ölü` | **Site yanıt vermiyor** — Temmuz 2026'da test edildi |
| `site_yok` | **Şirketin web sitesi bulunamadı** |

**EĞER `notlar` bot koruması veya sertifika sorunundan söz ediyorsa** — Creditwest'te
Cloudflare 403'ü, Eurocity/EIG/Tower'da geçersiz SSL gibi — bu ayrıntı burada tek
cümleyle yazılır. Ham HTTP kodu ekrana yazılmaz; okurun işine yarayan şey kodun kendisi
değil, siteye girip giremeyeceği.

**Sabit bağlam:**
> 39 şirketin 34'ünün sitesi çalışıyor. Üç site ölü, iki şirketin sitesi hiç yok.

**EĞER `police_sartlari_yayinda` false:**
> **Poliçe genel şartlarını yayımlamıyor.** 39 şirketin yalnızca üçü yayımlıyor —
> bu, sektörün geneli. Genel şartların resmî metinlerine KKSRSB'den Türkçe ve
> İngilizce ulaşabilirsiniz.

*Neden hemen ardından sektör oranı: tek başına "yayımlamıyor" bir suçlama. "39'un 36'sı
yayımlamıyor" ise bir sektör bulgusu. İkincisi doğru ve daha yararlı.*

---

## Bölüm 8 — İletişim

**H2:** İletişim

Adres · e-posta · WhatsApp · Instagram · Facebook — yalnızca **dolu olanlar** listelenir.

**EĞER `email_kurumsal` false ve e-posta varsa:**
> E-posta adresi şirketin kendi alan adında değil.

**EĞER adres yoksa:**
> Sitesinde açık adres yayımlanmamış.

*Neden telefon yok: `sirketler.json` telefon tutmuyor, araştırma dosyasındaki numaralar
Birlik listesinden. Veri setine girmeden sayfaya yazılmaz.*

---

## Bölüm 9 — Benzer şirketler

**H2:** Karşılaştırın

Üç şirket: aynı branşlardan en çok örtüşen, aynı türden, aynı şehirde ofisi olan.
Her kart: ad · şehir · branş sayısı · tek ayırt edici özellik.

**Bağlantı:** [{brans} yapan {n} şirketin tamamı →](/tr/sirketler/{brans}/)

*CTA kuralı: "teklif al" yok. Site poliçe satmıyor; eylem okumak.*

---

## Bölüm 10 — Sayfa altı

**Kaynak bloğu:**
> **Kaynak:** {kaynak_url} — Temmuz 2026'da tarandı.
> Birlik üyeliği: KKSRSB üye listesi. Şirket türü: Birlik listesindeki unvan.

**Düzeltme:**
> Bu sayfadaki bir bilgi yanlışsa kaynağıyla birlikte bildirin; inceleyip düzeltir ve
> düzeltme tarihini sayfaya yazarız. [Düzeltme talebi →](/tr/duzeltme/)

**Yasal ayak notu (sabit):**
> Bu sayfadaki bilgiler genel bilgilendirme amaçlıdır, sigorta tavsiyesi değildir.
> Puanlar dışarıdan gözlemlenebilir ölçütlere dayanır; mali güç ve hasar ödeme
> performansı puanlanmamaktadır.

**Son güncelleme:** Temmuz 2026

---

## Düşük puanlı şirketlerde ton

Puanı 3'ün altında 10 şirket var; dördü yayımlanmadığı için bu blok **altı sayfada**
görünecek: Gold Insurance (2,8) · EIG (2,4) · Tower (2,4) · Universal (2,2) ·
Türkiye Sigorta (1,9) · London Insurance (1,6). Bu sayfalar bir suçlama gibi
okunabilir. **Okunmamalı.** Şablona şu blok, yalnızca `genel_puan < 3` iken girer:

> **Düşük puan ne demek, ne demek değil.** Bu puan şirketin dışarıdan ne kadar
> görülebildiğini ölçüyor. Bir şirket iyi hizmet veriyor ama sitesini güncellemiyor
> olabilir — bunu ölçemiyoruz. Puan, sizin doğrulayabileceğiniz bilginin ne kadar az
> olduğunu gösterir; şirketin kötü olduğunu değil.

*Neden: brief'in "şirket övmüyoruz" kuralının simetrik hâli. Övmüyorsak yermiyoruz da.
Bu blok aynı zamanda sitenin en olası hukuki riskini karşılıyor.*

---

## Üretilmeyen 4 şirket

Adres, e-posta, branş ve dil verisinin **dördü birden boş** olan dört şirket için
bu şablon çalıştırılmaz:

Zurich Sigorta · Correct Choice Insurance · Eager Insurance · Segure Insurance

Bunlar `/tr/sirketler/` sayfasında tek bölümde toplanır:

**H2:** Veri toplayamadığımız dört şirket

> Bu dört şirket Birlik'in ruhsatlı üyesi, ama haklarında sayfa açacak kadar bilgi
> bulamadık. Zurich Sigorta'nın KKTC'ye özel bir sitesi yok; diğer üçünün alan adı
> yanıt vermiyor. Birinde alan adının süresi dolmuş görünüyor, birinde sunucu
> kontrol panelinin varsayılan sayfası açılıyor. Ürün sayfalarına ulaşamadığımız
> için hangi branşlarda çalıştıklarını yazamıyoruz.
>
> Ruhsatlı olmaları poliçelerinin geçerli olduğu anlamına gelir. Doğrulanabilir
> bilgi yayımlamamaları ayrı bir konudur.

*Neden ayrı bölüm, ayrı sayfa değil: dört ince sayfa, 35 iyi sayfanın güvenilirliğini
aşağı çeker. Tek bölüm hâlinde ise başlı başına bir bulgu: 39 ruhsatlı şirketin
beşinin çalışan web sitesi yok.*

**Sayfası üretilen ama branş verisi olmayan beş şirket** — Eurocity · EIG · Tower ·
Türkiye Sigorta · Universal — için Bölüm 5 şu cümleyle geçilir:

> **Hangi branşlarda çalıştığını yazamıyoruz.** Şirketin sitesinde ürün sayfası yok;
> ürün listesi yayımlamıyor. Branş bilgisi için doğrudan şirkete sormanız gerekiyor.

**Eurocity ve EIG profillerinde ayrıca — yorumsuz, karşılıklı bağlantılı:**
> Bu şirketin sitesi ile EIG Sigorta'nın sitesi aynı IP adresinde ve aynı şablonda
> yayında. İkisi de Birlik'in ayrı ayrı ruhsatlı üyesi. Bağlantının niteliğini
> doğrulayamadık.

---

## Yayın öncesi kontrol — sayfa başına

- [ ] Bölüm 2'deki özet cümlesi elle yazıldı, şablondan gelmedi
- [ ] Bölüm 4 dolu — boşluk ilanı ya da "eksik veri yok" cümlesi var
- [ ] Beyana dayalı her rakamda "şirket beyanı" etiketi var
- [ ] Title 60 karakterin altında ve puan içermiyor
- [ ] `AggregateRating` şeması yok — `Organization` + `BreadcrumbList` var
- [ ] Hiçbir yerde Türkiye limiti, cezası veya basamak oranı geçmiyor
- [ ] Grup bağlantısı iddiası yok (MAPFREE, London, Limasol adları için özellikle)
- [ ] Puan < 3 ise ton bloğu eklendi
