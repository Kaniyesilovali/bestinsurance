# Programatik SEO planı — KKTC Sigorta Merkezi

**Tarih:** 24 Temmuz 2026
**Dayanak:** `copy/01-icerik-stratejisi.md` · `data/sirketler.json` (39 şirket, 30 alan)
**Üretim:** `_build/uret.py` — `content/` + `_build/sablon/` → `dist/`

---

## 0. Bu planın tek kuralı

> **Şablon değişkeni değiştirmek içerik üretmek değildir.**
> Her sayfa, o sayfaya özgü **en az bir doğrulanmış olgu** ve **en az bir açıkça
> ilan edilmiş boşluk** içermek zorunda. İkisini de üretemeyen sayfa üretilmez.

Bu site için bu kural normalden daha bağlayıcı: elimizdeki veri **birincil kaynaktan
tek tek toplandı** (39 şirket sitesi tarandı, HTTP durumları ölçüldü). Bu, pSEO veri
savunulabilirlik hiyerarşisinde **"özgün / kendi ürettiğimiz"** kademesidir — kamuya
açık bir API'den çekilmiş veri değil. Avantaj burada; onu inceltip harcamayacağız.

---

## 1. Fırsat özeti

| Set | Desen | Sayfa | Öncelik | Veri kaynağı |
|---|---|---|---|---|
| **A** | Şirket profili | **35** (+4 gizli) | 1 | `sirketler.json` — tam kayıt |
| **B** | Branşa göre şirket listesi | **10** | 2 | `branslar[]` |
| **D** | Araç tipine göre taban prim | **12** | 3 | Araştırma §4.2 |
| **E** | Şehre göre şirket erişimi | **4** | 4 | `ofis_sehirler[]` |
| **F** | Özelliğe göre şirket listesi | **2** | 5 | Boolean alanlar |
| **G** | Sözlük | **20** | 6 | Brief terim sözlüğü + araştırma |
| | **TOPLAM** | **83** | | |

Mevcut site: 12 sayfa. Plan sonrası: **~95 TR sayfası.** Plan **önce TR'yi
tamamlamayı**, sonra setleri EN'e taşımayı öneriyor (gerekçe §8).

---

## 2. Set A — Şirket profilleri

**URL:** `/tr/sirketler/<slug>/` (slug'lar `sirketler.json` içinde hazır)
**Playbook:** Profiles + Directory
**Aciliyet:** Şirketler listesi ve ana sayfa **şu anda var olmayan bu adreslere bağlanıyor.**
Site canlıya alınırsa 39 kırık iç bağlantı doğar. Bu set birinci sırada.

### Sayfa iskeleti

```
1. Başlık bloğu       ad · şehir · şirket türü · kuruluş yılı (varsa) · genel puan
2. Tek cümlelik özet  şablondan değil, `notlar` alanından türetilir       ← ÖZGÜN
3. Altı ölçüt         şeffaflık · ürün · erişim · dijital · dil · kurumsal
                      her ölçütte "var" / "yok" listesi — puan değil kanıt
4. Neyi doğrulayamadık `veri_yok_olcutler[]` → açık boşluk ilanı           ← ÖZGÜN
5. Branş matrisi      12 branşta ✓ / — · her ✓ ilgili tür hub'ına bağlanır
6. Erişim             ofis şehirleri · acente sayısı (şirket beyanı etiketli)
7. Dijital denetim    online teklif/poliçe/hasar ihbarı · mobil uygulama · HTTP durumu
8. İletişim           adres · e-posta (kurumsal mı?) · WhatsApp · sosyal
9. Kaynak             `kaynak_url` + tarama tarihi
10. Benzer şirketler  aynı tür + aynı branş profilinden 3 tanesi
```

### Özgünlük bütçesi

Her profilde şablondan gelmeyen, o şirkete özel metin:

| Kaynak | Ortalama | En az |
|---|---|---|
| `notlar` alanı | 210 karakter | 89 karakter |
| Ölçüt "var/yok" kırılımı | 6 blok, şirkete göre farklı | — |
| Boşluk ilanı | 0–3 madde | 0 |
| Branş matrisi | 12 satır, kombinasyon şirkete özel | — |

Örnek — Dağlı Sigorta'nın `notlar` alanı zaten bir profil sayfasının çekirdeği:
> *"Acente sayısında sitede tutarsızlık: metinde '25 acentemizle', footer'da '22 Acente' —
> ikisi de beyan."*

Bu tek cümle bir rakip sitede yok. Sayfayı taşıyan da bu.

### ⚠ İnce içerik eşiği — 4 şirket

**Yanlış eşik:** "branşı olmayan şirket." Bu ölçüte göre 9 şirket elenirdi — ama
dokuzun beşinde sayfayı taşıyacak özgün olgu **var:**

| Şirket | Branş | Elimizdeki özgün olgu |
|---|---|---|
| Eurocity Sigorta | 0 | Tek sayfalık kartvizit sitesi, SSL geçersiz. **EIG Sigorta ile aynı IP ve aynı sayfa.** |
| EIG Sigorta | 0 | Aynı bulgunun diğer ucu. E-posta outlook.com. |
| Tower Insurance | 0 | ~190 karakterlik tek sayfa. HTTPS çalışmıyor. E-posta hotmail.com. |
| Türkiye Sigorta | 0 | KKTC alt alan adı Türkiye sitesinin kopyası; yalnızca iletişim sayfası Kıbrıs'a özel. |
| Universal Sigorta | 0 | Sitesi yok. Birlik listesindeki resmî e-posta bir gmail adresi. |

Beşinin de adresi ve iletişim bilgisi var; beşi de bir şey **söylüyor.**
Sayfaları üretilir.

**Doğru eşik: adres, e-posta, branş ve dil verisinin dördü birden boş.** Bu ölçütü
geçemeyen 4 şirket:

`zurich-sigorta` (0,9) · `correct-choice-insurance` (0,6) · `eager-insurance` (0,6) ·
`segure-insurance` (0,6)

- Ayrı URL **üretilmez.**
- `/tr/sirketler/` listesinde **"Veri toplayamadığımız dört şirket"** başlıklı tek
  bölümde toplanır; her biri için neden toplanamadığı yazılır.
- Bu bölüm başlı başına içerik: **39 ruhsatlı şirketin 5'inin çalışan web sitesi yok** —
  ikisinin sitesi hiç yok, üçünün alan adı yanıt vermiyor.

Bu yüzden set A **39 değil 35 sayfa.**

> **⭐ Bu taramadan çıkan ve P5'e gitmesi gereken bulgu:** Eurocity Sigorta ile EIG
> Sigorta'nın siteleri **aynı IP'de ve aynı şablonda.** İkisi de Birlik'in ayrı ayrı
> ruhsatlı üyesi. Bu bir iddia değil, bir gözlem — ve şirketlere sorulacak bir soru.
> Profil sayfalarında karşılıklı olarak birbirine bağlanır, yorum eklenmez.

### Meta şablonları

```
Title:  {ad} — KKTC sigorta şirketi profili ve doğrulanabilir ölçütler
        (60 karakteri aşarsa: "{kısa_ad} — KKTC sigorta şirketi profili")

Desc:   {sehir} merkezli {ad}. {brans_sayisi} branş, {sehir_sayisi} şehirde ofis.
        Şeffaflık, dijital hizmet ve dil desteği ölçütlerinde ne doğrulayabildiğimiz.

H1:     {ad}
```

**Değişken-yığma yasağı:** title'a puan yazılmaz (`8,6 puan` gibi) — puan bizim
gözlemimiz, arama sonucunda derecelendirme iddiası gibi görünür.

### Şema

`Organization` + `BreadcrumbList`. **`AggregateRating` KULLANILMAZ** — kullanıcı
değerlendirmesi değil, kendi ölçümümüz. Google zengin sonuç politikasına da aykırı,
brief'in "şirket övmüyoruz" kuralına da.

---

## 3. Set B — Branşa göre şirket listesi

**URL:** `/tr/sirketler/<brans>/`
**Playbook:** Curation + Directory
**Hedef desen:** "kktc trafik sigortası yapan şirketler", "kuzey kıbrıs sağlık sigortası şirketleri"

| Branş | Şirket | Sayfa? |
|---|---|---|
| trafik | 29 | ✓ |
| kasko | 29 | ✓ |
| konut | 28 | ✓ |
| isyeri | 27 | ✓ |
| ferdi_kaza | 21 | ✓ |
| nakliyat | 20 | ✓ |
| seyahat | 19 | ✓ |
| sorumluluk | 17 | ✓ |
| muhendislik | 15 | ✓ |
| saglik | 14 | ✓ |
| hayat | 9 | ✗ — hayat branşı ayrı ruhsat rejimi; karışıklık riski |
| yat | 7 | ✗ — 7 şirket, tür hub'ı yok, kendi başına zayıf |

**10 sayfa.** `hayat` ve `yat` üretilmez; ilgili şirketler profillerinde ve
`/tr/sigorta/` hub'larında görünmeye devam eder.

**Kannibalizasyon uyarısı:** `/tr/sigorta/trafik/` (ürün açıklayıcı) ile
`/tr/sirketler/trafik/` (şirket listesi) **farklı niyeti** karşılar ve birbirine
bağlanır. Ayrım title'da net yapılır:

- `/tr/sigorta/trafik/` → "KKTC zorunlu trafik sigortası — limitler, taban tarife ve kapsam"
- `/tr/sirketler/trafik/` → "KKTC'de trafik sigortası yapan 29 şirket — karşılaştırma"

### Sayfaya özgü içerik (şablon değil)

Her branş sayfası kendi verisinden bir **bulgu cümlesi** üretir:

- trafik: *"39 ruhsatlı şirketin 29'unda trafik ürünü doğrulandı. Kalan 10'da ürün
  sayfası bulunamadı — sunmadıkları anlamına gelmez."*
- saglik: *"Sağlık yalnızca 14 şirkette doğrulandı — trafik/kaskonun yarısından az.
  Yabancı uyruklu öğrenciler için ayrıca Sağlık Fonu ayrımına bakın."*
- yat/muhendislik gibi dar branşlarda liste kısa olduğu için **tam liste + neden dar
  olduğu** yazılır.

---

## 4. Set D — Araç tipine göre taban prim

**URL:** `/tr/tarife/<arac-tipi>/`
**Playbook:** Conversions/Templates hibriti
**Hedef desen:** "kktc taksi trafik sigortası fiyatı", "kuzey kıbrıs motosiklet sigortası ne kadar"

12 okunabilir kullanım tarzı kodu → 12 sayfa. **Okunamayan 4 satır için sayfa üretilmez.**

| Kod | Araç | 2025 Taban 1 | 2025 Taban 2 | 2024 Taban 1 | Artış |
|---|---|---|---|---|---|
| CX1 | Salon araç | 4.000,00 | 5.000,00 | 2.505,56 | +%59,6 |
| CY1 | Motosiklet | 2.000,00 | 2.500,00 | 1.202,67 | +%66,3 |
| CZ 300 | Van / kamyonet | 4.000,00 | 5.000,00 | — | — |
| CZ 301 | Kamyon | 5.000,00 | 5.500,00 | 3.006,68 | +%66,3 |
| CZ 312 | Trailer | 2.200,00 | 2.500,00 | — | — |
| CZ 9 | Motor trade | 8.000,00 | 9.500,00 | — | — |
| CZ 400 | Taksi | 11.500,00 | 13.500,00 | 7.316,24 | +%57,2 |
| CZ 600 | Otobüs/minibüs — ticari | 8.500,00 | 10.000,00 | — | — |
| CZ 605 | Otobüs/minibüs | 7.500,00 | 8.500,00 | — | — |
| CZ 801 | Özel tip | 4.000,00 | 4.500,00 | — | — |
| CZ 803 | Ambulans / cenaze | 4.500,00 | 5.000,00 | — | — |
| CZ 804 | Vinç | 5.000,00 | 6.000,00 | — | — |

### Bu setin zorunlu etiketleri

Bu, planın **en riskli setidir.** Fiyat arayan insan geliyor; yanlış rakam en çok
burada zarar verir. Her sayfada, sayfanın en üstünde, gövde metninden önce:

```
Bu tablo 2025 taban tarifesidir (20 Mart 2025'ten itibaren geçerli).
2026 tarifesi yayımlanmadı.
Bu bir fiyat değil, ALT SINIRDIR — şirketler bunun altında prim veremez, üstünde verebilir.
Sütun başlıkları kaynak PDF'te kısmen bozuk; iki sütunun tam anlamı doğrulanmadı.
Bu rakamlar Türkiye tarifesi DEĞİLDİR.
```

**Yazılmayacak:** "en ucuz", "ortalama fiyat", hasarsızlık indirimi uygulanmış tutar.
Basamak oranları KKTC için bilinmiyor.

**2026 tarifesi çıktığında:** 12 sayfa tek veri dosyasından güncellenir; 2025 sütunu
karşılaştırma olarak kalır. Set bunun için tasarlandı.

---

## 5. Set E — Şehre göre şirket erişimi

**URL:** `/tr/sirketler/sehir/<sehir>/`

| Şehir | Merkezi burada | Ofisi var | Sayfa |
|---|---|---|---|
| Lefkoşa | 36 | 36 | ✗ — 39'un 36'sı; ayırt edici değil, listeyi kopyalar |
| Girne | 2 | 13 | ✓ |
| Gazimağusa | 1 | 10 | ✓ |
| İskele | 0 | 7 | ✓ |
| Güzelyurt | 0 | 6 | ✓ |

**4 sayfa.** Lefkoşa üretilmez — ana şirketler listesinin kopyası olur.

Her sayfanın taşıyıcı bulgusu hazır:
- Girne: *"39 şirketten yalnızca ikisinin merkezi Girne'de; 13'ünün ofisi var."*
- İskele / Güzelyurt: *"Merkezi burada olan tek bir ruhsatlı şirket yok."*

### ⛔ Üretilmeyecek: branş × şehir matrisi

12 branş × 5 şehir = 60 sayfa teknik olarak üretilebilir ("Girne'de kasko yapan
şirketler"). **Üretilmeyecek.** Gerekçe:

- Aynı şirket listesinin permütasyonu — özgün olgu üretmiyor.
- Set B ve Set E'yi aynı anda kannibalize ediyor.
- 60 ince sayfa, 35 iyi profilin tamamının güvenilirliğini aşağı çeker.

Bu, planın bilinçli olarak **almadığı** en büyük hacim.

---

## 6. Set F — Özelliğe göre şirket listesi

**URL:** `/tr/sirketler/ozellik/<ozellik>/`

| Özellik | Şirket | Sayfa | Not |
|---|---|---|---|
| İngilizce hizmet veren | 17 | ✓ | EN sürümünün en değerli sayfası |
| Kurumsal e-posta kullanan | 23 | ✓ | Şeffaflık ölçütünün somut hâli |
| Rusça hizmet veren | **2** | ✗ | 2 şirket — sayfa değil |
| Mobil uygulaması olan | 4 | ✗ | 4 şirket — sayfa değil; şirket profilinin dijital denetim bölümünde görünür |
| Online hasar ihbarı | 5 | ✗ | Aynı — profilde görünür |
| Poliçe şartlarını yayımlayan | **3** | ✗ | **39'un 3'ü.** Sayfa değil ama P5'te
  yayımlanacak bir bulgu — şeffaflık sütununa gider |

**2 sayfa.** Beş şirketin altındaki hiçbir özellik ayrı sayfa olmuyor.

---

## 7. Set G — Sözlük

**URL:** `/tr/sozluk/<terim>/` · hub `/tr/sozluk/`
**Playbook:** Glossary

20 terim, brief'in terim sözlüğünden ve araştırmadan: taban tarife · hasarsızlık
indirimi · muallak hasar · Garanti Fonu · Fasıl 333 · 60/2010 · KKSRSB · KKSBM ·
Para Kambiyo Dairesi · Sigorta Yöneticisi · covernote · eksper · aktüer · broker ·
acente · reasürans · yeşil kart · Sağlık Fonu · teknik karşılık · yükümlülük sermaye yeterliliği

**Her terim sayfasının zorunlu üç bölümü:**
1. KKTC'deki tanımı ve yasal dayanağı
2. **Türkiye'deki karşılığı ve farkı** ← sayfayı özgün kılan şey; 20 terimin 14'ünde fark var
3. Nerede karşınıza çıkar (site içi bağlantı)

En az 150 kelime özgün metin üretilemeyen terim sayfa olmaz, hub'da tek satır kalır.
Bu eşik **yazım sırasında** uygulanır, üretim sonrası değil.

Şema: `DefinedTerm` + `DefinedTermSet`.

---

## 8. Dil açılımı

İki dilde tam açılım 83 × 2 = 166 sayfa eder. EN'de yalnızca şehir seti açılmaz.

| Set | TR | EN |
|---|---|---|
| A Şirket profilleri | ✓ 35 | ✓ 35 |
| B Branş listeleri | ✓ 10 | ✓ 10 |
| D Araç tipi tarife | ✓ 12 | ✓ 12 |
| E Şehir | ✓ 4 | — |
| F Özellik | ✓ 2 | ✓ 2 |
| G Sözlük | ✓ 20 | ✓ 20 |
| | **83** | **79** |

Gerekçeler:
- **EN:** neredeyse tam açılım. KKSRSB genel şartları **resmî olarak İngilizce yayımlıyor** —
  EN sürümü çeviri değil, birincil kaynağa dayanabiliyor. Bu setin kalitesini yükseltiyor.
- **E Şehir** EN'de açılmaz: şehir bazlı şirket erişimi sorgusu Türkçe aranıyor; EN'de
  `/en/companies/` listesindeki şehir bilgisi yeterli.

Toplam: **162 sayfa.**

---

## 9. Üretim — `_build/uret.py` uyarlaması

Mevcut hat `content/tr/sayfa/**` ve `content/tr/rehber/*.html` okuyup `dist/` üretiyor.
Programatik setler için **elle 83 HTML dosyası yazılmaz.** Gereken:

```
_build/sablon/
├── sirket-profil.html      Set A
├── liste-filtreli.html     Set B, E, F  (ortak — filtre + başlık + bulgu cümlesi)
├── tarife-arac.html        Set D
└── sozluk-terim.html       Set G

content/tr/veri/
├── taban-tarife-2025.json  kod, ad, taban1, taban2, 2024 karşılığı
├── sozluk.json             terim, tanım, TR farkı, dayanak
└── liste-tanimlari.json    hangi filtre → hangi başlık, bulgu cümlesi, meta
```

`uret.py` içine eklenecek: her set için bir üretici fonksiyon + `sitemap()`'e katılım
+ `baglanti_kontrol()`'ün bu sayfaları da taraması.

**Sitemap ayrımı:** `sitemap-sayfalar.xml` · `sitemap-sirketler.xml` · `sitemap-rehber.xml`
Sebep: 35 profilin indekslenme oranını ayrı ölçebilmek (strateji §8).

**`noindex` durumu:** `site.json` → `yayin.noindex: true` olduğu sürece tüm setler
noindex çıkar ve sitemap üretilmez. Alan adı belli olana kadar bu böyle kalır.

---

## 10. Kalite kapıları — yayın öncesi

- [ ] Her sayfada o sayfaya özgü **en az bir doğrulanmış olgu**
- [ ] Her sayfada **en az bir boşluk ilanı** ya da "bu sayfada doğrulanamayan veri yok" cümlesi
- [ ] Title'lar benzersiz · 60 karakter altı · şirket adı geçen title'da puan yok
- [ ] Meta description'lar benzersiz · şablon cümlesi tekrar etmiyor
- [ ] Hiçbir sayfada Türkiye limiti / cezası / basamak oranı yok
- [ ] Tarife sayfalarının tamamında "2025 · alt sınır · 2026 yayımlanmadı" bloğu var
- [ ] `AggregateRating` şeması hiçbir yerde yok
- [ ] Öksüz sayfa yok — `python3 _build/uret.py --kontrol` temiz
- [ ] Dört veri boşluğu şirketi ayrı URL almıyor · Eurocity–EIG çapraz bağlantısı var
- [ ] Branş × şehir matrisi üretilmemiş

---

## 11. Yayın sırası

| Sıra | Set | Sayfa | Neden bu sırada |
|---|---|---|---|
| 1 | A — Şirket profilleri | 35 | 39 kırık iç bağlantıyı kapatır |
| 2 | B — Branş listeleri | 10 | A'yı besler, tür hub'larını bağlar |
| 3 | D — Araç tipi tarife | 12 | En yüksek risk — A ve B yerleştikten sonra |
| 4 | E + F — Şehir + özellik | 6 | A'nın türevleri |
| 5 | G — Sözlük | 20 | En düşük aciliyet, en yüksek LLM alıntı değeri |

**A yayımlanmadan hiçbir set yayımlanmaz.** Diğer dört set A'ya bağlanıyor; A yoksa
hepsi öksüz doğar.
