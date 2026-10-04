# Şirket tanıtım sayfaları — kurallar ve tarama yolu

**Durum:** Aşama 1 (pilot: Alfa Sigorta, 3 Ekim 2026) · onay bekliyor
**Yerine geçtiği şey:** puanlama ve "güvenilir mi" profilleri (bkz. commit 9449ef7)

Şirketler, puanların gerçeği yansıtmadığı gerekçesiyle hukuki yola başvurdu. Puan
kalktı, ama profil sayfaları hâlâ bizim yargımızı taşıyordu: iç tarama notları,
✓/— listeleri, "mesafe bir maliyettir" gibi cümleler, iki şirketin aynı IP'de
olduğu iması. Tanıtım sayfası bunların hiçbirini taşımaz.

**Tek ilke:** Sayfada yazan her cümle, şirketin kendi sitesinde gösterilebilir.
Gösterilemiyorsa yazılmaz.

---

## 1. Ne yazılır

| Alan | Örnek | Kaynak |
|---|---|---|
| Birlik üyeliği | "Üye listesinde X unvanıyla yer alıyor." | kksrsb.org/uyelerimiz.html — tek dış kaynak |
| Kuruluş | "Tanıtım metnine göre kuruluş işlemleri 2021'de tamamlandı." | Hakkımızda |
| Şube / ofis | Şirketin saydığı şehirler | Hakkımızda, iletişim, şube sayfası |
| Acente sayısı | Yalnızca şirket bir sayı yazıyorsa, "şirketin sitesine göre" diye | Acente sayfası |
| Ürünler | Ayrı sayfası olan ürünler | Menü / ürün sayfaları |
| Site dilleri | Sitenin sunduğu diller | Dil seçici |
| Hizmetler | Online teklif, hesap, hasar hattı — "belirtiliyor" diye | İlgili sayfa |
| İletişim | Adres, telefon, e-posta, sosyal hesap | Sitenin altbilgisi / iletişim |

Ürün sayfasında: şirketin ürünü nasıl tanımladığı, sitede gösterilen teminat adları,
şirketin yanıtladığı **soruların başlıkları** (yanıtları değil) ve çalışan belge
bağlantıları.

## 2. Ne yazılmaz

- **Mali her şey:** sermaye, prim üretimi, pazar payı, satış, hasar ödeme oranı.
- **Rakamlar:** teminat tutarı, limit, fiyat, indirim, gün sayısı, süre. Şirketin
  sitesinde yazsa da yazılmaz — eski olabilir (Alfa'nın trafik sayfasındaki limit
  yasal limitle uyuşmuyor) ve eskiliğini söylemek de bir ithamdır. Limitler için
  kendi genel rehber sayfamıza bağlanılır.
  *İstisna:* kuruluş yılı, şube/acente/dil sayısı gibi tanıtım sayıları.
- **Reklam iddiaları:** "1 numaralı", "en uygun fiyat", "hızlı onay garantisi",
  "internete özel indirim". Atıfla bile aktarılmaz.
- **Gelecek zamanlı niyetler:** "…faaliyete başlayacaktır", "…hedeflemektedir".
- **Yer tutucular:** "yapım aşamasında" notlu bölümler, "1.23.45.67" gibi değerler.
- **Yokluk ve kusur:** çalışmayan bağlantı, eksik sayfa, SSL, eski telif yılı, test
  ibaresi, yayımlanmayan şartlar. Ne listelenir ne yorumlanır — yalnızca var olan yazılır.
- **Bizim yargımız:** sıfat, öneri, karşılaştırma, "güvenilir mi" gibi yargı taşıyan
  başlık, başka şirketle ilişki iması.
- **Birebir kopya:** şirketin cümleleri kendi cümlemizle, atıfla yazılır
  ("Şirket bu ürünü … olarak tanımlıyor").

Pilotta yazılmayanlar ve nedenleri veri dosyasının `yazilmayanlar` alanında durur
(yayınlanmaz, denetim içindir).

## 3. Tarama yolu (bir şirket)

1. Ana sayfayı tarayıcı kimliğiyle çek (bazı siteler `curl`'ün varsayılan kimliğini
   406 ile reddediyor). Menü ve altbilgideki iç bağlantıları listele.
2. Hakkımızda, iletişim/şubeler, acente ve **her ürün sayfasını** metne çevir.
3. Ürün sayfalarındaki belge bağlantılarını tek tek aç: yalnızca **200** dönenler
   yazılır.
4. Birlik üye listesinde unvanı doğrula.
5. `data/tanitim/<slug>.json` dosyasını yaz: her olgunun `kaynak` adresi zorunlu.
   Türkçe ilgi hâli (`ad_ilgi`: "Alfa Sigorta'nın") elle yazılır, türetilmez.
6. `data/sirketler-a.json` / `-b.json` içindeki ilgili alanları (şubeler, kuruluş
   yılı) tanıtımla uyumla → `python3 data/birlestir.py`.
7. `python3 _build/uret.py --kontrol` — kırık bağlantı yok demeli.
8. Üretilen sayfanın metnini §2'ye karşı satır satır oku.

## 4. Üretim

- `data/tanitim/<slug>.json` varsa `/tr/sirketler/<slug>/` sayfasını
  `sirket_tanitimi()` üretir (`_build/sablon/sirket-tanitim.html`); eski
  `sirket_profilleri()` o şirketi atlar.
- Her ürün `/tr/sirketler/<slug>/<urun-slug>/` adresinde ayrı sayfadır
  (`_build/sablon/sirket-urun.html`). Gövdesi `data/tanitim/<slug>/<urun-slug>.md`
  dosyasıdır; SEO başlığı (`baslik`) ve açıklaması (`aciklama`) veri dosyasında durur.

### Ürün yazısının yapısı (600–1000 kelime)

1. İlk paragraf: anahtar kelime (**"<Şirket> <ürün>"**) kalın ve ilk cümlede.
2. `## <Şirket> <ürünü> nasıl tanımlıyor` — yalnızca şirketin sitesi, atıfla.
   Alt başlıklar (H3): seçenekler/teminatlar, sitedeki işlemler, belgeler (yalnız 200 dönen).
3. `## KKTC'de <ürün> nasıl işler` — "Bu bölüm şirkete özgü değildir" cümlesiyle açılır.
   Kaynağı yalnızca `data/arastirma-kktc-sigorta.md` ve sitenin genel sayfalarıdır;
   brief'in ⛔ tablosu geçerlidir. Rakam yerine sahibi olan sayfaya bağlantı verilir.

**Şirkete bağlantı yok.** Atıf "alfasigorta.net'ten alındı" gibi düz metinle yapılır. Hiçbir sigorta şirketine ya da acenteye (sitesi, ürün sayfası, PDF'i, sosyal medya hesabı) bağlantı verilmez; bu bağlantılar ileride ücretli olarak satılacak. Şirket adı ve alan adı düz metin yazılır. Dış bağlantı yalnızca kamu kurumlarına (KKSRSB, KKSBM, gov.ct.tr) verilir. `_build/uret.py` izin listesi dışındaki dış bağlantıları zaten söker ve yayın çıktısında uyarır.
4. `## … sorulacaklar` — soru listesi; şirket hakkında iddia değil.
5. `## Sıkça Sorulan Sorular` + `### soru` — en az beşi; FAQPage şemasına otomatik basılır.
   Cevaplar yukarıdaki olguları tekrarlar, yeni bilgi eklemez.

İç bağlantı yalnızca `dist/` içinde üretilmiş adreslere verilir; `uret.py --kontrol`
kırık bağlantıyı yakalar.
- "Son kontrol" tarihi, sitemap `lastmod` ve şema `dateModified` aynı alandan
  (`kontrol_tarihi`) gelir.

## 5. Yenileme

- **Aşama 1 (şimdi):** pilot şirket insan onayıyla yayına girer. Onaydan sonra
  kalan 34 şirket aynı yolla hazırlanır.
- **Aşama 2:** aylık zamanlanmış ajan her şirketi §3'e göre yeniden tarar,
  değişiklik varsa veri dosyasını günceller, `kontrol_tarihi`'ni yeniler ve yayına
  gönderir. Değişiklik yoksa yalnızca tarih yenilenir.
- Şirketin sitesi yanıt vermiyorsa sayfa **değiştirilmez**; ajan durumu raporlar.
