#!/usr/bin/env python3
"""Build a private Nox wrapper from user-supplied game files and pinned archives."""
# SPDX-License-Identifier: MIT
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
REQUIRED = ('Game.exe', 'nox.cfg', 'video.bag', 'video.idx', 'Audio.bag', 'Audio.idx', 'maps')


def game_directory(source):
    source = source.resolve()
    candidates = [source, source / 'Contents/Resources/game/Nox.app/Contents/Resources/drive_c/Program Files/GOG.com/NOX']
    for candidate in candidates:
        if all((candidate / name).exists() for name in REQUIRED):
            return candidate
    raise ValueError('Select the GOG Nox.app or an extracted Nox game directory.')


def verify(path, expected):
    with path.open('rb') as f:
        actual = hashlib.file_digest(f, 'sha256').hexdigest()
    if actual != expected:
        raise ValueError(f'Checksum mismatch: {path.name}. Use the pinned upstream download.')


def copy_game(source, target):
    # Never follow a GOG Save link into the user's personal Library.
    for item in source.rglob('*'):
        relative = item.relative_to(source)
        if relative.parts[0].lower() == 'save':
            continue
        if item.is_symlink():
            raise ValueError(f'Unexpected symlink in game data: {relative}')
    shutil.copytree(source, target, ignore=lambda directory, names: [n for n in names if n.lower() == 'save'])
    (target / 'Save').mkdir()


def configure(text):
    # Change exact keys only; preserve upstream per-game compatibility sections.
    options = dict(width='1600', height='1200', windowed='true', fullscreen='false',
                   maintas='true', renderer='auto', devmode='true', border='true',
                   resizable='true', savesettings='1', posX='-32000', posY='-32000')
    section = ''
    result = []
    for line in text.splitlines():
        if line.strip().startswith('['):
            section = line.strip().lower()
        if section == '[ddraw]' and '=' in line and not line.lstrip().startswith(';'):
            key = line.split('=', 1)[0].strip()
            if key in options:
                line = key + '=' + options[key]
        result.append(line)
    return '\n'.join(result) + '\n'


def build(args):
    source = game_directory(args.game)
    output = args.output.resolve()
    if output.exists():
        raise ValueError('Output already exists. Choose a new folder; existing saves will not be overwritten.')
    if output.is_relative_to(source):
        raise ValueError('Output must be outside the source game directory.')
    pins = json.loads((ROOT / 'dependencies.json').read_text())
    verify(args.wine, pins['wine']['sha256'])
    verify(args.ddraw, pins['cnc-ddraw']['sha256'])
    output.parent.mkdir(parents=True, exist_ok=True)
    # Build beside the destination, then rename only after successful assembly.
    with tempfile.TemporaryDirectory(prefix='.nox-build-', dir=output.parent) as temp:
        temp = Path(temp)
        extracted = temp / 'wine'
        with tarfile.open(args.wine) as archive:
            archive.extractall(extracted, filter='data')
        bundle = temp / 'Nox Mac Launcher'
        app = bundle / 'Nox.app'
        resources = app / 'Contents/Resources'
        macos = app / 'Contents/MacOS'
        macos.mkdir(parents=True)
        resources.mkdir()
        shutil.copytree(extracted / 'Wine Stable.app/Contents/Resources/wine', resources / 'wine', symlinks=True)
        game = bundle / 'Data/drive_c/Nox'
        copy_game(source, game)
        with zipfile.ZipFile(args.ddraw) as archive:
            (game / 'ddraw.dll').write_bytes(archive.read('ddraw.dll'))
            (game / 'ddraw.ini').write_text(configure(archive.read('ddraw.ini').decode('utf-8-sig')))
        shutil.copy2(ROOT / 'launcher.sh', macos / 'Nox')
        (macos / 'Nox').chmod(0o755)
        info = dict(CFBundleExecutable='Nox', CFBundleIdentifier='local.nox.mac-launcher',
                    CFBundleName='Nox Mac Launcher', CFBundlePackageType='APPL',
                    CFBundleShortVersionString='0.1.0', CFBundleVersion='1',
                    LSMinimumSystemVersion='12.0', NSHighResolutionCapable=True)
        (app / 'Contents/Info.plist').write_bytes(plistlib.dumps(info))
        shutil.copytree(ROOT / 'licenses', resources / 'licenses')
        for name in ('LICENSE', 'THIRD_PARTY_NOTICES.md', 'dependencies.json'):
            shutil.copy2(ROOT / name, resources / name)
        (bundle / 'PRIVATE-BUILD.txt').write_text('This folder contains your proprietary game files. Do not upload it.\nKeep Nox.app and Data together. Saves: Data/drive_c/Nox/Save\n')
        subprocess.run(['codesign', '--force', '--deep', '--sign', '-', str(app)], check=True)
        subprocess.run(['codesign', '--verify', '--deep', '--strict', str(app)], check=True)
        bundle.rename(output)
    print(f'Private app ready: {output / "Nox.app"}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--wine', type=Path, required=True)
    parser.add_argument('--ddraw', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        build(args)
    except (ValueError, OSError, subprocess.CalledProcessError, tarfile.TarError, zipfile.BadZipFile) as error:
        parser.exit(1, f'Build failed: {error}\n')


if __name__ == '__main__':
    main()
