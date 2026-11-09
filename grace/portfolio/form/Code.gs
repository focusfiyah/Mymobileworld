/**
 * Grace With The Glow: "Get 3 free UGC ideas" form (Google Apps Script web app).
 * Same setup as the Diaspo lead system: paste this file + ideas.html into a new Apps Script project,
 * run setup() once, then Deploy > New deployment > Web app (Execute as: Me, Who has access: Anyone).
 * Each request is saved to the "Grace - 3 free UGC ideas" sheet and emailed to Grace (Reply goes to the brand).
 */
var GRACE_EMAIL = 'graceglows.ugc@gmail.com';
var FROM_NAME = 'Grace With The Glow';
var SHEET_NAME = 'Requests';
var HEADERS = ['Received', 'Name', 'Brand', 'Email', 'Product link', 'Videos for', 'Notes', 'Status'];

function setup() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('SHEET_ID');
  if (!id) {
    var ss = SpreadsheetApp.create('Grace - 3 free UGC ideas');
    var sh = ss.getSheets()[0];
    sh.setName(SHEET_NAME);
    sh.appendRow(HEADERS);
    sh.setFrozenRows(1);
    props.setProperty('SHEET_ID', ss.getId());
    id = ss.getId();
  }
  Logger.log('Sheet ready: https://docs.google.com/spreadsheets/d/' + id);
  return id;
}

function doGet() {
  return HtmlService.createHtmlOutputFromFile('ideas')
    .setTitle('3 free UGC ideas from Grace With The Glow')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function clean_(v, max) {
  return String(v == null ? '' : v).replace(/[\u0000-\u001f]/g, ' ').trim().slice(0, max || 300);
}

/** Called from ideas.html with google.script.run. Returns {ok:true} or {ok:false, error:"..."}. */
function submit(form) {
  // hidden field real people never see; browsers do not autofill this name (Diaspo lesson 2026-11-05)
  if (clean_(form.zq_check)) { console.log('honeypot blocked'); return { ok: true }; }
  var d = {
    name: clean_(form.name, 120), brand: clean_(form.brand, 120), email: clean_(form.email, 160),
    link: clean_(form.link, 500), use: clean_(form.use, 200), notes: clean_(form.notes, 2000)
  };
  if (!d.name || !d.brand || !d.link || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) {
    return { ok: false, error: 'Please fill in your name, brand, a real email and the product link.' };
  }
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var id = PropertiesService.getScriptProperties().getProperty('SHEET_ID') || setup();
    SpreadsheetApp.openById(id).getSheetByName(SHEET_NAME)
      .appendRow([new Date(), d.name, d.brand, d.email, d.link, d.use, d.notes, 'New']);
  } finally { lock.releaseLock(); }

  MailApp.sendEmail({
    to: GRACE_EMAIL,
    replyTo: d.email,
    name: 'Portfolio form',
    subject: '3 free UGC ideas request: ' + d.brand,
    body: 'New request from your portfolio.\n\nName: ' + d.name + '\nBrand: ' + d.brand + '\nEmail: ' + d.email +
      '\nProduct: ' + d.link + '\nVideos for: ' + (d.use || 'not given') + '\nNotes: ' + (d.notes || 'none') +
      '\n\nHit Reply to answer them directly.'
  });
  MailApp.sendEmail({
    to: d.email,
    replyTo: GRACE_EMAIL,
    name: FROM_NAME,
    subject: 'Your 3 free UGC ideas are on the way',
    body: 'Hi ' + d.name + ',\n\nThanks for sending ' + d.brand + '. I will look at your product and email you 3 video ideas.' +
      '\n\nIf you want to add anything, just reply to this email.\n\nGrace\nGrace With The Glow\nhttps://www.tiktok.com/@shewiththeglow'
  });
  return { ok: true };
}
