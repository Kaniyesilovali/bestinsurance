#!/usr/bin/env bash
# Yayına hazır siteyi üretir: CSS'i derler, sayfaları üretir, bağlantıları denetler.
# Sonuç dist/ klasöründe. O klasörün İÇİNDEKİLERİ sunucunun kök dizinine yüklenir.
#
#   ./yayinla.sh
#
set -euo pipefail
cd "$(dirname "$0")"

echo "1/3  Tailwind derleniyor…"
npx -y tailwindcss@3.4.17 -c _build/tailwind.config.js \
  -i _build/input.css -o assets/css/tailwind.css --minify 2>&1 | grep -i 'done\|error' || true

echo
echo "2/3  Şirket tablosu verisinden yenileniyor…"
python3 data/uret-sirketler.py

echo
echo "3/3  Sayfalar üretiliyor…"
python3 _build/uret.py --kontrol
