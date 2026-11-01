# myrepo-pkgs

Sources des paquets du dépôt **[packarch]** (binaires dans
[myrepo](https://github.com/packarch/myrepo), servis par
`https://packarch.github.io/myrepo/$arch`).

## Paquets

Chaque paquet de thèmes contient **tout** ce qu'il faut : rien d'autre à
installer.

| Paquet | Contenu |
|---|---|
| `packarch-backgrounds` | les fonds d'écran des 10 thèmes de `packarch-skin` (Openbox et XFCE) et de l'écran de connexion (`wallpaper-alt.png`, aussi celui du thème `default`), dans `/usr/share/backgrounds` ; `packarch-backgrounds-openbox` fusionné en 2.0-6, les autres fonds supprimés |
| `packarch-icons` | les thèmes d'icônes des thèmes de `packarch-skin` et de l'écran de connexion : **Packarch** (dossiers bleus ; la couleur des dossiers de chaque thème est appliquée par `packarch-folder-color`), Hack, Luv-Folders(-Dark), `Qogir-Pink-Dark` (dossiers roses), et ceux dont ils héritent : Packarch-Base, Packarch-Base-Dark, Papirus-Apps. BeautyLine vient de `aur/beautyline`, Qogir de `qogir-icon-theme`, Papirus de `papirus-icon-theme` (dépendances). `packarch-icons-openbox` fusionné en 2.0-9, Vimix-Black(-Dark) supprimés |
| `packarch-themes` | les thèmes GTK (avec xfwm4) et Openbox des thèmes de `packarch-skin`, un de chaque par thème (`Packarch-<Thème>` et `OB-Packarch-<Thème>`) ; `packarch-themes-openbox` fusionné en 2.0-7, les anciens thèmes GTK du bureau XFCE supprimés |
| `packarch-cursors` | les curseurs : Bibata, Fluentt, Future, Lyra, Pear, Qogirr, Sweet, Vimix |
| `packarch-fonts` | toutes les polices (`/usr/share/fonts/packarch`), dont la police d'icônes `packarch` |
| `packarch-openbox-settings` | (anciennement `packarch-openbox`, renommé en 7.0-72 comme `packarch-xfce-settings`) bureau Openbox : polybar, menus rofi, dunst, picom, kitty, 10 thèmes (`~/.config/openbox/themes/*/theme.toml`), menus et scripts (`/usr/share/packarch/openbox`), icônes de dunst, `packarch-tcma` (actions de Thunar) et `packarch-reload-theme`, en français. La configuration va dans `/etc/skel` |
| `packarch-system-settings` | réglages système communs aux bureaux XFCE et Openbox : greeter LightDM sombre (`lightdm-gtk-greeter.conf.d`), pavé numérique sur l'écran de connexion, pas d'extinction de l'écran par X, hooks pacman (Geany en nouvelle instance, entrées inutiles cachées des menus : `packarch-hide-desktop-entries`), cachy-update installé, son applet démarrée à chaque session et sa vérification quotidienne (`arch-update.timer`) activée pour tous les utilisateurs, Packarch dans `/etc/os-release` et `/etc/lsb-release`, identifiants compris (`ID=packarch`, `ID_LIKE="cachyos arch"`, hook `zz-packarch-branding`, après ceux de `cachyos-hooks`, qui renomme aussi l'entrée `/+CachyOS` de `limine.conf`), icône `packarch` du thème GRUB `cachyos` |
| `packarch-xfce-settings` | réglages XFCE de l'ISO (`cachyos-xfce-settings` 1.0.9 avec nos modifications : thème `default` de `packarch-skin` au départ, Firefox, Geany, LilouCalc, Thunar, pas de veille ni de verrouillage, pavé numérique) et thèmes de `packarch-skin` sur XFCE (1.0.9-7 : les 10 thèmes d'Openbox, `theme.toml` copiés de `packarch-openbox-settings` à la construction dans `/usr/share/xfcethemes/themes`, un lanceur par thème dans le tableau de bord avec une miniature de son fond d'écran, et « Couleur des dossiers » ; entrées de menu « Thèmes Packarch » (`packarch-skin chooser`) et « Restaurer le bouton des thèmes » (`packarch-skin panel`) ; `theme-switcher.sh` ne fait plus que traduire les anciennes couleurs) ; remplace `cachyos-xfce-settings`, en conflit avec `packarch-openbox-settings` (fichiers communs de `/etc/skel`) |
| `packarch-zsh-config` | configuration zsh de CachyOS (`cachyos-zsh-config`) sans la dépendance inutile à vim, avec notre configuration powerlevel10k par défaut (utilisée sans `~/.p10k.zsh`) et l’alias `cleanup` corrigé ; fournit `cachyos-zsh-config` |
| `packarch-mirrorlist` | `/etc/pacman.d/packarch-mirrorlist` |
| `apps/*` | nos applications, compilées depuis le dernier tag de leur dépôt GitHub : `cryptyrust`, `bombicat`, `deadpool`, `liloucalc`, `nounours-player`, `packarch-folder-color` (couleur des dossiers des thèmes d'icônes, utilisé par `packarch-skin`), `packarch-hello` (écran d'accueil), `packarch-pi` (Packarch Installer), `packarch-depannage` (dépannage à distance par Tailscale SSH, temporaire, autorisé par l'utilisateur), `packarch-skin` (ci-dessous), `packarch-rmatrix` (`apps/rmatrix`, effet « Matrix » en console) |
| `apps/packarch-skin` | sélecteur de thèmes des bureaux Openbox et XFCE (Rust, dépôt [packarch-skin](https://github.com/packarch/packarch-skin) depuis 1.1.0, paquet dans `apps/packarch-skin`, construit en premier) : `packarch-skin apply THÈME`, `bar`, `list`, `check`, `openbox-menu`… ; `render` écrit le thème `default` dans le `/etc/skel` de `packarch-openbox-settings` et de `packarch-xfce-settings` à leur construction (`makedepends`). Sur XFCE (1.0.0-19) : mêmes thèmes, copies des `theme.toml` de `packarch-openbox-settings` dans `/usr/share/xfcethemes/themes` ; `apply` règle fond d'écran, thèmes GTK/xfwm4/icônes (avec `folder_color`)/curseur, couleurs de xfce4-terminal et de Geany, bouton des thèmes du tableau de bord (polices, barre et menus : Openbox seulement) |
| `aur/*` | copies de PKGBUILD AUR : `gtkmm`, `nitrogen`, `xfce-polkit`, `lead-git`, `skippy-xd-git`, `ksuperkey`, `betterlockscreen`, `networkmanager-dmenu-git`, `light`, `beautyline` (thème d’icônes BeautyLine, dépendance de `packarch-icons`), `filebot` (renommage de films et séries, logiciel commercial : licence à acheter sur filebot.net) |

Les paquets de thèmes remplacent les anciens paquets séparés
(`packarch-icons-arc`, `packarch-icons-luna`…, `packarch-gtk-theme-*`, et
depuis la fusion `packarch-*-openbox` : `replaces`). Ce qu'aucun thème
n'utilisait (`packarch-icons-extra`, devenu `packarch-extra`) a été supprimé
le 2026-11-01 ; il reste dans l'historique git.

**Crédits** : la plupart des thèmes, icônes, curseurs, polices, fonds d'écran
et scripts ont été rassemblés ou créés par Aditya Shakya (adi1090x), sous
licence GPL3 ; les mentions d'auteur des fichiers sont conservées.

Les `PKGBUILD` de nos applications sont uniquement ici (`apps/`) : leurs
dépôts n'ont pas à en contenir pour Arch Linux. Pour en ajouter une : créer
`apps/<nom>/PKGBUILD` avec `url=` pointant vers son dépôt GitHub (tags
`vX.Y.Z`) et la source `…/archive/refs/tags/v${pkgver}.tar.gz`.

## Utilisation

```sh
./build.sh                     # construit ce qui a changé, copie dans ../myrepo/x86_64
./build.sh -f packarch-icons   # reconstruit un paquet
../myrepo/update.sh            # base de données, commit et push du dépôt binaire

./update.sh                    # reprend les PKGBUILD de l'AUR dans aur/
./update.sh --apps             # met pkgver de apps/* au dernier tag GitHub
```

Mise à jour complète : `./update.sh --apps`, `./update.sh`, `./build.sh`,
puis `../myrepo/update.sh`.

Après une modification, incrémenter `pkgrel` (ou `pkgver`) des paquets
modifiés : `build.sh` ne reconstruit que les versions absentes du dépôt
binaire (`update.sh --apps` le fait pour les nouvelles versions des
applications). `makepkg.conf` : code x86-64 générique (le `makepkg.conf` de
CachyOS peut être en `-march=native`), sans LTO (le code C embarqué par les
crates Rust, zstd ou sqlite, ne se lierait pas) et compression forte (limite
de 100 Mo par fichier de GitHub).
