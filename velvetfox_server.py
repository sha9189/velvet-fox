#!/usr/bin/env python3
"""
==============================================================================
THE VELVET FOX COLLECTION - Inventory & Sales Manager
Local server
==============================================================================
Runs a small web server on this computer only, so the app can read and write
the data file and photos. Nothing is exposed to the internet: the server binds
to 127.0.0.1, which is reachable only from this machine.

Start it with the "Start Velvet Fox" launcher, or from a terminal:

    python3 velvetfox_server.py

Everything lives beside this file:
    VelvetFox.html          the app
    velvet-fox-data.json    all inventory, sales and adjustments
    photos/                 item photos
    backups/                dated copies of the data file

FOR WHOEVER MAINTAINS THIS
    Standard library only - no pip installs, nothing to keep updated.
    Routes are listed in do_GET / do_POST / do_DELETE near the bottom.
==============================================================================
"""

import json
import os
import re
import shutil
import socket
import sys
import threading
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# --------------------------------------------------------------------------
# Paths - everything is relative to this file, so the folder can be moved,
# renamed, or synced to Dropbox without breaking anything.
# --------------------------------------------------------------------------
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
APP_FILE    = os.path.join(BASE_DIR, "VelvetFox.html")
DATA_FILE   = os.path.join(BASE_DIR, "velvet-fox-data.json")
PHOTO_DIR   = os.path.join(BASE_DIR, "photos")
BACKUP_DIR  = os.path.join(BASE_DIR, "backups")

KEEP_BACKUPS = 30
MAX_UPLOAD   = 25 * 1024 * 1024          # 25 MB ceiling on any single request
PHOTO_NAME   = re.compile(r"^[A-Za-z0-9._-]+$")   # no slashes, no traversal

BLANK_DATA = {
    "schemaVersion": 1,
    "business": "The Velvet Fox Collection",
    "nextItemNumber": 1, "nextSaleNumber": 1, "nextAdjustmentNumber": 1,
    "categories": [],
    "channels": ["Booth", "Show", "Online", "Direct"],
    "adjustmentReasons": ["Lost", "Damaged", "At Home", "Gifted",
                          "Personal Use", "Sold - price unknown", "Correction"],
    "items": [], "sales": [], "adjustments": [], "lastSaved": None,
}

_write_lock = threading.Lock()


# --------------------------------------------------------------------------
# Data file handling
# --------------------------------------------------------------------------
def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def read_data():
    """Load the data file, creating a blank one the first time."""
    if not os.path.exists(DATA_FILE):
        write_data(BLANK_DATA)
        return dict(BLANK_DATA)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_data(obj):
    """
    Atomic save. We write to a temporary file and then replace the real one,
    so a crash or a full disk can never leave a half-written data file behind.
    os.replace is atomic on both macOS and Windows.
    """
    with _write_lock:
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=1, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, DATA_FILE)


def make_backup(tag=None):
    """Copy the current data file into backups/, then prune old ones."""
    if not os.path.exists(DATA_FILE):
        return None
    os.makedirs(BACKUP_DIR, exist_ok=True)
    name = f"velvet-fox-data-{today_str()}{('-' + tag) if tag else ''}.json"
    dest = os.path.join(BACKUP_DIR, name)
    if os.path.exists(dest) and not tag:
        return None                      # already backed up today
    shutil.copy2(DATA_FILE, dest)
    kept = sorted(n for n in os.listdir(BACKUP_DIR) if n.endswith(".json"))
    while len(kept) > KEEP_BACKUPS:
        try:
            os.remove(os.path.join(BACKUP_DIR, kept.pop(0)))
        except OSError:
            break
    return name


def safe_photo_path(name):
    """Reject anything that is not a plain filename inside photos/."""
    if not name or not PHOTO_NAME.match(name):
        return None
    path = os.path.normpath(os.path.join(PHOTO_DIR, name))
    if os.path.dirname(path) != os.path.normpath(PHOTO_DIR):
        return None
    return path


# --------------------------------------------------------------------------
# HTTP handler
# --------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "VelvetFox"

    # ---- helpers ----------------------------------------------------------
    def _send(self, code, body=b"", ctype="application/json", extra=None):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        # the app is the only client; never let a page elsewhere call us
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj), "application/json")

    def _error(self, code, msg):
        self._json({"error": msg}, code)

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0:
            return b""
        if n > MAX_UPLOAD:
            raise ValueError("That file is too large.")
        return self.rfile.read(n)

    def _guard_origin(self):
        """
        A page on another site could try to talk to this server through the
        browser. Requests from a real origin are refused; the app itself sends
        none (same-origin fetch) or our own.
        """
        origin = self.headers.get("Origin")
        if origin and not re.match(r"^http://(127\.0\.0\.1|localhost)(:\d+)?$", origin):
            self._error(403, "Blocked cross-origin request.")
            return False
        return True

    def log_message(self, fmt, *args):
        pass          # keep the terminal window quiet and unthreatening

    # ---- routes -----------------------------------------------------------
    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path in ("/", "/index.html", "/VelvetFox.html"):
            if not os.path.exists(APP_FILE):
                return self._send(500, "VelvetFox.html is missing from this folder.",
                                  "text/plain; charset=utf-8")
            with open(APP_FILE, "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")

        if path == "/api/data":
            try:
                return self._json(read_data())
            except json.JSONDecodeError:
                return self._error(500, "The data file could not be read. It may be "
                                        "damaged - restore the newest file from the "
                                        "backups folder.")

        if path == "/api/info":
            return self._json({
                "folder": BASE_DIR,
                "folderName": os.path.basename(BASE_DIR),
                "dataFile": os.path.basename(DATA_FILE),
                "backups": (sorted(os.listdir(BACKUP_DIR))
                            if os.path.isdir(BACKUP_DIR) else []),
            })

        if path.startswith("/photos/"):
            target = safe_photo_path(path[len("/photos/"):])
            if not target or not os.path.exists(target):
                return self._error(404, "No such photo.")
            with open(target, "rb") as f:
                return self._send(200, f.read(), "image/jpeg")

        return self._error(404, "Not found.")

    def do_POST(self):
        if not self._guard_origin():
            return
        path = self.path.split("?", 1)[0]

        if path == "/api/data":
            try:
                payload = json.loads(self._body().decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as e:
                return self._error(400, f"Could not read what was sent: {e}")
            if not isinstance(payload, dict) or "items" not in payload:
                return self._error(400, "That does not look like Velvet Fox data.")
            try:
                make_backup()               # once a day, before the first change
                write_data(payload)
            except OSError as e:
                return self._error(500, f"Could not save: {e}")
            return self._json({"ok": True, "savedAt": datetime.now().isoformat()})

        if path == "/api/backup":
            try:
                name = make_backup(tag=datetime.now().strftime("%H%M%S"))
            except OSError as e:
                return self._error(500, f"Could not write the backup: {e}")
            return self._json({"ok": True, "file": name})

        if path == "/api/photo":
            name = self.headers.get("X-Photo-Name", "")
            target = safe_photo_path(name)
            if not target:
                return self._error(400, "Bad photo name.")
            try:
                blob = self._body()
            except ValueError as e:
                return self._error(413, str(e))
            if not blob:
                return self._error(400, "Empty upload.")
            os.makedirs(PHOTO_DIR, exist_ok=True)
            try:
                with open(target, "wb") as f:
                    f.write(blob)
            except OSError as e:
                return self._error(500, f"Could not save the photo: {e}")
            return self._json({"ok": True, "file": name})

        return self._error(404, "Not found.")

    def do_DELETE(self):
        if not self._guard_origin():
            return
        path = self.path.split("?", 1)[0]
        if path.startswith("/api/photo/"):
            target = safe_photo_path(path[len("/api/photo/"):])
            if not target:
                return self._error(400, "Bad photo name.")
            try:
                if os.path.exists(target):
                    os.remove(target)
            except OSError as e:
                return self._error(500, f"Could not delete the photo: {e}")
            return self._json({"ok": True})
        return self._error(404, "Not found.")


# --------------------------------------------------------------------------
# Startup
# --------------------------------------------------------------------------
def find_port(preferred=8770, tries=20):
    """Use the usual port, or the next free one if something else has it."""
    for port in range(preferred, preferred + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise SystemExit("Could not find a free port to use.")


def main():
    if sys.version_info < (3, 7):
        raise SystemExit("This needs Python 3.7 or newer.")

    os.makedirs(PHOTO_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        write_data(BLANK_DATA)

    port = find_port()
    url = f"http://127.0.0.1:{port}/"
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)

    print("=" * 62)
    print("  THE VELVET FOX COLLECTION - Inventory & Sales")
    print("=" * 62)
    print(f"  Folder : {BASE_DIR}")
    print(f"  Address: {url}")
    print()
    print("  The app should open in your browser in a moment.")
    print("  Leave this window open while you work.")
    print("  To stop: close this window, or press Control-C.")
    print("=" * 62)

    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped. Your data is saved.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
