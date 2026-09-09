#!/usr/bin/env python3
"""
sirketler-a.json + sirketler-b.json  →  sirketler.json

Bu betiğin öncülü data/puanla.py idi; puanlama kaldırıldığında yerini bu aldı.
Artık tek işi iki kaynak dosyayı birleştirmek, slug yinelemesini yakalamak ve
listeyi Türk alfabesine göre sıralamak. Şirketlere puan verilmiyor, sıra
numarası atanmıyor: sıralama bir iddia değil, yalnızca okuma kolaylığı.

Çalıştırma:  python3 data/birlestir.py
"""
import json, pathlib

KOK = pathlib.Path(__file__).parent

# Türk alfabesi, yabancı harfler TDK sırasına göre araya yerleştirilmiş:
# q → p'den sonra, w ve x → v'den sonra. Bunlar olmadan "AXA" ile
# "AKFİNANS" yanlış sıralanıyordu.
_TR_ALFABE = "abcçdefgğhıijklmnoöpqrsştuüvwxyz"
_TR_SIRA = {h: i for i, h in enumerate(_TR_ALFABE)}


def tr_sirala(ad):
    """Türk alfabesine göre sıralama anahtarı. data/uret-sirketler.py ve
    _build/uret.py içindeki aynı adlı yardımcıyla aynı sırayı verir."""
    t = ad.replace("I", "ı").replace("İ", "i").lower()
    return [_TR_SIRA.get(h, -1) for h in t]


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

    kayitlar.sort(key=lambda k: tr_sirala(k["ad"]))

    (KOK / "sirketler.json").write_text(
        json.dumps(kayitlar, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"{len(kayitlar)} şirket birleştirildi → data/sirketler.json\n")
    print(f"{'ŞİRKET':<36}{'MERKEZ':<14}BRANŞ")
    print("─" * 60)
    for k in kayitlar:
        print(f"{k['ad'][:35]:<36}{(k.get('sehir') or '—')[:13]:<14}"
              f"{len(k.get('branslar') or [])}")


if __name__ == "__main__":
    main()
