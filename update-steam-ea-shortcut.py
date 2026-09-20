#!/usr/bin/env python3

import os
import re
from pathlib import Path

import vdf
from dotenv import load_dotenv

load_dotenv()

STEAM_DIR = Path(
    os.getenv("STEAM_DIR", Path.home() / ".steam" / "steam")
)

STEAM_USER_ID = os.getenv("STEAM_USER_ID")
STEAM_APP_ID = os.getenv("STEAM_APP_ID")

APP_NAME = os.getenv("STEAM_APP_NAME", "EA Games")


if not STEAM_USER_ID:
    raise RuntimeError(
        "STEAM_USER_ID environment variable is not set."
    )

if not STEAM_APP_ID:
    raise RuntimeError(
        "STEAM_APP_ID environment variable is not set."
    )


SHORTCUTS_FILE = (
    STEAM_DIR
    / "userdata"
    / STEAM_USER_ID
    / "config"
    / "shortcuts.vdf"
)

EA_DESKTOP_DIR = (
    STEAM_DIR
    / "steamapps"
    / "compatdata"
    / STEAM_APP_ID
    / "pfx"
    / "drive_c"
    / "Program Files"
    / "Electronic Arts"
    / "EA Desktop"
)

def parse_version(folder_name):
    """
    Parse an EA Desktop version from a directory name.

    Examples:

        13.738
        13.768.7.6285
        13.791.0.6304-1789691035

    The optional "-build" suffix is ignored.
    """

    match = re.fullmatch(
        r"(\d+(?:\.\d+)*)(?:-.+)?",
        folder_name,
    )

    if not match:
        return None

    return tuple(
        int(component)
        for component in match.group(1).split(".")
    )


def find_newest_version():
    """Find the newest EA Desktop version directory."""

    versions = []

    if not EA_DESKTOP_DIR.is_dir():
        raise RuntimeError(
            f"EA Desktop directory does not exist:\n"
            f"{EA_DESKTOP_DIR}"
        )

    for path in EA_DESKTOP_DIR.iterdir():
        if not path.is_dir():
            continue

        version = parse_version(path.name)

        if version is not None:
            versions.append((version, path))

    if not versions:
        raise RuntimeError(
            f"No EA Desktop version directories found in:\n"
            f"{EA_DESKTOP_DIR}"
        )

    versions.sort(key=lambda item: item[0])

    return versions[-1][1]

def update_shortcut(new_version_dir):
    """Update the EA Games Steam shortcut."""

    exe = new_version_dir / "EA Desktop" / "EADesktop.exe"
    start_dir = new_version_dir / "EA Desktop"

    if not exe.exists():
        raise RuntimeError(
            f"EA Desktop executable not found:\n{exe}"
        )

    if not SHORTCUTS_FILE.exists():
        raise RuntimeError(
            f"Steam shortcuts file does not exist:\n"
            f"{SHORTCUTS_FILE}"
        )

    with SHORTCUTS_FILE.open("rb") as f:
        data = vdf.binary_load(f)

    shortcuts = data.get("shortcuts", {})

    for shortcut_id, shortcut in shortcuts.items():

        if shortcut.get("AppName") != APP_NAME:
            continue

        old_exe = shortcut.get("Exe", "")
        old_start_dir = shortcut.get("StartDir", "")

        new_exe = str(exe)
        new_start_dir = str(start_dir)

        if old_exe == new_exe and old_start_dir == new_start_dir:
            print("Shortcut is already up to date.")
            print(f"Version: {new_version_dir.name}")
            return

        print("Updating Steam shortcut:")
        print()
        print(f"  Old Exe:      {old_exe}")
        print(f"  New Exe:      {new_exe}")
        print()
        print(f"  Old StartDir: {old_start_dir}")
        print(f"  New StartDir: {new_start_dir}")

        shortcut["Exe"] = new_exe
        shortcut["StartDir"] = new_start_dir

        with SHORTCUTS_FILE.open("wb") as f:
            vdf.binary_dump(data, f)

        print()
        print(f"Updated EA Games shortcut to {new_version_dir.name}")
        return

    raise RuntimeError(
        f'Could not find Steam shortcut with AppName="{APP_NAME}"'
    )



def main():
    print(f"Steam directory: {STEAM_DIR}")
    print(f"Steam user ID:   {STEAM_USER_ID}")
    print(f"Steam app ID:    {STEAM_APP_ID}")
    print()

    newest = find_newest_version()

    print(f"Newest EA Desktop version: {newest.name}")
    print()

    update_shortcut(newest)


if __name__ == "__main__":
    main()
