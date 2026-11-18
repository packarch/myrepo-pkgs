#!/usr/bin/env python3
"""Barres waybar des 10 thèmes du bureau Packarch, d'après les barres polybar
des mêmes thèmes sous Openbox. Écrit themes/<id>/waybar/{config,style.css}.

Dans config : @nom@ = couleur du thème (remplacée par packarch-skin à la
copie dans ~/.config/packarch/waybar) ; "@output@" et "@marge15@" sont remplis
par scripts/statusbar au lancement."""
import json, os, sys

# Usage : ./gen-waybar.py files/etc/skel/.config/packarch/themes
OUT = sys.argv[1]
S = "~/.config/packarch/scripts"

def sp(color, text, font=None):
    f = f" font_family='{font}'" if font else ""
    return f"<span color='@{color}@'{f}>{text}</span>"

def bar_icons(icon, color, n=10, fill="━", empty="━"):
    """Niveaux 0..100 % en barre (volume-bar, backlight-bar de polybar)"""
    out = []
    for i in range(n + 1):
        out.append(f"{sp(color, icon)} {sp(color, fill * i)}{sp('foreground-alt', empty * (n - i))}")
    return out

# ---------------------------------------------------------------- modules
def m_cpu(icon="\uf4bc", color="yellow"):
    return {"interval": 5, "format": f"{sp(color, icon)} {{usage}}%", "tooltip": False,
            "on-click": "kitty -e htop"}

def m_memory(icon="\uefc5", color="cyan", percent=False):
    label = "{percentage}%" if percent else "{used:0.1f}G"
    return {"interval": 10, "format": f"{sp(color, icon)} {label}",
            "tooltip-format": "Mémoire : {used:0.1f} Go / {total:0.1f} Go", "on-click": "kitty -e htop"}

def m_disk(icon="󰋊", color="magenta"):
    return {"interval": 60, "paths": ["/"], "format": f"{sp(color, icon)} {{free}}",
            "tooltip-format": "/ : {used} utilisés sur {total}"}

def m_temp(icon="\uf2c9", color="magenta"):
    # @cpu-temp@ : capteur du processeur, trouvé par scripts/statusbar (ligne
    # retirée s'il n'y en a pas : waybar lit alors thermal_zone0)
    # Valeur en vert, orange à partir de 75 °C, rouge à partir de 90 °C
    # (orange : pas de couleur orange dans les thèmes)
    val = lambda c: f"{sp(color, icon)} <span color='{c}'>{{temperatureC}}°C</span>"
    return {"hwmon-path": "@cpu-temp@", "interval": 10, "warning-threshold": 75, "critical-threshold": 90,
            "format": val("@green@"), "format-warning": val("#ff8c1a"), "format-critical": val("@red@"),
            "tooltip-format": "Processeur : {temperatureC}°C"}

def m_backlight(color="cyan", bar=False):
    icons = bar_icons("󰃠", color) if bar else ["󰃞", "󰃟", "󰃝", "󰃠"]
    fmt = "{icon}" if bar else f"{sp(color, '{icon}')} {{percent}}%"
    return {"format": fmt, "format-icons": icons, "tooltip-format": "Luminosité : {percent}%",
            "on-scroll-up": "light -A 5", "on-scroll-down": "light -U 5"}

def m_battery(color="green", charging="red", full="green", time=False):
    label = "{capacity}% ({time})" if time else "{capacity}%"
    return {"interval": 60, "states": {"warning": 30, "critical": 15},
            "format": f"{sp(color, '{icon}')} {label}",
            "format-charging": f"{sp(charging, '\uf0e7')} {label}",
            "format-plugged": f"{sp(charging, '\uf1e6')} {{capacity}}%",
            "format-full": f"{sp(full, '\uf240')} Chargée",
            "format-icons": ["\uf244", "\uf243", "\uf242", "\uf241", "\uf240"], "format-time": "{H}h{M:02}",
            "tooltip-format": "{timeTo}"}

def m_bluetooth(color="blue"):
    return {"format": f"{sp(color, '\uf293')} {{status}}", "format-on": f"{sp(color, '\uf293')} Activé",
            "format-off": f"{sp('foreground-alt', '󰂲')} Désactivé",
            "format-disabled": f"{sp('foreground-alt', '󰂲')} Désactivé",
            "format-connected": f"{sp(color, '󰂱')} {{device_alias}}",
            "format-connected-battery": f"{sp(color, '󰂱')} {{device_alias}} {{device_battery_percentage}}%",
            "format-no-controller": "",
            "tooltip-format": "{controller_alias}\t{controller_address}",
            "tooltip-format-connected": "{controller_alias}\t{controller_address}\n\n{device_enumerate}",
            "tooltip-format-enumerate-connected": "{device_alias}\t{device_address}",
            "on-click": f"{S}/menu {S}/rofi_bluetooth", "on-click-right": "blueman-manager"}

def m_network(color="magenta", ext=False):
    if ext:
        wifi = f"{sp(color, '󰤨')} {{ifname}} · {{signalStrength}}% · {{ipaddr}} · {{essid}} · \uf019 {{bandwidthDownBytes}} · \uf093 {{bandwidthUpBytes}}"
        eth = f"{sp(color, '󰈀')} {{ifname}} · {{ipaddr}} · \uf019 {{bandwidthDownBytes}} · \uf093 {{bandwidthUpBytes}}"
    else:
        wifi = f"{sp(color, '󰤨')} {{essid}}"
        eth = f"{sp(color, '󰈀')} {{ifname}}"
    return {"interval": 5, "format-wifi": wifi, "format-ethernet": eth,
            "format-linked": f"{sp(color, '󰈀')} {{ifname}} (pas d'IP)",
            "format-disconnected": f"{sp('foreground-alt', '󰤭')} Hors ligne",
            "format-disabled": f"{sp('foreground-alt', '󰤭')} Désactivé",
            "tooltip-format": "{ifname} · {ipaddr}/{cidr} via {gwaddr}",
            "on-click": f"{S}/menu {S}/rofi_network",
            "on-click-right": "nm-connection-editor"}

def m_volume(color="blue", bar=False):
    icons = bar_icons("󰕾", color) if bar else ["󰕿", "󰖀", "󰕾"]
    fmt = "{icon}" if bar else f"{sp(color, '{icon}')} {{volume}}%"
    return {"format": fmt, "format-bluetooth": fmt,
            "format-muted": f"{sp('foreground-alt', '󰝟')} Muet",
            "format-icons": {"default": icons}, "scroll-step": 5.0,
            "tooltip-format": "Volume : {volume}% ({desc})",
            "on-click": "pulsemixer --toggle-mute", "on-click-right": "pavucontrol",
            "smooth-scrolling-threshold": 1}

def m_clock(color="red", icon="󰥔", date=False):
    fmt = "{:%d %b %H:%M}" if date else "{:%H:%M}"
    return {"interval": 60, "locale": "fr_FR.UTF-8",
            "format": f"{sp(color, icon)} {fmt}", "format-alt": f"{sp(color, icon)} {{:%A %d %B %Y}}",
            "tooltip-format": "<big>{:%B %Y}</big>\n<tt><small>{calendar}</small></tt>"}

def m_tray():
    return {"icon-size": 16, "spacing": 8}

def m_taskbar():
    return {"format": "{icon} {title:.25}", "icon-size": 16, "tooltip-format": "{title}",
            "on-click": "minimize-raise", "on-click-middle": "close", "on-click-right": "maximize",
            "all-outputs": True, "ignore-list": ["yad"]}

def m_workspaces(icons):
    return {"format": "{icon}", "format-icons": icons, "on-click": "activate",
            "sort-by-id": True, "all-outputs": True}

def m_menu(text, color):
    return {"format": sp(color, text) if color else text,
            "tooltip-format": "Applications (clic droit : lancer une commande)",
            "on-click": f"{S}/menu {S}/rofi_launcher", "on-click-right": f"{S}/menu {S}/rofi_runner"}

def m_power(color="red"):
    return {"format": sp(color, "\uf011"), "tooltip-format": "Éteindre, redémarrer, se déconnecter…",
            "on-click": f"{S}/menu {S}/rofi_powermenu"}

def m_updates(color="foreground"):
    return {"exec": "checkupdates 2>/dev/null | wc -l", "exec-if": "command -v checkupdates",
            "interval": 3600, "format": f"{sp(color, '󰏔')} {{}}", "tooltip-format": "Mises à jour disponibles",
            "on-click": "kitty -e sudo pacman -Syu"}

def m_text(text):
    return {"format": text, "tooltip": False}

LAUNCHERS = {
    "firefox": ("\uf269", "Firefox (clic droit : Gmail)", "firefox", "firefox https://mail.google.com", None),
    "thunar": ("\uf07b", "Fichiers (clic droit : en administrateur)", "thunar", f"{S}/asroot thunar", None),
    "kitty": ("\uf120", "Terminal (clic droit : en administrateur)", f"{S}/kitty", f"{S}/asroot 'kitty --class kitty-float --directory /root'", None),
    "discord": ("󰙯", "Discord", "discord", None, "discord"),
    "filezilla": ("\uf0ec", "FileZilla", "filezilla", None, "filezilla"),
    "mkvtoolnix": ("\uf008", "MKVToolNix", "mkvtoolnix-gui", None, "mkvtoolnix-gui"),
    "filebot": ("󰚩", "FileBot", "filebot", None, "filebot"),
    "themes": ("\U000f03d8", "Thèmes Packarch", "packarch-skin chooser", None, None),
}

def m_launch(app, color):
    icon, tip, cmd, right, need = LAUNCHERS[app]
    m = {"tooltip-format": tip, "on-click": cmd}
    if right:
        m["on-click-right"] = right
    if need:
        # Seulement si l'application est installée. exec doit écrire un
        # texte (non affiché : format n'a que l'icône) : waybar masque un
        # module custom dont la sortie est vide
        m.update({"exec": "echo installé", "exec-if": f"command -v {need}", "interval": "once"})
    m["format"] = sp(color, icon)
    return m

# ---------------------------------------------------------------- barres
class Bar:
    def __init__(self, name, position, height, **extra):
        self.d = {"name": name, "output": "@output@", "layer": "top", "position": position,
                  "height": height, "exclusive": True, "fixed-center": True, "spacing": 0,
                  "reload_style_on_change": True}
        self.d.update(extra)
        self.n = 0

    def add(self, zone, items):
        names = []
        for name, conf in items:
            if conf is not None:
                if name in self.d:  # même module, autre instance
                    self.n += 1
                    name = f"{name}#{self.n}"
                self.d[name] = conf
            names.append(name)
        self.d[f"modules-{zone}"] = names

def dots(prefix):
    """Fabrique de séparateurs numérotés"""
    c = [0]
    def f(text):
        c[0] += 1
        return (f"custom/{prefix}#{prefix[0]}{c[0]}", m_text(text))
    return f

def write(theme, bars, css):
    d = os.path.join(OUT, theme, "waybar")
    os.makedirs(d, exist_ok=True)
    head = (f"// Barre waybar du thème « {theme} » du bureau Packarch, comme\n"
            "// sa barre polybar sous Openbox. Copiée dans ~/.config/packarch/waybar/config\n"
            "// par packarch-skin, qui y remplace les @couleur@ par les couleurs du thème ;\n"
            "// \"@output@\" (écran principal) et \"@marge15@\" : remplis par scripts/statusbar.\n")
    with open(os.path.join(d, "config"), "w") as f:
        f.write(head + json.dumps([b.d for b in bars], ensure_ascii=False, indent=2) + "\n")
    with open(os.path.join(d, "style.css"), "w") as f:
        f.write(f"/* Style de la barre waybar du thème « {theme} » (Packarch), d'après sa\n"
                "   barre polybar sous Openbox. Couleurs et police : colors.css, écrit par\n"
                "   packarch-skin. */\n\n@import \"./colors.css\";\n" + BASE_CSS + css)

BASE_CSS = """
* {
	border: none;
	border-radius: 0;
	min-height: 0;
	box-shadow: none;
	text-shadow: none;
}

window#waybar {
	background-color: @background;
	color: @foreground;
}

tooltip {
	background-color: @background;
	border: 1px solid @background-alt;
}
tooltip label {
	color: @foreground;
}

button {
	background: none;
	border-radius: 0;
}

#workspaces button,
#taskbar button {
	padding: 0px 6px;
	color: @foreground-alt;
	background: none;
}
#workspaces button:hover,
#taskbar button:hover {
	background: none;
	color: @foreground;
}
#taskbar button.active {
	color: @foreground;
}
#taskbar button.minimized {
	opacity: 0.6;
}
#workspaces button.urgent {
	color: @green;
}

#battery.critical:not(.charging) {
	color: @red;
}
#tray > .needs-attention {
	-gtk-icon-effect: highlight;
}

#cpu, #memory, #disk, #temperature, #backlight, #battery, #bluetooth,
#network, #pulseaudio, #clock, #tray, #custom-updates,
#custom-menu, #custom-power {
	padding: 0px 8px;
}
"""

# ------------------------------------------------- famille « default »
def family_default(theme, red_satanic=False, power_bottom=False):
    """default, cyberpunk, pink-sylvanas, red-satanic : deux barres de 26 px
    avec une bordure de 6 px, des pastilles (LD/RD) et des points, et un
    trait noir (line-top, line-bottom) contre les fenêtres"""
    dot = dots("dot")
    if red_satanic:
        ws = m_workspaces({"default": "⛧", "active": "⛧"})
        menu = m_menu("󰚌", "accent")
        launch_colors = ("green", "green", "green")
        clock = m_clock("red")
        clock["format"] = f"{sp('red', '󰥔')} {sp('green', '{:%H:%M}')}"
    else:
        ws = m_workspaces({"default": "\uf10c", "active": "\uf111"})
        menu = m_menu("", "green")
        menu["format"] = sp("green", "", "packarch")
        launch_colors = ("magenta", "blue", "green")
        clock = m_clock("red")
    main = Bar("main", "top", 38)
    left = [("ext/workspaces", ws)]
    if not red_satanic:
        left += [dot("\uf444"), ("cpu", m_cpu("\uf4bc", "yellow")), dot("\uf444"), ("memory", m_memory("\uefc5", "cyan")),
                 dot("\uf444"), ("disk", m_disk("󰋊", "magenta"))]
    main.add("left", left)
    main.add("center", [("wlr/taskbar", m_taskbar())])
    main.add("right", [("backlight", m_backlight("cyan")), dot("\uf444"), ("battery", m_battery("green")), dot("\uf444"),
                       ("bluetooth", m_bluetooth("blue")), dot("\uf444"), ("network", m_network("magenta")), dot("\uf444"),
                       ("tray", m_tray()), ("custom/dot-alt#da1", m_text("\uf444")), ("custom/power", m_power())])
    bottom = Bar("bottom", "bottom", 38)
    launchers = [(f"custom/launch-{a}", m_launch(a, c)) for a, c in zip(("firefox", "thunar", "kitty"), launch_colors)]
    if red_satanic:
        bottom.add("left", [("custom/menu", menu), ("custom/dot-alt#da2", m_text("\uf444"))] + launchers)
        bottom.add("center", [("clock", clock)])
        vol = m_volume("blue")
        vol["format"] = f"{sp('blue', '{icon}')} {sp('green', '{volume}%')}"
        bottom.add("right", [("pulseaudio", vol)])
    else:
        bottom.add("left", [("custom/menu", menu)])
        bottom.add("center", [("group/launchers", {"orientation": "horizontal", "modules": [n for n, _ in launchers]})] )
        for n, c in launchers:
            bottom.d[n] = c
        right = [("pulseaudio", m_volume("blue")), ("custom/dot-alt#da2", m_text("\uf444")), ("clock", clock)]
        if power_bottom:
            right += [("custom/dot-alt#da3", m_text("\uf444")), ("custom/power", m_power())]
        bottom.add("right", right)
    css = """
/* Bordure de 6 px de la couleur de la barre, trait noir contre les fenêtres */
window#waybar.main {
	border-bottom: 1px solid #000000;
}
window#waybar.bottom {
	border-top: 1px solid #000000;
}

/* Pastilles (LD/RD de polybar) */
#workspaces, #taskbar, #battery, #tray, #custom-power, #custom-menu, #clock {
	background-color: @background-alt;
	border-radius: 13px;
	margin: 6px 0px;
	padding: 0px 10px;
}
#workspaces { padding: 0px 4px; }
#taskbar { padding: 0px 4px; }
window#waybar.empty #taskbar { background-color: transparent; }
#workspaces button { padding: 0px 5px; color: @accent; }
#workspaces button.active { color: @green; }
#custom-menu { font-size: 15px; padding: 0px 9px; }
#custom-power { padding: 0px 11px; }
#custom-launch-firefox, #custom-launch-thunar, #custom-launch-kitty { font-size: 14px; padding: 0px 8px; }

/* Points (dot, dot-alt) */
#custom-dot {
	color: @background-alt;
	padding: 0px 6px;
}
#custom-dot-alt {
	color: @foreground-alt;
	padding: 0px 6px;
}
"""
    if red_satanic:
        css += "#workspaces button { color: @foreground-alt; }\n#workspaces button.active { color: @accent; }\n"
    write(theme, [main, bottom], css)

# ---------------------------------------------------------------- thèmes
def pink_city():
    dot = dots("dot")
    b = Bar("main", "top", 38)
    menu = m_menu(" ", "green")
    menu["format"] = sp("green", "", "packarch")
    ws = m_workspaces({"1": "\uf120", "2": "\uf269", "3": "\uf07b", "4": "\uf044"})
    ws["format"] = "{icon}"
    b.add("left", [("custom/menu", menu), dot("\uf444"), ("ext/workspaces", ws), dot("\uf444"), ("tray", m_tray())])
    b.add("center", [("wlr/taskbar", m_taskbar())])
    clock = m_clock("cyan")
    clock["format"] = f"{sp('cyan', '\uf017')} {sp('cyan', '{:%H:%M}')}"
    b.add("right", [("pulseaudio", m_volume("blue", bar=True)), dot("\uf444"), ("backlight", m_backlight("cyan")), dot("\uf444"),
                    ("battery", m_battery("green")), dot("\uf444"), ("bluetooth", m_bluetooth("blue")), dot("\uf444"),
                    ("network", m_network("magenta")), dot("\uf444"), ("clock", clock), dot("\uf444"), ("custom/power", m_power())])
    css = """
window#waybar.main {
	border-bottom: 1px solid #000000;
	padding: 0px 8px;
}
#workspaces, #taskbar, #tray, #clock {
	background-color: @background-alt;
	border-radius: 13px;
	margin: 6px 0px;
	padding: 0px 8px;
}
window#waybar.empty #taskbar { background-color: transparent; }
#workspaces button { color: @foreground-alt; padding: 0px 6px; }
#workspaces button.active { color: @accent; border-bottom: 2px solid @accent; }
#custom-menu { font-size: 15px; }
#custom-dot {
	color: @background-alt;
	padding: 0px 10px;
}
"""
    write("pink-city", [b], css)

def hacking():
    sep = dots("sep")
    s = lambda: sep("∙")
    top = Bar("top", "top", 25)
    ws = m_workspaces({"1": "I", "2": "II", "3": "III", "4": "IV"})
    top.add("left", [("custom/menu", m_menu("󰣇", "foreground")), s(), ("ext/workspaces", ws), s(),
                     ("cpu", m_cpu("\uf4bc", "foreground")), s(), ("memory", m_memory("\uefc5", "foreground")), s(),
                     ("disk", m_disk("󰋊", "foreground"))])
    top.add("center", [("wlr/taskbar", m_taskbar())])
    net = m_network("foreground")
    net["format-wifi"] = net["format-ethernet"] = f"{sp('foreground', '󰖟')} En ligne"
    bat = m_battery("foreground", "foreground", "foreground", time=True)
    top.add("right", [("tray", m_tray()), s(), ("custom/updates", m_updates()), s(), ("network", net), s(),
                      ("battery", bat), s(), ("clock", m_clock("foreground", "󰥔")), s(),
                      ("custom/power", m_power("foreground"))])
    bottom = Bar("bottom", "bottom", 25)
    bottom.add("left", [("network", m_network("foreground", ext=True)), s(), ("bluetooth", m_bluetooth("foreground"))])
    bottom.add("center", [(f"custom/launch-{a}", m_launch(a, c)) for a, c in
                          (("firefox", "magenta"), ("thunar", "blue"), ("kitty", "green"))])
    bottom.add("right", [("pulseaudio", m_volume("green", bar=True)), s(), ("backlight", m_backlight("yellow", bar=True))])
    css = """
window#waybar { padding: 0px 8px; }
window#waybar.top { border-bottom: 1px solid @background-alt; }
window#waybar.bottom { border-top: 1px solid @background-alt; }
#workspaces button { color: @yellow; padding: 0px 8px; }
#workspaces button.active { color: @red; }
#custom-launch-firefox, #custom-launch-thunar, #custom-launch-kitty { font-size: 14px; padding: 0px 8px; }
#custom-sep {
	color: @accent;
	padding: 0px 14px;
}
"""
    write("hacking", [top, bottom], css)

def packarch():
    sep = dots("sep")
    top = Bar("top", "top", 38)
    ws = m_workspaces({"default": "󰊠", "active": "󰊠"})
    top.add("left", [("wlr/taskbar", m_taskbar())])
    top.add("center", [("ext/workspaces", ws)])
    top.add("right", [("clock", m_clock("cyan", "\uf017")), sep("\uf444"), ("pulseaudio", m_volume("yellow")), sep("\uf444"),
                      ("custom/power", m_power())])
    main = Bar("main", "bottom", 38)
    main.add("left", [("custom/menu", m_menu("󰮯", "accent")), sep("\uf444"),
                      ("custom/launch-themes", m_launch("themes", "yellow")), sep("\uf444"), ("cpu", m_cpu("󰍛", "green")), sep("\uf444"),
                      ("memory", m_memory("\uf2db", "cyan", percent=True)), sep("\uf444"), ("temperature", m_temp("\uf2c9", "magenta"))])
    apps = (("firefox", "magenta"), ("thunar", "blue"), ("kitty", "green"), ("discord", "cyan"),
            ("filezilla", "yellow"), ("mkvtoolnix", "red"), ("filebot", "bright-blue"))
    launchers = [(f"custom/launch-{a}", m_launch(a, c)) for a, c in apps]
    main.add("center", [("group/launchers", {"orientation": "horizontal", "modules": [n for n, _ in launchers]})])
    for n, c in launchers:
        main.d[n] = c
    main.add("right", [("backlight", m_backlight("cyan")), sep("\uf444"), ("battery", m_battery("green")), sep("\uf444"),
                       ("bluetooth", m_bluetooth("blue")), sep("\uf444"), ("tray", m_tray())])
    css = """
window#waybar { padding: 0px 16px; }
#workspaces, #taskbar, #launchers {
	background-color: @background-alt;
	border-radius: 8px;
	margin: 6px 0px;
	padding: 0px 4px;
}
window#waybar.empty #taskbar { background-color: transparent; }
/* Un fantôme par bureau : rouge pour le bureau actif */
#workspaces button { font-size: 14px; padding: 0px 5px; }
#workspaces button.active { color: @red; }
#custom-menu { font-size: 16px; }
#custom-launch-firefox, #custom-launch-thunar, #custom-launch-kitty, #custom-launch-discord,
#custom-launch-filezilla, #custom-launch-mkvtoolnix, #custom-launch-filebot {
	font-size: 15px;
	padding: 0px 8px;
}
/* sep : un point ; sep2 : un espace */
#custom-sep {
	color: @background;
	padding: 0px 6px;
}
"""
    write("packarch", [top, main], css)

def spark():
    sep = dots("sep")
    b = Bar("main", "bottom", 38, **{"margin-bottom": 15, "margin-left": "@marge15@", "margin-right": "@marge15@"})
    ws = m_workspaces({"default": "\uf0c8", "active": "\uf0c8"})
    b.add("left", [("ext/workspaces", ws)])
    b.add("center", [("wlr/taskbar", m_taskbar())])
    b.add("right", [("pulseaudio", m_volume("bright-magenta")), sep("\uf444"), ("backlight", m_backlight("bright-red")), sep("\uf444"),
                    ("battery", m_battery("bright-blue", "bright-red", "bright-green")), sep("\uf444"),
                    ("bluetooth", m_bluetooth("bright-blue")), sep("\uf444"), ("network", m_network("bright-yellow")), sep("\uf444"),
                    ("clock", m_clock("bright-cyan", "\uf017")), sep("\uf444"), ("tray", m_tray())])
    css = """
window#waybar {
	border-radius: 4px;
	padding: 0px 16px;
}
#workspaces button { color: @bright-cyan; padding: 0px 4px; font-size: 14px; }
#workspaces button.active { color: @accent; }
#custom-sep {
	color: @foreground-alt;
	padding: 0px 2px;
}
"""
    write("spark", [b], css)

def yellow_flower():
    sep = dots("sep")
    top = Bar("main", "top", 30, spacing=8)
    ws = m_workspaces({"default": "\uf10c", "active": "\uf111"})
    top.add("left", [("ext/workspaces", ws), sep("|"), ("cpu", m_cpu("\uf080", "yellow")),
                     ("memory", m_memory("\uf200", "blue")), ("disk", m_disk("\uf0a0", "magenta"))])
    top.add("center", [("clock", m_clock("red", "\uf017", date=True))])
    top.add("right", [("battery", m_battery("yellow", "red", "red")), ("bluetooth", m_bluetooth("blue")),
                      ("network", m_network("magenta")), sep("|"), ("backlight", m_backlight("yellow", bar=True)),
                      ("tray", m_tray())])
    bottom = Bar("bottom", "bottom", 30, spacing=8)
    menu = m_menu("", "accent")
    menu["format"] = sp("accent", "", "packarch")
    bottom.add("left", [("custom/menu", menu), sep("|")] + [(f"custom/launch-{a}", m_launch(a, c)) for a, c in
                                                          (("firefox", "magenta"), ("thunar", "blue"), ("kitty", "green"))])
    bottom.add("center", [("wlr/taskbar", m_taskbar())])
    bottom.add("right", [("pulseaudio", m_volume("blue", bar=True)), sep("|"), ("custom/power", m_power())])
    css = """
window#waybar { padding: 0px 16px; }
window#waybar.main { border-bottom: 1px solid @accent; }
window#waybar.bottom { border-top: 1px solid @accent; }
#workspaces button { color: @accent; padding: 0px 4px; }
#workspaces button.active { color: @red; }
#custom-menu { font-size: 14px; }
#custom-launch-firefox, #custom-launch-thunar, #custom-launch-kitty { font-size: 14px; padding: 0px 4px; }
#cpu, #memory, #disk, #battery, #bluetooth, #network { padding: 0px 2px; }
#custom-sep { color: @background-alt; }
"""
    write("yellow-flower", [top, bottom], css)

def adaptive():
    """Barre de 34 px, segments en dégradé (gradient1..6) séparés par des
    flèches (2RD…7RD de polybar)"""
    b = Bar("main", "top", 34)
    ws = m_workspaces({"default": "\uf10c", "active": "\uf111"})
    b.add("left", [("ext/workspaces", ws)])
    b.add("center", [("wlr/taskbar", m_taskbar())])
    arrows = [("custom/arrow#a2", m_text(""))] + [(f"custom/arrow#a{i}", m_text("")) for i in range(3, 8)]
    b.add("right", [arrows[0], ("pulseaudio", m_volume("blue")), arrows[1], ("backlight", m_backlight("cyan")),
                    arrows[2], ("battery", m_battery("green")), arrows[3], ("bluetooth", m_bluetooth("blue")),
                    ("network", m_network("magenta")), arrows[4], ("clock", m_clock("green", "\uf017")), arrows[5],
                    ("tray", m_tray()), ("custom/power", m_power())])
    css = """
window#waybar { border-bottom: 1px solid @accent; }
#workspaces { padding: 0px 8px; }
#workspaces button { color: @accent; padding: 0px 4px; font-size: 11px; }
#workspaces button.active { color: @red; }
#custom-arrow {
	font-size: 26px;
	padding: 0px;
}
#custom-arrow.a2 { color: @gradient1; background-color: @background; }
#pulseaudio     { background-color: @gradient1; }
#custom-arrow.a3 { color: @gradient1; background-color: @gradient2; }
#backlight      { background-color: @gradient2; }
#custom-arrow.a4 { color: @gradient2; background-color: @gradient3; }
#battery        { background-color: @gradient3; }
#custom-arrow.a5 { color: @gradient3; background-color: @gradient4; }
#bluetooth, #network { background-color: @gradient4; }
#custom-arrow.a6 { color: @gradient4; background-color: @gradient5; }
#clock          { background-color: @gradient5; }
#custom-arrow.a7 { color: @gradient5; background-color: @gradient6; }
#tray, #custom-power { background-color: @gradient6; }
#custom-power   { padding: 0px 14px 0px 8px; }
"""
    write("adaptive", [b], css)

for t in ("default", "cyberpunk"):
    family_default(t)
family_default("pink-sylvanas", power_bottom=True)
family_default("red-satanic", red_satanic=True)
pink_city()
hacking()
packarch()
spark()
yellow_flower()
adaptive()
