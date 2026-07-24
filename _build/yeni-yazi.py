#!/usr/bin/env python3
"""Yeni blog yazısı iskeleti oluşturur.

    python3 _build/yeni-yazi.py "Hasar ihbarı nasıl yapılır"
    python3 _build/yeni-yazi.py "Hasar ihbarı nasıl yapılır" --kategori Hasar

content/tr/rehber/<slug>.md dosyasını taslak olarak açar. Taslaklar
üretilmez; yayına hazır olunca frontmatter'daki 'taslak' satırını silin.
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from uret import ICERIK, slugla                                    # noqa: E402

SABLON = """---
baslik: "{baslik}"
h1: "{baslik}"
aciklama: "ARAMA SONUCUNDA GÖRÜNEN AÇIKLAMA — 150-160 karakter."
ozet: "LİSTE SAYFASINDAKİ KARTTA GÖRÜNEN 2-3 CÜMLE."
giris: "YAZININ EN ÜSTÜNDEKİ İRİ PARAGRAF. Okuyucu buradan yazının ona ne vereceğini anlamalı."
kategori: {kategori}
tarih: {tarih}
guncelleme: {tarih}
taslak: evet
---

Giriş paragrafı. Doğrudan konuya girin; "bu yazımızda" gibi ısınma cümleleri
kullanmayın.

## İlk ana başlık

Normal paragraf. **Kalın** ve [bağlantı](/tr/sigorta/trafik/) böyle yazılır.

- Madde
- Madde
- Madde

## İkinci ana başlık

### Alt başlık

Sıralı liste:

1. Birinci adım
2. İkinci adım
3. Üçüncü adım

Tablo:

| Sütun | Sütun |
|---|---|
| Değer | Değer |

<!-- Tasarımlı özel bir bölüm gerekiyorsa satır başında <section> açın;
     bu blok Markdown'a girmeden olduğu gibi sayfaya geçer. Silmekte serbestsiniz. -->

<section class="bg-paper border-t border-line">
  <div class="mx-auto max-w-shell px-[22px] py-12 sm:py-16">
    <div class="max-w-prose">
      <p class="u-eyebrow mb-4">Öne çıkan</p>
      <h2 class="u-display text-[1.75rem] sm:text-[2.25rem] leading-[1.1] mb-6">Vurgulanacak başlık</h2>
      <p class="text-[15px] text-muted leading-relaxed">Metin.</p>
    </div>
  </div>
</section>

## Kaynaklar

Doğrulayamadığınız rakamı yazmayın; boş bırakıp neden boş olduğunu söyleyin.
"""


def main():
    argumanlar = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not argumanlar:
        sys.exit('Kullanım: python3 _build/yeni-yazi.py "Yazı başlığı" [--kategori Hasar]')

    baslik = argumanlar[0]
    kategori = "Genel"
    if "--kategori" in sys.argv:
        i = sys.argv.index("--kategori")
        if i + 1 < len(sys.argv):
            kategori = sys.argv[i + 1]

    hedef = ICERIK / "tr" / "rehber" / f"{slugla(baslik)}.md"
    if hedef.exists():
        sys.exit(f"Bu dosya zaten var: {hedef}")

    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(
        SABLON.format(baslik=baslik.replace('"', "'"), kategori=kategori,
                      tarih=date.today().isoformat()),
        encoding="utf-8",
    )
    print(f"Oluşturuldu: {hedef.relative_to(ICERIK.parent)}")
    print(f"Adres:       /tr/rehber/{slugla(baslik)}/")
    print("\nYazıyı doldurun, sonra frontmatter'daki 'taslak: evet' satırını silin.")


if __name__ == "__main__":
    main()
