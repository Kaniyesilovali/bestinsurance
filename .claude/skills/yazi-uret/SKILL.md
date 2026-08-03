---
name: yazi-uret
description: "Kıbrıs Sigorta Rehberi için kuyruktaki sıradaki blog yazısını üretir, doğrular ve yayına gönderir. Kullanıcı 'yeni yazı yaz', 'sıradaki yazıyı üret', 'blog yazısı yayınla', 'kuyruktan yaz' dediğinde ya da zamanlanmış yayın ajanı çalıştığında kullanılır. Yazı yazmadan önce kaynak doğrular; brief'in ⛔ tablosuna uymayan hiçbir cümleyi yayımlamaz."
metadata:
  version: 1.0.0
---

# Yazı üret — Kıbrıs Sigorta Rehberi

Bu beceri **tek bir blog yazısı** üretir ve yayına gönderir. Doğrudan `main` dalına
push eder; insan denetimi yoktur. Bu yüzden buradaki kurallar öneri değil, **kapıdır.**

Sitenin tek iddiası şudur: *doğrulayamadığımızı doğrulanmış gibi yazmayız.* Yazının
iyi olmasından çok bu iddianın korunması önemlidir. Bir adımda tereddüt ederseniz
**yayımlamayın** — kuyruk satırını `⛔` yapıp durun.

---

## 0. Önce oku (atlanamaz)

Yazmaya başlamadan bu üç dosya okunur:

| Dosya | Neden |
|---|---|
| `copy/00-brief.md` | ⛔ tablosu ve ses tonu. **Bu becerinin en üstündedir.** |
| `YAZI-YAZMA.md` | Dosya biçimi, frontmatter alanları, tasarım sınıfları |
| `copy/yayin-kuyrugu.md` | Hangi yazı yazılacak |

Ek olarak konuya göre: `data/arastirma-kktc-sigorta.md` (olgular ve kaynak listesi),
`copy/01-icerik-stratejisi.md` (sütun ve iç bağlantı kuralları).

---

## 1. Sıradaki satırı al

`copy/yayin-kuyrugu.md` içindeki **ilk `⬜` satırı.** Tarihe bakılmaz, sıraya bakılır.
`⛔` satırları atlanır. Satırdan şu altı alan alınır: başlık, kategori, hedef sorgu,
zorunlu bağlantılar, ilan edilecek boşluk, numara.

Kuyrukta `⬜` kalmadıysa: yeni başlık **uydurulmaz.** Dur, durumu bildir.

---

## 2. Kaynak doğrula — yazmadan önce

Bu adım yazıdan **önce** gelir, sonra değil. Amaç metni süslemek değil, yazının
dayandığı olguların hâlâ doğru olduğunu görmek.

1. Konunun olgularını `data/arastirma-kktc-sigorta.md` içinde bul. Araştırma dosyası
   birincil dayanaktır.
2. Araştırma dosyasında yoksa **birincil kaynağa git** — §8'deki listeden (KKSRSB,
   KKSBM, Para Kambiyo Dairesi, Muhaceret Dairesi, Resmî Gazete). WebFetch ile aç,
   ilgili cümleyi gör.
3. Kaynak açılmıyor, sayfa değişmiş ya da bilgi bulunamıyorsa: **o olgu yazılmaz.**
   Yerine boşluk cümlesi kurulur.
4. Ticari/ikincil kaynak (blog, acente sitesi, forum) **tek başına** hiçbir şeyi
   doğrulamaz. Kullanılacaksa metinde "ticari kaynak, resmî değil" etiketiyle geçer.

Doğrulama sırasında araştırma dosyasıyla çelişen bir bulgu çıkarsa: yazıyı yayımlama,
çelişkiyi bildir. Araştırma dosyasını **bu beceri değiştirmez.**

---

## 3. Rakam kuralı

**Varsayılan: rakam yazma.** Bu site rakam sitesi değil, ayrım sitesidir. Bir yazı
hiç rakam içermeden de tam olabilir — çoğu öyledir.

Bir sayı ancak şu üçü birden sağlanırsa yazılır:

1. `data/arastirma-kktc-sigorta.md` içinde **açıkça doğrulanmış** olarak duruyor, ya da
   bu çalışmada birincil kaynakta görüldü;
2. `copy/00-brief.md` ⛔ tablosunda **yasaklı değil**;
3. Yanına kaynağı ve tarihi yazılabiliyor.

### Asla yazılmayacaklar — ezberlenmez, her seferinde `00-brief.md` açılır

Kısaca: sigortasız araç cezası · hasarsızlık basamak/oranları · şirket bazında prim,
hasar, pazar payı, özkaynak · hasar ödeme sıralaması · Türkiye'nin trafik limitleri
KKTC limiti gibi · 2026 tarifesi · tahkim ücreti/limiti/süresi · Garanti Fonu ödeme
limiti · asgari sermaye · standart hasar ihbar süresi · MAPFRE ve London Insurance
grup bağı · KKTC'de zorunlu deprem sigortası.

Tam liste `copy/00-brief.md` içindedir ve **her yazıdan önce açılır.** Liste
güncellenmiş olabilir; buradaki özet yalnızca hatırlatmadır.

### Rakam yerine ne yazılır

> "Sigortasız araç kullanmanın cezası Fasıl 333'te düzenleniyor. Yasanın tam metnine
> ulaşamadık; internette dolaşan tutarlar Türkiye'nin mevzuatına ait. Rakam
> yazmıyoruz — güncel tutar için Para, Kambiyo ve İnkişaf Sandığı İşleri Dairesi'ne
> sorun."

Boşluğu gizleyen değil, **ilan eden** cümle. Sitenin ayırt edici deseni budur.

---

## 4. Dil ve ton — mevcut yazılarla aynı olmalı

Yazmadan önce `content/tr/rehber/` altındaki en az bir mevcut yazıyı aç ve ritmini gör.
Yeni yazı onların yanında yabancı durmamalı.

- Sakin ve olgusal. **Hiçbir cümlede ünlem yok.**
- Kısa cümle; bir cümle bir iş yapar.
- "Sen" değil "siz". Resmî değil ama saygılı.
- Şirket övülmez. Puan bir gözlemdir, tavsiye değil.
- "Bu yazımızda", "gelin birlikte bakalım", "unutmayın ki" gibi ısınma ve dolgu
  cümleleri yok. Doğrudan konuya girilir.
- Emoji yok. Abartılı sıfat yok ("muhteşem", "en iyi", "kesinlikle").
- CTA satın alma değil okuma eylemidir: "Şirketleri karşılaştır", "Nasıl
  puanladığımızı okuyun". "Teklif al", "en ucuzunu bul" **kullanılmaz.**

Terimler `copy/00-brief.md` sözlüğünde sabittir. Kurum adları çevrilmez, ilk geçişte
açıklanır (KKSRSB, KKSBM, Para Kambiyo Dairesi).

---

## 5. Yazıyı oluştur

```bash
python3 _build/yeni-yazi.py "Kuyruktaki başlık" --kategori Ayrım
```

Kategori kuyruktaki değerdir. **Yeni kategori uydurulmaz** — her yeni değer yeni bir
konu sayfası üretir. Geçerli olanlar: `Ayrım` · `Hasar` · `Yabancılar` ·
`Sınır geçişi` · `Şirket seçimi` · `Şeffaflık` · `Ürün`.

Frontmatter'da doldurulacaklar: `aciklama` (150–160 karakter, hedef sorguyu doğal
biçimde içerir), `ozet` (2–3 cümle), `giris` (bir paragraf), `tarih` ve `guncelleme`
(bugün). `taslak: evet` satırı **silinir** — yoksa yazı üretilmez.

### Gövde

Markdown. Uzunluk 900–1.600 kelime; dolgu yaparak uzatılmaz. İskelet:

1. Giriş — sorunun ne olduğu, doğrudan.
2. `## Kısa cevap` — sorunun cevabı 2–4 cümlede. **Bu bölüm zorunludur.**
3. Konu başlıkları (`##`) — her biri tek bir soruyu karşılar, soru biçiminde ya da
   olgusal başlıkla.
4. `## Doğrulayamadıklarımız` — kuyruğun boşluk sütunu buraya yazılır. **Zorunlu.**
5. `## Kaynaklar` — bakılan her kaynak, adı ve tarihiyle. **Zorunlu.**

Tablo, sıralı liste ve kısa paragraf serbesttir; `YAZI-YAZMA.md` §3'teki tasarım
sınıfları kullanılabilir. Ham `<section>` bloğu isteğe bağlıdır, zorunlu değildir.

### Arama ve AI görünürlüğü

Bu site referans sitesidir; ölçüsü trafik değil **alıntılanabilirliktir.** Pratikte:

- `## Kısa cevap` bölümü doğrudan alıntılanabilir olmalı — bağlamsız okunduğunda da
  doğru ve tam bir cevap vermeli.
- Her `##` başlığı gerçek bir soruya karşılık gelmeli; başlık altındaki ilk paragraf
  o sorunun cevabı olmalı.
- Olgular cümle içinde, kaynak adıyla birlikte durmalı: "KKSRSB'nin yayımladığı üye
  listesine göre…" — kaynağı gövdede taşıyan cümleler alıntılanır.
- Hedef sorgu `baslik`, `aciklama` ve ilk paragrafta doğal biçimde geçer. Anahtar
  kelime tekrarı **yapılmaz**; site ton olarak reklam metni değildir.
- `FAQPage` şeması, yazıda gerçekten soru-cevap yapısı varsa eklenir
  (`YAZI-YAZMA.md` §4). `BlogPosting` şeması **otomatik üretilir, tekrar yazılmaz.**

### İç bağlantı

Kuyruğun "zorunlu bağlantı" sütunundaki her adres yazıda geçmeli. Ek olarak
`copy/01-icerik-stratejisi.md` §5 kuralları:

- Fiyat ya da limit geçen her sayfa, KKTC ≠ Türkiye ayrımına bağlanır.
- "Doğrulayamadık" diyen her yer `/tr/duzeltme/` ya da `/tr/metodoloji/` sayfasına bağlanır.
- İlgili sigorta türü hub'ına (`/tr/sigorta/<brans>/`) bağlanır.
- İlgili şirket verisi varsa `/tr/sirketler/` sayfasına bağlanır.

**Her bağlantı adresi, vermeden önce var olduğu doğrulanır.** Adres `content/` altında
bir dosyaya ya da üretilen bir sayfaya karşılık gelmiyorsa **bağlantı verilmez.**
Kırık iç bağlantı bu sitede içerik hatasından ağır bir hatadır.

Kontrol:

```bash
grep -rl "aradığınız-slug" content/ dist/ 2>/dev/null | head
```

---

## 6. Doğrula — yayından önce

```bash
./yayinla.sh
```

Çıktıda şunlar aranır:

- **"kırık bağlantı"** geçiyorsa: bağlantıyı düzelt, tekrar çalıştır. Kırık
  bağlantıyla yayımlanmaz.
- Yazının adresi üretilenler arasında görünmeli. Görünmüyorsa `taslak` satırı
  silinmemiştir.
- Üretim hata verirse yayımlama; hatayı bildir.

Sonra metni bir kez daha oku ve şu beşini kontrol et:

1. ⛔ tablosundan bir şey yazılmış mı?
2. Kaynağı olmayan bir rakam kalmış mı?
3. `## Doğrulayamadıklarımız` ve `## Kaynaklar` bölümleri var mı?
4. Zorunlu iç bağlantıların hepsi geçiyor mu, hepsi var olan adresler mi?
5. Ton mevcut yazılarla aynı mı — ünlem, emoji, satış dili var mı?

Beşinden biri düşerse **düzelt ve baştan doğrula.** Düzeltilemiyorsa yayımlama.

---

## 7. Kuyruğu güncelle ve yayına gönder

`copy/yayin-kuyrugu.md` içinde o satırın `⬜` işaretini `✅` yap ve başlığın sonuna
yayın tarihini ekle. Sonra:

```bash
git add content/tr/rehber/<slug>.md copy/yayin-kuyrugu.md
git commit -m "Rehber: <yazı başlığı>"
git push origin main
```

`dist/` **commit edilmez** — GitHub Action kendi üretir. Yalnızca kaynak dosya ve
kuyruk gönderilir.

Push edildikten sonra `.github/workflows/yayinla.yml` siteyi üretip FTP ile canlıya
alır. Yayın birkaç dakika sürer.

---

## 8. Durma kuralları

Şu durumlarda **yayımlanmaz**, iş durur ve durum bildirilir:

| Durum | Ne yapılır |
|---|---|
| Kaynak doğrulanamadı ve konu kaynaksız yazılamıyor | Kuyruk satırını `⛔` yap, sebebi satıra yaz |
| ⛔ tablosundaki bir rakam olmadan yazı anlamsız kalıyor | Aynı — `⛔`, sebep yazılır |
| `./yayinla.sh` hata veriyor | Yayımlama, hatayı bildir |
| Kırık iç bağlantı düzeltilemiyor | Yayımlama |
| Kuyrukta `⬜` yok | Dur, yeni başlık uydurma |
| Araştırma dosyasıyla çelişen bulgu | Yayımlama, çelişkiyi bildir |
| `git push` reddedildi | `git pull --rebase` dene; çakışma varsa dur, bildir |

Yayımlamamak bir başarısızlık değildir. Bu sitede **yanlış yayımlamak** başarısızlıktır.
