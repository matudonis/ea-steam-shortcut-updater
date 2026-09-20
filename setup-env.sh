#!/usr/bin/env bash

set -euo pipefail

STEAM_DIR="${STEAM_DIR:-$HOME/.steam/steam}"
ENV_FILE=".env"

echo "Steam directory: $STEAM_DIR"
echo

# ---------------------------------------------------------------------
# Find Steam user ID
# ---------------------------------------------------------------------

mapfile -t USER_IDS < <(
    find "$STEAM_DIR/userdata" \
        -mindepth 1 \
        -maxdepth 1 \
        -type d \
        -printf '%f\n'
)

if [[ ${#USER_IDS[@]} -ne 1 ]]; then
    echo "Error: expected exactly one Steam user, found ${#USER_IDS[@]}." >&2
    echo >&2

    if [[ ${#USER_IDS[@]} -gt 0 ]]; then
        echo "Found:" >&2
        printf '  %s\n' "${USER_IDS[@]}" >&2
    fi

    echo >&2
    echo "Please set up STEAM_USER_ID manually in .env." >&2
    exit 1
fi

STEAM_USER_ID="${USER_IDS[0]}"

echo "Steam user ID: $STEAM_USER_ID"


# ---------------------------------------------------------------------
# Find EA Desktop installation / Steam App ID
# ---------------------------------------------------------------------

mapfile -t EA_PATHS < <(
    find "$STEAM_DIR/steamapps/compatdata" \
        -type d \
        -path '*/pfx/drive_c/Program Files/Electronic Arts/EA Desktop' \
        -print
)

if [[ ${#EA_PATHS[@]} -ne 1 ]]; then
    echo >&2
    echo "Error: expected exactly one EA Desktop installation, found ${#EA_PATHS[@]}." >&2
    echo >&2

    if [[ ${#EA_PATHS[@]} -gt 0 ]]; then
        echo "Found:" >&2
        printf '  %s\n' "${EA_PATHS[@]}" >&2
    fi

    echo >&2
    echo "Please set up STEAM_APP_ID manually in .env." >&2
    exit 1
fi

EA_PATH="${EA_PATHS[0]}"

STEAM_APP_ID="$(
    awk -F'/compatdata/|/pfx/' '{print $2}' <<< "$EA_PATH"
)"

if [[ -z "$STEAM_APP_ID" ]]; then
    echo "Error: could not determine Steam App ID from:" >&2
    echo "$EA_PATH" >&2
    exit 1
fi

echo "Steam App ID:  $STEAM_APP_ID"


# ---------------------------------------------------------------------
# Create .env
# ---------------------------------------------------------------------

cat > "$ENV_FILE" <<EOF
STEAM_USER_ID=$STEAM_USER_ID
STEAM_APP_ID=$STEAM_APP_ID
EOF

echo
echo "Created $ENV_FILE:"
cat "$ENV_FILE"
echo
echo "Setup complete."
