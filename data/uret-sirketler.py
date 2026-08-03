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
    return f'''      <li class="border border-line bg-white rounded-[14px] p-5">
        <p class="u-display text-[15px] mb-1">{e(s['ad'])}</p>
        <p class="font-mono text-[11px] text-muted mb-3">{kunye}</p>
        <p class="text-[14px] text-muted leading-relaxed">{e(sebep)}</p>
      </li>
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

<section class="bg-paper border-b border-line">
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

    # Ana sayfadaki ilk 5 satırı gerçek veriyle değiştir
    ana = KOK / "content" / "tr" / "sayfa" / "index.html"
    s = ana.read_text(encoding="utf-8")
    ilk5 = "".join(satir_html_koyu(x, i) for i, x in enumerate(SAYFALI[:5]))
    import re
    s2, n = re.subn(r"          <tbody>.*?          </tbody>",
                    "          <tbody>\n" + ilk5 + "          </tbody>",
                    s, count=1, flags=re.S)
    if n:
        s2 = s2.replace('<p class="badge badge--taslak mb-4">Taslak veri</p>\n\n        ', '')
        ana.write_text(s2, encoding="utf-8")
        print("→ content/tr/sayfa/index.html sıralaması gerçek veriyle güncellendi")


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
