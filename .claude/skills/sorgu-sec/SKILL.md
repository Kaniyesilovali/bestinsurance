---
name: sorgu-sec
description: "KKTC Sigorta Merkezi için hedef sorgu ve içerik kararı verir. Kullanıcı 'şu sorguda birinci çıkmak istiyorum', 'bu konuda içerik yazalım mı', 'hangi sorguyu hedefleyelim', 'SEO planı', 'kuyruğa satır ekle' dediğinde kullanılır. Yazmaz — neyin yazılacağına karar verir ve kuyruğa satır üretir. Yazma işi yazi-uret becerisinindir."
metadata:
  version: 1.0.0
---

# Sorgu seç — KKTC Sigorta Merkezi

Bu beceri **karar** üretir, metin değil. Çıktısı bir kuyruk satırı ya da bir
"bu hedeflenmez" gerekçesidir. Yazı yazılacaksa devir `yazi-uret` becerisinedir.

Var olma sebebi: genel SEO becerileri bu projenin kurallarını bilmez. Pazar kapsamı,
sorgu sahipliği ve boşluk ilanı bu sitede öneri değil **kapıdır** — dışarıdan gelen
bir denetim listesi bunları atlar.

---

## 0. Önce oku (atlanamaz)

| Dosya | Neden |
|---|---|
| `copy/00-brief.md` | Pazar kapsamı ve ⛔ tablosu. **Bu becerinin en üstündedir.** |
| `copy/yayin-kuyrugu.md` | Sorgunun sahibi zaten var mı |
| `copy/01-icerik-stratejisi.md` | Hangi sütuna düşüyor, iç bağlantı kuralları |
| `copy/03-marka-sorgulari.md` §10 | Sorgu sahipliği kuralının kendisi |

Konu şirket verisine dayanıyorsa ek olarak `data/sirketler.json`.

---

## 1. Sorulan soruyu sabitle

Kullanıcının cümlesini **kendi kelimeleriyle** tek satıra yaz. Cevap bu satıra
dönmek zorunda.

Bu adımın sebebi: araştırma sırasında ilginç bir bulgu çıkar ve sorulan sorunun
yerine geçer. Bulgu değerli olabilir — ama sorulan soru cevapsız kalırsa tur boşa
gitmiştir. Bulguyu ayrı bir aday olarak kenara yaz, sorunun önüne koyma.

---

## 2. Aday sorguları çıkar

Kullanıcının verdiği sorgu ve varyasyonları. Her adayı ayrı satır yap. Bu aşamada
eleme yok, sonraki dört kapı eler.

---

## 3. Kapı 1 — Pazar kapsamı

`copy/00-brief.md` → "Pazar kapsamı" bölümü uygulanır.

- Sorguda **`kktc` ya da `kuzey kıbrıs` nitelemesi var mı?** Yoksa hedeflenmez.
- Çıplak sorgu (`trafik sigortası`, `online sigorta`, `konut sigortası`) hedeflenmez.
  Sebebi hacim değil **niyet**: o sorgunun sahibi poliçe satın almak istiyor, bu site
  poliçe satmıyor ve vereceği cevap o okur için yanlış.

Elenen sorgu için gerekçe yazılır ve **alınabilir varyasyonu önerilir.** "Hedeflenmez"
tek başına cevap değildir; kullanıcı o sorguyu bir sebeple istemiştir.

### Rakip sonuç sayfasına bakmak

Bakılabilir — hedefin alınabilir olup olmadığı ancak orada görülür. İki kural:

1. Bulgular **karar** verisidir, **metin** malzemesi değil. Sonuçta Türkiye çıkması,
   yazının Türkiye'yle açılacağı anlamına gelmez.
2. Ölçülen şey rakibin derinliği ve türüdür: satıcı mı, acente mi, bağımsız mı.
   Bağımsız karşılaştırma yoksa alan boştur — bu sitenin girdiği yer orasıdır.

---

## 4. Kapı 2 — Sorgu sahipliği

`copy/03-marka-sorgulari.md` §10'un kuralı: **bir sorgunun bir sahibi olur.**

`copy/yayin-kuyrugu.md` "Hedef sorgu" sütununda ve yayındaki sayfalarda bu sorguyu
ara. Bulursan üç seçenek vardır — birleştirme yoktur:

| Durum | Yapılacak |
|---|---|
| Sahip var, konusu aynı | Yeni satır açma. Var olan sayfa güncellenir. |
| Sahip var, konusu farklı | Sorgu birine verilir, diğerinin hedef sorgusu değiştirilir |
| Sahip yok | Yeni satır açılabilir |

Kapatılan satır kuyrukta silinmez: `✅` yapılır ve **"— X ile karşılandı, ayrıca
yazılmayacak"** notu düşülür. Numaralandırma bozulmaz.

> "Ayrı konu, ayrı sorgu demek değildir." — §10

---

## 5. Kapı 3 — Veri

Bu sitenin üstünlüğü yazı kalitesi değil, **dışarıdan doğrulanabilen veri.**

- Bu sorguya `data/sirketler.json` ya da `data/arastirma-kktc-sigorta.md` ile
  rakiplerden daha iyi cevap verebiliyor muyuz?
- Veremiyorsak yazı ne söyleyecek? Yalnızca herkesin bildiğini tekrar edecekse
  satır açılmaz.
- Veri varsa **hangi alanla** cevap verileceği satırda yazılır.

---

## 6. Kapı 4 — Dil

Hedef kitle TR konuşmuyorsa (öğrenci, expat, yabancı uyruklu araç sahibi) sorgu TR
sayfayla karşılanamaz.

- `dist/` altında o dil üretiliyor mu?
- `copy/en|ru|fa/` altında ilgili taslak var mı?

Yoksa çıktı yeni bir TR yazısı değil, **çeviri/dil açma işidir.** Bunu böyle söyle;
TR yazı önermek sorunu çözmez.

---

## 7. Boşluk ifadesi

Kuyruğa giren her satır bir **"bunu doğrulayamadık"** cümlesi taşır. Boşluk
bulunamıyorsa konu muhtemelen yeterince araştırılmamıştır — satır açılmaz.

Boşluk uydurma. `data/arastirma-kktc-sigorta.md` ve `copy/00-brief.md` ⛔/⚠
tablolarındaki gerçek boşluklardan gelir.

---

## 8. Çıktı

İki parçadır. Metin yazılmaz.

**a. Sorgu sahipliği tablosu** — hangi sorgu hangi sayfanın:

| Sorgu | Sahip sayfa | Durum |
|---|---|---|

**b. Kuyruk satırı** — `copy/yayin-kuyrugu.md` biçiminde, doğrudan yapıştırılabilir:

```
| № | ⬜ | Başlık | Kategori | Hedef sorgu | Zorunlu bağlantı | İlan edilecek boşluk |
```

Kategori değerleri sabittir: `Ayrım` · `Hasar` · `Yabancılar` · `Sınır geçişi` ·
`Şirket seçimi` · `Şeffaflık` · `Ürün`. Yeni kategori **uydurulmaz** — her yeni
değer yeni bir konu sayfası üretir.

Zorunlu bağlantılar **var olan** adresler olmalı. `dist/` altında yoksa yazılmaz.

---

## 9. Bu beceri şunları yapmaz

- **Yazı yazmaz.** Kuyruk satırı üretir, `yazi-uret` yazar.
- **Kuyruğun sırasını değiştirmez.** Yeni satır bloğun sonuna eklenir; ilk `⬜` kazanır.
- **`data/arastirma-kktc-sigorta.md` dosyasını değiştirmez.**
- **Hacim tahmini üretmez.** GSC bağlanana kadar bu sitede arama hacmi verisi yok;
  `01-icerik-stratejisi.md` bunu açıkça yazıyor. Tahmini ölçüm gibi sunmak, sitenin
  kendi kuralını sitenin planında çiğnemek olur.

---

## 10. Tereddüt edersen

Dur ve sor. Bu beceri `yazi-uret`'ten farklı olarak yayına push etmez — durmanın
maliyeti düşüktür. Yanlış sorguya yazılmış bir yazının maliyeti yüksektir: sorgu
sahipliği bozulur ve iki sayfa birbiriyle yarışır.
