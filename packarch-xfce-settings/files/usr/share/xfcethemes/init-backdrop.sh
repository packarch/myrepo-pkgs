#!/usr/bin/env bash
#
# init-backdrop.sh — appelé par ~/.xprofile avant le démarrage de la session
# XFCE (LightDM). xfdesktop 4.20 range le fond d'écran par nom de sortie vidéo
# (/backdrop/screen0/monitor<SORTIE>/workspace<N>/last-image) ; sur une session
# neuve ou un nouvel écran, ce réglage n'existe pas et xfdesktop affiche son
# image intégrée (la souris XFCE). On crée donc les réglages manquants avec le
# fond d'écran du thème courant, sans toucher à ceux qui existent déjà.
#
# Migration de l'ancien sélecteur de thèmes (couleurs) vers les thèmes de
# packarch-skin : une ancienne couleur dans .current_theme est remplacée par
# le thème le plus proche, appliqué une fois (une fois la session ouverte :
# xfconfd, xfwm4 et le tableau de bord doivent tourner).

STATE_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/xfcethemes"

command -v xfconf-query >/dev/null 2>&1 || exit 0

current="$(cat "$STATE_DIR/.current_theme" 2>/dev/null)"
if command -v packarch-skin >/dev/null 2>&1 && [[ -n $current ]] &&
    ! packarch-skin list | cut -f1 | grep -xF "$current" >/dev/null; then
    # shellcheck source=/usr/share/xfcethemes/theme-switcher.sh
    source "$(dirname "$(readlink -f "$0")")/theme-switcher.sh"
    theme="$(theme_of "$current")"
    echo "$theme" > "$STATE_DIR/.current_theme"
    (sleep 10 && packarch-skin apply "$theme") >/dev/null 2>&1 &
    disown
fi

command -v xrandr >/dev/null 2>&1 || exit 0

# Fond d'écran à utiliser : celui déjà appliqué à un autre écran, sinon celui
# du thème courant
image="$(xfconf-query -c xfce4-desktop -l -v 2>/dev/null \
    | awk '$1 ~ /\/workspace0\/last-image$/ { print $2; exit }')"
if [[ -z "$image" || ! -f "$image" ]]; then
    image="$(packarch-skin wallpaper 2>/dev/null)"
fi
[[ -f "$image" ]] || image="/usr/share/backgrounds/wallpaper-alt.png"

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
