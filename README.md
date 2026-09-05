# The Velvet Fox Collection — Inventory & Sales Manager

A small local app for tracking what the shop bought and what it sold. Runs on
one Mac, no internet, no accounts. One HTML file plus a tiny Python server
(standard library only — nothing to install but Python 3).

## Run it

Double-click **`Start Velvet Fox.command`**. It starts the server and opens the
app in your browser. Leave the Terminal window open while you work; close it to
stop. First run: right-click the launcher → **Open** once to get past the macOS
warning, and make sure it is executable:

```bash
chmod +x "Start Velvet Fox.command"
```

## What's in the folder

| File | Purpose |
|---|---|
| `VelvetFox.html` | The app (all UI + logic, logo embedded). |
| `velvetfox_server.py` | Local server that reads/writes the data file. |
| `Start Velvet Fox.command` | Double-click launcher (macOS). |
| `velvet-fox-logo*.{png,webp}` | Brand logo — mark used in the app, plus the original. |
| `Velvet Fox - Owner's Guide.docx` | Everyday guide for the shop owner. |
| `Velvet Fox - Mac Setup and User Guide.md` | Fuller guide, incl. a technical appendix. |
| `velvet-fox-data.json` | **The business records.** Not in git — see below. |
| `photos/`, `backups/` | Item photos and dated auto-backups. Not in git. |

## Data is not in git

`velvet-fox-data.json`, `photos/`, and `backups/` are the shop's live data and are
listed in `.gitignore`. Git carries the **code only**. Back up the data by copying
the whole folder to iCloud / Dropbox / a USB stick.

## Updating the client's copy

Push code changes from the dev machine, then on the shop's Mac run `git pull` in
this folder. The data files are ignored, so a pull never touches them. Full
first-time setup steps are kept with the dev notes.
