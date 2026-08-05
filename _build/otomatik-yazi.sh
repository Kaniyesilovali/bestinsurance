#!/usr/bin/env bash
# Haftalık yazı üretimi. launchd Pzt/Çrş/Cum 09:00'da çalıştırır.
#
# Elle çalıştırmak (denemek) için:
#   ./_build/otomatik-yazi.sh
#
# Zamanlayıcı:  ~/Library/LaunchAgents/com.kktcsigortamerkezi.yazi.plist
# Günlük:       _build/otomatik-yazi.log
# İstem:        _build/otomatik-yazi-istem.txt
# Yordam:       .claude/skills/yazi-uret/SKILL.md
#
# launchd kendi ortamını kurmaz — PATH burada elle verilir, yoksa node, python3
# ve claude bulunamaz.

set -uo pipefail

DEPO="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
LOG="$DEPO/_build/otomatik-yazi.log"

cd "$DEPO" || exit 1

{
    echo
    echo "═══════════ $(date '+%d.%m.%Y %H:%M:%S %Z') ═══════════"

    # Günlük şişmesin: 2 MB'ı geçerse son 500 satır kalsın.
    if [ -f "$LOG" ] && [ "$(wc -c <"$LOG")" -gt 2097152 ]; then
        tail -n 500 "$LOG" >"$LOG.tmp" && mv "$LOG.tmp" "$LOG"
    fi

    # Çalışma dizini kirliyse başlama — yarım kalmış elle düzenleme varsa
    # ajanın onu commit'lemesini istemiyoruz.
    if [ -n "$(git status --porcelain -- content copy _build data)" ]; then
        echo "İPTAL: commit edilmemiş değişiklik var. Önce onları halledin."
        git status --short -- content copy _build data
        exit 1
    fi

    # Uzaktakini al. Çakışma varsa hiç başlama.
    if ! git pull --rebase --quiet origin main; then
        echo "İPTAL: git pull başarısız. Çakışma olabilir."
        exit 1
    fi

    claude -p "$(cat "$DEPO/_build/otomatik-yazi-istem.txt")" \
        --model opus \
        --permission-mode bypassPermissions \
        --allowedTools "Bash Read Write Edit Glob Grep WebFetch WebSearch Skill" \
        --output-format text
    kod=$?

    echo
    echo "─── claude çıkış kodu: $kod ───"
    echo "─── son commit: $(git log --oneline -1) ───"
} >>"$LOG" 2>&1
