# Nox Mac Launcher

Build a Mac launcher for your own GOG copy of **Nox (2000)** using Wine and cnc-ddraw. Includes a resizable window, saved window dimensions, and an unlocked mouse cursor.

This is an unofficial compatibility launcher for the original game. It is not a native engine port and has no OpenNox dependency. No game files, game artwork, saved games, or Wine binaries are distributed in this repository.

## Status

Early source-only release. The original local wrapper was tested by a user on an Apple M1 Max: the game menu worked and the updated window and mouse behavior were confirmed. A complete campaign, multiplayer, other Macs, and every audio device have not been validated. The reusable builder is a new packaging step; see `VALIDATION.md` for its checks.

## Requirements

- macOS 12 or later as this launcher's declared minimum; only the machine above has been tested.
- Rosetta 2 on Apple Silicon, already installed. The builder does not install it.
- Python 3.12 or later and Apple's `codesign` tool.
- Your own installed GOG Nox game files. Supports the legacy GOG Mac `Nox.app` or an already extracted Windows game directory containing `Game.exe`. Windows offline installers must be extracted separately first.
- A few GB of free space for the private build and temporary extraction.

The Wine package's upstream release also lists GStreamer as a dependency. This builder does not install system frameworks. If multimedia fails, consult the [Wine package requirements](https://github.com/Gcenx/macOS_Wine_builds/releases/tag/11.0_1); do not assume all video and audio paths are covered by our menu test.

## Build your private app

Download these two exact archives from their maintainers:

1. [Wine Stable 11.0_1](https://github.com/Gcenx/macOS_Wine_builds/releases/download/11.0_1/wine-stable-11.0_1-osx64.tar.xz)
2. [cnc-ddraw 7.1.0.0](https://github.com/FunkyFr3sh/cnc-ddraw/releases/download/v7.1.0.0/cnc-ddraw.zip)

In this project's folder, run (adjust the paths):

```sh
python3 build.py \
  --game "/Applications/Games/Nox.app" \
  --wine "$HOME/Downloads/wine-stable-11.0_1-osx64.tar.xz" \
  --ddraw "$HOME/Downloads/cnc-ddraw.zip" \
  --output "$HOME/Applications/Nox Mac Launcher"
```

The builder checks both archives against the SHA-256 values in `dependencies.json`. It reads your game without modifying it, imports no existing saves, and refuses to overwrite an existing output directory. It creates a locally ad-hoc-signed `Nox.app` and adjacent `Data` folder. **Keep those two together.** No administrator access or system Wine installation is needed. This is not a notarized distribution.

Double-click `Nox.app`. First launch initializes a fresh Wine prefix and can take longer. Subsequent launches use that prefix. Your private output includes proprietary game data: **do not upload it to GitHub or attach it to issues**.

## Controls and files

- Drag a window edge to resize; dimensions are remembered after normal exit.
- Option + Enter switches window/fullscreen mode.
- Control + Tab releases the cursor if captured. The default configuration leaves it unlocked.
- Saves: `Data/drive_c/Nox/Save`
- Display settings: `Data/drive_c/Nox/ddraw.ini`
- Launch log: `nox-launch.log` alongside the app. Review logs before sharing.

Default window: 1600 × 1200, with original aspect ratio retained. This upscales the original game; it does not add widescreen game content. Wine is a compatibility environment, not a security sandbox.

## Development

```sh
python3 -m unittest discover -s tests -v
bash -n launcher.sh
```

Use a new output folder for packaging tests. Never upload the generated app, `Data`, runtime archives, or personal logs. The repository's distribution is source-only; dependencies are downloaded by users from upstream. Binary redistribution would require a separate dependency and corresponding-source review, including bundled libraries.

## Legal and credits

Nox is a Westwood Studios game published by Electronic Arts. Rights in the game, name and artwork remain with their respective holders. GOG is referenced only to identify the supported game distribution. This project is not affiliated with, sponsored by, or endorsed by Electronic Arts, Westwood Studios, or GOG.

Users supply their own lawfully obtained copy. This project grants no rights to distribute Nox game content.

Original launcher/build code is MIT licensed. Wine and cnc-ddraw retain their own licenses. See [third-party notices](THIRD_PARTY_NOTICES.md) and `licenses/`.
