#!/usr/bin/env bash
#
# init-backdrop.sh — appelé par ~/.xprofile avant le démarrage de la session
# XFCE (LightDM). xfdesktop 4.20 range le fond d'écran par nom de sortie vidéo
# (/backdrop/screen0/monitor<SORTIE>/workspace<N>/last-image) ; sur une session
# neuve ou un nouvel écran, ce réglage n'existe pas et xfdesktop affiche son
# image intégrée (la souris XFCE). On crée donc les réglages manquants avec le
# fond d'écran du thème courant, sans toucher à ceux qui existent déjà.
#
# Il prépare aussi le thème d'icônes Packarch à la couleur de dossiers du
# thème XFCE (packarch-folder-color) : à la première session (aucun thème
# choisi, /etc/skel donne Packarch en bleu) celle du thème "default", et à la
# place d'un ancien thème Luna (supprimés de packarch-icons 2.0-8) celle de
# ce thème.

STATE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/xfcethemes"

command -v xfconf-query >/dev/null 2>&1 || exit 0

# Thème d'icônes
if command -v packarch-folder-color >/dev/null 2>&1; then
    # shellcheck source=/usr/share/xfcethemes/theme-switcher.sh
    source "$(dirname "$(readlink -f "$0")")/theme-switcher.sh"
    set +euo pipefail  # options de theme-switcher.sh : pas ici
    current_icons="$(xfconf-query -c xsettings -p /Net/IconThemeName 2>/dev/null)"
    xfce_theme="$(cat "$STATE_DIR/.current_theme" 2>/dev/null)"
    case "$current_icons" in
        Luna-Dark) icon_theme_for_old=yellow ;;
        Luna-Green-Dark) icon_theme_for_old=green ;;
        Luna-Purple-Dark) icon_theme_for_old=purple ;;
        Luna-Red-Dark) icon_theme_for_old=red ;;
        Luna-Antidote-Dark) icon_theme_for_old=blue ;;
        *) icon_theme_for_old="" ;;
    esac
    if [[ -n $icon_theme_for_old ]]; then
        apply_icon_theme "$icon_theme_for_old"
    elif [[ -z $xfce_theme && $current_icons == Packarch ]]; then
        apply_icon_theme default
    fi
fi

command -v xrandr >/dev/null 2>&1 || exit 0

# Fond d'écran à utiliser : celui déjà appliqué à un autre écran, sinon le
# dernier fond du thème courant, sinon le fond du thème "default".
image="$(xfconf-query -c xfce4-desktop -l -v 2>/dev/null \
    | awk '$1 ~ /\/workspace0\/last-image$/ { print $2; exit }')"
if [[ -z "$image" || ! -f "$image" ]]; then
    theme="$(cat "$STATE_DIR/.current_theme" 2>/dev/null)"
    image="$(cat "$STATE_DIR/.last_wallpaper/$theme" 2>/dev/null)"
fi
[[ -f "$image" ]] || image="/usr/share/backgrounds/xfce-default.png"

count="$(xfconf-query -c xfwm4 -p /general/workspace_count 2>/dev/null || echo 4)"

while read -r monitor; do
    [[ -z "$monitor" ]] && continue
    for ((ws = 0; ws < count; ws++)); do
        base="/backdrop/screen0/monitor${monitor}/workspace${ws}"
        xfconf-query -c xfce4-desktop -p "$base/last-image" >/dev/null 2>&1 && continue
        xfconf-query -c xfce4-desktop -p "$base/last-image" -n -t string -s "$image"
        xfconf-query -c xfce4-desktop -p "$base/image-style" -n -t int -s 5
    done
done < <(xrandr --listmonitors 2>/dev/null | awk 'NR > 1 { print $NF }')

exit 0
