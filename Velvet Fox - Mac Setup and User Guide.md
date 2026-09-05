# The Velvet Fox Collection
## Inventory & Sales Manager — Setup & User Guide (Mac)

**In one sentence:** this app keeps track of two things — what you bought, and what you sold. Everything else it shows you (money tied up in stock, profit, what is not moving) is worked out from those two lists.

---

## What you should have

All of these need to live together in **one folder**. Don't separate them.

| File | What it is |
|---|---|
| `Start Velvet Fox.command` | What you double-click to open the app. |
| `Update Velvet Fox.command` | Double-click to install a new version (your records are left alone). Your helper adds this file. |
| `VelvetFox.html` | The app itself. Never open this one directly. |
| `velvetfox_server.py` | The engine that reads and writes your files. |
| `velvet-fox-data.json` | **All your inventory and sales.** This is your records. |
| `photos/` | Item photos. Created automatically. |
| `backups/` | Dated copies of your records. Created automatically. |

> **The one thing to remember:** back up that folder and you have backed up the whole business. Copy it to iCloud, Dropbox or a USB stick now and then. That is the entire backup routine.

---

## One-time setup

You do this once. Budget fifteen minutes, and it is a reasonable thing to do with your technical helper on the phone.

### Step 1 — Put the folder somewhere sensible

Make a folder called **VelvetFox** in your **Documents** folder and put all the files above inside it.

### Step 2 — Check you have Python

The app needs Python 3, which is free and made by a non-profit. Many Macs already have it.

1. Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Return).
2. Type this and press Return:

   ```
   python3 --version
   ```

**If you see something like `Python 3.11.4`** — you're done, skip to Step 3.

**If you see "command not found"**, or a box appears offering to install developer tools:

- If the box appeared, click **Install** and wait. That's the easiest route.
- Otherwise go to **https://www.python.org/downloads/**, download the macOS installer, and run it. Click through with the default options.

Then run `python3 --version` again to confirm.

### Step 3 — Make the launcher clickable

macOS won't let a downloaded script run until you say so. Copy this line into Terminal exactly as written and press Return:

```
chmod +x ~/Documents/VelvetFox/"Start Velvet Fox.command"
```

Nothing visible happens. That's correct — silence means it worked.

*(If you put the folder somewhere other than Documents, adjust the path. Easier alternative: type `chmod +x ` — with a space at the end — then drag the `Start Velvet Fox.command` file from Finder into the Terminal window, which fills in the path for you, then press Return.)*

### Step 4 — Open it for the first time

The first time only, **right-click** (or Control-click) `Start Velvet Fox.command` and choose **Open**. macOS will warn you that it's from an unidentified developer — click **Open** again.

You only have to do this once. After that a normal double-click works.

---

## Using it day to day

**To start:** double-click **Start Velvet Fox.command**.

A Terminal window appears with the Velvet Fox banner, and the app opens in your browser a second later.

**While you work:** leave that Terminal window open. Minimise it if it's in the way, but don't close it — it *is* the app. Closing it is like closing the program.

**To stop:** close the Terminal window (or press `Control + C` in it). Your data is already saved; the app saves after every change.

> **Which browser?** Any of them. Safari, Chrome, Edge and Firefox all work. It opens in whichever is your default.

**To get an update:** when your technical helper says there's a new version, close the app and double-click **Update Velvet Fox.command**. It downloads the latest program files; your inventory, sales and photos are left untouched. First run: right-click it and choose **Open**, same as Step 4.

---

## The six screens

| Screen | What it is for |
|---|---|
| **Overview** | The numbers at a glance — stock on hand, money tied up, what sold this month, how much has been confirmed in the store. |
| **Inventory** | Everything you have bought. Add items, edit them, add photos, sell them. |
| **Sales** | Every sale, one line each. Search by month. |
| **Adjustments** | Things that left stock without being sold — lost, broken, taken home. |
| **Stock Check** | The every-few-months walk-round: tick off each piece you can actually see in the store. |
| **Data & Backup** | Download spreadsheets, make a backup, tidy up categories. |

---

## The things you will do most

### Adding something you just bought

**Inventory → + Add item.** Fill in what you know. Only the description really matters; everything else can be added later.

- **Category** — the broad type: Lamp, Picture, Bowl. Start typing and it suggests ones you've used before. Reusing an existing category beats making a new one that means the same thing.
- **Description** — enough detail that you'd recognise the piece: maker, pattern, material, size.
- **Cost each** and **Selling price each** — both are per *single item*, not per lot.
- **Bought from** and **Where it is** — these work the same way as Category: start typing and it offers the places and locations you've used before, or type a new one and it's remembered for next time. Keeping **Where it is** filled in is what makes a Stock Check walk-round fast.

### When you buy a lot — the 48 spoons rule

This is the one part worth reading twice, because it's where the old spreadsheet struggled.

If you buy 48 spoons for $57.60 and plan to sell them one at a time, you do **not** create 48 items. You create **one** item:

| Field | What you enter | Not this |
|---|---|---|
| Description | Silver plated spoons | — |
| How many bought | `48` | `1` |
| Cost each | `1.20`  ($57.60 ÷ 48) | `57.60` |
| Selling price each | `4.00` | `192.00` |

Now every time someone buys one spoon, you record a sale of quantity 1 against that item, and the count drops: 48, 47, 46. The app works out the rest — how many are left, how much you've made, and how much of the original $57.60 is still sitting on the shelf.

> **Same rule, smaller numbers.** A set of 6 teacups you'll sell as singles: quantity 6. A set of 6 you'll only ever sell together as one set: quantity 1, described as a set. The question is always *"how many separate things can I sell from this?"*

### Recording a sale

Two ways, both the same:

- Find the item in **Inventory** and click **Sell** next to it — usually quickest.
- Or **Sales → + Record a sale** and pick the item from the list.

The price fills in from the item automatically. Change it if it sold for less — that's normal and the app expects it. Before you save, it shows you the total, the profit, and how many will be left.

> **Sold three at once?** That's one sale line with quantity 3, not three separate sales.

### When something is lost, broken, or comes home

Use **Adjustments**, not a sale. A sale at a price of zero would drag your average prices and profit down and make the figures lie. An adjustment removes the item from stock and records why.

Reasons available: Lost, Damaged, At Home, Gifted, Personal Use, Sold – price unknown, Correction.

### Adding photos

Open an item with **Edit**, then choose the photos. You can add several at once and they're shrunk automatically so the folder doesn't balloon. A thumbnail then shows beside the item in the Inventory list.

One quirk: save a brand new item first, then reopen it to add photos. The app needs the item to exist before it can file pictures against it.

### Fixing a mistake

- **Wrong details on an item** — Inventory → Edit → change it → Save changes.
- **Sale entered wrong** — Sales → Delete on that line, then enter it again. Deleting a sale puts the stock back automatically.
- **Adjustment entered wrong** — same thing, on the Adjustments screen.
- **Deleting an item** — only possible if it has no sales against it. This is deliberate: deleting it would erase real sales history.

---

## What came across from the old spreadsheet

All 541 rows are already loaded. A few things so nothing surprises you:

- **Everything is quantity 1.** The old sheet never recorded how many of something you bought, so nothing was guessed. About 34 items look like they might be sets or lots — they're flagged for you to check.
- **The old "Color" column was really a status.** It was being used to record Sold, Lost and At Home. Those became sales and adjustments.
- **18 sales were created** from items marked Sold that had a price. The old sheet never recorded *when* they sold, so the purchase date was used as a placeholder — correct these if you remember the real dates.
- **15 items had prices that couldn't be read reliably** — things like `$2.50/12` or `one dollar. 67`. Rather than guess, the original text was kept in the notes and the price left blank.
- **There are 168 categories,** because the old "Item Name" column was free text — you'll see Pic, Picture and Pictures all separately.

To work through these: **Inventory → Show → Needs attention.** Editing an item and saving it clears its flag, so the list shrinks as you go. There's no rush — the app works fine in the meantime.

**Tidying categories:** Data & Backup → Categories. Pick the messy one, pick the one you want to keep, click Merge. Every item moves across. Doing a few of these makes everything downstream more useful.

---

## Stock Check — confirming what is really in the store

The records came from an old spreadsheet that had not been kept up to date, so at the start the app is really saying *"this is what the spreadsheet believed."* **Stock Check** is how you turn that into *"this is what we have actually seen."*

It is meant to be done as a walk-round of the store **every few months**, not every day.

### How it works

Every item is in one of three states, shown as a small tag on the **Inventory** list and on the **Stock Check** screen:

| Tag | Meaning |
|---|---|
| **unconfirmed** | Nobody has confirmed this piece in the store yet. Every old-spreadsheet item starts here. |
| **confirmed 3/2/2026** | Someone had it in their hands and pressed Confirm on that date. |
| **re-check due** | It was confirmed once, but more than six months ago — time to look again. |

There is **no "start over" button**. A confirmation simply ages out after about six months, and the item quietly comes back onto the list for the next round. That way the work spreads out and there is nothing to reset or get wrong.

### Doing a check

1. Open **Stock Check**. The three tiles at the top show how far along you are — how many pieces confirmed, and how much of your stock value that covers.
2. If your items have a **"Where it is"** filled in (Booth 12, storage, back room…), use the **Where it is** box to show one shelf or area at a time, and work through it physically.
3. For each piece you are holding: find it in the list (type part of the description or the ID into **Search**), and press **✓ Confirm**. The row turns green and drops off the list.
4. Something wrong on the record — wrong price, wrong description? Press **Edit**, fix it, save, then press **✓ Confirm**.
5. Wrong quantity — the label says 6 but you count 4? Fix the count in **Edit** (or, if two were sold and never recorded, add them on the **Sales** or **Adjustments** screen), then **✓ Confirm**.
6. Cannot find a piece at all? Leave it unconfirmed for now. If a proper search later says it is genuinely gone, record it on the **Adjustments** screen (Lost, or *Sold – price unknown*) — that takes it out of stock.

### Fixing a confirm you didn't mean

Set **Show** to **Already confirmed**, find the item, and press **Undo**. It goes straight back onto the to-do list.

### Seeing the result

- **Overview** has a **"Confirmed in stock"** figure — items and dollar value that have been verified. This is the number you can actually stand behind.
- **Inventory → Show → Not confirmed** lists everything still needing a look.
- The **Inventory CSV** (Data & Backup) now has **Confirm Status** and **Last Confirmed** columns.

> **Changing how often checks are due.** The six-month window is one line near the top of `VelvetFox.html` — `const RECHECK_MONTHS = 6;`. Your technical helper can change the number. Nothing else needs to change.

---

## Backups and getting your data out

A dated backup is written automatically the first time you change anything each day, and the last 30 are kept. You can also click **Make a backup now** at any time.

From **Data & Backup** you can download an **Inventory CSV**, a **Sales CSV** (with profit worked out per line), an **Adjustments CSV**, or the whole data file. CSVs open straight into Excel or Numbers — this is what you send the accountant.

---

## If something goes wrong

| What you see | What to do |
|---|---|
| "This page was opened directly instead of through the launcher" | You double-clicked `VelvetFox.html`. Close the tab and use `Start Velvet Fox.command` instead. |
| Terminal says "Python 3 is not installed" | Go back to Step 2 of setup. |
| `"Start Velvet Fox.command" cannot be opened` | Right-click it and choose **Open**, then click Open in the warning box. |
| Nothing happens when you double-click the launcher | The `chmod` step was missed. Go back to Step 3. |
| Browser says it can't connect | The Terminal window was closed. Start the app again. |
| **NOT SAVED** in the top corner | The Terminal window was closed while the app was open. Restart the app and check your last change is still there. |
| Photos show as grey squares | The `photos` folder was moved or renamed. Put it back beside the data file. |
| You deleted something by accident | Open `backups`, find the newest file, and give it to your helper — the app has no undo. |
| The app won't load your data | Copy the newest file out of `backups`, rename it `velvet-fox-data.json`, and replace the damaged one. |

> **The golden rule:** never edit `velvet-fox-data.json` by hand in a text editor. One stray comma and the app can't read it. Change things through the app.

---
---

# Appendix — for whoever helps technically

*The owner does not need to read this.*

### Stack

Two files: one HTML page (vanilla HTML/CSS/JS, no build step, no framework, no CDN, no external libraries) and one Python file using **only the standard library** — no pip, no virtualenv, nothing to keep patched. Edit either in a text editor, save, refresh the browser.

### Why there is a server at all

The first version used the File System Access API (`showDirectoryPicker`) from a `file://` page. That was wrong: the pickers require a secure context, a double-clicked local page doesn't reliably qualify, and Safari — the default browser on macOS — doesn't implement them at all. A loopback HTTP server sidesteps the entire problem and costs one dependency (Python) that macOS either has or installs with a single click.

The trade is deliberate: **one dependency, in exchange for working in every browser with no permission prompts and no handle-persistence machinery.**

### Server

`velvetfox_server.py` binds `127.0.0.1` only — not reachable from the network. Routes:

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Serves `VelvetFox.html` |
| GET | `/api/data` | Returns the JSON data file |
| POST | `/api/data` | Daily backup, then atomic write |
| GET | `/api/info` | Folder path, backup listing |
| POST | `/api/backup` | On-demand timestamped backup |
| POST | `/api/photo` | Upload (filename in `X-Photo-Name`) |
| DELETE | `/api/photo/<name>` | Remove a photo |
| GET | `/photos/<name>` | Serve a photo |

Notes: writes go to a temp file then `os.replace`, which is atomic on macOS and Windows, so a crash can't leave a half-written data file. Photo filenames are regex-restricted and re-checked against the resolved parent directory to block traversal. Non-loopback `Origin` headers are refused. Port 8770, or the next free one.

### Data model

| Collection | Purpose | Key fields |
|---|---|---|
| `items` | Everything purchased. One row per *purchase*, not per unit. | `id, category, description, purchaseDate, qtyPurchased, unitCost, listPrice`, and optionally `verifiedAt` |
| `sales` | One row per sale event. | `id, itemId, date, qty, unitPrice, channel` |
| `adjustments` | Non-sale stock removal. | `id, itemId, date, qty, reason` |

Stock on hand is **never stored**. It is always computed as `qtyPurchased − Σ(sales.qty) − Σ(adjustments.qty)`. This is the central design decision: there is no denormalised count to drift, so no reconciliation job is ever needed, and deleting a sale restores stock for free. Item status is likewise derived — the old spreadsheet kept a hand-maintained status column, which is exactly how it went stale.

**Stock Check** follows the same rule. The only thing stored is `item.verifiedAt` — a `"YYYY-MM-DD"` date, or the field is absent. Everything else (the unconfirmed / confirmed / re-check-due state, the badges, the progress figures, the CSV column) is derived from that one date by `checkState()` in section 4, against `RECHECK_MONTHS` (section 1, default 6). Confirming sets the date; Undo deletes it. No third state, no sessions, no reset.

### Code layout

The HTML's script block is numbered in nine sections: 1 Config, 2 State, 3 Storage, 4 Derived data, 5 UI helpers, 6 Views, 7 Actions, 8 Export, 9 Startup. **Only section 3 talks to the server**; everything else is pure UI over the in-memory `DATA` object. Rendering is deliberately naive — any change calls `renderAll()`, which rebuilds every screen. At this data volume that's instant and it removes a whole class of stale-UI bugs.

The **Stock Check** screen (`renderCheck()` in section 6, `confirmCheck()` / `uncheckItem()` in section 7) is built entirely from the existing pieces — same table markup, same filter pattern as Inventory, same `save()` + `renderAll()` cycle. It adds no server route and no dependency.

### Adding a field

Three edits, all near each other:

1. Add it to the form HTML in `itemForm()`.
2. Read it in `saveItem()` with `val("your-id")`.
3. Add it to the export row in `exportInventory()`.

Existing records simply have the field `undefined`, which renders blank. No migration. For a default, `loadData()` merges the loaded file over `blankData()`.

### Tests

`test_app.js` runs the app's pure logic under Node against the real seed data — stock maths, lot drawdown, CSV escaping, ID generation:

```
node test_app.js
```

33 assertions passed against the previous build. **They have not been re-run since the storage layer was rewritten** — the sandbox running this work had shell access disabled at that point. Please run it once, along with a manual smoke test (start the app, add an item, record a sale, add a photo, restart, confirm everything persisted), before the owner relies on it.

### Known limits

- One person at a time. Two people editing the same folder over a synced drive would overwrite each other.
- Inventory and sales tables render the first 400 matching rows; search narrows it.
- No undo. The daily backups in `backups/` are the safety net.
- Photos are stored as JPEG at max 1400px. Originals are not kept.

### If it needs to grow

If the business ever needs multiple users or phone access, keep the data model exactly as it is and move storage to a hosted database. The three collections map cleanly onto three tables, and only the handful of functions in section 3 of the HTML would change.
