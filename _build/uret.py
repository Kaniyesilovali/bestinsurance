#!/usr/bin/env python3
"""Siteyi üretir: content/ + _build/sablon/ -> dist/

    python3 _build/uret.py            # tümünü üret
    python3 _build/uret.py --kontrol  # üret + kırık bağlantı raporu

dist/ klasörü yayına hazır statik sitedir; olduğu gibi sunucuya yüklenir.
Kaynak dosyalara (content/, site.json, _build/) dokunulmaz.
"""

import json
import os
import re
import shutil
import sys
import unicodedata
from datetime import date, datetime
from html import escape
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

KOK = Path(__file__).resolve().parent.parent
SABLON = KOK / "_build" / "sablon"
ICERIK = KOK / "content"
CIKTI = KOK / "dist"

try:
    import markdown as md_kutuphane
    from jinja2 import Environment, FileSystemLoader
except ImportError as hata:
    sys.exit(
        f"Eksik paket: {hata.name}\n"
        "Kurulum:  pip3 install --user markdown jinja2"
    )

AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
         "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

TR_HARF = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")

# Ham HTML bloğu: satır başında <section ...> ile başlayıp satır başında
# </section> ile biten parça. Markdown'a girmeden olduğu gibi geçer.
HAM_BLOK = re.compile(r"^<section\b.*?^</section>\s*$", re.S | re.M)
JSONLD = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>\s*',
    re.S | re.I,
)


# ── yardımcılar ────────────────────────────────────────────────────────────

def slugla(metin):
    """Türkçe başlığı URL parçasına çevirir: 'Sınır geçişi' -> 'sinir-gecisi'."""
    metin = metin.translate(TR_HARF)
    metin = unicodedata.normalize("NFKD", metin)
    metin = "".join(k for k in metin if not unicodedata.combining(k))
    metin = re.sub(r"[^a-zA-Z0-9]+", "-", metin).strip("-").lower()
    return metin or "konu"


def tarih_oku(deger, varsayilan=None):
    if isinstance(deger, date):
        return deger
    if not deger:
        return varsayilan
    metin = str(deger).strip()
    for kalip in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(metin, kalip).date()
        except ValueError:
            continue
    return varsayilan


def tarih_tr(gun, uzun=False):
    if not gun:
        return ""
    if uzun:
        return f"{gun.day} {AYLAR[gun.month - 1]} {gun.year}"
    return f"{AYLAR[gun.month - 1]} {gun.year}"


def evet_mi(deger):
    return str(deger).strip().lower() in {"evet", "true", "1", "yes", "var"}


def frontmatter_ayikla(kaynak):
    """--- ile sarılı başlık bloğunu sözlüğe çevirir, gövdeyi ayrı döndürür.

    Desteklenen biçimler:
        anahtar: değer
        anahtar:
          alt: değer          (iç içe tek seviye)
        anahtar:
          - öğe               (liste)
        anahtar: |            (satır satır korunan blok)
    """
    if not kaynak.startswith("---"):
        return {}, kaynak
    kapanis = re.search(r"^---\s*$", kaynak[3:], re.M)
    if not kapanis:
        return {}, kaynak
    ham = kaynak[3:3 + kapanis.start()]
    govde = kaynak[3 + kapanis.end():].lstrip("\n")

    veri, satirlar, i = {}, ham.splitlines(), 0
    while i < len(satirlar):
        satir = satirlar[i]
        i += 1
        if not satir.strip() or satir.lstrip().startswith("#"):
            continue
        if ":" not in satir:
            continue
        anahtar, _, deger = satir.partition(":")
        anahtar, deger = anahtar.strip(), deger.strip()

        if deger == "|":                                   # korunan blok
            blok = []
            while i < len(satirlar) and (not satirlar[i].strip()
                                         or satirlar[i].startswith("  ")):
                blok.append(satirlar[i][2:])
                i += 1
            veri[anahtar] = "\n".join(blok).strip("\n")
        elif deger == "":                                  # liste ya da sözlük
            liste, sozluk = [], {}
            while i < len(satirlar) and satirlar[i].startswith("  "):
                alt = satirlar[i].strip()
                i += 1
                if alt.startswith("- "):
                    liste.append(alt[2:].strip())
                elif ":" in alt:
                    a2, _, d2 = alt.partition(":")
                    sozluk[a2.strip()] = d2.strip()
            veri[anahtar] = liste if liste else sozluk
        else:
            veri[anahtar] = deger.strip('"').strip("'")
    return veri, govde


def jsonld_ayikla(govde):
    """Gövdedeki ld+json bloklarını çıkarır; <head>'e taşınmak üzere döndürür."""
    bloklar = [b.strip() for b in JSONLD.findall(govde)]
    return JSONLD.sub("", govde), bloklar


def markdown_uret():
    return md_kutuphane.Markdown(
        extensions=["extra", "sane_lists", "smarty"],
        output_format="html5",
    )


def govde_isle(kaynak, markdown_mi, cevirici):
    """Markdown parçalarını dönüştürür, ham <section> bloklarını olduğu gibi bırakır."""
    if not markdown_mi:
        return kaynak.strip()

    parcalar, son = [], 0
    for eslesme in HAM_BLOK.finditer(kaynak):
        parcalar.append(("md", kaynak[son:eslesme.start()]))
        parcalar.append(("ham", eslesme.group(0)))
        son = eslesme.end()
    parcalar.append(("md", kaynak[son:]))

    cikti = []
    for tur, metin in parcalar:
        if tur == "ham":
            cikti.append(metin.strip())
            continue
        if not metin.strip():
            continue
        cevirici.reset()
        icerik = cevirici.convert(metin.strip())
        cikti.append(
            '<section class="bg-white border-t border-line">\n'
            '  <div class="mx-auto max-w-shell px-[22px] py-12 sm:py-16">\n'
            '    <div class="u-prose u-md">\n'
            f"{icerik}\n"
            "    </div>\n"
            "  </div>\n"
            "</section>"
        )
    return "\n\n".join(cikti)


def yaz(hedef: Path, metin):
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(metin, encoding="utf-8")


def url_to_path(url):
    """'/tr/rehber/x/' -> dist/tr/rehber/x/index.html"""
    return CIKTI / url.strip("/") / "index.html" if url != "/" else CIKTI / "index.html"


# ── içerik okuma ───────────────────────────────────────────────────────────

class Belge:
    """Bir içerik dosyası: statik sayfa ya da blog yazısı."""

    def __init__(self, dosya: Path, dil, tur, cevirici):
        self.dosya = dosya
        self.dil = dil
        self.tur = tur                                     # "sayfa" | "yazi"
        ham = dosya.read_text(encoding="utf-8")
        self.meta, govde = frontmatter_ayikla(ham)
        govde, self.jsonld = jsonld_ayikla(govde)
        self.govde = govde_isle(govde, dosya.suffix == ".md", cevirici)

        self.taslak = evet_mi(self.meta.get("taslak", "hayir"))
        self.h1 = self.meta.get("h1") or self.meta.get("baslik", "")
        self.baslik = self.meta.get("baslik") or self.h1
        self.kisa_baslik = self.meta.get("kisa_baslik", "")
        self.aciklama = self.meta.get("aciklama", "")
        self.ozet = self.meta.get("ozet", "") or self.aciklama
        self.giris = self.meta.get("giris", "")
        self.kategori = self.meta.get("kategori", "")
        self.menu = self.meta.get("menu", "")
        self.og_tur = self.meta.get("og_tur") or ("article" if tur == "yazi" else "website")
        self.og_baslik = self.meta.get("og_baslik") or self.h1 or self.baslik
        self.og_aciklama = self.meta.get("og_aciklama") or self.ozet
        self.og_gorsel = self.meta.get("og_gorsel", "")
        self.ceviriler = self.meta.get("ceviriler") or {}
        if not isinstance(self.ceviriler, dict):
            self.ceviriler = {}

        bugun = date.today()
        self.tarih = tarih_oku(self.meta.get("tarih"), bugun)
        self.guncelleme = tarih_oku(self.meta.get("guncelleme"), self.tarih)
        self.url = self.meta.get("url") or self._url_turet(dil, tur)
        self.slug = self.url.strip("/").rsplit("/", 1)[-1]

    def _url_turet(self, dil, tur):
        """Dosya yolundan adres üretir; frontmatter'da url varsa o kazanır."""
        if tur == "yazi":
            return f"/{dil}/rehber/{self.dosya.stem}/"
        govde_yol = self.dosya.relative_to(ICERIK / dil / "sayfa").with_suffix("")
        parca = "" if govde_yol.name == "index" else str(govde_yol)
        if govde_yol.name == "index" and govde_yol.parent != Path("."):
            parca = str(govde_yol.parent)
        return f"/{dil}/" + (f"{parca}/" if parca else "")

    # liste kartlarında kullanılan kısaltılmış özet
    @property
    def ozet_kisa(self):
        if len(self.ozet) <= 110:
            return self.ozet
        return self.ozet[:107].rsplit(" ", 1)[0] + "…"

    @property
    def tarih_tr(self):
        return tarih_tr(self.tarih)

    @property
    def guncelleme_tr(self):
        return tarih_tr(self.guncelleme)


# ── üretici ────────────────────────────────────────────────────────────────

class Uretici:
    def __init__(self):
        self.yapilandirma = json.loads((KOK / "site.json").read_text(encoding="utf-8"))
        self.alan_adi = self.yapilandirma["alan_adi"].rstrip("/")
        self.noindex = bool(self.yapilandirma.get("yayin", {}).get("noindex", False))
        self.sayfa_basina = int(self.yapilandirma.get("yayin", {}).get("sayfa_basina_yazi", 12))
        self.jinja = Environment(
            loader=FileSystemLoader(str(SABLON)),
            autoescape=False,
            trim_blocks=False,
            lstrip_blocks=False,
        )
        self.cevirici = markdown_uret()
        self.sayfalar = []
        self.yazilar = []
        self.uretilen = []                                 # (url, lastmod)
        self.mevcut = set()                                # üretilecek tüm adresler

    # -- okuma --------------------------------------------------------------

    def oku(self):
        for dil in self.yapilandirma["diller"]:
            sayfa_kok = ICERIK / dil / "sayfa"
            if sayfa_kok.is_dir():
                for dosya in sorted(sayfa_kok.rglob("*")):
                    if dosya.suffix in {".html", ".md"} and dosya.is_file():
                        self.sayfalar.append(Belge(dosya, dil, "sayfa", self.cevirici))
            yazi_kok = ICERIK / dil / "rehber"
            if yazi_kok.is_dir():
                for dosya in sorted(yazi_kok.rglob("*")):
                    if dosya.suffix in {".html", ".md"} and dosya.is_file():
                        self.yazilar.append(Belge(dosya, dil, "yazi", self.cevirici))

        taslaklar = [y for y in self.yazilar if y.taslak]
        self.yazilar = [y for y in self.yazilar if not y.taslak]
        self.sayfalar = [s for s in self.sayfalar if not s.taslak]
        self.yazilar.sort(key=lambda y: (y.tarih, y.slug), reverse=True)

        # Gerçekten üretilecek adresler. hreflang ve dil değiştirici bunu
        # kullanır: henüz yazılmamış bir dile bağlantı verilmez, o dilin
        # içeriği eklendiği anda bağlantılar kendiliğinden belirir.
        self.mevcut = {s.url for s in self.sayfalar} | {y.url for y in self.yazilar}
        for dil, blog in self.yapilandirma.get("blog", {}).items():
            if any(y.dil == dil for y in self.yazilar):
                self.mevcut.add(blog["kok"])
        return taslaklar

    # -- ortak bağlam -------------------------------------------------------

    def hreflang(self, url, dil, ceviriler=None):
        """Sayfanın dört dildeki adresi. Yalnızca tanımlı olanlar döner."""
        harita = dict(self.yapilandirma.get("rotalar", {}).get(url, {}))
        if ceviriler:
            harita.update(ceviriler)
        sonuc = {dil: url}
        for kod, adres in harita.items():
            if kod in self.yapilandirma["diller"] and adres and adres in self.mevcut:
                sonuc[kod] = adres
        return {k: sonuc[k] for k in self.yapilandirma["diller"] if k in sonuc}

    def baglam(self, *, dil, url, baslik, aciklama="", aktif_menu="",
               og_tur="website", og_baslik="", og_aciklama="", og_gorsel="",
               jsonld=None, ceviriler=None):
        d = self.yapilandirma["diller"][dil]
        site_adi = self.yapilandirma["site_adi"]
        tam_baslik = baslik if baslik.endswith(site_adi) else f"{baslik} | {site_adi}"
        return {
            "dil": dil,
            "dil_dir": d["dir"],
            "diller": self.yapilandirma["diller"],
            "og_locale": d["og_locale"],
            "alan_adi": self.alan_adi,
            "site_adi": site_adi,
            "site_adi_kisa": self.yapilandirma["site_adi_kisa"],
            "site_aciklamasi": self.yapilandirma["site_aciklamasi"],
            "url": url,
            "title": tam_baslik,
            "aciklama": aciklama,
            "noindex": self.noindex,
            "hreflang": self.hreflang(url, dil, ceviriler),
            "og_tur": og_tur,
            "og_baslik": og_baslik or baslik,
            "og_aciklama": og_aciklama or aciklama,
            "og_gorsel": og_gorsel,
            "jsonld": jsonld or [],
            "menu": self.yapilandirma["menu"].get(dil, []),
            "aktif_menu": aktif_menu,
            "footer": self.yapilandirma["footer"].get(dil, {}),
            "blog": self.yapilandirma["blog"].get(dil, {}),
        }

    def sayfa_yaz(self, url, baglam, icerik, lastmod):
        baglam = dict(baglam)
        baglam["icerik"] = icerik
        yaz(url_to_path(url), self.jinja.get_template("iskelet.html").render(**baglam))
        self.uretilen.append((url, lastmod))

    # -- statik sayfalar ----------------------------------------------------

    def statik_sayfalar(self):
        for s in self.sayfalar:
            bag = self.baglam(
                dil=s.dil, url=s.url, baslik=s.baslik, aciklama=s.aciklama,
                aktif_menu=s.menu, og_tur=s.og_tur, og_baslik=s.og_baslik,
                og_aciklama=s.og_aciklama, og_gorsel=s.og_gorsel,
                jsonld=s.jsonld, ceviriler=s.ceviriler,
            )
            self.sayfa_yaz(s.url, bag, s.govde, s.guncelleme)

    # -- blog yazıları ------------------------------------------------------

    def ilgili_yazilar(self, yazi, adet=3):
        ayni = [y for y in self.yazilar
                if y.dil == yazi.dil and y is not yazi and y.kategori == yazi.kategori]
        diger = [y for y in self.yazilar
                 if y.dil == yazi.dil and y is not yazi and y not in ayni]
        return (ayni + diger)[:adet]

    def yazi_jsonld(self, yazi):
        veri = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": yazi.h1,
            "description": yazi.ozet,
            "url": f"{self.alan_adi}{yazi.url}",
            "inLanguage": yazi.dil,
            "datePublished": yazi.tarih.isoformat(),
            "dateModified": yazi.guncelleme.isoformat(),
            "isPartOf": {
                "@type": "Blog",
                "name": f"{self.yapilandirma['site_adi']} — {self.yapilandirma['blog'][yazi.dil]['baslik']}",
                "url": f"{self.alan_adi}{self.yapilandirma['blog'][yazi.dil]['kok']}",
            },
            "publisher": {"@type": "Organization", "name": self.yapilandirma["site_adi"]},
        }
        if yazi.kategori:
            veri["articleSection"] = yazi.kategori
        return json.dumps(veri, ensure_ascii=False)

    def blog_yazilari(self):
        sablon = self.jinja.get_template("yazi.html")
        for y in self.yazilar:
            bag = self.baglam(
                dil=y.dil, url=y.url, baslik=y.baslik, aciklama=y.aciklama,
                aktif_menu=y.menu or "rehber", og_tur="article",
                og_baslik=y.og_baslik, og_aciklama=y.og_aciklama,
                og_gorsel=y.og_gorsel,
                jsonld=[self.yazi_jsonld(y)] + y.jsonld,
                ceviriler=y.ceviriler,
            )
            govde = sablon.render(yazi=y, icerik_govde=y.govde,
                                  ilgili=self.ilgili_yazilar(y), **bag)
            self.sayfa_yaz(y.url, bag, govde, y.guncelleme)

    # -- liste, sayfalama, konular -----------------------------------------

    def konu_listesi(self, dil):
        sayac = {}
        for y in self.yazilar:
            if y.dil == dil and y.kategori:
                sayac[y.kategori] = sayac.get(y.kategori, 0) + 1
        kok = self.yapilandirma["blog"][dil]["konu_kok"]
        return [{"ad": ad, "sayi": sayi, "url": f"{kok}{slugla(ad)}/"}
                for ad, sayi in sorted(sayac.items(), key=lambda x: (-x[1], x[0]))]

    def liste_uret(self, dil, yazilar, kok_url, h1, giris, konu=None, konular=None):
        """Bir yazı kümesini sayfalara böler; 1. sayfa kök adreste durur."""
        sablon = self.jinja.get_template("liste.html")
        blog = self.yapilandirma["blog"][dil]
        toplam = max(1, -(-len(yazilar) // self.sayfa_basina))

        for no in range(1, toplam + 1):
            dilim = yazilar[(no - 1) * self.sayfa_basina: no * self.sayfa_basina]
            url = kok_url if no == 1 else f"{kok_url}sayfa/{no}/"
            baslik = h1 if no == 1 else f"{h1} — sayfa {no}"
            sayfalama = {
                "simdiki": no,
                "toplam": toplam,
                "onceki": None if no == 1 else (kok_url if no == 2 else f"{kok_url}sayfa/{no - 1}/"),
                "sonraki": None if no == toplam else f"{kok_url}sayfa/{no + 1}/",
            }
            bag = self.baglam(
                dil=dil, url=url, baslik=baslik, aciklama=giris,
                aktif_menu="rehber", og_tur="website", og_aciklama=giris,
                jsonld=[self.blog_jsonld(dil, dilim)] if no == 1 and not konu else [],
            )
            if no > 1 or konu:
                bag["hreflang"] = {dil: url}                # çeviri karşılığı yok
            govde = sablon.render(
                yazilar=dilim, sayfalama=sayfalama, konu=konu,
                konular=konular or [], liste_h1=h1, liste_giris=giris,
                **bag,
            )
            son = max((y.guncelleme for y in dilim), default=date.today())
            self.sayfa_yaz(url, bag, govde, son)

    def blog_jsonld(self, dil, yazilar):
        blog = self.yapilandirma["blog"][dil]
        return json.dumps({
            "@context": "https://schema.org",
            "@type": "Blog",
            "name": f"{self.yapilandirma['site_adi']} — {blog['baslik']}",
            "url": f"{self.alan_adi}{blog['kok']}",
            "inLanguage": dil,
            "description": blog["aciklama"],
            "blogPost": [{
                "@type": "BlogPosting",
                "headline": y.h1,
                "url": f"{self.alan_adi}{y.url}",
                "inLanguage": dil,
                "datePublished": y.tarih.isoformat(),
                "dateModified": y.guncelleme.isoformat(),
            } for y in yazilar],
        }, ensure_ascii=False)

    def bloglar(self):
        for dil, blog in self.yapilandirma.get("blog", {}).items():
            yazilar = [y for y in self.yazilar if y.dil == dil]
            if not yazilar:
                continue
            konular = self.konu_listesi(dil)
            self.liste_uret(dil, yazilar, blog["kok"], blog["baslik"],
                            blog["aciklama"], konular=konular)
            for konu in konular:
                kume = [y for y in yazilar if y.kategori == konu["ad"]]
                self.liste_uret(
                    dil, kume, konu["url"], konu["ad"],
                    f"{blog['baslik']} bölümünde “{konu['ad']}” konulu yazılar.",
                    konu=konu["ad"], konular=konular,
                )
            self.besleme(dil, yazilar[:20], blog)

    # -- besleme (RSS) ------------------------------------------------------

    def besleme(self, dil, yazilar, blog):
        ogeler = []
        for y in yazilar:
            ogeler.append(
                "    <item>\n"
                f"      <title>{xml_escape(y.h1)}</title>\n"
                f"      <link>{self.alan_adi}{y.url}</link>\n"
                f"      <guid isPermaLink=\"true\">{self.alan_adi}{y.url}</guid>\n"
                f"      <description>{xml_escape(y.ozet)}</description>\n"
                f"      <pubDate>{y.tarih.strftime('%a, %d %b %Y')} 00:00:00 +0000</pubDate>\n"
                + (f"      <category>{xml_escape(y.kategori)}</category>\n" if y.kategori else "")
                + "    </item>"
            )
        icerik = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{xml_escape(self.yapilandirma['site_adi'])} — {xml_escape(blog['baslik'])}</title>\n"
            f"    <link>{self.alan_adi}{blog['kok']}</link>\n"
            f"    <description>{xml_escape(blog['aciklama'])}</description>\n"
            f"    <language>{dil}</language>\n"
            f'    <atom:link href="{self.alan_adi}{blog["kok"]}feed.xml" rel="self" type="application/rss+xml"/>\n'
            + "\n".join(ogeler) + "\n"
            "  </channel>\n"
            "</rss>\n"
        )
        yaz(CIKTI / blog["kok"].strip("/") / "feed.xml", icerik)

    # -- sitemap, robots, kök yönlendirme, 404 ------------------------------

    def sitemap(self):
        if self.noindex:
            return False
        satirlar = ['<?xml version="1.0" encoding="UTF-8"?>',
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
                    '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
        mevcut = {u for u, _ in self.uretilen}
        for url, lastmod in sorted(self.uretilen):
            dil = url.strip("/").split("/")[0]
            alternatifler = self.hreflang(url, dil) if url in mevcut else {}
            alternatifler = {k: v for k, v in alternatifler.items() if v in mevcut}
            satirlar.append("  <url>")
            satirlar.append(f"    <loc>{self.alan_adi}{url}</loc>")
            if len(alternatifler) > 1:
                for kod, adres in alternatifler.items():
                    satirlar.append(
                        f'    <xhtml:link rel="alternate" hreflang="{kod}" href="{self.alan_adi}{adres}"/>')
                if "tr" in alternatifler:
                    satirlar.append(
                        f'    <xhtml:link rel="alternate" hreflang="x-default" href="{self.alan_adi}{alternatifler["tr"]}"/>')
            satirlar.append(f"    <lastmod>{lastmod.isoformat()}</lastmod>")
            satirlar.append("  </url>")
        satirlar.append("</urlset>")
        yaz(CIKTI / "sitemap.xml", "\n".join(satirlar) + "\n")
        return True

    def robots(self, sitemap_var):
        if self.noindex:
            metin = ("# Site henüz yayında değil (site.json > yayin.noindex).\n"
                     "User-agent: *\nDisallow: /\n")
        else:
            metin = ("User-agent: *\nAllow: /\n\n"
                     f"Sitemap: {self.alan_adi}/sitemap.xml\n")
        yaz(CIKTI / "robots.txt", metin)

    def kok_yonlendirme(self):
        # Yalnızca içeriği üretilmiş diller listelenir; boş bir dile
        # yönlendirmek 404 demektir.
        diller = [k for k in self.yapilandirma["diller"] if f"/{k}/" in self.mevcut]
        varsayilan = self.yapilandirma["varsayilan_dil"]
        if varsayilan not in diller and diller:
            varsayilan = diller[0]
        baglantilar = "\n".join(
            f'    <li><a href="/{k}/">{self.yapilandirma["diller"][k]["ad"]}</a></li>'
            for k in diller
        )
        hreflang = "\n".join(
            f'<link rel="alternate" hreflang="{k}" href="{self.alan_adi}/{k}/">'
            for k in diller
        )
        yaz(CIKTI / "index.html", f"""<!DOCTYPE html>
<html lang="{varsayilan}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(self.yapilandirma['site_adi'])}</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{self.alan_adi}/{varsayilan}/">
{hreflang}
<link rel="alternate" hreflang="x-default" href="{self.alan_adi}/{varsayilan}/">
<script>
  /* Tarayıcı diline göre yönlendir; tanımadığımız dillerde varsayılan dil. */
  (function () {{
    var supported = {json.dumps(diller)};
    var langs = navigator.languages || [navigator.language || '{varsayilan}'];
    var pick = '{varsayilan}';
    for (var i = 0; i < langs.length; i++) {{
      var code = String(langs[i]).slice(0, 2).toLowerCase();
      if (supported.indexOf(code) > -1) {{ pick = code; break; }}
    }}
    location.replace('/' + pick + '/');
  }})();
</script>
<meta http-equiv="refresh" content="0; url=/{varsayilan}/">
</head>
<body style="font-family:system-ui;padding:2rem">
  <p>Yönlendiriliyorsunuz…</p>
  <ul>
{baglantilar}
  </ul>
</body>
</html>
""")

    def sayfa_404(self):
        dil = self.yapilandirma["varsayilan_dil"]
        bag = self.baglam(dil=dil, url="/404.html", baslik="Sayfa bulunamadı",
                          aciklama="Aradığınız sayfa taşınmış ya da silinmiş olabilir.")
        bag["hreflang"] = {}
        bag["noindex"] = True
        icerik = f"""
<section class="bg-white">
  <div class="mx-auto max-w-shell px-[22px] pt-[96px] pb-[80px] sm:pt-[140px] sm:pb-[120px]">
    <div class="max-w-prose">
      <p class="u-eyebrow mb-4">404</p>
      <h1 class="u-display u-display--tight text-[2.25rem] sm:text-[3rem] leading-[1.05] mb-6">
        Bu sayfayı bulamadık
      </h1>
      <p class="u-lead mb-8">
        Adres değişmiş ya da sayfa kaldırılmış olabilir. Aşağıdaki bölümlerden devam edebilirsiniz.
      </p>
      <div class="flex flex-wrap gap-4">
        <a href="/{dil}/" class="btn">Ana sayfa</a>
        <a href="/{dil}/sirketler/" class="btn btn--secondary">Şirketler</a>
        <a href="/{dil}/rehber/" class="btn btn--secondary">Rehber</a>
      </div>
    </div>
  </div>
</section>
"""
        bag["icerik"] = icerik
        yaz(CIKTI / "404.html", self.jinja.get_template("iskelet.html").render(**bag))

    # -- varlıklar ----------------------------------------------------------

    def varliklar(self):
        hedef = CIKTI / "assets"
        if (KOK / "assets").is_dir():
            shutil.copytree(KOK / "assets", hedef, dirs_exist_ok=True)
        for ad in ("favicon.ico", "favicon.svg", "apple-touch-icon.png"):
            if (KOK / ad).is_file():
                shutil.copy2(KOK / ad, CIKTI / ad)

    # -- bağlantı denetimi --------------------------------------------------

    def baglanti_kontrol(self):
        hedefler = set()
        for dosya in CIKTI.rglob("*.html"):
            metin = dosya.read_text(encoding="utf-8")
            kaynak = "/" + str(dosya.relative_to(CIKTI).parent).replace("\\", "/").strip(".")
            for adres in re.findall(r'href="(/[^"#?]*)"', metin):
                hedefler.add((adres, kaynak))

        kirik = []
        for adres, kaynak in sorted(hedefler):
            yol = CIKTI / adres.strip("/")
            if adres.endswith("/"):
                var = (yol / "index.html").is_file()
            else:
                var = yol.is_file() or (yol.with_suffix("") / "index.html").is_file()
            if not var:
                kirik.append((adres, kaynak))
        return kirik

    # -- çalıştır -----------------------------------------------------------

    def calistir(self, kontrol=False):
        taslaklar = self.oku()
        if CIKTI.exists():
            shutil.rmtree(CIKTI)
        CIKTI.mkdir(parents=True)

        self.varliklar()
        self.statik_sayfalar()
        self.blog_yazilari()
        self.bloglar()
        sitemap_var = self.sitemap()
        self.robots(sitemap_var)
        self.kok_yonlendirme()
        self.sayfa_404()

        print(f"  {len(self.sayfalar):>3} sayfa")
        print(f"  {len(self.yazilar):>3} blog yazısı")
        print(f"  {len(self.uretilen):>3} toplam HTML adresi")
        if taslaklar:
            print(f"  {len(taslaklar):>3} taslak atlandı: "
                  + ", ".join(t.dosya.name for t in taslaklar))
        if self.noindex:
            print("  ! noindex açık — sitemap üretilmedi, robots.txt her şeyi kapatıyor.")
            print("    Yayına alırken site.json > yayin.noindex = false yapın.")
        else:
            print("  sitemap.xml + robots.txt üretildi")
        print(f"\n  Çıktı: {CIKTI}")

        if kontrol:
            kirik = self.baglanti_kontrol()
            print("\n  Bağlantı denetimi:")
            if not kirik:
                print("    kırık iç bağlantı yok")
            else:
                print(f"    {len(kirik)} kırık bağlantı:")
                for adres, kaynak in kirik:
                    print(f"      {adres}   <- {kaynak}")
            return 1 if kirik else 0
        return 0


if __name__ == "__main__":
    print("\nSite üretiliyor…\n")
    sys.exit(Uretici().calistir(kontrol="--kontrol" in sys.argv))
