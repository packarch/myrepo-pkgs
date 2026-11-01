#!/usr/bin/env bash
#
# theme-switcher.sh — ancien sélecteur de thèmes XFCE (couleurs blue, gray,
# green, purple, red, yellow, default), remplacé par packarch-skin, qui
# applique sur XFCE les mêmes thèmes que sur Openbox
# (/usr/share/xfcethemes/themes, « packarch-skin list »).
#
# Gardé pour les lanceurs du tableau de bord des utilisateurs existants
# (~/.config/xfce4/panel/launcher-30/theme-<couleur>.desktop) : chaque
# couleur applique le thème le plus proche.
#
# Usage : theme-switcher.sh --<couleur>|<thème>

set -euo pipefail

declare -A OLD=(
    [default]=default [blue]=packarch [purple]=pink-sylvanas [red]=red-satanic
    [yellow]=yellow-flower [green]=hacking [gray]=adaptive
)

# Couleur de l'ancien sélecteur (aussi utilisé par init-backdrop.sh)
theme_of() {
    local arg="${1#--}"
    echo "${OLD[$arg]:-$arg}"
}

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
    if [[ $# -ne 1 ]]; then
        echo "Usage : $(basename "$0") --<thème> (voir « packarch-skin list »)" >&2
        exit 1
    fi
    exec packarch-skin apply "$(theme_of "$1")"
fi
