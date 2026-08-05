# Yayın kuyruğu — KKTC Sigorta Merkezi

**Oluşturma:** 3 Ağustos 2026 · **Kapsam:** 78 yazı ≈ 26 hafta (Pzt · Çrş · Cum)
**Durum:** 2 yayında · 76 bekliyor
**Dayanak:** `copy/01-icerik-stratejisi.md` sütunları · `copy/00-brief.md` ⛔ tablosu ·
`data/arastirma-kktc-sigorta.md`

Bu dosya otomasyonun **tek girdisidir.** `.claude/skills/yazi-uret/` becerisi her
çalıştığında buradaki **ilk `⬜` satırını** alır, yazıyı üretir, satırı `✅` yapar
ve yayın tarihini yazar. Sırayı değiştirmek istiyorsanız satırları taşıyın —
beceri tarih değil, **sıra** okur.

---

## Kuyruk kuralları

1. **İlk `⬜` kazanır.** Tarih sütunu plandır, bağlayıcı değil. Bir hafta kaçarsa
   sıra kaymaz, takvim kayar.
2. **`⛔` satırı atlanır.** Kaynağı okunmadığı için henüz yazılamayan başlıklar
   böyle işaretlidir. Kaynak okunduğunda `⬜`'ye çevrilir.
3. **Bir satır bir yazıdır.** Beceri asla iki satırı birleştirmez, bölmez.
4. **"Zorunlu bağlantı" sütunu şarttır.** O adresler yazı içinde geçmiyorsa yazı
   eksiktir. Adres henüz üretilmemişse (`_build/uret.py` çıktısında yoksa) o
   bağlantı **atlanır**, kırık bağlantı yazılmaz.
5. **"Boşluk" sütunu da şarttır.** Her yazı en az bir "bunu doğrulayamadık"
   cümlesi taşır. Sitenin ayırt edici deseni bu.
6. Kategori değerleri sabittir: `Ayrım` · `Hasar` · `Yabancılar` · `Sınır geçişi` ·
   `Şirket seçimi` · `Şeffaflık` · `Ürün`. Yeni kategori **uydurulmaz** —
   her yeni değer yeni bir konu sayfası üretir.

## Bu kuyruğun hedeflemediği şey

"Trafik sigortası", "online sigorta", "konut sigortası" gibi **çıplak** sorgular
bu kuyruğun hedefi değil. O sonuç sayfalarında Türkiye'nin sigorta şirketleri var
ve arayanların çoğu poliçe satın almak istiyor; bu site poliçe satmıyor. Kuyruğun
tamamı **"kktc / kuzey kıbrıs" nitelemesi taşıyan** sorgulara yazılmıştır. Hedef
sütunundaki her ifade bu niteliği taşır; taşımayan bir hedef kuyruğa girmez.

---

## Ağustos 2026

| № | Durum | Başlık | Kategori | Hedef sorgu | Zorunlu bağlantı | İlan edilecek boşluk |
|---|---|---|---|---|---|---|
| 01 | ✅ | KKTC trafik sigortası Türkiye'den ne kadar farklı — *3 Ağu 2026* | Ayrım | kktc trafik sigortası türkiye farkı | `/tr/sigorta/trafik/` · `/tr/metodoloji/` | Sigortasız araç cezası — Fasıl 333 md. 17 okunmadı |
| 02 | ✅ | Taban tarife nedir, KKTC'de fiyatı nasıl belirler — *5 Ağu 2026* | Ayrım | kktc taban tarife sigorta | `/tr/sigorta/trafik/` · `/tr/sirketler/` | 2026 tarifesi yayımlanmadı |
| 03 | ⬜ | Sigortasız araç çarptı: KKTC'de Garanti Fonu'na başvuru | Hasar | kktc garanti fonu sigortasız araç | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Fonun ödeme limiti — tüzük okunmadı |
| 04 | ⬜ | KKTC'de sigorta şirketi mi acente mi — nasıl ayırt edilir | Ayrım | kktc sigorta acente şirket farkı | `/tr/sirketler/` · `/tr/metodoloji/` | Acente sayısı beyanları doğrulanamıyor |
| 05 | ⬜ | Hasar dosyanız reddedilirse: KKTC'de beş basamaklı yol | Hasar | kktc sigorta hasar reddi itiraz | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` · `/tr/duzeltme/` | Yasal itiraz süresi tespit edilemedi |
| 06 | ⬜ | KKTC'de şirket bazında mali veri neden yayımlanmıyor | Şeffaflık | kktc sigorta şirketi mali durum | `/tr/metodoloji/` · `/tr/sirketler/` | 2016 sonrası şirket bazlı veri yok — bulgunun kendisi |
| 07 | ⬜ | Metehan'dan geçerken sigorta: saatler ve pratik | Sınır geçişi | metehan sınır kapısı sigorta | `/tr/rehber/sinir-gecisi-sigortasi/` | Kapı saatleri resmî kaynakta yayımlı değil |
| 08 | ⬜ | KKTC'de trafik sigortası hangi zararı karşılar | Ayrım | kktc zorunlu trafik sigortası kapsam | `/tr/sigorta/trafik/` | Limitlerin son güncelleme tarihi belirsiz |
| 09 | ⬜ | KKTC konut sigortası neyi kapsar, neyi kapsamaz | Ürün | kktc konut sigortası kapsam | `/tr/sigorta/konut/` · `/tr/sirketler/` | Zorunlu deprem sigortası kanıtı yok |
| 10 | ⬜ | Sigorta Tahkim Komisyonu'na KKTC'de nasıl başvurulur | Hasar | kktc sigorta tahkim komisyonu | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Tahkim ücreti, limiti ve süresi — tüzük okunmadı |
| 11 | ⬜ | Yeşil kart KKTC'de neden geçmiyor | Sınır geçişi | kktc yeşil kart sigorta | `/tr/rehber/sinir-gecisi-sigortasi/` | — (bu yazıda boşluk: Güney'in kabul rejimi doğrulanmadı) |
| 12 | ⬜ | KKTC sağlık sigortası: özel poliçe neyi karşılar | Ürün | kktc özel sağlık sigortası | `/tr/sigorta/saglik/` · `/tr/rehber/ogrenci-saglik-sigortasi/` | Devlet hastanesi katkı payı rejimi doğrulanmadı |
| 13 | ⬜ | KKTC'de sigortayı kim denetler | Ayrım | kktc sigorta denetim kurumu | `/tr/metodoloji/` | Merkezî tüketici şikâyet mercii belirsiz |

## Eylül 2026

| № | Durum | Başlık | Kategori | Hedef sorgu | Zorunlu bağlantı | İlan edilecek boşluk |
|---|---|---|---|---|---|---|
| 14 | ⬜ | Hasarsızlık indirimi KKTC'de nasıl işliyor | Ayrım | kktc hasarsızlık indirimi | `/tr/sigorta/trafik/` | Basamak sayısı ve oranlar hiçbir kamu kaynağında yok |
| 15 | ⬜ | KKTC'de trafik sigortası yaptıracak şirket nasıl seçilir | Şirket seçimi | kktc trafik sigortası hangi şirket | `/tr/sirketler/` · `/tr/metodoloji/` | Hasar ödeme performansı ölçülemiyor |
| 16 | ⬜ | Eksper ne yapar, raporuna itiraz edilebilir mi | Hasar | kktc sigorta eksper raporu itiraz | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Eksper atama usulü doğrulanmadı |
| 17 | ⬜ | Beyarmudu, Derinya, Akyar: hangi kapıda ne var | Sınır geçişi | kktc sınır kapısı sigorta nerede | `/tr/rehber/sinir-gecisi-sigortasi/` | İki kapının poliçe sayısı raporun okunamayan satırında |
| 18 | ⬜ | 39 şirketin yalnızca üçü poliçe genel şartlarını yayımlıyor | Şeffaflık | kktc sigorta poliçe genel şartları | `/tr/sirketler/` · `/tr/metodoloji/` | Yayımlamayan şirketlerin gerekçesi sorulmadı |
| 19 | ⬜ | Türkiye'den KKTC'ye taşınırken poliçenizde ne değişir | Ayrım | türkiyeden kktc ye taşınma sigorta | `/tr/sigorta/trafik/` · `/tr/sigorta/saglik/` | TR poliçesinin devir usulü doğrulanmadı |
| 20 | ⬜ | Kaçan araç çarptıysa KKTC'de ne yapılır | Hasar | kktc kaçan araç çarptı sigorta | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Fonun başvuru süresi doğrulanmadı |
| 21 | ⬜ | KKTC'de online poliçe kesebilen şirketler | Şirket seçimi | kktc online sigorta poliçe | `/tr/sirketler/` | Online akışların hepsi test edilmedi |
| 22 | ⬜ | Üç aydan uzun ikamette sağlık sigortası şartı | Yabancılar | kktc ikamet sağlık sigortası zorunlu | `/tr/rehber/ogrenci-saglik-sigortasi/` · `/tr/sigorta/saglik/` | Hangi poliçe türünün kabul edildiği net değil |
| 23 | ⬜ | KKTC'de kasko poliçesinde sık atlanan maddeler | Ürün | kktc kasko poliçe kapsam | `/tr/sigorta/kasko/` | Kasko fiyat aralığı yalnızca ticari kaynakta |
| 24 | ⬜ | Puanlama modelimiz neden mali gücü içermiyor | Şeffaflık | kktc sigorta şirketi güvenilir mi | `/tr/metodoloji/` | Ödenmiş sermaye verisi yayımlanmıyor |
| 25 | ⬜ | Yabancı plakayla KKTC'de araç kullanmak | Yabancılar | yabancı plaka kktc sigorta | `/tr/rehber/sinir-gecisi-sigortasi/` | Azami kullanım süresi doğrulanmadı |
| 26 | ⬜ | KKTC'de işyeri sigortası neyi kapsar | Ürün | kktc işyeri sigortası | `/tr/sigorta/isyeri/` · `/tr/sirketler/` | Zorunlu işveren sorumluluk rejimi belirsiz |

## Ekim 2026

| № | Durum | Başlık | Kategori | Hedef sorgu | Zorunlu bağlantı | İlan edilecek boşluk |
|---|---|---|---|---|---|---|
| 27 | ⬜ | KKSBM ile Türkiye'nin SBM'si aynı kurum değil | Ayrım | kktc sigorta bilgi merkezi | `/tr/metodoloji/` | KKSBM'nin sorgulanabilir kayıt açıp açmadığı belirsiz |
| 28 | ⬜ | Kaza yerinde çekilmesi gereken fotoğraflar | Hasar | kktc kaza fotoğraf sigorta | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Şirketlerin fotoğraf şartı poliçede yayımlı değil |
| 29 | ⬜ | Kuzey'de alınan poliçe Güney'de neden geçmez | Sınır geçişi | kuzey kıbrıs poliçe güneyde geçerli mi | `/tr/rehber/sinir-gecisi-sigortasi/` | Güney'in kabul ettiği belge listesi doğrulanmadı |
| 30 | ⬜ | Girne'de ofisi olan sigorta şirketleri | Şirket seçimi | girne sigorta şirketi | `/tr/sirketler/` | Şube-acente ayrımı her şirkette net değil |
| 31 | ⬜ | Muallak hasar ne demek, ödenmiş hasardan farkı ne | Şeffaflık | muallak hasar nedir | `/tr/metodoloji/` | KKTC'de ödenen hasar sıralaması hiç yayımlanmadı |
| 32 | ⬜ | Öğrenci Sağlık Fonu ile özel sağlık sigortası farkı | Yabancılar | kktc öğrenci sağlık fonu | `/tr/rehber/ogrenci-saglik-sigortasi/` · `/tr/sigorta/saglik/` | Prim tutarı teyit edilmeli |
| 33 | ⬜ | KKTC'de aracınız pert olursa süreç | Hasar | kktc araç pert sigorta | `/tr/sigorta/kasko/` | Pert eşiği oranı doğrulanmadı |
| 34 | ⬜ | 39 şirketin web varlığı: üç ölü alan adı, iki eksik site | Şeffaflık | kktc sigorta şirketleri listesi | `/tr/sirketler/` | Sitesi olmayan şirketlere ulaşılamadı |
| 35 | ⬜ | KKTC'de seyahat sigortası: yurt dışına çıkarken | Ürün | kktc seyahat sigortası | `/tr/sigorta/seyahat/` | Schengen başvurusunda kabul rejimi doğrulanmadı |
| 36 | ⬜ | Poliçe genel şartlarını nereden okursunuz | Ayrım | kktc sigorta genel şartlar nerede | `/tr/sigorta/trafik/` · `/tr/metodoloji/` | Genel şartların son güncelleme tarihi belirsiz |
| 37 | ⬜ | Kiralık araçla Güney'e geçiş | Sınır geçişi | kktc kiralık araç güneye geçiş | `/tr/rehber/sinir-gecisi-sigortasi/` | Kiralama şirketlerinin izin politikası standart değil |
| 38 | ⬜ | Banka grubuna bağlı sigorta şirketleri | Şirket seçimi | kktc banka sigorta şirketi | `/tr/sirketler/` | Grup içi reasürans ilişkisi doğrulanmadı |
| 39 | ⬜ | KKTC'de kiracıysanız konut sigortası kime ait | Ürün | kktc kiracı konut sigortası | `/tr/sigorta/konut/` | Kira sözleşmelerinde standart madde yok |

## Kasım 2026

| № | Durum | Başlık | Kategori | Hedef sorgu | Zorunlu bağlantı | İlan edilecek boşluk |
|---|---|---|---|---|---|---|
| 40 | ⬜ | Sigorta şirketiniz cevap vermiyorsa şikâyet zinciri | Hasar | kktc sigorta şikayet nereye | `/tr/duzeltme/` · `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Merkezî şikâyet mercii tespit edilemedi |
| 41 | ⬜ | AB tüketici mekanizmaları KKTC'de neden işlemez | Yabancılar | north cyprus insurance complaint | `/tr/metodoloji/` | KKTC şirketlerinin AB şema dışılığı resmî metinle doğrulanmadı |
| 42 | ⬜ | KKTC'de online teklif veren şirketler | Şirket seçimi | kktc online sigorta teklif | `/tr/sirketler/` | Teklif ekranlarının fiyat verip vermediği test edilmedi |
| 43 | ⬜ | Aynı IP adresinde iki ruhsatlı sigorta şirketi | Şeffaflık | kktc sigorta şirketi ruhsat | `/tr/sirketler/` · `/tr/duzeltme/` | Bağlantının niteliği doğrulanamadı |
| 44 | ⬜ | Ehliyetsiz sürücünün yaptığı kazada haklarınız | Hasar | kktc ehliyetsiz sürücü kaza sigorta | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Fonun rücu usulü doğrulanmadı |
| 45 | ⬜ | KKTC'de ev satın alan yabancı için konut sigortası | Yabancılar | kuzey kıbrıs ev sigortası yabancı | `/tr/sigorta/konut/` | Tapu sürecinde sigorta şartı olup olmadığı belirsiz |
| 46 | ⬜ | Gazimağusa'da ofisi olan sigorta şirketleri | Şirket seçimi | gazimağusa sigorta şirketi | `/tr/sirketler/` | Ofis-acente ayrımı beyana dayalı |
| 47 | ⬜ | Türkiye'de yaptırdığınız kasko KKTC'de geçerli mi | Ayrım | türkiye kasko kktc geçerli mi | `/tr/sigorta/kasko/` | TR poliçelerinin coğrafi kapsam maddesi tek tek incelenmedi |
| 48 | ⬜ | Konut hasarında ilk 24 saat | Hasar | kktc konut hasarı ne yapmalı | `/tr/sigorta/konut/` · `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Konut branşında ihbar süresi doğrulanmadı |
| 49 | ⬜ | İskele ve Güzelyurt'ta sigortaya erişim | Şirket seçimi | iskele güzelyurt sigorta | `/tr/sirketler/` | Merkezi bu şehirlerde olan şirket yok — bulgunun kendisi |
| 50 | ⬜ | Ferdi kaza sigortası KKTC'de kime gerekir | Ürün | kktc ferdi kaza sigortası | `/tr/sirketler/` | Zorunlu olduğu meslek grupları tespit edilemedi |
| 51 | ⬜ | Neden "KKTC'nin en iyi sigorta şirketi" listesi yapmıyoruz | Şeffaflık | kktc en iyi sigorta şirketi | `/tr/metodoloji/` · `/tr/sirketler/` | Sıralamayı mümkün kılacak verinin tamamı eksik |
| 52 | ⬜ | Yaya geçişlerinde sigorta gerekir mi | Sınır geçişi | lokmacı yaya geçiş sigorta | `/tr/rehber/sinir-gecisi-sigortasi/` | Yaya geçişte sağlık kapsamı doğrulanmadı |

## Aralık 2026

| № | Durum | Başlık | Kategori | Hedef sorgu | Zorunlu bağlantı | İlan edilecek boşluk |
|---|---|---|---|---|---|---|
| 53 | ⬜ | Kapatılması gereken 12 veri boşluğu | Şeffaflık | kktc sigorta verileri | `/tr/metodoloji/` · `/tr/duzeltme/` | Listenin kendisi — 12 maddenin tamamı açık |
| 54 | ⬜ | Karşı taraf poliçe bilgisini vermiyorsa | Hasar | kktc kaza karşı taraf sigorta bilgisi | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Poliçe sorgulama kanalı kamuya açık değil |
| 55 | ⬜ | Çalışma izniyle KKTC'ye gelenler için sigorta | Yabancılar | kktc çalışma izni sigorta | `/tr/sigorta/saglik/` | İşveren yükümlülüğünün kapsamı belirsiz |
| 56 | ⬜ | KKTC'de sigorta sözleşmesi hangi yasaya tabi | Ayrım | kktc sigorta yasası | `/tr/metodoloji/` | 60/2010 md. 39 okunamadı |
| 57 | ⬜ | Mobil uygulaması olan KKTC sigorta şirketleri | Şirket seçimi | kktc sigorta mobil uygulama | `/tr/sirketler/` | Uygulamaların içeride ne yaptığı test edilmedi |
| 58 | ⬜ | Nakliyat sigortası: KKTC'ye mal getiren için | Ürün | kktc nakliyat sigortası | `/tr/sirketler/` | Liman ve gümrük şartları doğrulanmadı |
| 59 | ⬜ | Hasar ihbarını kaç gün içinde yapmalısınız | Hasar | kktc hasar ihbar süresi | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | KKTC'ye özgü süre tespit edilemedi |
| 60 | ⬜ | İngilizce hizmet veren şirketler nasıl bulunur | Yabancılar | north cyprus english speaking insurance | `/tr/sirketler/` | Hizmetin gerçekten İngilizce verildiği test edilmedi |
| 61 | ⬜ | Kurumsal e-posta neden bir şeffaflık göstergesi | Şeffaflık | kktc sigorta şirketi iletişim | `/tr/metodoloji/` · `/tr/sirketler/` | Ölçütün sınırı: küçük şirket dezavantajlı olabilir |
| 62 | ⬜ | Türkiye şubesi olarak çalışan şirketler | Şirket seçimi | kktc türkiye sigorta şubesi | `/tr/sirketler/` | Şube-ortaklık ayrımı Birlik listesinde net değil |
| 63 | ⬜ | Emeklilikte KKTC'ye yerleşenler için sağlık | Yabancılar | kuzey kıbrıs emekli sağlık sigortası | `/tr/sigorta/saglik/` | Yaş üst sınırı politikaları yayımlı değil |
| 64 | ⬜ | Polis raporu hasar dosyasında ne işe yarar | Hasar | kktc kaza polis raporu sigorta | `/tr/rehber/kaza-sonrasi-ilk-48-saat/` | Raporun zorunlu olduğu haller doğrulanmadı |
| 65 | ⬜ | Online sigorta KKTC'de nereye kadar mümkün | Ürün | kktc online sigorta | `/tr/sirketler/` · `/tr/sigorta/trafik/` | Uçtan uca dijital akış oranı ölçülmedi |

## Ocak 2027

| № | Durum | Başlık | Kategori | Hedef sorgu | Zorunlu bağlantı | İlan edilecek boşluk |
|---|---|---|---|---|---|---|
| 66 | ⬜ | Acente ağı büyüklüğü size ne anlatır | Şirket seçimi | kktc sigorta acente | `/tr/sirketler/` | Acente sayıları şirket beyanı, doğrulanmadı |
| 67 | ⬜ | Turist olarak araç kiralarken sigorta | Yabancılar | kuzey kıbrıs araç kiralama sigorta | `/tr/rehber/sinir-gecisi-sigortasi/` | Kiralama poliçelerinin muafiyeti yayımlı değil |
| 68 | ⬜ | Bir bilgiyi bu sitede nasıl doğruluyoruz | Şeffaflık | — (marka sorgusu) | `/tr/metodoloji/` · `/tr/duzeltme/` | Yöntemin sınırı: birincil kaynağa erişilemeyen alanlar |
| 69 | ⬜ | Sigorta şirketi değiştirirken nelere bakılır | Şirket seçimi | kktc sigorta şirketi değiştirme | `/tr/sirketler/` · `/tr/metodoloji/` | Hasarsızlık geçmişinin taşınması doğrulanmadı |
| 70 | ⬜ | KKTC'de zorunlu deprem sigortası var mı | Ayrım | kktc dask deprem sigortası | `/tr/sigorta/konut/` | DASK benzeri bir rejimin varlığına dair kanıt yok |
| 71 | ⬜ | Vize ve ikamet başvurusunda hangi sigorta belgesi isteniyor | Yabancılar | kktc ikamet izni sigorta belgesi | `/tr/rehber/ogrenci-saglik-sigortasi/` | Muhaceret'in kabul ettiği belge listesi yayımlı değil |
| 72 | ⬜ | 2024 raporundaki iki farklı prim rakamı | Şeffaflık | kktc sigorta sektörü büyüklüğü | `/tr/metodoloji/` | Hangi rakamın doğru olduğu Birlik'e sorulmadı |
| 73 | ⬜ | Yat sigortası: KKTC'de dar bir pazar | Ürün | kktc yat sigortası | `/tr/sirketler/` | Marina şartları ve kapsam doğrulanmadı |
| 74 | ⬜ | 36/2025 reformu sigortalı için ne değiştirdi | Ayrım | kktc sigorta yasası değişiklik | `/tr/metodoloji/` | Yürürlük takvimi ve geçiş hükümleri okunmadı |
| 75 | ⬜ | Rusça hizmet: KKTC sigortasında gerçek durum | Yabancılar | северный кипр страхование | `/tr/sirketler/` | İki şirket dışında Rusça hizmet doğrulanamadı |
| 76 | ⬜ | Kasko mu trafik mi: KKTC'de ne farkı var | Ayrım | kktc kasko trafik farkı | `/tr/sigorta/kasko/` · `/tr/sigorta/trafik/` | Kasko fiyat aralığı yalnızca ticari kaynakta |
| 77 | ⬜ | Sigortasız araç kullanmanın KKTC'deki sonucu | Ayrım | kktc sigortasız araç cezası | `/tr/sigorta/trafik/` | **Ceza tutarı yazılmaz** — Fasıl 333 md. 17 okunmadı |
| 78 | ⬜ | Taban primlerdeki artış sigortalı için ne anlama geliyor | Şeffaflık | kktc sigorta zam | `/tr/sigorta/trafik/` | 2026 tarifesi yayımlanmadı; karşılaştırma yapılamıyor |

---

## Kuyruk bittiğinde

78. satır `✅` olduğunda beceri **yeni başlık uydurmaz.** Şu üçünden birini yapar:

1. `⛔` işaretli satır varsa, kaynağı okunup okunmadığını sorar.
2. Kuyruğu yenilemek için `copy/01-icerik-stratejisi.md` §4 öncelik tablosuna
   ve `data/arastirma-kktc-sigorta.md` §7'ye bakılmasını ister.
3. Yeni başlık gerekiyorsa **öneri listesi üretir, kendiliğinden yayımlamaz.**

## Kuyruğa satır eklerken

Yeni satır için üç şey zorunlu: hedef sorguda **"kktc" ya da "kuzey kıbrıs"**
nitelemesi, en az bir **var olan** iç bağlantı adresi, ve bir **boşluk ifadesi.**
Üçünden biri yoksa satır kuyruğa girmez.
