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


# Kendi sayfası üretilmeyen şirketin ölçütü: adres, e-posta, branş ve dil
# verisinin DÖRDÜ BİRDEN boş. "Branşı yok" tek başına eşik değildir — branşsız
# dokuz şirketin beşinde sayfayı taşıyan özgün bir bulgu var (ölü alan adı,
# aynı IP'de iki şirket, kişisel e-posta). Bu dördünde o bulgu da yok.
# Gerekçe: copy/02-programatik-seo.md §2 "İnce içerik eşiği".
def sayfasiz_mi(sirket):
    return not any((
        sirket.get("adres"),
        sirket.get("email"),
        sirket.get("branslar"),
        sirket.get("diller"),
    ))


# Kendi liste sayfası üretilmeyen branşlar. hayat: ayrı ruhsat rejimi, hayat
# dışı listesiyle karışır. yat: yedi şirket, tür hub'ı yok, tek başına zayıf.
# İkisi de profillerin branş matrisinde görünmeye devam eder — bağlantısız.
BRANS_SAYFASIZ = {"hayat", "yat"}


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


# §9.2 — otomatik marka bağlama.
# Türkçe büyük/küçük harf çiftleri: re.IGNORECASE bunları doğru eşleştirmez
# (i↔İ ve ı↔I ayrı çiftlerdir), bu yüzden her harf kendi sınıfına çevrilir.
TR_CIFT = {"i": "iİ", "İ": "İi", "ı": "ıI", "I": "Iı",
           "ş": "şŞ", "Ş": "Şş", "ğ": "ğĞ", "Ğ": "Ğğ",
           "ü": "üÜ", "Ü": "Üü", "ö": "öÖ", "Ö": "Öö",
           "ç": "çÇ", "Ç": "Çç"}
# Sözcük sınırı: önünde harf, rakam, alt çizgi ya da tire olmasın. Tire önemli —
# "As-Can Sigorta" içinde "Can Sigorta" eşleşmemeli.
MARKA_ON = r"(?<![0-9A-Za-zÇĞİÖŞÜçğıöşü_\-])"
MARKA_ARD = r"(?![0-9A-Za-zÇĞİÖŞÜçğıöşü_])"
# İçinde bağlama yapılmayan öğeler.
MARKA_KORUMALI = {"a", "h1", "h2", "h3", "h4", "h5", "h6",
                  "script", "style", "code", "pre"}


def marka_deseni(ad):
    """Bir marka adını büyük/küçük harf duyarsız desene çevirir."""
    parcalar = []
    for harf in ad:
        if harf in TR_CIFT:
            parcalar.append(f"[{TR_CIFT[harf]}]")
        elif harf.isalpha():
            parcalar.append(f"[{harf.upper()}{harf.lower()}]")
        elif harf == " ":
            parcalar.append(r"\s+")
        else:
            parcalar.append(re.escape(harf))
    return MARKA_ON + "".join(parcalar) + MARKA_ARD


class MarkaBaglayici:
    """Rehber yazılarında geçen şirket adlarını profil sayfasına bağlar.

    Kural (copy/03-marka-sorgulari.md §9.2): bir yazıda aynı şirkete en fazla
    bir bağlantı, yalnız ilk geçişte. Başlıklarda, mevcut bağlantıların ve kod
    bloklarının içinde bağlama yapılmaz.
    """

    def __init__(self, kok):
        self.desenler = []
        self.korunan = []
        yol = kok / "data" / "marka-adlari.json"
        veri_yolu = kok / "data" / "sirketler.json"
        if not yol.is_file() or not veri_yolu.is_file():
            return
        blob = json.loads(yol.read_text(encoding="utf-8"))
        kayitlar = blob.get("kayitlar", {})
        # Kurum adları korunur: "Kuzey Kıbrıs Sigorta Bilgi Merkezi" içindeki
        # "Kıbrıs Sigorta" bir şirket değil, kurumun adının parçasıdır.
        self.korunan = [re.compile(marka_deseni(a)) for a in blob.get("korunan", [])]
        gecerli = {x["slug"] for x in json.loads(veri_yolu.read_text(encoding="utf-8"))}
        ciftler = [(slug, ad) for slug, adlar in kayitlar.items()
                   if slug in gecerli for ad in adlar]
        # Uzun desen önce: "Anadolu Anonim Türk Sigorta" tüketilmeden
        # "Türk Sigorta" denenirse yanlış şirkete bağlanır.
        ciftler.sort(key=lambda p: len(p[1]), reverse=True)
        self.desenler = [(slug, re.compile(marka_deseni(ad))) for slug, ad in ciftler]

    def bagla(self, html):
        if not self.desenler:
            return html
        # Yazar zaten elle profile bağlamışsa ikinci bağlantı eklenmez.
        kullanilmis = set(re.findall(r'href="/tr/sirketler/([^/"]+)/"', html))
        parcalar = re.split(r"(<[^>]+>)", html)
        derinlik = 0
        for i, parca in enumerate(parcalar):
            if parca.startswith("<"):
                etiket = re.match(r"</?\s*([A-Za-z0-9]+)", parca)
                if etiket and etiket.group(1).lower() in MARKA_KORUMALI:
                    if parca.startswith("</"):
                        derinlik = max(0, derinlik - 1)
                    elif not parca.rstrip().endswith("/>"):
                        derinlik += 1
                continue
            if derinlik or not parca.strip():
                continue
            for slug, desen in self.desenler:
                if slug in kullanilmis:
                    continue
                # Kurum adlarının kapladığı aralıklar her denemede yeniden
                # hesaplanır; metin bağlantı eklendikçe değişiyor.
                yasak = [(m.start(), m.end())
                         for k in self.korunan for m in k.finditer(parca)]
                eslesme = next(
                    (m for m in desen.finditer(parca)
                     if not any(m.start() < bit and bas < m.end()
                                for bas, bit in yasak)),
                    None)
                if not eslesme:
                    continue
                kullanilmis.add(slug)
                parca = (parca[:eslesme.start()]
                         + f'<a href="/tr/sirketler/{slug}/" class="link-u">'
                         + eslesme.group(0) + "</a>"
                         + parca[eslesme.end():])
            parcalar[i] = parca
        return "".join(parcalar)


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
        self.dogrulama = {k: v for k, v in self.yapilandirma.get("dogrulama", {}).items() if v}
        self.sayfa_basina = int(self.yapilandirma.get("yayin", {}).get("sayfa_basina_yazi", 12))
        self.jinja = Environment(
            loader=FileSystemLoader(str(SABLON)),
            autoescape=False,
            trim_blocks=False,
            lstrip_blocks=False,
        )
        self.cevirici = markdown_uret()
        self.marka = MarkaBaglayici(KOK)          # §9.2
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
            "dogrulama": self.dogrulama,
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
            govde = sablon.render(yazi=y, icerik_govde=self.marka.bagla(y.govde),
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

    # -- şirket profilleri --------------------------------------------------

    def sirket_profilleri(self):
        """data/sirketler.json → /tr/sirketler/<slug>/ profil sayfaları.

        39 şirketin 35'ine sayfa üretilir. Veri-fakiri dördüne üretilmez: adres,
        e-posta, branş ve dil verisinin dördü birden boş olan şirket için sayfa
        bir "doğrulayamadık" beyanından ibaret kalırdı ve 35 iyi profilin
        güvenilirliğini aşağı çekerdi. O dördü şirketler listesinde tek bir
        bölümde, neden veri toplanamadığı yazılarak durur.
        Gerekçe: copy/02-programatik-seo.md §2 "İnce içerik eşiği".
        """
        veri_yolu = KOK / "data" / "sirketler.json"
        if not veri_yolu.is_file():
            return
        tum_veri = json.loads(veri_yolu.read_text(encoding="utf-8"))
        veri = [s for s in tum_veri if not sayfasiz_mi(s)]
        indeks = {s["slug"]: s for s in veri}

        OLCUT = [
            ("seffaflik", "Şeffaflık ve doğrulanabilirlik", 25),
            ("urun", "Ürün genişliği", 20),
            ("erisim", "Erişilebilirlik", 20),
            ("dijital", "Dijital hizmet", 20),
            ("dil", "Yabancı dilde hizmet", 10),
            ("kurumsal", "Kurumsal derinlik", 5),
        ]
        BRANS = [
            ("trafik", "Trafik"), ("kasko", "Kasko"), ("saglik", "Sağlık"),
            ("konut", "Konut"), ("isyeri", "İşyeri"), ("seyahat", "Seyahat"),
            ("nakliyat", "Nakliyat"), ("muhendislik", "Mühendislik"),
            ("sorumluluk", "Sorumluluk"), ("ferdi_kaza", "Ferdi kaza"),
            ("hayat", "Hayat"), ("yat", "Yat"),
        ]
        TUR = {
            "yerel": "KKTC'de kurulmuş yerel şirket",
            "tr_subesi": "Türkiye şirketinin KKTC şubesi",
            "tr_ortakligi": "Türkiye sigortacısıyla yerel ortaklık",
            "banka_bagli": "Banka grubuna bağlı",
            "bilinmiyor": "Şirket yapısı doğrulanamadı",
        }
        # §4.4 "kimin şirketi" — sirket_turu'nun beş değeri, beş ayrı cevap.
        # Hiçbirinde hissedar adı geçmez: veride ana_kuruluş alanı yok, uydurulmaz.
        TUR_KIMIN = {
            "yerel": ("KKTC'de kurulmuş yerel bir şirket",
                      "Kuzey Kıbrıs'ta kurulmuş, KKTC yasalarına tabi ayrı bir tüzel kişi. "
                      "Türkiye'de aynı ya da benzer adı taşıyan bir şirket varsa, onunla "
                      "hukuki bağını doğrulayamadık — böyle bir bağ olduğunu varsaymayın."),
            "banka_bagli": ("Bir banka grubuna bağlı",
                      "Şirketin bir banka grubuna bağlı olduğunu Birlik listesindeki unvandan "
                      "ve şirketin kendi yayınlarından çıkardık. Hissedarlık oranlarını ve grup "
                      "içi yükümlülük yapısını doğrulayamadık. Poliçenin tarafı bankanın kendisi "
                      "değil, sigorta şirketidir."),
            "tr_subesi": ("Türkiye merkezli bir şirketin KKTC'deki yapısı",
                      "Türkiye merkezli bir sigorta şirketinin Kuzey Kıbrıs'taki yapısı. "
                      "KKTC'de düzenlenen poliçeye hangi mevzuatın uygulandığını doğrulayamadık. "
                      "Türkiye'deki genel şartların, teminat limitlerinin ve tahkim yolunun "
                      "burada aynen geçerli olduğunu varsaymayın."),
            "tr_ortakligi": ("Türkiye'deki bir sigortacıyla kurulmuş yerel ortaklık",
                      "Türkiye'deki bir sigortacıyla kurulmuş yerel ortaklık yapısı. "
                      "\u0022(Kıbrıs) Ltd.\u0022 unvanı ayrı bir tüzel kişiliktir. Ortaklık paylarını "
                      "ve grup içi yükümlülük yapısını doğrulayamadık."),
            "bilinmiyor": ("Ortaklık yapısı doğrulanamadı",
                      "Şirketin ortaklık yapısını ne Birlik üye listesinden ne de kendi "
                      "sitesinden çıkarabildik. Profil sayfası olan 35 şirketin 11'inde durum "
                      "aynı. Bu bir suçlama değil, bir boşluk tespitidir — şirketin kim "
                      "olduğunu okurun öğrenebileceği yayımlanmış bir kaynak yok."),
        }
        # §6 H-d — birbirine benzeyen yerel adlar. Karıştırılma gerçek; ikisi de ruhsatlı.
        KARISAN = {
            "can-sigorta": ["as-can-sigorta"],
            "as-can-sigorta": ["can-sigorta"],
            "kibris-sigorta": ["kibris-iktisat-sigorta", "kibris-kapital-insurance"],
            "kibris-iktisat-sigorta": ["kibris-sigorta", "kibris-kapital-insurance"],
            "kibris-kapital-insurance": ["kibris-sigorta", "kibris-iktisat-sigorta"],
            "eurocity-sigorta": ["eig-sigorta"],
            "eig-sigorta": ["eurocity-sigorta"],
        }
        HTTP_KISA = {200: "Çalışıyor", "ölü": "Yanıt vermiyor", "site_yok": "Yok"}
        HTTP_UZUN = {
            200: "Site Temmuz 2026'da test edildi ve yanıt verdi.",
            "ölü": "Şirketin alan adı Temmuz 2026'da yanıt vermedi.",
            "site_yok": "Şirketin bir web sitesi bulunamadı.",
        }
        DIL_ADI = {"en": "İngilizce", "ru": "Rusça", "el": "Yunanca", "fa": "Farsça"}
        ESLI = {"eurocity-sigorta": "eig-sigorta", "eig-sigorta": "eurocity-sigorta"}

        def vir(x):
            return str(x).replace(".", ",")

        def liste_metni(xs):
            return " · ".join(xs) if xs else ""

        def yil_den(yil):
            """1958'den, 2013'ten, 1967'den — okunuşun son sözcüğüne göre ek."""
            son2, son1 = int(yil) % 100, int(yil) % 10
            ONLUK = {0: "den", 10: "dan", 20: "den", 30: "dan", 40: "tan",
                     50: "den", 60: "tan", 70: "ten", 80: "den", 90: "dan"}
            BIRLIK = {0: "dan", 1: "den", 2: "den", 3: "ten", 4: "ten",
                      5: "ten", 6: "dan", 7: "den", 8: "den", 9: "dan"}
            ek = ONLUK[son2] if son1 == 0 else BIRLIK[son1]
            return f"{yil}'{ek}"

        def liste_metni_ve(xs):
            """Cümle içi liste: 'a, b ve c'."""
            xs = list(xs)
            if not xs:
                return ""
            if len(xs) == 1:
                return xs[0]
            return ", ".join(xs[:-1]) + " ve " + xs[-1]

        # §9.3 — her profil, adının karıştırıldığı sayfalara bağlanır.
        # Set H sayfaları böylece öksüz kalmaz.
        kar_yolu = KOK / "data" / "ad-karisikliklari.json"
        karsilastirma = {}
        if kar_yolu.is_file():
            for kay in json.loads(kar_yolu.read_text(encoding="utf-8")).get("kayitlar", []):
                for sl in kay["taraflar"]:
                    karsilastirma.setdefault(sl, []).append({
                        "url": f"/tr/sirketler/karsilastirma/{kay['slug']}/",
                        "h1": kay["h1"],
                    })

        sablon = self.jinja.get_template("sirket-profil.html")

        for s in veri:
            olcutler = s.get("olcutler", {})
            branslar = set(s.get("branslar") or [])
            sehirler = s.get("ofis_sehirler") or ([s["sehir"]] if s.get("sehir") else [])
            veri_yok = set(s.get("veri_yok_olcutler") or [])

            olcut_ctx, bosluk_ctx = [], []
            for anahtar, ad, agirlik in OLCUT:
                o = olcutler.get(anahtar, {})
                puan = o.get("puan")
                detay = o.get("detay", {}) or {}
                if puan is None:
                    sebep = o.get("sebep") or "Bu ölçüt için veri toplanamadı."
                    olcut_ctx.append({"ad": ad, "agirlik": agirlik, "veri_yok": True,
                                      "sebep": sebep})
                    bosluk_ctx.append({"ad": ad, "sebep": sebep})
                else:
                    olcut_ctx.append({
                        "ad": ad, "agirlik": agirlik, "veri_yok": False,
                        "puan": vir(puan),
                        "var": liste_metni(detay.get("var") or []),
                        "yok": liste_metni(detay.get("yok") or []),
                    })

            # Sayfası olmayan branş matriste görünür ama bağlantı almaz.
            brans_matris = [{
                "key": k, "ad": ad, "var": k in branslar,
                "url": None if k in BRANS_SAYFASIZ else f"/tr/sirketler/{k}/",
            } for k, ad in BRANS]
            ilk_brans = next(((k, ad) for k, ad in BRANS
                              if k in branslar and k not in BRANS_SAYFASIZ), None)

            diller_yabanci = [DIL_ADI.get(d, d) for d in (s.get("diller") or []) if d != "tr"]

            dijital = [
                {"ad": "Online teklif", "var": bool(s.get("online_teklif"))},
                {"ad": "Online poliçe", "var": bool(s.get("online_police"))},
                {"ad": "Online hasar ihbarı", "var": bool(s.get("online_hasar_ihbar"))},
                {"ad": "Mobil uygulama", "var": bool(s.get("mobil_uygulama"))},
            ]

            iletisim = []
            if s.get("adres"):
                iletisim.append(("Adres", s["adres"]))
            if s.get("email"):
                iletisim.append(("E-posta", s["email"]))
            if s.get("whatsapp"):
                iletisim.append(("WhatsApp", s["whatsapp"]))
            if s.get("instagram"):
                iletisim.append(("Instagram", s["instagram"]))
            if s.get("facebook"):
                iletisim.append(("Facebook", s["facebook"]))

            # Benzer: aynı tür + branş örtüşmesi; yoksa yalnız branş örtüşmesi.
            def ortak(o):
                return len(branslar & set(o.get("branslar") or []))
            adaylar = [o for o in veri if o["slug"] != s["slug"]]
            ayni_tur = [o for o in adaylar if o.get("sirket_turu") == s.get("sirket_turu")]
            havuz = sorted(ayni_tur, key=ortak, reverse=True)
            if len([o for o in havuz if ortak(o)]) < 3:
                havuz = sorted(adaylar, key=ortak, reverse=True)
            benzer = [{
                "slug": o["slug"], "ad": o["ad"], "sehir": o.get("sehir", ""),
                "brans_sayisi": len(o.get("branslar") or []), "puan": vir(o["genel_puan"]),
            } for o in havuz[:3] if ortak(o) or o.get("sirket_turu") == s.get("sirket_turu")]

            web = (s.get("web") or "").strip()
            puan = s["genel_puan"]

            # ---- §4.1 Cevap-önce özeti -------------------------------------
            # LLM ve AI Overviews'un çıkarıp alıntıladığı blok. Kural: puan yok,
            # sıfat yok, bağlantı yok. Yalnız olgu.
            if s.get("http_durum") == "site_yok":
                online_cumlesi = "Şirketin bir web sitesi bulunamadı"
            elif s.get("http_durum") == "ölü":
                online_cumlesi = "Şirketin alan adı Temmuz 2026'da yanıt vermedi"
            elif s.get("online_teklif") or s.get("online_police") or s.get("online_hasar_ihbar"):
                _dv = [d["ad"].replace("Online ", "online ") for d in dijital if d["var"]]
                online_cumlesi = "Sitesinde " + liste_metni_ve(_dv) + " var"
            else:
                online_cumlesi = "Sitesinde çalışan bir online teklif ya da poliçe işlevi bulunamadı"

            cevap_once = (
                f"{s['ad']}, Kuzey Kıbrıs Sigorta ve Reasürans Şirketleri Birliği'ne üye "
                f"ruhsatlı bir sigorta şirketidir — acente değil."
            )
            if p_sehir := s.get("sehir", ""):
                cevap_once += f" {p_sehir} merkezli"
                cevap_once += (f", {yil_den(s['kurulus_yili'])} beri faaliyette."
                               if s.get("kurulus_yili") else ".")
            cevap_once += (
                (f" {len(branslar)} branşta ürünü doğrulandı, "
                 if branslar else " Ürün sayfalarında doğrulanabilen bir branş bulunamadı, ")
                + f"{len(sehirler)} şehirde ofisi var. {online_cumlesi}. "
                f"Hasar ödeme performansı ve mali gücü — KKTC'deki hiçbir şirkette "
                f"olduğu gibi — ölçülemiyor; nedeni aşağıda."
            )

            # ---- §4.2 "güvenilir mi" — doğrulananlar ve doğrulanamayanlar ---
            dogrulanan = []
            _sef = (olcutler.get("seffaflik", {}).get("detay") or {}).get("var") or []
            for madde in _sef:
                dogrulanan.append(f"Sitesinde {madde} yayımlıyor")
            if branslar:
                dogrulanan.append(f"{len(branslar)} branşta ürün sayfası var")
            if sehirler:
                dogrulanan.append(
                    f"{len(sehirler)} şehirde ofisi var: {liste_metni(sehirler)}")
            if s.get("acente_sayisi"):
                dogrulanan.append(
                    f"{s['acente_sayisi']} acente beyan ediyor (şirket beyanı, doğrulanmadı)")
            _dij = [d["ad"] for d in dijital if d["var"]]
            if _dij:
                dogrulanan.append("Çalışır durumda: " + liste_metni(_dij))
            if diller_yabanci:
                dogrulanan.append("Türkçe dışında " + liste_metni(diller_yabanci) + " sunuyor")
            if s.get("http_durum") == 200:
                dogrulanan.append("Sitesi Temmuz 2026'da test edildi ve yanıt verdi")

            dogrulanamayan = [
                "Mali gücü ve ödenmiş sermayesi",
                "Hasar ödeme oranı — kaç ihbarın kabul edildiği, ne kadar sürede ödendiği",
                "Pazar payı ve prim üretimi",
            ]
            if not s.get("police_sartlari_yayinda"):
                dogrulanamayan.append(
                    "Poliçe genel şartları — yayımlamadığı için teminat kapsamını okuyamıyoruz")

            # ---- §4.3 Sorun kanalları --------------------------------------
            sirkete = []
            if s.get("email"):
                sirkete.append(s["email"])
            if s.get("whatsapp"):
                sirkete.append("WhatsApp " + s["whatsapp"])
            hasar_ihbar_online = bool(s.get("online_hasar_ihbar"))

            # ---- §4.4 Kimin şirketi ----------------------------------------
            kimin_baslik, kimin_cevap = TUR_KIMIN.get(
                s.get("sirket_turu"), TUR_KIMIN["bilinmiyor"])

            # ---- §6 H-d karıştırılan adlar ---------------------------------
            karisan = [{"slug": k, "ad": indeks[k]["ad"]}
                       for k in KARISAN.get(s["slug"], []) if k in indeks]

            # ---- §4.5 SSS — beş soru, koşullu altıncı ----------------------
            _brans_adlari = [ad for k, ad in BRANS if k in branslar]
            _ulasim = []
            if s.get("adres"):
                _ulasim.append("Adresi: " + s["adres"])
            if s.get("email"):
                _ulasim.append("E-posta: " + s["email"])
            if s.get("whatsapp"):
                _ulasim.append("WhatsApp: " + s["whatsapp"])
            _ulasim_metni = (". ".join(_ulasim) + ". "
                             if _ulasim else "Açık bir iletişim bilgisi bulamadık. ")

            sss = [
                {"soru": f"{s['ad']} ruhsatlı bir sigorta şirketi mi?",
                 "cevap": (f"Evet. Kuzey Kıbrıs Sigorta ve Reasürans Şirketleri Birliği'nin "
                           f"üye listesinde yer alıyor; acente ya da broker değil, poliçenin "
                           f"arkasındaki risk taşıyıcının kendisi. KKTC'de \u0022sigorta\u0022 adıyla "
                           f"çalışan her kuruluş ruhsatlı şirket değildir — bu ayrım poliçe "
                           f"alırken kontrol edilmesi gereken ilk şeydir.")},
                {"soru": f"{s['ad']} güvenilir mi?",
                 "cevap": (f"Bu soruyu KKTC'de hiç kimse veriyle cevaplayamıyor: şirket bazında "
                           f"mali güç ve hasar ödeme verisi yayımlanmıyor. Doğrulayabildiğimiz "
                           f"{len(dogrulanan)} şey var — Birlik üyeliği, {len(branslar)} branşta "
                           f"ürün, {len(sehirler)} şehirde ofis ve dijital hizmetleri. "
                           f"Doğrulayamadıklarımız sayfada ayrıca listeli. Karar sizin.")},
                {"soru": f"{s['ad']} hangi sigortaları yapıyor?",
                 "cevap": ((f"Ürün sayfalarında {len(branslar)} branş doğrulandı: "
                            f"{liste_metni_ve([b.lower() for b in _brans_adlari])}. "
                            f"Bu ölçüt şirketin ne sattığını söylediğini ölçer, fiilen ne "
                            f"sattığını değil.")
                           if branslar else
                           ("Şirketin sitesinde hangi branşlarda ürün sunduğunu gösteren bir "
                            "sayfa bulamadık. Branş bilgisi için şirkete doğrudan sorun."))},
                {"soru": f"{s['ad']} ile nasıl iletişime geçilir?",
                 "cevap": (_ulasim_metni
                           + (f"Ofisi {liste_metni(sehirler)} şehrinde. " if sehirler else "")
                           + ("Online hasar ihbarı sitesinden yapılabiliyor."
                              if hasar_ihbar_online else
                              "Online hasar ihbarı yok; ihbar telefon ya da "
                              "e-posta ile yapılıyor."))},
                {"soru": f"{s['ad']} ile ilgili şikâyetimi nereye götürürüm?",
                 "cevap": ("Önce şirketin kendisine yazılı olarak başvurun. Sonuç alamazsanız "
                           "KKSRSB bünyesindeki Sigorta Tahkim Komisyonu'na gidebilirsiniz; "
                           "tahkimin ücreti, parasal limiti ve süresi tüzük metni "
                           "incelenmediği için bu sayfada yazılmıyor. Düzenleyici mercii "
                           "Para, Kambiyo ve İnkişaf Sandığı İşleri Dairesi'dir. KKTC'de "
                           "merkezî bir tüketici şikâyet mercii tespit edemedik.")},
            ]
            for k in karisan:
                sss.append({
                    "soru": f"{s['ad']} ile {k['ad']} aynı şirket mi?",
                    "cevap": (f"Hayır. İkisi de Birlik'in ayrı ayrı ruhsatlı üyesi, ayrı tüzel "
                              f"kişilikler. Adlarının benzemesi bir mülkiyet ya da grup ilişkisi "
                              f"göstermez; böyle bir ilişki doğrulayamadık. Poliçe alırken "
                              f"sözleşmedeki tam unvana bakın — hasar ve şikâyet yolu "
                              f"hangi şirketle sözleştiyseniz ona işler."),
                })


            p = {
                "ad": s["ad"], "slug": s["slug"], "sehir": s.get("sehir", ""),
                "tur_metni": TUR.get(s.get("sirket_turu"), "Şirket yapısı doğrulanamadı"),
                "kurulus_yili": s.get("kurulus_yili"),
                "puan": vir(puan), "dusuk": puan is not None and puan < 3,
                "brans_sayisi": len(branslar), "sehir_sayisi": len(sehirler),
                "http_kisa": HTTP_KISA.get(s.get("http_durum"), "Bilinmiyor"),
                "http_uzun": HTTP_UZUN.get(s.get("http_durum"), ""),
                "ozet": s.get("notlar") or "Bu şirket hakkında doğrulanabilir bir gözlem derleyemedik.",
                "olcutler": olcut_ctx, "bosluklar": bosluk_ctx,
                "brans_matris": brans_matris,
                "ilk_brans": ilk_brans[1] if ilk_brans else "",
                "ilk_brans_key": ilk_brans[0] if ilk_brans else "",
                "ofis_metni": liste_metni(sehirler),
                "tek_sehir": len(sehirler) == 1,
                "acente_sayisi": s.get("acente_sayisi"),
                "dijital": dijital,
                "police_sartlari": bool(s.get("police_sartlari_yayinda")),
                "notlar_dijital": "",
                "esli_slug": ESLI.get(s["slug"]),
                "esli_ad": indeks[ESLI[s["slug"]]]["ad"] if s["slug"] in ESLI else "",
                "iletisim": iletisim, "has_email": bool(s.get("email")),
                "has_adres": bool(s.get("adres")),
                "email_kurumsal": s.get("email_kurumsal"),
                "benzer": benzer,
                "kaynak_url": s.get("kaynak_url"), "kaynak_web": web or s.get("kaynak_url", ""),
                # İP-1 — copy/03-marka-sorgulari.md §4
                "cevap_once": cevap_once,
                "dogrulanan": dogrulanan, "dogrulanamayan": dogrulanamayan,
                "sirkete": sirkete, "hasar_ihbar_online": hasar_ihbar_online,
                "kimin_baslik": kimin_baslik, "kimin_cevap": kimin_cevap,
                "karisan": karisan, "sss": sss,
                "karsilastirma": karsilastirma.get(s["slug"], []),
            }

            url = f"/tr/sirketler/{s['slug']}/"
            title = f"{s['ad']} — KKTC sigorta şirketi profili"
            if len(title) >= 60:
                title = f"{s['ad']} — şirket profili"
            if len(branslar) >= 8:
                desc = (f"{p['sehir']} merkezli {s['ad']}. {len(branslar)} branşta ürün, "
                        f"{len(sehirler)} şehirde ofis. Şeffaflık, dijital hizmet ve dil "
                        f"desteğinde ne doğrulayabildiğimiz.")
            elif len(branslar) >= 4:
                desc = (f"{p['sehir']} merkezli {s['ad']}. {len(branslar)} branşta ürün "
                        f"doğrulandı. Hangi bilgileri yayımladığı, hangilerini yayımlamadığı.")
            else:
                desc = (f"{p['sehir']} merkezli {s['ad']}. Şeffaflık, erişim ve dijital hizmet "
                        f"ölçütlerinde neyi doğrulayabildiğimiz, neyi doğrulayamadığımız.")

            # §9.1 — Sayfa şirketin KENDİSİ değil, şirket HAKKINDA. Bu yüzden
            # ProfilePage + mainEntity; çıplak Organization sayfanın şirket
            # olduğunu ima ediyordu. sameAs varlık eşleşmesinin ana sinyali.
            # parentOrganization basılmıyor: veride doğrulanmış ana kuruluş yok.
            varlik = {
                "@type": "Organization",
                "name": s["ad"],
                "url": f"https://{web}" if web else f"{self.alan_adi}{url}",
                "areaServed": "Cyprus",
                "address": {"@type": "PostalAddress", "addressLocality": p["sehir"],
                            "addressRegion": "Kuzey Kıbrıs", "addressCountry": "CY"},
            }
            sameas = [x for x in (f"https://{web}" if web else None,
                                  s.get("instagram"), s.get("facebook")) if x]
            if sameas:
                varlik["sameAs"] = sameas
            if s.get("kurulus_yili"):
                varlik["foundingDate"] = str(s["kurulus_yili"])
            if s.get("email"):
                varlik["email"] = s["email"]

            jsonld = [
                json.dumps({
                    "@context": "https://schema.org", "@type": "ProfilePage",
                    "dateModified": "2026-07-24",
                    "mainEntity": varlik,
                }, ensure_ascii=False),
                json.dumps({
                    "@context": "https://schema.org", "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": q["soru"],
                         "acceptedAnswer": {"@type": "Answer", "text": q["cevap"]}}
                        for q in sss
                    ],
                }, ensure_ascii=False),
                json.dumps({
                    "@context": "https://schema.org", "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Ana sayfa",
                         "item": f"{self.alan_adi}/tr/"},
                        {"@type": "ListItem", "position": 2, "name": "Şirketler",
                         "item": f"{self.alan_adi}/tr/sirketler/"},
                        {"@type": "ListItem", "position": 3, "name": s["ad"],
                         "item": f"{self.alan_adi}{url}"},
                    ],
                }, ensure_ascii=False),
            ]

            bag = self.baglam(
                dil="tr", url=url, baslik=title, aciklama=desc,
                aktif_menu="sirketler", og_tur="profile", og_baslik=s["ad"],
                og_aciklama=desc, jsonld=jsonld,
            )
            bag["hreflang"] = {"tr": url}
            govde = sablon.render(p=p, **bag)
            self.sayfa_yaz(url, bag, govde, date(2026, 7, 24))

    # -- İP-2: web varlığı doğrulanamayan şirketler --------------------------

    def veri_yok_sayfalari(self):
        """Birlik üyesi ama web varlığı doğrulanamayan şirketler için kısa sayfa.

        Eşik "veri var mı" değil, "özgün ve doğrulanmış bir şey söyleyebiliyor
        muyuz". Dördünde de söyleyebiliyoruz: DNS, HTTP ve SSL ölçümleri.
        ⛔ Faaliyet durumu hakkında çıkarım yazılmaz — yalnız ölçülen yazılır.
        Gerekçe: copy/03-marka-sorgulari.md §5 ve §13.
        """
        olcum_yolu = KOK / "data" / "veri-yok-olcumleri.json"
        veri_yolu = KOK / "data" / "sirketler.json"
        if not olcum_yolu.is_file() or not veri_yolu.is_file():
            return
        blob = json.loads(olcum_yolu.read_text(encoding="utf-8"))
        kayitlar = blob.get("kayitlar", {})
        olcum_tarihi = blob.get("olcum_tarihi", "Temmuz 2026")
        tum = json.loads(veri_yolu.read_text(encoding="utf-8"))
        idx = {x["slug"]: x for x in tum}

        karsilastirma = {}
        kar_yolu = KOK / "data" / "ad-karisikliklari.json"
        if kar_yolu.is_file():
            for kay in json.loads(kar_yolu.read_text(encoding="utf-8")).get("kayitlar", []):
                for sl in kay["taraflar"]:
                    karsilastirma.setdefault(sl, []).append({
                        "url": f"/tr/sirketler/karsilastirma/{kay['slug']}/",
                        "h1": kay["h1"],
                    })

        sablon = self.jinja.get_template("sirket-veri-yok.html")

        for slug, kay in kayitlar.items():
            x = idx.get(slug)
            if x is None:
                continue
            v = {
                "ad": x["ad"], "slug": slug,
                "ozet": kay["ozet"], "olcumler": kay["olcumler"],
                "ek": kay.get("ek", ""), "olcum_tarihi": olcum_tarihi,
                "karsilastirma": karsilastirma.get(slug, []),
            }

            url = f"/tr/sirketler/{slug}/"
            title = f"{x['ad']} — neden bilgi bulunamıyor"
            desc = (f"{x['ad']} KKSRSB üyesi ruhsatlı bir sigorta şirketi. "
                    f"Web varlığını {olcum_tarihi} tarihinde ölçtük ve doğrulayamadık; "
                    f"ölçümün yöntemi ve sonucu bu sayfada.")

            sss = [
                {"soru": f"{x['ad']} ruhsatlı bir sigorta şirketi mi?",
                 "cevap": (f"Evet. {olcum_tarihi} tarihinde Kuzey Kıbrıs Sigorta ve "
                           f"Reasürans Şirketleri Birliği'nin üye listesinde ruhsatlı "
                           f"sigorta şirketi olarak yer alıyordu. Bir şirketin web "
                           f"sitesinin yanıt vermemesi, ruhsatı hakkında bir şey söylemez.")},
                {"soru": f"{x['ad']} hakkında neden internette bilgi yok?",
                 "cevap": kay["ozet"]},
                {"soru": f"{x['ad']} şirketinden poliçem var, ne yapmalıyım?",
                 "cevap": ("Poliçenizin geçerliliği hakkında bir şey söyleyemeyiz — bunu "
                           "ölçmedik. Sorunuz varsa KKTC Sigorta ve Reasürans Şirketleri "
                           "Birliği'ne ya da Para, Kambiyo ve İnkişaf Sandığı İşleri "
                           "Dairesi'ne sorun. Poliçenizi ve ödeme belgelerinizi saklayın.")},
            ]

            jsonld = [
                json.dumps({
                    "@context": "https://schema.org", "@type": "ProfilePage",
                    "dateModified": "2026-07-24",
                    "mainEntity": {
                        "@type": "Organization", "name": x["ad"],
                        "url": f"{self.alan_adi}{url}", "areaServed": "Cyprus",
                        "address": {"@type": "PostalAddress",
                                    "addressRegion": "Kuzey Kıbrıs", "addressCountry": "CY"},
                    },
                }, ensure_ascii=False),
                json.dumps({
                    "@context": "https://schema.org", "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": q["soru"],
                         "acceptedAnswer": {"@type": "Answer", "text": q["cevap"]}}
                        for q in sss
                    ],
                }, ensure_ascii=False),
                json.dumps({
                    "@context": "https://schema.org", "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Ana sayfa",
                         "item": f"{self.alan_adi}/tr/"},
                        {"@type": "ListItem", "position": 2, "name": "Şirketler",
                         "item": f"{self.alan_adi}/tr/sirketler/"},
                        {"@type": "ListItem", "position": 3, "name": x["ad"],
                         "item": f"{self.alan_adi}{url}"},
                    ],
                }, ensure_ascii=False),
            ]

            bag = self.baglam(
                dil="tr", url=url, baslik=title, aciklama=desc,
                aktif_menu="sirketler", og_tur="profile", og_baslik=x["ad"],
                og_aciklama=desc, jsonld=jsonld,
            )
            bag["hreflang"] = {"tr": url}
            self.sayfa_yaz(url, bag, sablon.render(v=v, **bag), date(2026, 7, 24))

    # -- Set H: karıştırılan adlar ------------------------------------------

    def ad_karisikliklari(self):
        """data/ad-karisikliklari.json → /tr/sirketler/karsilastirma/<slug>/

        Ad benzerliği yüzünden karıştırılan şirketleri yan yana koyar. Tablodaki
        her alan sirketler.json'dan gelir; yorum metinleri veri dosyasında durur.
        Gerekçe: copy/03-marka-sorgulari.md §6.
        """
        yol = KOK / "data" / "ad-karisikliklari.json"
        veri_yolu = KOK / "data" / "sirketler.json"
        if not yol.is_file() or not veri_yolu.is_file():
            return
        kayitlar = json.loads(yol.read_text(encoding="utf-8")).get("kayitlar", [])
        tum = json.loads(veri_yolu.read_text(encoding="utf-8"))
        idx = {x["slug"]: x for x in tum}
        # İP-2 sonrası dört veri-yok şirketinin de kendi sayfası var.
        olcum_yolu = KOK / "data" / "veri-yok-olcumleri.json"
        veri_yok_sayfali = set()
        if olcum_yolu.is_file():
            veri_yok_sayfali = set(
                json.loads(olcum_yolu.read_text(encoding="utf-8")).get("kayitlar", {}))
        profilli = {x["slug"] for x in tum if not sayfasiz_mi(x)} | veri_yok_sayfali

        TUR = {
            "yerel": "KKTC'de kurulmuş yerel şirket",
            "tr_subesi": "Türkiye şirketinin KKTC yapısı",
            "tr_ortakligi": "Türkiye sigortacısıyla yerel ortaklık",
            "banka_bagli": "Banka grubuna bağlı",
            "bilinmiyor": "Doğrulanamadı",
        }

        def vir(x):
            return str(x).replace(".", ",")

        def duz(t):
            """Şema ve meta açıklaması için: vurgu işaretlerini söker."""
            return t.replace("**", "")

        def vurgu(t):
            """Görüntü için: kaçışlar, sonra **x** -> <strong>. Şablonda
            autoescape kapalı olduğu için kaçış burada yapılır."""
            return re.sub(r"\*\*(.+?)\*\*",
                          r'<strong class="text-text">\1</strong>', escape(t))

        sablon = self.jinja.get_template("ad-karisikligi.html")

        for kay in kayitlar:
            taraflar = []
            for sl in kay["taraflar"]:
                x = idx.get(sl)
                if not x:
                    continue
                taraflar.append({
                    "slug": sl, "ad": x["ad"], "sehir": x.get("sehir") or "—",
                    "brans_sayisi": len(x.get("branslar") or []),
                    "puan": vir(x["genel_puan"]),
                    "profil_var": sl in profilli,
                    "_x": x,
                })
            if not taraflar:
                continue

            def satir(ad, uret):
                hucreler = []
                for t in taraflar:
                    d = uret(t["_x"])
                    hucreler.append({"deger": d or "Doğrulanamadı", "bos": not d})
                return {"ad": ad, "hucreler": hucreler}

            tablo = [
                satir("Ruhsat", lambda x: "KKSRSB üyesi"),
                satir("Şirket türü", lambda x: TUR.get(x.get("sirket_turu"))),
                satir("Kuruluş", lambda x: str(x["kurulus_yili"]) if x.get("kurulus_yili") else None),
                satir("Merkez", lambda x: x.get("sehir")),
                satir("Doğrulanan branş", lambda x: str(len(x.get("branslar") or []))
                      if (x.get("branslar") or []) else None),
                satir("Alan adı", lambda x: x.get("web")),
                satir("Genel puan", lambda x: vir(x["genel_puan"])),
            ]

            k = {
                "h1": kay["h1"], "kisa_cevap": vurgu(kay["kisa_cevap"]),
                "karisiklik": vurgu(kay["karisiklik"]), "pratik": vurgu(kay["pratik"]),
                "dogrulanamayan": [vurgu(d) for d in kay["dogrulanamayan"]],
                "dis_taraf": kay.get("dis_taraf"),
                "taraflar": taraflar, "tablo": tablo,
            }

            url = f"/tr/sirketler/karsilastirma/{kay['slug']}/"
            adlar = " ile ".join(t["ad"] for t in taraflar)
            _cevap_duz = duz(kay["kisa_cevap"])
            desc = _cevap_duz[:157]
            if len(_cevap_duz) > 157:
                desc = desc.rsplit(" ", 1)[0] + "…"

            sss = [{"soru": kay["h1"], "cevap": _cevap_duz}]
            sss.append({
                "soru": "Poliçemi hangi şirketten aldığımı nasıl anlarım?",
                "cevap": ("Sözleşmenin üstündeki tam unvana bakın. Hasar ihbarı ve şikâyet "
                          "yolu, poliçede adı geçen şirkete işler — benzer adlı başka bir "
                          "şirkete değil."),
            })

            jsonld = [
                json.dumps({
                    "@context": "https://schema.org", "@type": "FAQPage",
                    "mainEntity": [
                        {"@type": "Question", "name": q["soru"],
                         "acceptedAnswer": {"@type": "Answer", "text": q["cevap"]}}
                        for q in sss
                    ],
                }, ensure_ascii=False),
                json.dumps({
                    "@context": "https://schema.org", "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Ana sayfa",
                         "item": f"{self.alan_adi}/tr/"},
                        {"@type": "ListItem", "position": 2, "name": "Şirketler",
                         "item": f"{self.alan_adi}/tr/sirketler/"},
                        {"@type": "ListItem", "position": 3, "name": kay["h1"],
                         "item": f"{self.alan_adi}{url}"},
                    ],
                }, ensure_ascii=False),
            ]

            bag = self.baglam(
                dil="tr", url=url, baslik=kay.get("title") or kay["h1"], aciklama=desc,
                aktif_menu="sirketler", og_tur="article", og_baslik=kay["h1"],
                og_aciklama=desc, jsonld=jsonld,
            )
            bag["hreflang"] = {"tr": url}
            self.sayfa_yaz(url, bag, sablon.render(k=k, **bag), date(2026, 7, 24))

    # -- branşa göre şirket listeleri ---------------------------------------

    def sirket_branslari(self):
        """/tr/sirketler/<brans>/ — bir branşta ürünü doğrulanan şirketler."""
        veri_yolu = KOK / "data" / "sirketler.json"
        if not veri_yolu.is_file():
            return
        veri = json.loads(veri_yolu.read_text(encoding="utf-8"))

        BRANS = {
            "trafik": "Trafik", "kasko": "Kasko", "saglik": "Sağlık",
            "konut": "Konut", "isyeri": "İşyeri", "seyahat": "Seyahat",
            "nakliyat": "Nakliyat", "muhendislik": "Mühendislik",
            "sorumluluk": "Sorumluluk", "ferdi_kaza": "Ferdi kaza",
            "hayat": "Hayat", "yat": "Yat",
        }
        HUB = {"trafik", "kasko", "saglik", "konut", "seyahat", "isyeri"}
        HUB_URL = {b: f"/tr/sigorta/{b}/" for b in HUB}
        sablon = self.jinja.get_template("sirket-brans.html")

        # Hangi branşlarda kaç şirket var
        havuz = {}
        for s in veri:
            for br in (s.get("branslar") or []):
                havuz.setdefault(br, []).append(s)

        for br, ad in BRANS.items():
            if br in BRANS_SAYFASIZ:
                continue
            sirketler = havuz.get(br, [])
            if not sirketler:
                continue
            sirketler = sorted(sirketler, key=lambda s: s["genel_puan"], reverse=True)
            liste = [{
                "slug": s["slug"], "ad": s["ad"], "sehir": s.get("sehir", ""),
                "brans_sayisi": len(s.get("branslar") or []),
                "puan": str(s["genel_puan"]).replace(".", ","),
                "puan_sayi": s["genel_puan"],
            } for s in sirketler]

            bulgu = (f"39 ruhsatlı hayat dışı şirketin {len(sirketler)}'inde {ad.lower()} "
                     f"ürünü sitesinden doğrulandı. Genel puana göre sıralı; her ad "
                     f"şirketin tam profiline gider.")

            b = {"key": br, "ad": ad, "ad_kucuk": ad.lower(), "sayi": len(sirketler),
                 "sirketler": liste, "bulgu": bulgu, "hub_url": HUB_URL.get(br)}

            url = f"/tr/sirketler/{br}/"
            title = f"KKTC'de {ad.lower()} sigortası yapan {len(sirketler)} şirket"
            desc = (f"Kuzey Kıbrıs'ta {ad.lower()} branşında ürünü doğrulanan {len(sirketler)} "
                    f"ruhsatlı sigorta şirketi, genel puana göre sıralı. Her şirketin tam profili.")
            jsonld = [json.dumps({
                "@context": "https://schema.org", "@type": "ItemList",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": s["ad"],
                     "url": f"{self.alan_adi}/tr/sirketler/{s['slug']}/"}
                    for i, s in enumerate(sirketler)
                ],
            }, ensure_ascii=False)]

            bag = self.baglam(dil="tr", url=url, baslik=title, aciklama=desc,
                              aktif_menu="sirketler", og_aciklama=desc, jsonld=jsonld)
            bag["hreflang"] = {"tr": url}
            govde = sablon.render(b=b, **bag)
            self.sayfa_yaz(url, bag, govde, date(2026, 7, 24))

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
        dogrulama = "\n".join(
            f'<meta name="{escape(ad)}" content="{escape(deger)}">'
            for ad, deger in self.dogrulama.items()
        )
        yaz(CIKTI / "index.html", f"""<!DOCTYPE html>
<html lang="{varsayilan}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(self.yapilandirma['site_adi'])}</title>
{dogrulama}
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

    def oksuz_kontrol(self):
        """Üretilen hiçbir sayfaya başka bir sayfadan bağlantı yoksa bildirir.
        sitemap'te olup hiçbir yerden bağlanmayan sayfa aranamaz sayılır.
        Gerekçe: copy/03-marka-sorgulari.md §9.3."""
        baglanan = set()
        for dosya in CIKTI.rglob("*.html"):
            kaynak = "/" + str(dosya.relative_to(CIKTI).parent).replace("\\", "/").strip(".")
            if not kaynak.endswith("/"):
                kaynak += "/"
            for adres in re.findall(r'href="(/[^"#?]*)"', dosya.read_text(encoding="utf-8")):
                if adres != kaynak:                       # kendine bağlantı sayılmaz
                    baglanan.add(adres.rstrip("/") + "/")
        return sorted(u for u, _ in self.uretilen
                      if u != "/" and u.rstrip("/") + "/" not in baglanan)

    # -- çalıştır -----------------------------------------------------------

    def calistir(self, kontrol=False):
        taslaklar = self.oku()
        if CIKTI.exists():
            shutil.rmtree(CIKTI)
        CIKTI.mkdir(parents=True)

        self.varliklar()
        self.statik_sayfalar()
        self.sirket_profilleri()
        self.veri_yok_sayfalari()
        self.ad_karisikliklari()
        self.sirket_branslari()
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
            oksuz = self.oksuz_kontrol()
            if oksuz:
                print(f"\n  Öksüz sayfa ({len(oksuz)} adet — hiçbir sayfadan bağlanmıyor):")
                for u in oksuz[:10]:
                    print(f"    {u}")
                if len(oksuz) > 10:
                    print(f"    … {len(oksuz) - 10} sayfa daha")
            else:
                print("\n  Öksüz sayfa yok")
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
