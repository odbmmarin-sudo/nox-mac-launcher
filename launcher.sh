#!/bin/bash
# SPDX-License-Identifier: MIT
set -eu
MACOS_DIR="$(cd "$(dirname "$0")" && pwd)"
RESOURCES="$MACOS_DIR/../Resources"
PACKAGE_DIR="$(cd "$MACOS_DIR/../../.." && pwd)"
export WINEPREFIX="$PACKAGE_DIR/Data"
export WINEDEBUG=-all
export MVK_CONFIG_LOG_LEVEL=0
export WINEDLLOVERRIDES="ddraw=n,b;mscoree,mshtml,winemenubuilder="
exec >> "$PACKAGE_DIR/nox-launch.log" 2>&1
if [ ! -f "$WINEPREFIX/system.reg" ]; then
    "$RESOURCES/wine/bin/wine" wineboot -u
fi
cd "$WINEPREFIX/drive_c/Nox"
exec "$RESOURCES/wine/bin/wine" 'C:\Nox\Game.exe'
