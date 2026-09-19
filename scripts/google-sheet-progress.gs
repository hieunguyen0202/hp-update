/**
 * Flashcards progress API — bind this script to a Google Sheet.
 *
 * Setup (once):
 * 1. Create a Google Sheet (e.g. "hieu-flashcards").
 * 2. In that sheet: Extensions → Apps Script. Paste this file.
 * 3. Change SECRET below to a passphrase only you know.
 * 4. Deploy → New deployment → Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 5. Copy the Web app URL (.../exec) and paste it into Flashcards → Sheet.
 * 6. After any later edit: Deploy → Manage deployments → pencil → New version.
 *
 * Sheet tab "progress" is created automatically:
 *   A: deck | B: updated_at | C: json
 */

const SECRET = "change-me";
const SHEET_NAME = "progress";

function jsonOut_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}

function getSheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(["deck", "updated_at", "json"]);
    sh.setFrozenRows(1);
    sh.setColumnWidth(1, 220);
    sh.setColumnWidth(2, 200);
    sh.setColumnWidth(3, 640);
  }
  return sh;
}

function findRow_(sh, deck) {
  const values = sh.getDataRange().getValues();
  for (let i = 1; i < values.length; i++) {
    if (String(values[i][0]) === String(deck)) return i + 1;
  }
  return null;
}

function parseBody_(e) {
  if (e && e.postData && e.postData.contents) {
    return JSON.parse(e.postData.contents);
  }
  return (e && e.parameter) || {};
}

function assertSecret_(data) {
  const got = data && data.secret != null ? String(data.secret) : "";
  if (!SECRET || got !== SECRET) {
    return jsonOut_({ ok: false, error: "unauthorized" });
  }
  return null;
}

function saveDeck_(data) {
  const deck = String(data.deck || "").trim();
  if (!deck) return jsonOut_({ ok: false, error: "missing deck" });
  const sh = getSheet_();
  const now = new Date().toISOString();
  const json = JSON.stringify(data.payload == null ? {} : data.payload);
  const row = findRow_(sh, deck);
  if (row) {
    sh.getRange(row, 1, 1, 3).setValues([[deck, now, json]]);
  } else {
    sh.appendRow([deck, now, json]);
  }
  return jsonOut_({ ok: true, deck: deck, updatedAt: now });
}

function loadDeck_(deck) {
  const key = String(deck || "").trim();
  if (!key) return jsonOut_({ ok: false, error: "missing deck" });
  const sh = getSheet_();
  const row = findRow_(sh, key);
  if (!row) return jsonOut_({ ok: true, found: false, deck: key, payload: null });
  const json = String(sh.getRange(row, 3).getValue() || "");
  let payload = null;
  try {
    payload = json ? JSON.parse(json) : null;
  } catch (err) {
    return jsonOut_({ ok: false, error: "invalid json in sheet" });
  }
  return jsonOut_({
    ok: true,
    found: true,
    deck: key,
    updatedAt: String(sh.getRange(row, 2).getValue() || ""),
    payload: payload,
  });
}

function doPost(e) {
  try {
    const data = parseBody_(e);
    const denied = assertSecret_(data);
    if (denied) return denied;
    const action = String(data.action || "save");
    if (action === "save") return saveDeck_(data);
    if (action === "load") return loadDeck_(data.deck);
    if (action === "ping") return jsonOut_({ ok: true, ping: true });
    return jsonOut_({ ok: false, error: "unknown action" });
  } catch (err) {
    return jsonOut_({ ok: false, error: String(err) });
  }
}

function doGet(e) {
  try {
    const data = (e && e.parameter) || {};
    if (String(data.action || "") === "ping") {
      return jsonOut_({ ok: true, ping: true });
    }
    const denied = assertSecret_(data);
    if (denied) return denied;
    if (String(data.action || "load") === "load") return loadDeck_(data.deck);
    return jsonOut_({ ok: false, error: "unknown action" });
  } catch (err) {
    return jsonOut_({ ok: false, error: String(err) });
  }
}
