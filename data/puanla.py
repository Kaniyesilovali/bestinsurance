#!/usr/bin/env python3
"""
sirketler-a.json + sirketler-b.json  →  sirketler.json (puanlanmış)

Metodolojiye birebir uyar (/tr/metodoloji/):
  - Altı ölçüt, sabit ağırlıklarla.
  - Bir ölçütte veri toplanamadıysa o ölçüt SIFIR SAYILMAZ; ağırlığı kalan
    ölçütlere orantılı dağıtılır ve şirket sayfasında "veri toplanamadı" olarak
    işaretlenir.
  - Mali güç ve hasar ödeme performansı hiç puanlanmaz (kamuya açık veri yok).

Çalıştırma:  python3 data/puanla.py
"""
import json, pathlib, unicodedata

KOK = pathlib.Path(__file__).parent

AGIRLIK = {
    "seffaflik":     0.25,
    "urun":          0.20,
    "erisim":        0.20,
    "dijital":       0.20,
    "dil":           0.10,
    "kurumsal":      0.05,
}

OLCUT_ADI = {
    "seffaflik": "Şeffaflık ve doğrulanabilirlik",
    "urun":      "Ürün ve teminat genişliği",
    "erisim":    "Erişilebilirlik",
    "dijital":   "Dijital hizmet",
    "dil":       "Yabancı dilde hizmet",
    "kurumsal":  "Kurumsal derinlik",
}

CANLI = (200, 301, 302)


def _canli(s):
    return s.get("http_durum") in CANLI


# ─── Ölçütler ────────────────────────────────────────────────────────────────
# Her fonksiyon (puan, gerekce) veya (None, sebep) döner.
# None = veri toplanamadı → ağırlık yeniden dağıtılır.

def olc_seffaflik(s):
    p, var, yok = 0, [], []
    for alan, ad, agir in [
        ("kurulus_yili", "kuruluş yılı", 2),
        ("adres", "açık adres", 2),
        ("email", "e-posta", 2),
    ]:
        if s.get(alan):
            p += agir; var.append(ad)
        else:
            yok.append(ad)
    if s.get("email") and s.get("email_kurumsal"):
        p += 2; var.append("kurumsal e-posta alan adı")
    elif s.get("email"):
        yok.append("kurumsal e-posta alan adı")
    if s.get("police_sartlari_yayinda"):
        p += 2; var.append("poliçe genel şartları yayında")
    else:
        yok.append("poliçe genel şartları")
    return p, {"var": var, "yok": yok}


def olc_urun(s):
    n = len(s.get("branslar") or [])
    if n == 0:
        return None, "Şirketin yayımladığı bir ürün listesi bulunamadı"
    return min(10.0, n * 10 / 11), {"brans_sayisi": n}


def olc_erisim(s):
    sehirler = s.get("ofis_sehirler") or ([s["sehir"]] if s.get("sehir") else [])
    p = min(6.0, len(sehirler) * 2)
    ac = s.get("acente_sayisi")
    if ac is None:
        ac_p = 0
    elif ac >= 50:
        ac_p = 2
    elif ac >= 20:
        ac_p = 1.5
    else:
        ac_p = 1
    p += ac_p
    if s.get("whatsapp"):
        p += 2
    return min(10.0, p), {"sehir_sayisi": len(sehirler), "acente": ac}


def olc_dijital(s):
    if not _canli(s):
        return 0.0, {"neden": "Web sitesi yayında değil"}
    p = 2.0
    ozellik = []
    for alan, ad in [("online_teklif", "online teklif"),
                     ("online_police", "online poliçe"),
                     ("online_hasar_ihbar", "online hasar ihbarı"),
                     ("mobil_uygulama", "mobil uygulama")]:
        if s.get(alan):
            p += 2; ozellik.append(ad)
    return p, {"ozellikler": ozellik}


def olc_dil(s):
    if not _canli(s):
        return None, "Web sitesine erişilemediği için dil desteği gözlemlenemedi"
    if s.get("diller_makine"):
        return 0.0, {"neden": "Dil seçenekleri otomatik makine çevirisi, insan çevirisi değil"}
    yabanci = [d for d in (s.get("diller") or []) if d != "tr"]
    puan = {"en": 5, "ru": 3, "el": 1, "de": 1, "fa": 2, "ar": 1}
    p = sum(puan.get(d, 1) for d in yabanci)
    return min(10.0, float(p)), {"diller": yabanci}


def olc_kurumsal(s):
    yil, tur = s.get("kurulus_yili"), s.get("sirket_turu")
    if not yil and tur in (None, "bilinmiyor"):
        return None, "Kuruluş yılı ve şirket yapısı doğrulanamadı"
    p = 0.0
    if yil:
        yas = 2026 - yil
        p += 5 if yas >= 50 else 4 if yas >= 25 else 3 if yas >= 10 else 2
    if tur in ("tr_subesi", "banka_bagli", "tr_ortakligi"):
        p += 5
    elif tur == "yerel":
        p += 3
    return min(10.0, p), {"kurulus_yili": yil, "tur": tur}


OLCUTLER = {
    "seffaflik": olc_seffaflik,
    "urun":      olc_urun,
    "erisim":    olc_erisim,
    "dijital":   olc_dijital,
    "dil":       olc_dil,
    "kurumsal":  olc_kurumsal,
}


def puanla(s):
    alt, veri_yok = {}, []
    for anahtar, fn in OLCUTLER.items():
        p, detay = fn(s)
        if p is None:
            veri_yok.append(anahtar)
            alt[anahtar] = {"puan": None, "sebep": detay}
        else:
            alt[anahtar] = {"puan": round(p, 1), "detay": detay}

    # Ağırlıkları yalnızca ölçülebilen ölçütlere dağıt
    olculen = [k for k in OLCUTLER if alt[k]["puan"] is not None]
    toplam_agirlik = sum(AGIRLIK[k] for k in olculen)
    genel = sum(alt[k]["puan"] * AGIRLIK[k] for k in olculen) / toplam_agirlik if toplam_agirlik else 0.0

    s["olcutler"] = alt
    s["veri_yok_olcutler"] = veri_yok
    s["genel_puan"] = round(genel, 1)
    # Şeritteki bant değerleri — metodolojideki sabit sıra
    s["profil"] = [
        (alt[k]["puan"] / 10 if alt[k]["puan"] is not None else None)
        for k in ["seffaflik", "urun", "erisim", "dijital", "dil", "kurumsal"]
    ]
    return s


def main():
    kayitlar = []
    for ad in ("sirketler-a.json", "sirketler-b.json"):
        kayitlar += json.loads((KOK / ad).read_text(encoding="utf-8"))

    slugs = [k["slug"] for k in kayitlar]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("Yinelenen slug var: " +
                         str([x for x in slugs if slugs.count(x) > 1]))

    for k in kayitlar:
        k.setdefault("diller_makine", False)
        puanla(k)

    kayitlar.sort(key=lambda k: (-k["genel_puan"],
                                 unicodedata.normalize("NFKD", k["ad"])))
    for i, k in enumerate(kayitlar, 1):
        k["sira"] = i

    (KOK / "sirketler.json").write_text(
        json.dumps(kayitlar, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{len(kayitlar)} şirket puanlandı → data/sirketler.json\n")
    print(f"{'#':>2}  {'ŞİRKET':<34}{'PUAN':>6}   eksik ölçüt")
    print("─" * 78)
    for k in kayitlar:
        eksik = ", ".join(OLCUT_ADI[x].split()[0].lower() for x in k["veri_yok_olcutler"])
        print(f"{k['sira']:>2}  {k['ad'][:33]:<34}{k['genel_puan']:>6.1f}   {eksik}")


if __name__ == "__main__":
    main()
