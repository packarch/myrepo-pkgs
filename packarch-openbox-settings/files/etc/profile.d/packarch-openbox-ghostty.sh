# Openbox session: accounts from before Ghostty whose kitty was removed are
# switched to Ghostty before Openbox reads its configuration (7.0-84,
# /usr/bin/packarch-openbox-ghostty; does nothing once done)
case "$DESKTOP_SESSION:$XDG_SESSION_DESKTOP" in
*openbox*) [ -x /usr/bin/packarch-openbox-ghostty ] && /usr/bin/packarch-openbox-ghostty ;;
esac
