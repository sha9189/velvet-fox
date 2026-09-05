#!/bin/bash
# ============================================================================
#  THE VELVET FOX COLLECTION - start the Inventory & Sales app  (macOS)
#  Double-click this file. Leave the window that opens alone while you work.
# ============================================================================

# Work in the folder this file lives in, wherever that folder has been moved to.
cd "$(dirname "$0")" || exit 1

clear
echo "=============================================================="
echo "   THE VELVET FOX COLLECTION"
echo "   Starting the Inventory & Sales app..."
echo "=============================================================="
echo

# --- Find Python 3 ----------------------------------------------------------
PY=""
for candidate in python3 /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    # Confirm it really runs - on a fresh Mac /usr/bin/python3 is only a stub
    # that pops up the developer tools installer instead of running.
    if "$candidate" -c "import sys; sys.exit(0 if sys.version_info>=(3,7) else 1)" >/dev/null 2>&1; then
      PY="$candidate"
      break
    fi
  fi
done

if [ -z "$PY" ]; then
  echo "  Python 3 is not installed on this Mac yet."
  echo
  echo "  It is free and takes about two minutes, once only:"
  echo
  echo "     1. Go to      https://www.python.org/downloads/"
  echo "     2. Download the macOS installer and run it."
  echo "     3. Double-click 'Start Velvet Fox' again."
  echo
  echo "  (If a box appeared asking to install developer tools, you can click"
  echo "   Install instead - that works too.)"
  echo
  echo "  Press any key to close this window."
  read -n 1 -s
  exit 1
fi

if [ ! -f "velvetfox_server.py" ]; then
  echo "  velvetfox_server.py is missing from this folder."
  echo "  All the Velvet Fox files need to stay together in one folder."
  echo
  echo "  Press any key to close this window."
  read -n 1 -s
  exit 1
fi

# --- Go ---------------------------------------------------------------------
"$PY" velvetfox_server.py

echo
echo "  The app has stopped. You can close this window."
read -n 1 -s
