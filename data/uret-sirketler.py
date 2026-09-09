#!/usr/bin/env python3
"""
data/sirketler.json → content/tr/sayfa/sirketler/index.html  (filtrelenebilir tablo)
ve content/tr/sayfa/index.html ana sayfa sıralamasının ilk 5 satırı.

Çıktı bir içerik parçasıdır: head/header/footer'ı _build/uret.py ekler.
Sayfaların frontmatter bloğu korunur, yalnızca gövde yenilenir.

Çalıştırma:  python3 data/uret-sirketler.py && python3 _build/uret.py
"""
import json, pathlib, html

KOK = pathlib.Path(__file__).parent.parent
VERI = json.loads((KOK / "data" / "sirketler.json").read_text(encoding="utf-8"))


# Kendi profil sayfası üretilmeyen şirketin ölçütü: adres, e-posta, branş ve dil
# verisinin DÖRDÜ BİRDEN boş. Ölçüt _build/uret.py > sayfasiz_mi() ile aynıdır;
# ikisi birlikte değişir. Gerekçe: copy/02-programatik-seo.md §2.
def sayfasiz_mi(s):
    return not any((s.get("adres"), s.get("email"), s.get("branslar"), s.get("diller")))


SAYFALI = [s for s in VERI if not sayfasiz_mi(s)]      # tabloda, profili var
SAYFASIZ = [s for s in VERI if sayfasiz_mi(s)]         # tablonun altında, profili yok

# Set H — karıştırılan adlar. Profili olmayan şirketin kartı buradan bağlanır.
try:
    KARISIKLIK = json.loads(
        (KOK / "data" / "ad-karisikliklari.json").read_text(encoding="utf-8")
    ).get("kayitlar", [])
except (OSError, ValueError):
    KARISIKLIK = []

# İP-2 — kendi ölçüm sayfası üretilen şirketler.
try:
    VERI_YOK_SAYFALI = set(json.loads(
        (KOK / "data" / "veri-yok-olcumleri.json").read_text(encoding="utf-8")
    ).get("kayitlar", {}))
except (OSError, ValueError):
    VERI_YOK_SAYFALI = set()

BRANS_ADI = {
    "trafik": "Trafik", "kasko": "Kasko", "saglik": "Sağlık", "hayat": "Hayat",
    "konut": "Konut", "isyeri": "İşyeri", "seyahat": "Seyahat",
    "nakliyat": "Nakliyat", "muhendislik": "Mühendislik",
    "sorumluluk": "Sorumluluk", "ferdi_kaza": "Ferdi kaza",
    "tarim": "Tarım", "yat": "Yat",
}
TUR_ADI = {
    "yerel": "Yerel şirket", "tr_subesi": "Türkiye şubesi",
    "tr_ortakligi": "Türkiye ortaklığı", "banka_bagli": "Banka bağlantılı",
    "bilinmiyor": "Yapısı bilinmiyor",
}
BRANS_ADI_EN = {
    "trafik": "Compulsory motor", "kasko": "Comprehensive (kasko)",
    "saglik": "Health", "hayat": "Life", "konut": "Home", "isyeri": "Business",
    "seyahat": "Travel", "nakliyat": "Marine cargo", "muhendislik": "Engineering",
    "sorumluluk": "Liability", "ferdi_kaza": "Personal accident",
    "tarim": "Agriculture", "yat": "Yacht",
}
OLCUT_KISA_EN = ["Transparency", "Product breadth", "Accessibility",
                 "Digital service", "Foreign language", "Corporate depth"]

OLCUT_SIRA = ["seffaflik", "urun", "erisim", "dijital", "dil", "kurumsal"]
OLCUT_KISA = ["Şeffaflık", "Ürün genişliği", "Erişilebilirlik",
              "Dijital hizmet", "Yabancı dil", "Kurumsal derinlik"]


def e(x):
    return html.escape(str(x), quote=True)


# Ana sayfada şirketin tam ticari unvanı değil kısa marka adı görünür
# ("DAĞLI SİGORTA CO LTD." değil "Dağlı Sigorta").
#
# Bu ad TÜRETİLMEZ, okunur. Bir denemede algoritmik büyük/küçük harf çevrimi
# 35 addan en az onunu bozdu: Türkçe I→ı kuralı yabancı markada yanlış sonuç
# veriyor ("CREDITWEST" → "Credıtwest") ve tire kaybı sitenin ayırmaya
# çalıştığı karışıklığı üretiyor ("AS-CAN SİGORTA" → "Ascan Sigorta").
# Adlar data/marka-adlari.json → gorunen_adlar içinde elle yazılır.
try:
    MARKA = json.loads(
        (KOK / "data" / "marka-adlari.json").read_text(encoding="utf-8")
    )
except (OSError, ValueError):
    MARKA = {}

GORUNEN_ADLAR = MARKA.get("gorunen_adlar", {})


def kisa_ad(s):
    """Ana sayfada görünecek kısa ad. Yoksa durur — uydurmaz."""
    ad = GORUNEN_ADLAR.get(s["slug"])
    if not ad:
        raise SystemExit(
            f"DURDU: '{s['ad']}' ({s['slug']}) ilk beşe girdi ama görünen adı yok.\n"
            f"data/marka-adlari.json → gorunen_adlar içine kısa adını yazın.\n"
            f"Ad elle yazılır: büyük/küçük harf çevrimi Türkçe I/İ kuralı ve\n"
            f"tireli adlar yüzünden güvenilir değil."
        )
    return ad


def serit(s, koyu=False, satir=0, dil="tr"):
    """Teminat profili şeridi — 6 puanlanan bant + 2 'veri yok' bandı."""
    olcut_kisa = OLCUT_KISA_EN if dil == "en" else OLCUT_KISA
    yok = "no data collected" if dil == "en" else "veri toplanamadı"
    son = ("Financial strength and claims payment: not published"
           if dil == "en" else "Mali güç ve hasar ödemesi: veri yayımlanmıyor")
    bas = "Cover profile" if dil == "en" else "Teminat profili"
    bant, etiket = [], []
    for i, k in enumerate(OLCUT_SIRA):
        v = s["olcutler"][k]["puan"]
        if v is None:
            bant.append('<i class="cp-nd"></i>')
            etiket.append(f"{olcut_kisa[i]}: {yok}")
        else:
            bant.append(f'<i style="--v:{v/10:.2f}"></i>')
            # Puan her zaman tek ondalıkla yazılır. Veride aynı ölçüt kimi
            # şirkette int (8), kimisinde float (8.0) tutuluyor; str() ile
            # basılınca tek etiketin içinde "Şeffaflık 8" ile "Dijital hizmet
            # 8,0" yan yana düşüyordu. Biçim veriye değil ölçeğe bağlıdır.
            p = f"{v:.1f}" if dil == "en" else f"{v:.1f}".replace('.', ',')
            etiket.append(f"{olcut_kisa[i]} {p}")
    bant.append('<i class="cp-nd"></i><i class="cp-nd"></i>')
    etiket.append(son)
    cls = "cp cp--on-dark" if koyu else "cp"
    return (f'<span class="{cls}" style="--row:{satir}" role="img" '
            f'aria-label="{bas}: {e("; ".join(etiket))}">'
            + "".join(bant) + "</span>")


def satir_html(s, i):
    branslar = s.get("branslar") or []
    sehirler = s.get("ofis_sehirler") or [s["sehir"]]
    canli = s.get("http_durum") in (200, 301, 302)
    puan_renk = "text-sundeep" if s["genel_puan"] >= 6 else "text-text"

    meta = [f'{len(branslar)} branş' if branslar else 'ürün listesi yok',
            " · ".join(sehirler[:3]) + ("…" if len(sehirler) > 3 else "")]
    rozet = ""
    if not canli:
        rozet = ('<span class="badge badge--zorunlu ms-2">Site yayında değil</span>')

    return f'''            <tr data-name="{e(s['ad'])}" data-city="{e(' '.join(sehirler))}"
                data-branches="{e(' '.join(branslar))}" data-score="{s['genel_puan']}"
                data-rank="{s['sira']}">
              <td class="rank-no align-top pt-4">{s['sira']:02d}</td>
              <td class="pe-4">
                <a href="/tr/sirketler/{e(s['slug'])}/" class="u-display text-[15px] link-u">{e(s['ad'])}</a>{rozet}
                <div class="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1.5">
                  {serit(s, koyu=False, satir=i)}
                  <span class="font-mono text-[11px] text-muted">{e(' · '.join(meta))}</span>
                </div>
              </td>
              <td class="text-end align-top pt-3 u-num text-[20px] {puan_renk}">{str(s['genel_puan']).replace('.', ',')}</td>
            </tr>
'''


def frontmatter(dosya):
    """Sayfanın mevcut frontmatter bloğunu korur.

    Bu betik yalnızca gövdeyi (tabloyu) yeniler; başlık, açıklama ve adres
    içerik dosyasında elle düzenlenir. Sayfa iskeletini _build/uret.py ekler.
    """
    if dosya.is_file():
        metin = dosya.read_text(encoding="utf-8")
        if metin.startswith("---"):
            son = metin.find("\n---", 3)
            if son != -1:
                return metin[:son + 5]
    raise SystemExit(f"frontmatter bulunamadı: {dosya}")


SAYI_ADI = {1: "bir", 2: "iki", 3: "üç", 4: "dört", 5: "beş",
            6: "altı", 7: "yedi", 8: "sekiz", 9: "dokuz", 10: "on"}


def yazi_sayi(n):
    return SAYI_ADI.get(n, str(n))


def sayfasiz_kart(s):
    """Profili olmayan şirket için kart: ne bulduğumuz değil, ne bulamadığımız.

    Gerekçe metni `notlar` alanından gelir — o alan tarama sırasında neden veri
    toplanamadığını zaten yazıyor. Şablon cümle üretmiyoruz.
    """
    sebep = s.get("notlar") or "Tarama sırasında şirkete ait doğrulanabilir bir kayıt bulunamadı."
    web = (s.get("web") or "").strip()
    durum = {"ölü": "alan adı yanıt vermiyor", "site_yok": "web sitesi bulunamadı"}.get(
        s.get("http_durum"), "sitesi doğrulanamadı")
    kunye = f"{e(web)} — {durum}" if web else durum
    # İP-2 — bu şirketin kendi ölçüm sayfası varsa kart adı oraya bağlanır.
    ek = ""
    if s["slug"] in VERI_YOK_SAYFALI:
        ek = (f'\n        <p class="text-[14px] mt-3"><a href="/tr/sirketler/{e(s["slug"])}/" '
              f'class="text-sea link-u arrow arrow--sm">Ne ölçtük, nasıl ölçtük</a></p>')
    else:
        for kay in KARISIKLIK:
            if s["slug"] in kay["taraflar"]:
                ek = (f'\n        <p class="text-[14px] mt-3"><a href="/tr/sirketler/karsilastirma/'
                      f'{kay["slug"]}/" class="text-sea link-u arrow arrow--sm">{e(kay["h1"])}</a></p>')
                break
    return f'''      <li class="border border-line bg-white rounded-[14px] p-5">
        <p class="u-display text-[15px] mb-1">{e(s['ad'])}</p>
        <p class="font-mono text-[11px] text-muted mb-3">{kunye}</p>
        <p class="text-[14px] text-muted leading-relaxed">{e(sebep)}</p>{ek}
      </li>
'''


# ── EN ────────────────────────────────────────────────────────────────────
# /en/companies/ aynı veriden üretilir. Elle yazılsaydı puanlar güncellendiğinde
# sessizce bayatlar ve iki dil aynı şirket için farklı puan gösterirdi.
#
# Şirket profilleri yalnızca TR'de var (35 sayfa). EN satırındaki ad bu yüzden
# TR profiline bağlanır ve bağlantı görünür biçimde TR olarak işaretlenir —
# okuru habersiz başka bir dile göndermek yerine ne olduğunu söylüyoruz.
# Boşluk sayfanın kendisinde de ilan edilir (bkz. copy/04-dil-katmani.md §5).

def satir_html_en(s, i):
    branslar = s.get("branslar") or []
    sehirler = s.get("ofis_sehirler") or [s["sehir"]]
    canli = s.get("http_durum") in (200, 301, 302)
    puan_renk = "text-sundeep" if s["genel_puan"] >= 6 else "text-text"

    meta = [f'{len(branslar)} classes' if branslar else 'no product list',
            " · ".join(sehirler[:3]) + ("…" if len(sehirler) > 3 else "")]
    rozet = "" if canli else '<span class="badge badge--zorunlu ms-2">Website down</span>'

    return f'''            <tr data-name="{e(s['ad'])}" data-city="{e(' '.join(sehirler))}"
                data-branches="{e(' '.join(branslar))}" data-score="{s['genel_puan']}"
                data-rank="{s['sira']}">
              <td class="rank-no align-top pt-4">{s['sira']:02d}</td>
              <td class="pe-4">
                <a href="/tr/sirketler/{e(s['slug'])}/" hreflang="tr" class="u-display text-[15px] link-u">{e(s['ad'])}</a><span class="u-cap ms-1.5" title="Company profiles are published in Turkish only">TR</span>{rozet}
                <div class="flex flex-wrap items-center gap-x-3 gap-y-1 mt-1.5">
                  {serit(s, koyu=False, satir=i, dil="en")}
                  <span class="font-mono text-[11px] text-muted">{e(' · '.join(meta))}</span>
                </div>
              </td>
              <td class="text-end align-top pt-3 u-num text-[20px] {puan_renk}">{s['genel_puan']:.1f}</td>
            </tr>
'''


def sayfasiz_kart_en(s):
    sebep = s.get("notlar") or "No verifiable record for this company was found during the survey."
    web = (s.get("web") or "").strip()
    durum = {"ölü": "domain does not respond", "site_yok": "no website found"}.get(
        s.get("http_durum"), "website could not be verified")
    kunye = f"{e(web)} — {durum}" if web else durum
    return f'''      <li class="border border-line bg-white rounded-[14px] p-5">
        <p class="u-display text-[15px] mb-1">{e(s['ad'])}</p>
        <p class="font-mono text-[11px] text-muted mb-3">{kunye}</p>
        <p class="text-[14px] text-muted leading-relaxed" lang="tr">{e(sebep)}</p>
      </li>
'''


def satir_html_ana_en(s, i):
    sehirler = s.get("ofis_sehirler") or [s["sehir"]]
    branslar = s.get("branslar") or []
    meta = (f"{sehirler[0]} · {len(branslar)} classes" if branslar
            else f"{sehirler[0]} · no product list")
    return f'''        <tr>
          <td class="rank-no align-top">{s['sira']:02d}</td>
          <td class="pe-4">
            <a href="/tr/sirketler/{e(s['slug'])}/" hreflang="tr" class="text-[17px] font-medium link-u">{e(kisa_ad(s))}</a><span class="u-cap ms-1.5" title="Company profiles are published in Turkish only">TR</span>
            <div class="flex flex-wrap items-center gap-x-3 gap-y-1 mt-2">
              {serit(s, koyu=False, satir=i, dil="en")}
              <span class="u-cap">{e(meta)}</span>
            </div>
          </td>
          <td class="text-end align-top u-num text-[28px] font-medium leading-[1.1]">{s['genel_puan']:.1f}</td>
        </tr>
'''


EN_FRONTMATTER = '''---
baslik: "39 insurance companies licensed in the TRNC — scores and comparison"
aciklama: "The full list of the 39 non-life insurance companies licensed in Northern Cyprus, with scores for transparency, product breadth, accessibility and digital service."
url: /en/companies/
menu: sirketler
og_aciklama: "Which company sells what in Northern Cyprus, and which one can you actually reach? An independent comparison on six observable measures."
---

'''


def govde_en(canli, olu):
    branslar = sorted({b for s in VERI for b in (s.get("branslar") or [])},
                      key=lambda b: BRANS_ADI_EN[b])
    brans_opt = "\n".join(
        f'            <option value="{e(b)}">{e(BRANS_ADI_EN[b])}</option>' for b in branslar)
    satirlar = "".join(satir_html_en(s, i) for i, s in enumerate(SAYFALI))
    kartlar = "".join(sayfasiz_kart_en(s) for s in SAYFASIZ)

    return f'''
<section class="bg-ink text-white">
  <div class="mx-auto max-w-shell px-5 sm:px-8 py-14 sm:py-16">
    <nav aria-label="Location" class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-6">
      <a href="/en/" class="hover:text-white">Home</a> <span class="mx-2">/</span> Companies
    </nav>
    <div class="grid lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] gap-10 lg:gap-16 items-start">
      <div>
        <h1 class="u-display u-display--tight text-[2.25rem] sm:text-[3rem] leading-[1.05] mb-5">
          {len(VERI)} insurance companies licensed in the TRNC
        </h1>
        <p class="text-[17px] leading-relaxed text-white/75 mb-4">
          Every company here is a member of KKSRSB, the association of insurance and
          reinsurance companies of Northern Cyprus. Agents and brokers are not on this
          list — they are not the risk carrier behind your policy.
        </p>
        <p class="text-[15px] leading-relaxed text-white/55 border-s-2 border-sun ps-4">
          Scores are based on six observable measures. Financial strength and claims
          payment performance are not scored — in the TRNC these data are not published
          company by company.
          <a href="/en/methodology/" class="text-sun link-u">Methodology</a>
        </p>
      </div>
      <dl class="grid grid-cols-2 gap-x-8 gap-y-5">
        <div class="border-t border-ink3 pt-3">
          <dt class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-1">Licensed companies</dt>
          <dd class="u-num text-[28px] text-sun">{len(VERI)}</dd>
        </div>
        <div class="border-t border-ink3 pt-3">
          <dt class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-1">Working website</dt>
          <dd class="u-num text-[28px]">{canli}</dd>
        </div>
        <div class="border-t border-ink3 pt-3">
          <dt class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-1">No site or dead</dt>
          <dd class="u-num text-[28px] text-flag">{olu}</dd>
        </div>
        <div class="border-t border-ink3 pt-3">
          <dt class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-1">Data collected</dt>
          <dd class="text-[15px] text-white/85 pt-1.5">July 2026</dd>
        </div>
      </dl>
    </div>
  </div>
</section>

<section class="border-b border-line">
  <div class="mx-auto max-w-shell px-5 sm:px-8 py-10 sm:py-14">

    <div class="flex flex-wrap items-end gap-4 mb-6">
      <div class="flex-1 min-w-[200px]">
        <label for="ara" class="u-eyebrow block mb-2">Search company or city</label>
        <input id="ara" type="search" data-filter-search placeholder="e.g. Dağlı, Girne"
               class="w-full border border-line bg-white px-4 py-2.5 text-[15px] rounded-sm">
      </div>
      <div class="min-w-[180px]">
        <label for="brans" class="u-eyebrow block mb-2">By class of insurance</label>
        <select id="brans" data-filter-branch class="w-full border border-line bg-white px-4 py-2.5 text-[15px] rounded-sm">
            <option value="">All classes</option>
{brans_opt}
        </select>
      </div>
      <p class="text-sm text-muted pb-3">
        <span data-filter-count class="u-num text-text">{len(SAYFALI)}</span> companies shown
      </p>
    </div>

    <div class="overflow-x-auto">
      <table class="rank rank--light" data-filter-table>
        <caption class="sr-only">Insurance companies licensed in the TRNC, ranked by overall score</caption>
        <thead>
          <tr>
            <th scope="col" class="w-8">#</th>
            <th scope="col">Company · cover profile</th>
            <th scope="col" class="text-end cursor-pointer" data-sort="score" aria-sort="descending" tabindex="0">Score</th>
          </tr>
        </thead>
        <tbody>
{satirlar}        </tbody>
      </table>
    </div>

    <p class="text-sm text-muted mt-5 max-w-3xl leading-relaxed">
      <strong class="text-text">Company profiles are published in Turkish only.</strong>
      Each name above links to its Turkish profile page, marked TR. We have not yet
      produced English profiles for the {len(SAYFALI)} companies; the scores, cities and
      classes shown in this table are the same data those pages are built from.
    </p>

    <div class="mt-8 grid md:grid-cols-[auto_minmax(0,1fr)] gap-6 md:gap-10 items-start border border-line bg-white p-6">
      <div aria-hidden="true">
        <span class="cp cp--lg">
          <i style="--v:.85"></i><i style="--v:.72"></i><i style="--v:.64"></i><i style="--v:.80"></i><i style="--v:.50"></i><i style="--v:.70"></i><i class="cp-nd"></i><i class="cp-nd"></i>
        </span>
        <div class="flex gap-1 mt-2">
          <span class="u-num text-[10px] text-muted w-[18px] text-center">01</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">02</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">03</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">04</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">05</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">06</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center ms-[14px]">—</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">—</span>
        </div>
      </div>
      <div>
        <p class="u-eyebrow mb-3">Reading the bands</p>
        <ol class="grid sm:grid-cols-2 gap-x-8 gap-y-1 text-sm text-muted mb-4">
          <li><span class="u-num text-sundeep">01</span> Transparency <span class="u-num text-xs">25%</span></li>
          <li><span class="u-num text-sundeep">02</span> Product breadth <span class="u-num text-xs">20%</span></li>
          <li><span class="u-num text-sundeep">03</span> Accessibility <span class="u-num text-xs">20%</span></li>
          <li><span class="u-num text-sundeep">04</span> Digital service <span class="u-num text-xs">20%</span></li>
          <li><span class="u-num text-sundeep">05</span> Foreign language <span class="u-num text-xs">10%</span></li>
          <li><span class="u-num text-sundeep">06</span> Corporate depth <span class="u-num text-xs">5%</span></li>
        </ol>
        <p class="text-sm text-muted leading-relaxed">
          <strong class="text-text">Hatched bands are measures that are not scored.</strong>
          The last two are the same for every company: financial strength and claims payment
          performance — in the TRNC these have not been published company by company since
          2016. If a company has a hatched band among its other measures, no data could be
          collected for that measure; it does not count as zero, its weight is distributed
          across the remaining measures.
        </p>
      </div>
    </div>

    <p class="text-sm text-muted mt-6 max-w-3xl leading-relaxed">
      Data collected in July 2026. If something here about your company is wrong,
      <a href="/tr/duzeltme/" hreflang="tr" class="text-sea link-u">tell us with the
      source</a> <span class="u-cap">TR</span> — we will check it and correct it. Only
      verifiable evidence changes a score.
    </p>
  </div>
</section>

<section id="veri-yok" class="bg-paper border-b border-line">
  <div class="mx-auto max-w-shell px-5 sm:px-8 py-12 sm:py-14">
    <div class="max-w-prose mb-8">
      <p class="u-eyebrow mb-3">Not in the table above</p>
      <h2 class="u-display text-[1.5rem] sm:text-[1.875rem] leading-[1.15] mb-4">
        {len(SAYFASIZ)} companies we could not collect data on
      </h2>
      <p class="text-[15px] text-muted leading-relaxed">
        These {len(SAYFASIZ)} companies are licensed members of the association — they have
        not been struck off. But we could not find <strong class="text-text">any of the
        four</strong>: address, email, products or service languages. With nothing to score
        we do not put them in the table, and with nothing to tell we do not give them a page.
        What we looked for and what we could not find is written here.
      </p>
    </div>

    <ul class="grid sm:grid-cols-2 gap-4 mb-6">
{kartlar}    </ul>
  </div>
</section>
'''


def main():
    canli = sum(1 for s in VERI if s.get("http_durum") in (200, 301, 302))
    olu = len(VERI) - canli
    branslar = sorted({b for s in VERI for b in (s.get("branslar") or [])},
                      key=lambda b: BRANS_ADI[b])
    sehirler = sorted({c for s in VERI for c in (s.get("ofis_sehirler") or [s["sehir"]])})
    sayfasiz_kartlar = "".join(sayfasiz_kart(s) for s in SAYFASIZ)

    brans_opt = "\n".join(
        f'            <option value="{e(b)}">{e(BRANS_ADI[b])}</option>' for b in branslar)

    govde = f'''
<section class="bg-ink text-white">
  <div class="mx-auto max-w-shell px-5 sm:px-8 py-14 sm:py-16">
    <nav aria-label="Konum" class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-6">
      <a href="/tr/" class="hover:text-white">Ana sayfa</a> <span class="mx-2">/</span> Şirketler
    </nav>
    <div class="grid lg:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)] gap-10 lg:gap-16 items-start">
      <div>
        <h1 class="u-display u-display--tight text-[2.25rem] sm:text-[3rem] leading-[1.05] mb-5">
          KKTC'de güvenilir sigorta şirketi nasıl seçilir
        </h1>
        <p class="text-[17px] leading-relaxed text-white/75 mb-4">
          Güvenilirliğin ölçülebilen kısmı, şirketin kendisi hakkında ne yayımladığıdır.
          Mali güç ve hasar ödeme verisi Kuzey Kıbrıs'ta şirket bazında yayımlanmıyor —
          bu yüzden puanlamıyoruz. Aşağıdaki {len(VERI)} ruhsatlı şirketi, dışarıdan
          doğrulanabilen altı ölçüte göre sıraladık.
        </p>
        <p class="text-[15px] leading-relaxed text-white/75 mb-4">
          Listedeki her şirket KKTC Sigorta ve Reasürans Şirketleri Birliği üyesidir.
          Acenteler ve brokerler bu listede yer almaz — poliçenizin arkasındaki risk
          taşıyıcı onlar değildir.
        </p>
        <p class="text-[15px] leading-relaxed text-white/55 border-s-2 border-sun ps-4">
          Bir şirketi kendiniz kontrol etmek isterseniz sekiz işaret var; her biri
          şirketin kendi sitesinden beş dakikada doğrulanır.
          <a href="/tr/rehber/kktc-sigorta-sirketi-guvenilir-mi/" class="text-sun link-u">Güvenilirlik nasıl ölçülür</a>
          <span class="mx-1">·</span>
          <a href="/tr/metodoloji/" class="text-sun link-u">Metodoloji</a>
        </p>
      </div>
      <dl class="grid grid-cols-2 gap-x-8 gap-y-5">
        <div class="border-t border-ink3 pt-3">
          <dt class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-1">Toplam şirket</dt>
          <dd class="u-num text-[28px] text-sun">{len(VERI)}</dd>
        </div>
        <div class="border-t border-ink3 pt-3">
          <dt class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-1">Sitesi çalışan</dt>
          <dd class="u-num text-[28px]">{canli}</dd>
        </div>
        <div class="border-t border-ink3 pt-3">
          <dt class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-1">Sitesi yok veya ölü</dt>
          <dd class="u-num text-[28px] text-flag">{olu}</dd>
        </div>
        <div class="border-t border-ink3 pt-3">
          <dt class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-1">Veri toplama</dt>
          <dd class="text-[15px] text-white/85 pt-1.5">Temmuz 2026</dd>
        </div>
      </dl>
    </div>
  </div>
</section>

<section class="border-b border-line">
  <div class="mx-auto max-w-shell px-5 sm:px-8 py-10 sm:py-14">

    <div class="flex flex-wrap items-end gap-4 mb-6">
      <div class="flex-1 min-w-[200px]">
        <label for="ara" class="u-eyebrow block mb-2">Şirket veya şehir ara</label>
        <input id="ara" type="search" data-filter-search placeholder="Örn. Dağlı, Girne"
               class="w-full border border-line bg-white px-4 py-2.5 text-[15px] rounded-sm">
      </div>
      <div class="min-w-[180px]">
        <label for="brans" class="u-eyebrow block mb-2">Branşa göre</label>
        <select id="brans" data-filter-branch class="w-full border border-line bg-white px-4 py-2.5 text-[15px] rounded-sm">
            <option value="">Tüm branşlar</option>
{brans_opt}
        </select>
      </div>
      <p class="text-sm text-muted pb-3">
        <span data-filter-count class="u-num text-text">{len(SAYFALI)}</span> şirket gösteriliyor
      </p>
    </div>

    <div class="overflow-x-auto">
      <table class="rank rank--light" data-filter-table>
        <caption class="sr-only">KKTC'de ruhsatlı sigorta şirketleri, genel puana göre sıralanmış</caption>
        <thead>
          <tr>
            <th scope="col" class="w-8">#</th>
            <th scope="col">Şirket · teminat profili</th>
            <th scope="col" class="text-end cursor-pointer" data-sort="score" aria-sort="descending" tabindex="0">Puan</th>
          </tr>
        </thead>
        <tbody>
{"".join(satir_html(s, i) for i, s in enumerate(SAYFALI))}        </tbody>
      </table>
    </div>

    <div class="mt-8 grid md:grid-cols-[auto_minmax(0,1fr)] gap-6 md:gap-10 items-start border border-line bg-white p-6">
      <div aria-hidden="true">
        <span class="cp cp--lg">
          <i style="--v:.85"></i><i style="--v:.72"></i><i style="--v:.64"></i><i style="--v:.80"></i><i style="--v:.50"></i><i style="--v:.70"></i><i class="cp-nd"></i><i class="cp-nd"></i>
        </span>
        <div class="flex gap-1 mt-2">
          <span class="u-num text-[10px] text-muted w-[18px] text-center">01</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">02</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">03</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">04</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">05</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">06</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center ms-[14px]">—</span>
          <span class="u-num text-[10px] text-muted w-[18px] text-center">—</span>
        </div>
      </div>
      <div>
        <p class="u-eyebrow mb-3">Şeridi okuma</p>
        <ol class="grid sm:grid-cols-2 gap-x-8 gap-y-1 text-sm text-muted mb-4">
          <li><span class="u-num text-sundeep">01</span> Şeffaflık ve doğrulanabilirlik <span class="u-num text-xs">%25</span></li>
          <li><span class="u-num text-sundeep">02</span> Ürün ve teminat genişliği <span class="u-num text-xs">%20</span></li>
          <li><span class="u-num text-sundeep">03</span> Erişilebilirlik <span class="u-num text-xs">%20</span></li>
          <li><span class="u-num text-sundeep">04</span> Dijital hizmet <span class="u-num text-xs">%20</span></li>
          <li><span class="u-num text-sundeep">05</span> Yabancı dilde hizmet <span class="u-num text-xs">%10</span></li>
          <li><span class="u-num text-sundeep">06</span> Kurumsal derinlik <span class="u-num text-xs">%5</span></li>
        </ol>
        <p class="text-sm text-muted leading-relaxed">
          <strong class="text-text">Taralı bantlar puanlanmayan ölçütlerdir.</strong>
          Sondaki ikisi her şirkette aynıdır: mali güç ve hasar ödeme performansı —
          KKTC'de bu veriler 2016'dan beri şirket bazında yayımlanmıyor. Bir şirketin
          ölçütleri arasında ayrıca taralı bant varsa, o ölçütte veri toplanamamış demektir;
          o ölçüt sıfır sayılmaz, ağırlığı kalan ölçütlere dağıtılır.
        </p>
      </div>
    </div>

    <p class="text-sm text-muted mt-6 max-w-3xl leading-relaxed">
      Veriler Temmuz 2026'da toplandı. Hakkınızdaki bir bilgi yanlışsa
      <a href="/tr/duzeltme/" class="text-sea link-u">kaynağıyla birlikte bildirin</a> —
      inceleyip düzeltiriz. Puanı yalnızca doğrulanabilir kanıt değiştirir.
    </p>
  </div>
</section>

<section id="veri-yok" class="bg-paper border-b border-line">
  <div class="mx-auto max-w-shell px-5 sm:px-8 py-12 sm:py-14">
    <div class="max-w-prose mb-8">
      <p class="u-eyebrow mb-3">Yukarıdaki tabloda olmayanlar</p>
      <h2 class="u-display text-[1.5rem] sm:text-[1.875rem] leading-[1.15] mb-4">
        Veri toplayamadığımız {yazi_sayi(len(SAYFASIZ))} şirket
      </h2>
      <p class="text-[15px] text-muted leading-relaxed">
        Bu {yazi_sayi(len(SAYFASIZ))} şirket Birlik'in ruhsatlı üyesidir — listeden
        düşmüş değillerdir. Ama adres, e-posta, ürün ve hizmet dili verisinin
        <strong class="text-text">dördünü birden</strong> bulamadık. Puanlayacak bir
        şey olmadığı için tabloya, anlatacak bir şey olmadığı için de ayrı sayfaya
        koymuyoruz. Ne aradığımızı ve ne bulamadığımızı burada yazıyoruz.
      </p>
    </div>

    <ul class="grid sm:grid-cols-2 gap-4 mb-6">
{sayfasiz_kartlar}    </ul>

    <p class="text-sm text-muted max-w-prose leading-relaxed">
      Bu şirketlerden birini temsil ediyorsanız
      <a href="/tr/duzeltme/" class="text-sea link-u">bize yazın</a> — adres, iletişim
      ve ürün bilgisi geldiğinde şirket tabloya girer ve kendi sayfası açılır.
    </p>
  </div>
</section>
'''

    # Çıktı artık içerik parçasıdır: head/header/footer'ı _build/uret.py ekler.
    # Sayfanın frontmatter'ı korunur, yalnızca gövde yenilenir.
    cikti = KOK / "content" / "tr" / "sayfa" / "sirketler" / "index.html"
    cikti.parent.mkdir(parents=True, exist_ok=True)
    cikti.write_text(frontmatter(cikti) + govde.lstrip("\n"), encoding="utf-8")
    print(f"→ content/tr/sayfa/sirketler/index.html ({len(SAYFALI)} profilli satır, {len(SAYFASIZ)} profilsiz, {canli} canlı, {olu} ölü)")

    # EN şirketler sayfası — aynı veriden, aynı anda.
    en_cikti = KOK / "content" / "en" / "sayfa" / "companies" / "index.html"
    en_cikti.parent.mkdir(parents=True, exist_ok=True)
    en_fm = frontmatter(en_cikti) if en_cikti.is_file() else EN_FRONTMATTER
    en_cikti.write_text(en_fm + govde_en(canli, olu).lstrip("\n"), encoding="utf-8")
    print(f"→ content/en/sayfa/companies/index.html ({len(SAYFALI)} satır, {len(SAYFASIZ)} profilsiz)")

    # Ana sayfalardaki ilk 5 satır gerçek veriyle değiştirilir — TR ve EN.
    ana_sirala(KOK / "content" / "tr" / "sayfa" / "index.html",
               satir_html_ana, "content/tr/sayfa/index.html")
    ana_sirala(KOK / "content" / "en" / "sayfa" / "index.html",
               satir_html_ana_en, "content/en/sayfa/index.html")


def ana_sirala(dosya, satirci, ad):
    """Ana sayfadaki sıralama tablosunun gövdesini veriden yeniler.

    Girinti sabit yazılmaz: ana sayfa elle düzenlenen bir dosya ve girintisi
    bir kez değiştiğinde sabit desen sessizce eşleşmez olur. Eşleşme
    bulunamazsa **durulur** — sessiz atlamak, şirketler sayfası güncellenmişken
    ana sayfanın eski puanları göstermesi demekti.
    """
    import re
    if not dosya.is_file():
        return
    s = dosya.read_text(encoding="utf-8")
    ilk5 = "".join(satirci(x, i) for i, x in enumerate(SAYFALI[:5]))
    esles = re.search(r"([ \t]*)<tbody>.*?\1</tbody>", s, re.S)
    if not esles:
        raise SystemExit(
            f"DURDU: {ad} içinde <tbody>…</tbody> bulunamadı.\n"
            "Sıralama tablosu elle değiştirilmiş olabilir. Tablo güncellenmeden\n"
            "bırakılırsa ana sayfa ile şirketler sayfası aynı şirketler için\n"
            "farklı puan gösterir — bu yüzden atlanmıyor, duruluyor."
        )
    girinti = esles.group(1)
    s2 = (s[:esles.start()] + f"{girinti}<tbody>\n" + ilk5
          + f"{girinti}</tbody>" + s[esles.end():])
    s2 = s2.replace('<p class="badge badge--taslak mb-4">Taslak veri</p>\n\n        ', '')
    if s2 != s:
        dosya.write_text(s2, encoding="utf-8")
        print(f"→ {ad} sıralaması gerçek veriyle güncellendi")
    else:
        print(f"→ {ad} sıralaması zaten güncel")


def satir_html_ana(s, i):
    sehirler = s.get("ofis_sehirler") or [s["sehir"]]
    branslar = s.get("branslar") or []
    meta = (f"{sehirler[0]} · {len(branslar)} branş" if branslar
            else f"{sehirler[0]} · ürün listesi yok")
    return f'''        <tr>
          <td class="rank-no align-top">{s['sira']:02d}</td>
          <td class="pe-4">
            <a href="/tr/sirketler/{e(s['slug'])}/" class="text-[17px] font-medium link-u">{e(kisa_ad(s))}</a>
            <div class="flex flex-wrap items-center gap-x-3 gap-y-1 mt-2">
              {serit(s, koyu=False, satir=i)}
              <span class="u-cap">{e(meta)}</span>
            </div>
          </td>
          <td class="text-end align-top u-num text-[28px] font-medium leading-[1.1]">{str(s['genel_puan']).replace('.', ',')}</td>
        </tr>
'''


if __name__ == "__main__":
    main()
