# Third-party notices

The public source repository contains no runtime binaries or game data. The private builder consumes these separately downloaded packages:

| Component | Version | License / notice | Upstream |
| --- | --- | --- | --- |
| Wine | 11.0, macOS package 11.0_1 | LGPL-2.1-or-later; `licenses/Wine-NOTICE.txt` and `licenses/Wine-LGPL-2.1.txt` | [Wine source](https://github.com/wine-mirror/wine/tree/wine-11.0), [macOS build project](https://github.com/Gcenx/macOS_Wine_builds/tree/11.0_1) |
| cnc-ddraw | 7.1.0.0 | MIT; `licenses/cnc-ddraw-MIT.txt` | [Source](https://github.com/FunkyFr3sh/cnc-ddraw/tree/v7.1.0.0) |

Thanks to the Wine project contributors, Gcenx and contributors to the macOS packages, and FunkyFr3sh and cnc-ddraw contributors. The builder uses the upstream cnc-ddraw configuration and adjusts only display/mouse defaults. It does not change either runtime binary.

The Wine package also includes third-party libraries; their terms are not replaced by the launcher license or this list. These notices do not establish that a binary distribution has met all obligations. This project publishes only its own source and notices; it does not offer the generated private application as a downloadable release. If that changes, audit every bundled component and provide the exact corresponding source, build changes and applicable notices before distributing it.

Game data imported locally stays subject to its original terms. No rights in game files or artwork are granted by this repository. OpenNox code, branding and license text are not included or used.
