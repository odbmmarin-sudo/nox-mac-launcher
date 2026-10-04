# Validation — 2026-10-04

- Original private wrapper: user confirmed the game menu, larger/resizable window and mouse behavior on Apple M1 Max.
- Reusable builder: assembled a separate application from a pristine copy of the GOG game directory and the two pinned upstream archives.
- SHA-256 checks and local ad-hoc signature verification passed.
- Fresh first-launch Wine initialization completed and the `C:\Nox\Game.exe` process started. This was a process-level smoke test, not a visual or campaign validation of the new build. The separate test instance was then closed.
- Four automated tests passed: save symlinks are excluded, other external symlinks are rejected, configuration edits preserve compatibility sections/comments, and incorrect dependency hashes are rejected.
- Launcher shell syntax checked.
- Public source reviewed for local usernames/absolute personal paths; none included. Public files contain no game assets, runtime executables, app icons or saved games.

Remaining: visual confirmation of a clean build on a second Mac, campaign/multiplayer testing, broader audio-device coverage, and a simpler graphical setup flow. No notarized or game-containing application release is offered.
