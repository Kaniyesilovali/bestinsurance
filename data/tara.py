#!/usr/bin/env python3
"""
Bir şirketin sitesini tanıtım sayfası için tarar. Yazmaz — yalnızca okur ve
okunanları metin olarak bırakır. Hangi bilginin sayfaya gireceğine
copy/05-sirket-tanitim.md karar verir, bu betik değil.

    python3 data/tara.py <slug> <ana-sayfa-url> [hedef-klasör]

Çıktı (varsayılan /tmp/tarama/<slug>/):
  _linkler.txt     ana sayfadaki iç bağlantılar (adres | bağlantı metni)
  _belgeler.txt    taranan sayfalardaki PDF/DOC bağlantıları ve HTTP durumları
  _ozet.txt        hangi sayfa hangi durum kodunu döndü, sitenin lang etiketi
  NN_<yol>.txt     her taranan sayfanın düz metni

Notlar
- Tarayıcı kimliğiyle istenir: bazı siteler curl'ün varsayılan kimliğini 406 ile
  reddediyor (mod_security).
- Yalnızca ana sayfadan bağlanan ve adı/adresi tanıtımla ilgili görünen sayfalar
  taranır; en çok SINIR sayfa. Site haritası gezilmez.
- JavaScript ile çizilen sitelerde metin boş gelir; bu bir bulgu değil, taramanın
  sınırıdır. Öyle bir sitede sayfa elle (tarayıcıyla) okunur.
"""
import html, pathlib, re, subprocess, sys, tempfile
from urllib.parse import urljoin, urlparse

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128 Safari/537.36")
SINIR = 45
ANAHTAR = re.compile(
    r"hakk|about|kurumsal|corporate|biz kimiz|who we|tarih|history|iletisim|iletişim|"
    r"contact|sube|şube|branch|office|ofis|acente|agenc|agent|urun|ürün|product|"
    r"sigorta|insurance|kasko|trafik|motor|konut|home|isyeri|işyeri|saglik|sağlık|"
    r"health|seyahat|travel|ferdi|accident|nakliyat|cargo|marine|muhendis|engineer|"
    r"sorumluluk|liabil|yat|yacht|hayat|life|hasar|claim|online|teklif|quote|"
    r"bireysel|kurumsal|personal|commercial|ticari|cam|hirsiz|hırsız|fire|yangin|yangın",
    re.I)
ATLA = re.compile(r"\.(jpg|jpeg|png|gif|svg|webp|zip|mp4)$|^mailto:|^tel:|^javascript:|"
                  r"whatsapp|facebook|instagram|twitter|linkedin|youtube|wa\.me|"
                  r"/login|/giris|/register|/cart|/sepet|wp-json|feed", re.I)
BELGE = re.compile(r"\.(pdf|docx?|xlsx?)(\?|$)", re.I)


def cek(url):
    p = subprocess.run(["curl", "-sL", "-k", "-A", UA, "-H", "Accept-Language: tr,en;q=0.8",
                        "--max-time", "30", "-w", "\n%{http_code} %{url_effective}", url],
                       capture_output=True)
    b = p.stdout
    i = b.rfind(b"\n")
    kod, _, son = b[i + 1:].decode().partition(" ")
    return int(kod or 0), son, b[:i].decode("utf-8", "replace")


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def cek_js(url):
    """JavaScript ile çizilen sayfa: headless Chrome'un oluşturduğu DOM."""
    if not pathlib.Path(CHROME).exists():
        return ""
    # Her çağrı kendi profilinde: aynı anda çalışan iki Chrome varsayılan profili kilitliyor.
    with tempfile.TemporaryDirectory() as profil:
        try:
            p = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-agent={UA}",
                                f"--user-data-dir={profil}", "--virtual-time-budget=15000", "--timeout=30000",
                                "--dump-dom", url], capture_output=True, timeout=60)
        except subprocess.TimeoutExpired:
            return ""
    return p.stdout.decode("utf-8", "replace")


def cek_akilli(url):
    """Önce düz istek; metin neredeyse boşsa tarayıcıyla yeniden dener."""
    kod, son, t = cek(url)
    if kod in (403, 406, 429, 503):        # bot koruması: tarayıcı geçebiliyor
        js = cek_js(son or url)
        if len(metin(js)) > 300:
            return 200, son or url, js
    if kod == 200 and len(metin(t)) < 300:
        js = cek_js(son or url)
        if len(metin(js)) > len(metin(t)):
            return kod, son, js
    return kod, son, t


def durum(url):
    p = subprocess.run(["curl", "-sIL", "-k", "-A", UA, "--max-time", "20", "-o", "/dev/null",
                        "-w", "%{http_code}", url], capture_output=True, text=True)
    kod = p.stdout.strip()
    if kod in ("403", "405", "000", ""):   # HEAD'i reddeden sunucular
        p = subprocess.run(["curl", "-sL", "-k", "-A", UA, "--max-time", "20", "-r", "0-1023",
                            "-o", "/dev/null", "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        kod = p.stdout.strip()
    return kod


def cf_coz(h):
    """Cloudflare e-posta gizlemesini çözer: ilk bayt anahtar, gerisi XOR."""
    b = bytes.fromhex(h)
    return "".join(chr(x ^ b[0]) for x in b[1:])


def metin(t):
    t = re.sub(r'(?is)<[^>]*data-cfemail="([0-9a-f]+)"[^>]*>.*?</[^>]+>',
               lambda m: cf_coz(m.group(1)), t)
    t = re.sub(r'/cdn-cgi/l/email-protection#([0-9a-f]+)', lambda m: "mailto:" + cf_coz(m.group(1)), t)
    t = re.sub(r"(?is)<(script|style|noscript|svg|head)\b[^>]*>.*?</\1\s*>", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|td|th|section|ul|ol|title|a|span|label|option)>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    satirlar = [re.sub(r"[ \t\xa0]+", " ", x).strip() for x in t.split("\n")]
    cikti, onceki = [], None
    for s in satirlar:
        if s and s != onceki:
            cikti.append(s)
        onceki = s
    return "\n".join(cikti)


def linkler(t, taban):
    out = []
    for h, a in re.findall(r'(?is)<a\b[^>]*?href=["\']([^"\'#]+)["\'][^>]*>(.*?)</a>', t):
        a = re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", a))).strip()
        out.append((urljoin(taban, h.strip()), a))
    return out


def ayni_alan(u, kok):
    a = urlparse(u).netloc.lower().removeprefix("www.")
    return a == kok or a.endswith("." + kok)


def main():
    slug, ana = sys.argv[1], sys.argv[2]
    hedef = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else f"/tmp/tarama/{slug}")
    hedef.mkdir(parents=True, exist_ok=True)
    kod, son, t = cek_akilli(ana)
    kok = urlparse(son or ana).netloc.lower().removeprefix("www.")
    lang = re.findall(r'(?i)<html[^>]*\blang=["\']?([\w-]+)', t)
    ozet = [f"ANA {kod} {son}", f"lang={lang}"]
    (hedef / "00_ana.txt").write_text(metin(t), encoding="utf-8")
    tum = linkler(t, son or ana)
    # Menüsü JavaScript ile kurulan sitelerde bağlantılar yalnızca çizilmiş DOM'da var.
    tum += [x for x in linkler(cek_js(son or ana), son or ana) if x not in tum]
    ic = []
    for h, a in tum:
        if ayni_alan(h, kok) and not ATLA.search(h) and h.rstrip("/") != (son or ana).rstrip("/"):
            if h not in [x for x, _ in ic]:
                ic.append((h, a))
    (hedef / "_linkler.txt").write_text(
        "\n".join(f"{h} | {a}" for h, a in ic)
        + "\n\n# dış bağlantılar\n"
        + "\n".join(sorted({h for h, _ in tum if not ayni_alan(h, kok)})), encoding="utf-8")
    secilen = [(h, a) for h, a in ic if not BELGE.search(h) and (ANAHTAR.search(h) or ANAHTAR.search(a))]
    belgeler = {h: a for h, a in tum if BELGE.search(h)}
    for n, (h, a) in enumerate(secilen[:SINIR], 1):
        k, s, tt = cek_akilli(h)
        ozet.append(f"{n:02d} {k} {h} | {a}")
        ad = re.sub(r"[^\w-]+", "_", urlparse(h).path.strip("/"))[:60] or "kok"
        (hedef / f"{n:02d}_{ad}.txt").write_text(f"URL: {h}\nHTTP: {k}\n\n" + metin(tt), encoding="utf-8")
        for bh, ba in linkler(tt, s or h):
            if BELGE.search(bh):
                belgeler.setdefault(bh, ba)
    if len(secilen) > SINIR:
        ozet.append(f"… {len(secilen) - SINIR} sayfa sınır nedeniyle taranmadı")
    (hedef / "_belgeler.txt").write_text(
        "\n".join(f"{durum(h)} | {a} | {h}" for h, a in belgeler.items()), encoding="utf-8")
    (hedef / "_ozet.txt").write_text("\n".join(ozet), encoding="utf-8")
    print("\n".join(ozet[:2]), f"\n{len(ic)} iç bağlantı, {min(len(secilen), SINIR)} sayfa tarandı, "
          f"{len(belgeler)} belge → {hedef}")


if __name__ == "__main__":
    main()
