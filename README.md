# EA Games Shortcut Updater

Updates a Steam shortcut for the EA App.

## Requirements

* Linux
* Python 3
* Steam
* EA App installed through Steam/Proton

## Important

Close Steam before running the script.

## TL;DR

```bash
git clone https://github.com/marifpn/ea-steam-shortcut-updater.git
cd ea-steam-shortcut-updater/
chmod u+x setup-env.sh
./setup-env.sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 update-steam-ea-shortcut.py
```

## What is this for?

If you have EA Games installed via Steam's protontricks, you may have noticed the EA Games app "stops working" after a while. This happens because EA Games auto-updates, its installation path changes, and Steam no longer locates it.

If your EA Games installation on Steam is not launching (or launches and then closes), use this script to update the EA Games application shortcut to its newest installed version on Steam.

### Explanation

EA Desktop installs each version into a separate directory, for example:

```text
EA Desktop/
├── 13.738/
├── 13.768.7.6285/
└── 13.791.0.6304-1789691035/
```

This script detects the newest version and updates the Steam shortcut's:

* `Exe`
* `StartDir`

The Steam `shortcuts.vdf` file is binary, so the script uses the Python `vdf` package to read and write it.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

If you have one Steam user and one installation of the EA Games application, you can use the setup script to configure your environment:

```bash
chmod u+x setup-env.sh
./setup-env.sh
```

Otherwise, follow the instructions below.

Create a `.env` file in the repository:

```text
STEAM_USER_ID=XXXX
STEAM_APP_ID=XXXXXX
```

### Finding your Steam user ID

If you have only one Steam user configured, you can automatically get the user ID with:

```bash
find ~/.steam/steam/userdata -mindepth 1 -maxdepth 1 -type d -printf '%f\n'
``

Steam stores user-specific configuration under:

```text
~/.steam/steam/userdata/
```

List the directories:

```bash
ls ~/.steam/steam/userdata/
```

You should see one or more numeric directories:

```text
123456789
987654321
```

The directory containing your `config/shortcuts.vdf` is your Steam user ID.

For example:

```text
~/.steam/steam/userdata/123456789/config/shortcuts.vdf
```

means:

```text
STEAM_USER_ID=123456789
```

You can also locate the file directly:

```bash
find ~/.steam/steam/userdata -name shortcuts.vdf
```

If you have multiple Steam accounts, make sure you select the account whose `shortcuts.vdf` contains the EA Games shortcut.

### Finding the Steam App ID

If you have only one EA Desktop installation, you can automatically find its App ID with:

```bash
find ~/.steam/steam/steamapps/compatdata \
    -type d \
    -path '*/pfx/drive_c/Program Files/Electronic Arts/EA Desktop' \
    -printf '%p\n' |
    awk -F'/compatdata/|/pfx/' '{print $2}'
```

The `STEAM_APP_ID` used here is the ID of the Steam shortcut/application whose Proton prefix contains the EA App.

The easiest way to identify it is to look at the Proton `compatdata` directories:

```bash
ls ~/.steam/steam/steamapps/compatdata/
```

Then check which directory contains your EA Desktop installation.

For example:

```text
~/.steam/steam/steamapps/compatdata/987654321/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/
```

means:

```text
STEAM_APP_ID=987654321
```

You can search for the EA Desktop directory directly:

```bash
find ~/.steam/steam/steamapps/compatdata \
    -type d \
    -path "*/drive_c/Program Files/Electronic Arts/EA Desktop"
```

This should produce something similar to:

```text
/home/user/.steam/steam/steamapps/compatdata/987654321/pfx/drive_c/Program Files/Electronic Arts/EA Desktop
```

The number immediately after `compatdata/` is the App ID.

## Steam installation directory

By default, the script assumes Steam is installed at:

```text
~/.steam/steam
```

This can be overridden with:

```text
STEAM_DIR=/path/to/steam
```

For example:

```text
STEAM_DIR=/home/user/.steam/steam
STEAM_USER_ID=123456789
STEAM_APP_ID=987654321
```

If you use the default Steam location, `STEAM_DIR` does not need to be specified.

## Running

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
python update-steam-ea-shortcut.py
```

## Idempotency

The script is intentionally safe to run repeatedly. 

It only modifies `shortcuts.vdf` when the EA Desktop shortcut points to an older version.

This makes it suitable for running after an EA App update.
