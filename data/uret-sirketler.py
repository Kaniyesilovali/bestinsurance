#!/usr/bin/env python3
"""
data/sirketler.json → tr/sirketler/index.html  (statik, filtrelenebilir tablo)
ve tr/index.html ana sayfa sıralamasının ilk 5 satırı.

Üretilen çıktı saf HTML'dir; sitede çalışma anında hiçbir şablon motoru yok.
Çalıştırma:  python3 data/uret-sirketler.py
"""
import json, pathlib, html

KOK = pathlib.Path(__file__).parent.parent
VERI = json.loads((KOK / "data" / "sirketler.json").read_text(encoding="utf-8"))

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
OLCUT_SIRA = ["seffaflik", "urun", "erisim", "dijital", "dil", "kurumsal"]
OLCUT_KISA = ["Şeffaflık", "Ürün genişliği", "Erişilebilirlik",
              "Dijital hizmet", "Yabancı dil", "Kurumsal derinlik"]


def e(x):
    return html.escape(str(x), quote=True)


def serit(s, koyu=False, satir=0):
    """Teminat profili şeridi — 6 puanlanan bant + 2 'veri yok' bandı."""
    bant, etiket = [], []
    for i, k in enumerate(OLCUT_SIRA):
        v = s["olcutler"][k]["puan"]
        if v is None:
            bant.append('<i class="cp-nd"></i>')
            etiket.append(f"{OLCUT_KISA[i]}: veri toplanamadı")
        else:
            bant.append(f'<i style="--v:{v/10:.2f}"></i>')
            etiket.append(f"{OLCUT_KISA[i]} {str(v).replace('.', ',')}")
    bant.append('<i class="cp-nd"></i><i class="cp-nd"></i>')
    etiket.append("Mali güç ve hasar ödemesi: veri yayımlanmıyor")
    cls = "cp cp--on-dark" if koyu else "cp"
    return (f'<span class="{cls}" style="--row:{satir}" role="img" '
            f'aria-label="Teminat profili: {e("; ".join(etiket))}">'
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


BASLIK = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KKTC sigorta şirketleri — 39 ruhsatlı şirket karşılaştırması | Kıbrıs Sigorta Rehberi</title>
<meta name="description" content="Kuzey Kıbrıs'ta ruhsatlı 39 sigorta şirketinin tam listesi. Şeffaflık, ürün genişliği, erişilebilirlik, dijital hizmet ve yabancı dilde hizmet açısından karşılaştırın. Branşa ve şehre göre filtreleyin.">
<link rel="canonical" href="https://ORNEK-ALAN-ADI.com/tr/sirketler/">
<link rel="alternate" hreflang="tr" href="https://ORNEK-ALAN-ADI.com/tr/sirketler/">
<link rel="alternate" hreflang="en" href="https://ORNEK-ALAN-ADI.com/en/companies/">
<link rel="alternate" hreflang="ru" href="https://ORNEK-ALAN-ADI.com/ru/kompanii/">
<link rel="alternate" hreflang="fa" href="https://ORNEK-ALAN-ADI.com/fa/companies/">
<link rel="alternate" hreflang="x-default" href="https://ORNEK-ALAN-ADI.com/tr/sirketler/">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:title" content="KKTC sigorta şirketleri — 39 ruhsatlı şirket karşılaştırması">
<meta property="og:description" content="Ruhsatlı şirketlerin tam listesi, altı gözlemlenebilir ölçütle karşılaştırıldı.">
<meta property="og:url" content="https://ORNEK-ALAN-ADI.com/tr/sirketler/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = { theme: { extend: {
  colors: {
    ink:'#0D2B28', ink2:'#123B36', ink3:'#1B4F47',
    paper:'#EFF1ED', line:'#D7DAD2',
    sea:'#0F6E62', seadeep:'#0A4F46', seasoft:'#DCE9E5',
    sun:'#E0A43B', sundeep:'#A9711A', sunsoft:'#F7ECD7',
    flag:'#C8102E', flagsoft:'#FBE7EA',
    muted:'#586965', muteddark:'#8FA9A3'
  },
  fontFamily: {
    display:['Archivo','system-ui','sans-serif'],
    body:['"IBM Plex Sans"','system-ui','sans-serif'],
    mono:['"IBM Plex Mono"','ui-monospace','monospace']
  },
  maxWidth: { shell:'78rem' }
}}}
</script>
<link rel="stylesheet" href="/assets/css/site.css">
</head>

<body class="min-h-screen flex flex-col">
<a href="#icerik" class="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:m-3 focus:bg-ink focus:text-white focus:px-4 focus:py-2">İçeriğe atla</a>

<header class="sticky top-0 z-40 bg-paper/95 backdrop-blur border-b border-line">
  <div class="mx-auto max-w-shell px-5 sm:px-8 h-16 flex items-center justify-between gap-6">
    <a href="/tr/" class="u-display text-[15px] sm:text-base tracking-tight shrink-0">
      Kıbrıs Sigorta<span class="text-muted font-medium"> Rehberi</span>
    </a>
    <nav class="hidden lg:flex items-center gap-7 text-sm" aria-label="Ana menü">
      <a href="/tr/sirketler/" class="link-u text-sea font-medium" aria-current="page">Şirketler</a>
      <a href="/tr/sigorta/trafik/" class="link-u">Trafik</a>
      <a href="/tr/sigorta/kasko/" class="link-u">Kasko</a>
      <a href="/tr/sigorta/saglik/" class="link-u">Sağlık</a>
      <a href="/tr/rehber/" class="link-u">Rehber</a>
      <a href="/tr/metodoloji/" class="link-u">Nasıl puanlıyoruz</a>
    </nav>
    <div class="flex items-center gap-3">
      <nav aria-label="Dil" class="hidden sm:flex items-center gap-1 font-mono text-[11px] tracking-widest uppercase">
        <span class="px-1.5 py-0.5 bg-ink text-white rounded-sm" aria-current="true">TR</span>
        <a href="/en/companies/" class="px-1.5 py-0.5 text-muted hover:text-ink">EN</a>
        <a href="/ru/kompanii/" class="px-1.5 py-0.5 text-muted hover:text-ink">RU</a>
        <a href="/fa/companies/" class="px-1.5 py-0.5 text-muted hover:text-ink">FA</a>
      </nav>
      <button data-menu-toggle aria-expanded="false" aria-controls="mobil-menu" class="lg:hidden p-2 -mr-2" aria-label="Menüyü aç">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
  <div id="mobil-menu" data-menu hidden class="lg:hidden border-t border-line bg-paper">
    <nav class="mx-auto max-w-shell px-5 py-4 grid gap-1 text-[15px]" aria-label="Mobil menü">
      <a href="/tr/sirketler/" class="py-2 text-sea font-medium">Şirketler</a>
      <a href="/tr/sigorta/trafik/" class="py-2">Trafik sigortası</a>
      <a href="/tr/sigorta/kasko/" class="py-2">Kasko</a>
      <a href="/tr/sigorta/saglik/" class="py-2">Sağlık sigortası</a>
      <a href="/tr/rehber/" class="py-2">Rehber</a>
      <a href="/tr/metodoloji/" class="py-2">Nasıl puanlıyoruz</a>
    </nav>
  </div>
</header>

<main id="icerik" class="flex-1">
'''

ALTBILGI = '''</main>

<footer class="bg-ink2 text-white/70 text-sm">
  <div class="mx-auto max-w-shell px-5 sm:px-8 py-12">
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-8 mb-10">
      <div>
        <p class="u-display text-white text-[15px] mb-3">Kıbrıs Sigorta Rehberi</p>
        <p class="leading-relaxed">Kuzey Kıbrıs'taki sigorta şirketlerini bağımsız olarak değerlendiren bilgi sitesi.</p>
      </div>
      <nav aria-label="Sigorta türleri">
        <p class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-3">Sigorta türleri</p>
        <ul class="space-y-2">
          <li><a href="/tr/sigorta/trafik/" class="link-u">Zorunlu trafik</a></li>
          <li><a href="/tr/sigorta/kasko/" class="link-u">Kasko</a></li>
          <li><a href="/tr/sigorta/saglik/" class="link-u">Sağlık</a></li>
          <li><a href="/tr/sigorta/konut/" class="link-u">Konut</a></li>
          <li><a href="/tr/sigorta/seyahat/" class="link-u">Seyahat</a></li>
        </ul>
      </nav>
      <nav aria-label="Site">
        <p class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-3">Site</p>
        <ul class="space-y-2">
          <li><a href="/tr/sirketler/" class="link-u">Şirketler</a></li>
          <li><a href="/tr/metodoloji/" class="link-u">Puanlama yöntemi</a></li>
          <li><a href="/tr/rehber/" class="link-u">Rehber</a></li>
          <li><a href="/tr/hakkimizda/" class="link-u">Hakkımızda</a></li>
          <li><a href="/tr/iletisim/" class="link-u">İletişim</a></li>
        </ul>
      </nav>
      <nav aria-label="Yasal ve dil">
        <p class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-3">Yasal</p>
        <ul class="space-y-2 mb-6">
          <li><a href="/tr/yasal-uyari/" class="link-u">Yasal uyarı</a></li>
          <li><a href="/tr/gizlilik/" class="link-u">Gizlilik</a></li>
          <li><a href="/tr/duzeltme/" class="link-u">Düzeltme talebi</a></li>
        </ul>
        <p class="font-mono text-[11px] uppercase tracking-widest text-muteddark mb-3">Dil</p>
        <div class="flex gap-2 font-mono text-[11px] uppercase tracking-widest">
          <span class="px-2 py-1 bg-white/15 text-white rounded-sm">TR</span>
          <a href="/en/companies/" class="px-2 py-1 hover:text-white">EN</a>
          <a href="/ru/kompanii/" class="px-2 py-1 hover:text-white">RU</a>
          <a href="/fa/companies/" class="px-2 py-1 hover:text-white">FA</a>
        </div>
      </nav>
    </div>
    <hr class="hairline hairline--dark mb-6">
    <div class="flex flex-col sm:flex-row gap-4 sm:items-center sm:justify-between text-[13px] text-white/50">
      <p>© 2026 Kıbrıs Sigorta Rehberi</p>
      <p class="max-w-xl leading-relaxed">
        Bu sitedeki bilgiler genel bilgilendirme amaçlıdır, sigorta tavsiyesi değildir.
        Poliçe kararı vermeden önce şirketin güncel poliçe şartlarını okuyun.
      </p>
    </div>
  </div>
</footer>

<script src="/assets/js/site.js" defer></script>
</body>
</html>
'''


def main():
    canli = sum(1 for s in VERI if s.get("http_durum") in (200, 301, 302))
    olu = len(VERI) - canli
    branslar = sorted({b for s in VERI for b in (s.get("branslar") or [])},
                      key=lambda b: BRANS_ADI[b])
    sehirler = sorted({c for s in VERI for c in (s.get("ofis_sehirler") or [s["sehir"]])})

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
          KKTC'de ruhsatlı 39 sigorta şirketi
        </h1>
        <p class="text-[17px] leading-relaxed text-white/75 mb-4">
          Listedeki her şirket KKTC Sigorta ve Reasürans Şirketleri Birliği üyesidir.
          Acenteler ve brokerler bu listede yer almaz — poliçenizin arkasındaki risk
          taşıyıcı onlar değildir.
        </p>
        <p class="text-[15px] leading-relaxed text-white/55 border-s-2 border-sun ps-4">
          Puanlar altı gözlemlenebilir ölçüte dayanır. Mali güç ve hasar ödeme
          performansı puanlanmaz — KKTC'de bu veriler şirket bazında yayımlanmıyor.
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
        <span data-filter-count class="u-num text-text">{len(VERI)}</span> şirket gösteriliyor
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
{"".join(satir_html(s, i) for i, s in enumerate(VERI))}        </tbody>
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
'''

    cikti = KOK / "tr" / "sirketler" / "index.html"
    cikti.parent.mkdir(parents=True, exist_ok=True)
    cikti.write_text(BASLIK + govde + ALTBILGI, encoding="utf-8")
    print(f"→ tr/sirketler/index.html ({len(VERI)} satır, {canli} canlı, {olu} ölü)")

    # Ana sayfadaki ilk 5 satırı gerçek veriyle değiştir
    ana = KOK / "tr" / "index.html"
    s = ana.read_text(encoding="utf-8")
    ilk5 = "".join(satir_html_koyu(x, i) for i, x in enumerate(VERI[:5]))
    import re
    s2, n = re.subn(r"          <tbody>.*?          </tbody>",
                    "          <tbody>\n" + ilk5 + "          </tbody>",
                    s, count=1, flags=re.S)
    if n:
        s2 = s2.replace('<p class="badge badge--taslak mb-4">Taslak veri</p>\n\n        ', '')
        ana.write_text(s2, encoding="utf-8")
        print("→ tr/index.html sıralaması gerçek veriyle güncellendi")


def satir_html_koyu(s, i):
    sehirler = s.get("ofis_sehirler") or [s["sehir"]]
    branslar = s.get("branslar") or []
    meta = f"{sehirler[0]} · {len(branslar)} branş" if branslar else f"{sehirler[0]} · ürün listesi yok"
    renk = "text-sun" if s["genel_puan"] >= 7 else "text-white/90"
    return f'''            <tr>
              <td class="rank-no align-top pt-4">{s['sira']:02d}</td>
              <td class="pe-4">
                <a href="/tr/sirketler/{e(s['slug'])}/" class="u-display text-[15px] link-u">{e(s['ad'])}</a>
                <div class="flex items-center gap-3 mt-1.5">
                  {serit(s, koyu=True, satir=i)}
                  <span class="font-mono text-[11px] text-muteddark">{e(meta)}</span>
                </div>
              </td>
              <td class="text-end align-top pt-3 u-num text-[22px] {renk}">{str(s['genel_puan']).replace('.', ',')}</td>
            </tr>
'''


if __name__ == "__main__":
    main()
