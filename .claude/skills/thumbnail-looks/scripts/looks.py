#!/usr/bin/env python3
"""Thumbnail looks: a different, measured thumbnail or cover look for every video, on any channel.

A target is either a Day One job folder (jobs/<slug>, run from the Dayone-ai root; reads job.json "look") or a spec
file (any project, 16:9 or 9:16; every relative path in it resolves against the spec's own folder):

  {"name": "pbf-v2", "out": "cover.png", "size": "9:16", "top": "...", "big": "...", "badge": "",
   "image": "still.png" | "url": "https://...", "prompt", "stat", "stat_label", "focus", "accent",
   "pool": ["../*/cover.png"], "ledger": "../looks.json", "mark": null}

  looks.py render TARGET              3 candidate looks + a labelled sheet (_looks_sheet.png next to the target)
  looks.py render TARGET --band B     final image in band B, recorded in the target's ledger
  looks.py render TARGET --auto       final image in the best candidate (least alike, text fits)
  looks.py check TARGET [TARGET ...]  sameness vs the pool, band repeat and text fit; prints CHECK_PASS n/n
  looks.py control [--pool GLOB]      the old one-template thumbnails must all read as too alike
  looks.py selftest [--out DIR]       every band fits a real title at each size; an absurd one must fail
  looks.py bands                      list the bands and the sizes each one has

Day One job key: "look": {"band", "top", "big", "badge", "image", "image_mobile", "url", "crop_y", "focus",
"prompt", "stat", "stat_label", "accent"}; missing text falls back to thumb_top / thumb_big / thumb_badge, the image
to thumb_url, then the first web shot's url.
"""
import argparse, base64, colorsys, datetime, html, io, itertools, json, re, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

# Per size: canvas, sameness grid, the safe area every text box, badge and mark must sit in, and no-go boxes.
# 16:9: YouTube prints the video length over the bottom-right corner. 9:16: TikTok's profile grid shows only the
# middle 3:4 of a cover, and the feed puts its like/share rail down the right side.
SIZES = {
    "16:9": dict(w=1280, h=720, grid=(32, 18), safe=(0, 0, 1280, 720), nogo=[(1110, 650, 1280, 720)]),
    "9:16": dict(w=1080, h=1920, grid=(18, 32), safe=(0, 240, 1080, 1680), nogo=[(960, 1000, 1080, 1680)]),
}
CLOSE, LIMIT = 30.0, 0.30                    # RGB distance that counts as "same colour", max shared share
REPEAT_WINDOW = 5                            # a band may not repeat within the last 5 thumbnails
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo+Black&family=Anton&family=Bebas+Neue"
         "&family=DM+Serif+Display&family=Space+Grotesk:wght@700&family=JetBrains+Mono:wght@700"
         "&family=Permanent+Marker&family=Rubik:wght@900&display=swap")
ACCENTS = ["#ff4d2e", "#2f6bff", "#14b37d", "#ffb800", "#c13cff", "#ff2e7e", "#00a6c8", "#7a5cff"]

# ---------------------------------------------------------------- bands
# Each band is a familiar format described by its parts (the prompt pack's BAND rule): it reads at once and copies
# nobody's design. Classes: .fit = text that must fit its box (auto-shrinks to data-min px); .avoid = image areas,
# which no .fit text may cover (nor the .badge or .mark).
BASE_CSS = """*{box-sizing:border-box}html,body{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:{BG}}
.fit{overflow:hidden}.mark{position:absolute;width:76px;height:76px;border-radius:50%}.mark[src=""],.badge:empty{display:none!important}
.badge{position:absolute;font-family:'Archivo Black';font-size:34px;padding:8px 20px;border-radius:10px;
background:{ACCENT};color:{ON_ACCENT};white-space:nowrap}"""

BANDS = {
    "stack": dict(
        needs=[], note="three browser windows fanned in depth under a full-width title",
        html="""<div class="fit" data-min="64" style="position:absolute;left:56px;top:34px;width:1168px;height:110px;
font-family:'Space Grotesk';font-size:96px;line-height:1;color:{INK};white-space:nowrap">{BIG}</div>
<div class="fit" data-min="28" style="position:absolute;left:60px;top:148px;width:760px;height:46px;font-family:'Space Grotesk';
font-size:40px;color:{ACCENT};white-space:nowrap">{TOP}</div>
<div style="position:absolute;left:0;top:0;width:1280px;height:720px;perspective:1600px">
 <div class="avoid win" style="left:110px;top:300px;transform:rotateY(24deg) rotateZ(-2deg)"><i></i><img src="{IMG}" style="object-position:0% 60%"></div>
 <div class="avoid win" style="left:600px;top:290px;transform:rotateY(-22deg) rotateZ(2deg)"><i></i><img src="{IMG}" style="object-position:100% 30%"></div>
 <div class="avoid win" style="left:330px;top:250px;width:620px;height:430px;z-index:2"><i></i><img src="{IMG}" style="object-position:{FOCUS}"></div>
</div>
<div class="badge" style="right:56px;top:160px;transform:rotate(3deg)">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:40px;bottom:30px">""",
        css=""".win{position:absolute;width:560px;height:390px;border-radius:14px;overflow:hidden;background:#fff;
border:3px solid {INK};box-shadow:0 30px 60px rgba(0,0,0,.35)}.win i{display:block;height:30px;background:{INK}}
.win img{width:100%;height:calc(100% - 30px);object-fit:cover}"""),
    "split": dict(
        needs=["prompt"], note="what you type on the left, what you get on the right, title on a bottom plate",
        v="""<div style="position:absolute;left:0;top:0;width:1080px;height:820px;background:{INK}"></div>
<div class="fit" data-min="30" style="position:absolute;left:60px;top:262px;width:600px;height:60px;font-family:'Archivo Black';
font-size:44px;color:{ACCENT};white-space:nowrap">{TOP}</div>
<div class="fit" data-min="34" style="position:absolute;left:60px;top:350px;width:900px;height:400px;font-family:'JetBrains Mono';
font-size:62px;line-height:1.2;color:{PAPER}">&gt; {PROMPT}<span style="color:{ACCENT}">&#9608;</span></div>
<div class="avoid" style="position:absolute;left:0;top:820px;width:1080px;height:600px;overflow:hidden">
 <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:470px;top:760px;width:130px;height:130px;border-radius:50%;background:{ACCENT};
color:{ON_ACCENT};font:900 90px/130px Rubik;text-align:center;transform:rotate(90deg)">&#8594;</div>
<div style="position:absolute;left:0;top:1420px;width:1080px;height:500px;background:{ACCENT}"></div>
<div class="fit" data-min="80" style="position:absolute;left:60px;top:1436px;width:860px;height:240px;font-family:'Anton';
font-size:130px;line-height:1.05;color:{ON_ACCENT}">{BIG}</div>
<div class="badge" style="right:60px;top:256px;background:{PAPER};color:{INK}">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:860px;top:860px">""",
        html="""<div style="position:absolute;left:0;top:0;width:520px;height:560px;background:{INK}"></div>
<div class="fit" data-min="26" style="position:absolute;left:44px;top:40px;width:440px;height:300px;font-family:'JetBrains Mono';
font-size:44px;line-height:1.2;color:{PAPER}">&gt; {PROMPT}<span style="color:{ACCENT}">&#9608;</span></div>
<div class="fit" data-min="26" style="position:absolute;left:44px;top:420px;width:440px;height:100px;font-family:'Archivo Black';
font-size:40px;line-height:1.15;color:{ACCENT}">{TOP}</div>
<div class="avoid" style="position:absolute;left:520px;top:0;width:760px;height:560px;overflow:hidden">
 <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:468px;top:230px;width:104px;height:104px;border-radius:50%;background:{ACCENT};
color:{ON_ACCENT};font:900 70px/104px Rubik;text-align:center">&#8594;</div>
<div style="position:absolute;left:0;top:560px;width:1280px;height:160px;background:{ACCENT}"></div>
<div class="fit" data-min="64" style="position:absolute;left:44px;top:574px;width:1000px;height:132px;font-family:'Anton';
font-size:118px;line-height:1.1;color:{ON_ACCENT};white-space:nowrap">{BIG}</div>
<img class="mark" src="{MARK}" style="left:1080px;top:570px">
<div class="badge" style="right:40px;top:24px;background:{INK};color:{PAPER}">{BADGE}</div>"""),
    "loupe": dict(
        needs=[], note="the full page, dimmed, with a magnifier on the one thing that matters",
        v="""<img src="{IMG}" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;
object-position:{FOCUS};filter:brightness(.42) saturate(.7)">
<div style="position:absolute;left:50px;top:270px;width:980px;height:520px;background:{PAPER_PLATE};border-radius:8px"></div>
<div class="fit" data-min="28" style="position:absolute;left:90px;top:300px;width:900px;height:60px;font-family:'Archivo Black';
font-size:48px;color:{ACCENT};white-space:nowrap">{TOP}</div>
<div class="fit" data-min="80" style="position:absolute;left:90px;top:370px;width:900px;height:390px;font-family:'Archivo Black';
font-size:140px;line-height:1.02;color:{INK}">{BIG}</div>
<div class="avoid" style="position:absolute;left:170px;top:850px;width:700px;height:700px;border-radius:50%;
border:16px solid {ACCENT};background:url('{IMG}') {FOCUS}/{LOUPE9}px auto no-repeat #fff;box-shadow:0 0 0 12px rgba(0,0,0,.35)"></div>
<div style="position:absolute;left:770px;top:1500px;width:200px;height:52px;background:{ACCENT};border-radius:26px;transform:rotate(45deg)"></div>
<div class="badge" style="left:50px;top:1600px">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:860px;top:1592px">""",
        html="""<img src="{IMG}" style="position:absolute;left:0;top:0;width:1280px;height:720px;object-fit:cover;
object-position:0 0;filter:brightness(.42) saturate(.7)">
<div class="avoid" style="position:absolute;left:640px;top:110px;width:520px;height:520px;border-radius:50%;
border:14px solid {ACCENT};background:url('{IMG}') {FOCUS}/{LOUPE16}px auto no-repeat #fff;box-shadow:0 0 0 10px rgba(0,0,0,.35)"></div>
<div style="position:absolute;left:1035px;top:560px;width:180px;height:44px;background:{ACCENT};border-radius:22px;transform:rotate(45deg)"></div>
<div style="position:absolute;left:40px;top:150px;width:580px;height:330px;background:{PAPER_PLATE};border-radius:6px"></div>
<div class="fit" data-min="22" style="position:absolute;left:72px;top:176px;width:520px;height:44px;font-family:'Archivo Black';
font-size:36px;color:{ACCENT};white-space:nowrap">{TOP}</div>
<div class="fit" data-min="64" style="position:absolute;left:72px;top:228px;width:520px;height:230px;font-family:'Archivo Black';
font-size:100px;line-height:1.02;color:{INK}">{BIG}</div>
<div class="badge" style="left:40px;top:60px">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:44px;bottom:40px">"""),
    "cover": dict(
        needs=[], note="a magazine cover: the tool's name as the masthead, the result as the cover photo, one cover line",
        v="""<div class="fit" data-min="64" style="position:absolute;left:40px;top:250px;width:1000px;height:170px;font-family:'DM Serif Display';
font-size:160px;line-height:1;color:{INK};text-align:center;white-space:nowrap;letter-spacing:-2px">{TOP}</div>
<div style="position:absolute;left:40px;top:440px;width:1000px;height:8px;background:{INK}"></div>
<div style="position:absolute;left:40px;top:470px;width:1000px;height:1210px;overflow:hidden;border-radius:4px">
 <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:40px;top:1220px;width:820px;height:460px;background:{ACCENT}"></div>
<div class="fit" data-min="100" style="position:absolute;left:80px;top:1250px;width:740px;height:400px;font-family:'Anton';
font-size:150px;line-height:1;color:{ON_ACCENT}">{BIG}</div>
<div class="badge" style="right:70px;top:500px;background:{INK};color:{PAPER};border-radius:50%;width:190px;height:190px;
padding:0;display:flex;align-items:center;justify-content:center;text-align:center;white-space:normal;font-size:32px;line-height:1.05;transform:rotate(10deg)">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:70px;top:500px">""",
        html="""<div class="fit" data-min="60" style="position:absolute;left:40px;top:14px;width:1200px;height:150px;font-family:'DM Serif Display';
font-size:150px;line-height:1;color:{INK};text-align:center;white-space:nowrap;letter-spacing:-2px">{TOP}</div>
<div style="position:absolute;left:40px;top:168px;width:1200px;height:6px;background:{INK}"></div>
<div style="position:absolute;left:40px;top:190px;width:1200px;height:500px;overflow:hidden;border-radius:4px">
 <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:40px;top:470px;width:760px;height:220px;background:{ACCENT}"></div>
<div class="fit" data-min="60" style="position:absolute;left:70px;top:488px;width:700px;height:190px;font-family:'Anton';
font-size:96px;line-height:1;color:{ON_ACCENT}">{BIG}</div>
<div class="badge" style="right:60px;top:212px;background:{INK};color:{PAPER};border-radius:50%;width:150px;height:150px;
padding:0;display:flex;align-items:center;justify-content:center;text-align:center;white-space:normal;font-size:26px;line-height:1.05;transform:rotate(10deg)">{BADGE}</div>
<img class="mark" src="{MARK}" style="right:56px;top:400px">"""),
    "prompt": dict(
        needs=["prompt"], note="a dark chat box with the real prompt typed in, pointing at the result",
        html="""<div class="fit" data-min="60" style="position:absolute;left:56px;top:40px;width:1168px;height:120px;font-family:'Bebas Neue';
font-size:128px;line-height:1;color:{PAPER};white-space:nowrap">{BIG}</div>
<div style="position:absolute;left:56px;top:210px;width:520px;height:380px;border-radius:26px;background:#232323;border:2px solid #3a3a3a"></div>
<div class="fit" data-min="26" style="position:absolute;left:88px;top:240px;width:456px;height:320px;font-family:'JetBrains Mono';
font-size:40px;line-height:1.25;color:#f2f2f2">{PROMPT}<span style="color:{ACCENT}">&#9608;</span></div>
<div style="position:absolute;left:592px;top:350px;font:900 90px Rubik;color:{ACCENT}">&#8594;</div>
<div class="avoid" style="position:absolute;left:700px;top:190px;width:530px;height:420px;border-radius:20px;overflow:hidden;border:6px solid {ACCENT}">
 <img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div class="fit" data-min="22" style="position:absolute;left:58px;top:622px;width:620px;height:50px;font-family:'Space Grotesk';
font-size:40px;color:{ACCENT};white-space:nowrap">{TOP}</div>
<div class="badge" style="left:700px;top:626px">{BADGE}</div>
<img class="mark" src="{MARK}" style="right:50px;top:44px">"""),
    "number": dict(
        needs=["stat"], note="one giant number with its label, the screen as a pinned print",
        v="""<div class="fit" data-min="220" style="position:absolute;left:60px;top:250px;width:960px;height:520px;font-family:'Anton';
font-size:520px;line-height:1;color:{ON_ACCENT};white-space:nowrap">{STAT}</div>
<div class="fit" data-min="36" style="position:absolute;left:66px;top:780px;width:900px;height:80px;font-family:'Archivo Black';
font-size:64px;color:{ON_ACCENT};white-space:nowrap">{STAT_LABEL}</div>
<div class="avoid" style="position:absolute;left:120px;top:900px;width:840px;height:520px;background:#fff;padding:18px 18px 70px;
transform:rotate(-3deg);box-shadow:0 24px 50px rgba(0,0,0,.3)"><img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:0;top:1440px;width:1080px;height:480px;background:{INK}"></div>
<div class="fit" data-min="64" style="position:absolute;left:60px;top:1460px;width:860px;height:210px;font-family:'Archivo Black';
font-size:100px;line-height:1.05;color:{PAPER}">{BIG}</div>
<div class="badge" style="right:60px;top:256px;background:{INK};color:{PAPER}">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:60px;top:1350px">""",
        html="""<div class="fit" data-min="160" style="position:absolute;left:40px;top:20px;width:620px;height:400px;font-family:'Anton';
font-size:400px;line-height:1;color:{ON_ACCENT};white-space:nowrap">{STAT}</div>
<div class="fit" data-min="30" style="position:absolute;left:52px;top:420px;width:600px;height:70px;font-family:'Archivo Black';
font-size:56px;color:{ON_ACCENT};white-space:nowrap">{STAT_LABEL}</div>
<div class="avoid" style="position:absolute;left:690px;top:60px;width:540px;height:420px;background:#fff;padding:16px 16px 60px;
transform:rotate(4deg);box-shadow:0 24px 50px rgba(0,0,0,.3)"><img src="{IMG}" style="width:100%;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div style="position:absolute;left:0;top:540px;width:1280px;height:180px;background:{INK}"></div>
<div class="fit" data-min="56" style="position:absolute;left:52px;top:556px;width:1060px;height:150px;font-family:'Archivo Black';
font-size:84px;line-height:1.05;color:{PAPER}">{BIG}</div>
<div class="badge" style="right:40px;top:14px;background:{INK};color:{PAPER}">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:1150px;top:470px">"""),
    "phone": dict(
        needs=[], note="the result inside a phone on a two-tone field, title beside it",
        html="""<div style="position:absolute;left:0;top:0;width:760px;height:720px;background:{ACCENT}"></div>
<div class="fit" data-min="22" style="position:absolute;left:56px;top:60px;width:620px;height:44px;font-family:'Space Grotesk';
font-size:38px;color:{ON_ACCENT};white-space:nowrap">{TOP}</div>
<div class="fit" data-min="80" style="position:absolute;left:56px;top:120px;width:620px;height:420px;font-family:'Rubik';
font-size:118px;line-height:1;color:{ON_ACCENT}">{BIG}</div>
<div class="avoid" style="position:absolute;left:800px;top:40px;width:330px;height:660px;border-radius:52px;background:{INK};padding:16px;
box-shadow:-30px 30px 70px rgba(0,0,0,.35)"><img src="{IMG}" style="width:100%;height:100%;border-radius:38px;object-fit:cover;object-position:{FOCUS}"></div>
<div class="badge" style="left:56px;bottom:56px;background:{INK};color:{PAPER}">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:680px;top:24px">"""),
    "poster": dict(
        needs=[], note="a gig poster: the title huge in the middle, the screen as a strip of film across the bottom",
        v="""<div class="fit" data-min="28" style="position:absolute;left:180px;top:262px;width:720px;height:60px;font-family:'Space Grotesk';
font-size:48px;color:{ACCENT};text-align:center;white-space:nowrap;letter-spacing:6px">{TOP}</div>
<div class="fit" data-min="140" style="position:absolute;left:40px;top:340px;width:1000px;height:560px;font-family:'Bebas Neue';
font-size:300px;line-height:1;color:{PAPER};text-align:center">{BIG}</div>
<div class="avoid" style="position:absolute;left:-80px;top:1000px;width:1240px;height:440px;transform:rotate(-5deg);
background:{ACCENT};padding:22px 0;display:flex;gap:22px">
 <img src="{IMG}" style="flex:1;height:100%;object-fit:cover;object-position:0% 0%">
 <img src="{IMG}" style="flex:1;height:100%;object-fit:cover;object-position:{FOCUS}"></div>
<div class="badge" style="left:60px;top:1560px;transform:rotate(-4deg);background:{PAPER};color:{INK}">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:40px;top:250px">""",
        html="""<div class="fit" data-min="22" style="position:absolute;left:60px;top:40px;width:1160px;height:50px;font-family:'Space Grotesk';
font-size:42px;color:{ACCENT};text-align:center;white-space:nowrap;letter-spacing:6px">{TOP}</div>
<div class="fit" data-min="80" style="position:absolute;left:40px;top:100px;width:1200px;height:300px;font-family:'Bebas Neue';
font-size:260px;line-height:1;color:{PAPER};text-align:center;white-space:nowrap">{BIG}</div>
<div class="avoid" style="position:absolute;left:-60px;top:440px;width:1400px;height:250px;transform:rotate(-4deg);
background:{ACCENT};padding:18px 0;display:flex;gap:18px">
 <img src="{IMG}" style="flex:1;height:100%;object-fit:cover;object-position:0% 0%">
 <img src="{IMG}" style="flex:1;height:100%;object-fit:cover;object-position:{FOCUS}">
 <img src="{IMG}" style="flex:1;height:100%;object-fit:cover;object-position:100% 100%"></div>
<div class="badge" style="left:40px;bottom:24px;transform:rotate(-4deg);background:{PAPER};color:{INK}">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:40px;top:24px">"""),
    "note": dict(
        needs=[], note="the real page full-bleed with a taped sticky note written in marker",
        v="""<img src="{IMG}" style="position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;object-position:{FOCUS};filter:brightness(.8)">
<div style="position:absolute;left:90px;top:420px;width:900px;height:880px;background:{NOTE};transform:rotate(-3deg);
box-shadow:0 30px 60px rgba(0,0,0,.45)"></div>
<div style="position:absolute;left:430px;top:390px;width:220px;height:66px;background:rgba(255,255,255,.55);transform:rotate(3deg)"></div>
<div class="fit" data-min="28" style="position:absolute;left:150px;top:500px;width:780px;height:70px;font-family:'Permanent Marker';
font-size:56px;color:{ACCENT_DARK};white-space:nowrap;transform:rotate(-3deg)">{TOP}</div>
<div class="fit" data-min="110" style="position:absolute;left:150px;top:590px;width:780px;height:640px;font-family:'Permanent Marker';
font-size:150px;line-height:1.05;color:#1a1a1a;transform:rotate(-3deg)">{BIG}</div>
<div class="badge" style="left:100px;top:270px">{BADGE}</div>
<img class="mark" src="{MARK}" style="left:100px;top:1560px">""",
        html="""<img src="{IMG}" style="position:absolute;left:0;top:0;width:1280px;height:720px;object-fit:cover;object-position:{FOCUS};filter:brightness(.8)">
<div style="position:absolute;left:70px;top:90px;width:600px;height:520px;background:{NOTE};transform:rotate(-4deg);
box-shadow:0 30px 60px rgba(0,0,0,.45)"></div>
<div style="position:absolute;left:290px;top:62px;width:180px;height:56px;background:rgba(255,255,255,.55);transform:rotate(3deg)"></div>
<div class="fit" data-min="22" style="position:absolute;left:120px;top:150px;width:510px;height:52px;font-family:'Permanent Marker';
font-size:40px;color:{ACCENT_DARK};white-space:nowrap;transform:rotate(-4deg)">{TOP}</div>
<div class="fit" data-min="60" style="position:absolute;left:116px;top:212px;width:520px;height:330px;font-family:'Permanent Marker';
font-size:100px;line-height:1.05;color:#1a1a1a;transform:rotate(-4deg)">{BIG}</div>
<div class="badge" style="right:50px;top:50px">{BADGE}</div>
<img class="mark" src="{MARK}" style="right:60px;top:130px">"""),
}

# Each band's background: dark bands on ink, light bands on paper, the number band on the accent.
BAND_BG = {"stack": "paper", "split": "paper", "loupe": "ink", "cover": "paper", "prompt": "ink",
           "number": "accent", "phone": "paper", "poster": "ink", "note": "ink"}

FIT_JS = """([safe, nogo]) => {
 const out = [];
 const inter = (t, a) => !(t.right <= a.left || t.left >= a.right || t.bottom <= a.top || t.top >= a.bottom);
 const box = z => ({left: z[0], top: z[1], right: z[2], bottom: z[3]});
 const outside = r => r.left < safe[0] - 1 || r.top < safe[1] - 1 || r.right > safe[2] + 1 || r.bottom > safe[3] + 1
                      || nogo.some(z => inter(r, box(z)));
 for (const e of document.querySelectorAll('.badge,.mark')) {
  const r = e.getBoundingClientRect();
  if (r.width && outside(r)) out.push({text: e.className, size: 0, min: 0, overflow: false, offcanvas: true, covers_image: false});
 }
 const avoid = [...document.querySelectorAll('.avoid,.badge,.mark')].map(e => e.getBoundingClientRect());
 for (const e of document.querySelectorAll('.fit')) {
  const min = +e.dataset.min || 20; let fs = parseFloat(getComputedStyle(e).fontSize);
  const over = () => e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 1;
  while (over() && fs > min) { fs -= 2; e.style.fontSize = fs + 'px'; }
  // what shows = the text's box clipped to its own box (.fit hides overflow); tall glyph ascents don't count
  const r = document.createRange(); r.selectNodeContents(e); const tr = r.getBoundingClientRect(), b = e.getBoundingClientRect();
  const t = {left: Math.max(tr.left, b.left), top: Math.max(tr.top, b.top), right: Math.min(tr.right, b.right), bottom: Math.min(tr.bottom, b.bottom)};
  const off = outside(t);
  const hit = avoid.filter(a => a.width).some(a => inter(t, a));
  out.push({text: e.innerText.slice(0, 40), size: fs, min, overflow: over(), offcanvas: off, covers_image: hit});
 }
 return out;
}"""


# ---------------------------------------------------------------- colour
def hexrgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luma(rgb):
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def brand_accent(img):
    """The page's own brand colour: the most common saturated hue, as its median pixel. None for a grey page."""
    a = np.asarray(img.convert("RGB").resize((240, 135)), float) / 255
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in a.reshape(-1, 3)])
    m = (hsv[:, 1] > 0.45) & (hsv[:, 2] > 0.35)
    if m.mean() < 0.01:
        return None
    bins = (hsv[m, 0] * 24).astype(int) % 24
    top = np.bincount(bins, minlength=24).argmax()
    px = a.reshape(-1, 3)[m][bins == top]
    return "#%02x%02x%02x" % tuple(int(v * 255) for v in np.median(px, axis=0))


def busy_focus(img):
    """Where the page has the most detail, as a CSS position ("62% 30%"): the default framing and loupe target."""
    from PIL import ImageFilter
    g = img.convert("L").resize((320, 200)).filter(ImageFilter.FIND_EDGES)
    e = np.asarray(g.resize((8, 5), Image.BOX), float)
    e[0, :] *= 0.5                                    # the top row is usually the site's menu bar
    y, x = np.unravel_index(e.argmax(), e.shape)
    return f"{round((x + .5) / 8 * 100)}% {round((y + .5) / 5 * 100)}%"


def palette(accent, bg):
    ink, paper = "#141414", "#f4f1ea"
    on_accent = ink if luma(hexrgb(accent)) > 150 else "#ffffff"
    r, g, b = hexrgb(accent)
    note = "#%02x%02x%02x" % tuple(int(c + (255 - c) * 0.72) for c in (r, g, b))      # accent, light, for paper
    dark = "#%02x%02x%02x" % tuple(int(c * 0.55) for c in (r, g, b))
    return {"ACCENT": accent, "ON_ACCENT": on_accent, "INK": ink, "PAPER": paper, "PAPER_PLATE": paper,
            "BG": {"paper": paper, "ink": ink, "accent": accent}[bg], "NOTE": note, "ACCENT_DARK": dark}


# ---------------------------------------------------------------- browser
def browser():
    from playwright.sync_api import sync_playwright
    p = sync_playwright().start()
    exe = "/opt/pw-browsers/chromium" if Path("/opt/pw-browsers/chromium").exists() else None
    b = p.chromium.launch(executable_path=exe, args=["--disable-dev-shm-usage", "--disable-gpu"])
    return p, b


# Bot walls and cookie boxes: a thumbnail of "Verifying you are human" happened on the first test (canva.com, 2026-10-23).
WALL = re.compile(r"verifying you are human|verify you are human|just a moment|checking your browser|access denied|"
                  r"attention required|are you a robot|enable javascript and cookies|get past this page|ray ?id:", re.I)
HIDE_OVERLAYS = """() => { for (const e of document.querySelectorAll('body *')) { const cs = getComputedStyle(e);
  if ((cs.position === 'fixed' || cs.position === 'sticky') && /cookie|consent|privacy|we use/i.test(e.innerText || ''))
    e.style.setProperty('display', 'none', 'important'); } }"""


def capture(url, out, crop_y=0, mobile=False):
    p, b = browser()
    try:
        vp = {"viewport": {"width": 390, "height": 844}, "device_scale_factor": 2, "is_mobile": True} if mobile \
            else {"viewport": {"width": 1440, "height": 900}}
        pg = b.new_page(**vp)
        try:
            pg.goto(url, wait_until="networkidle", timeout=45000)
        except Exception:
            pg.goto(url, wait_until="load", timeout=45000)
        pg.wait_for_timeout(2500)
        text = pg.evaluate("document.body ? document.body.innerText.slice(0, 3000) : ''")
        if pg.query_selector("iframe[src*='challenges.cloudflare.com']"):   # the checkbox lives in this iframe
            text += " verify you are human"
        if WALL.search(text) and len(text) < 1500:
            sys.exit(f"{url} answered with a bot wall ({WALL.search(text).group(0)!r}); set look.url to another page "
                     f"or look.image to a saved picture of the result")
        pg.evaluate(HIDE_OVERLAYS)
        pg.evaluate(f"window.scrollTo(0,{0 if mobile else int(crop_y)})")
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(out))
    finally:
        b.close(); p.stop()


def data_uri(img_or_path, fmt="JPEG"):
    im = Image.open(img_or_path) if not isinstance(img_or_path, Image.Image) else img_or_path
    buf = io.BytesIO(); im.convert("RGB").save(buf, fmt, quality=90)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def page_html(band, fields, pal, size):
    spec = BANDS[band]
    v = size == "9:16"
    css = BASE_CSS + spec.get("v_css" if v else "css", "")
    body = spec["v" if v else "html"]
    fields = {**fields, "W": str(SIZES[size]["w"]), "H": str(SIZES[size]["h"])}
    for k, v in {**pal, **fields}.items():
        css, body = css.replace("{%s}" % k, v), body.replace("{%s}" % k, v)
    return (f"<!doctype html><html><head><meta charset=utf-8><link href='{FONTS}' rel=stylesheet>"
            f"<style>{css}</style></head><body>{body}</body></html>")


def render_png(pages, size="16:9"):
    """pages: list of (html, out_path). Returns the fit report for each."""
    p, b = browser()
    reports = []
    z = SIZES[size]
    try:
        pg = b.new_page(viewport={"width": z["w"], "height": z["h"]})
        for doc, out in pages:
            pg.set_content(doc, wait_until="networkidle")
            pg.evaluate("document.fonts.ready.then(()=>1)")
            pg.wait_for_timeout(300)
            rep = pg.evaluate(FIT_JS, [list(z["safe"]), [list(n) for n in z["nogo"]]])
            pg.screenshot(path=str(out))
            reports.append(rep)
    finally:
        b.close(); p.stop()
    return reports


def fit_ok(rep):
    return all(not (r["overflow"] or r["offcanvas"] or r["covers_image"]) for r in rep)


# ---------------------------------------------------------------- sameness
def cells(path_or_img, grid=(32, 18)):
    im = path_or_img if isinstance(path_or_img, Image.Image) else Image.open(path_or_img)
    return np.asarray(im.convert("RGB").resize(grid, Image.BOX), float)


def shared(a, b):
    """Share of the frame (32x18 cells, 18x32 for 9:16) whose average colour matches within 30 RGB units."""
    return float((np.linalg.norm(a - b, axis=2) < CLOSE).mean())


def closest(img, t):
    """The most alike earlier image in the target's pool, as (shared, name)."""
    grid = SIZES[t.size]["grid"]
    c = cells(img, grid)
    best = (0.0, None)
    for f in t.pool_files():
        if f.resolve() == t.out.resolve():
            continue
        cand = (shared(c, cells(f, grid)), f.parent.name if f.name in ("thumbnail.png", "cover.png") else f.stem)
        if cand[0] > best[0]:   # compare scores only: a tie at 0.0 against the (0.0, None) start used to crash
            best = cand
    return best


# ---------------------------------------------------------------- ledger
def ledger(path):
    return json.loads(path.read_text()) if path.exists() else {}


def recent_bands(led, before_slug=None, n=REPEAT_WINDOW):
    items = sorted(led.items(), key=lambda kv: kv[1]["date"])
    if before_slug in led:
        items = [kv for kv in items if kv[1]["date"] < led[before_slug]["date"]]
    return [v["band"] for _, v in items[-n:]]


# ---------------------------------------------------------------- targets
class Target:
    """One image to make: where it goes, what it says, what it is built from, what it must differ from."""

    def __init__(self, arg):
        p = Path(arg)
        if p.is_dir() and (p / "job.json").exists():          # a Day One job, run from the Dayone-ai root
            job = json.loads((p / "job.json").read_text())
            look = job.get("look", {})
            first_web = next((x["shot"].get("url") for x in job["segments"] if x["shot"]["type"] == "web"), None)
            self.name, self.dir, self.out, self.size = p.name, p, p / "thumbnail.png", "16:9"
            self.base, self.look = p, look
            self.pool, self.ledger_path = [str(Path("jobs/*/thumbnail.png").resolve())], Path("data/looks.json").resolve()
            self.mark = Path("brand/avatar.png") if Path("brand/avatar.png").exists() else None
            top, big, badge = job.get("thumb_top", job.get("tool", "")), job.get("thumb_big", ""), job.get("thumb_badge", "JUST LAUNCHED")
            self.url = look.get("url") or job.get("thumb_url") or first_web
            self.crop_y = look.get("crop_y", job.get("thumb_crop_y", 0))
        elif p.suffix == ".json" and p.exists():               # a spec, any project
            look = json.loads(p.read_text())
            self.base, self.look = p.parent, look
            self.name, self.dir = look.get("name", p.parent.name), p.parent
            self.out, self.size = p.parent / look.get("out", "thumbnail.png"), look.get("size", "16:9")
            self.pool = [str((p.parent / g).resolve()) for g in look.get("pool", [])]
            self.ledger_path = (p.parent / look.get("ledger", "looks.json")).resolve()
            self.mark = p.parent / look["mark"] if look.get("mark") else None
            top, big, badge = look.get("top", ""), look.get("big", ""), ""
            self.url, self.crop_y = look.get("url"), look.get("crop_y", 0)
        else:
            sys.exit(f"{arg}: not a Day One job folder (with job.json) or a look spec .json")
        if self.size not in SIZES:
            sys.exit(f"{arg}: size must be one of {list(SIZES)}")
        self.fields = {"TOP": look.get("top", top).upper(), "BIG": look.get("big", big),
                       "BADGE": look.get("badge", badge), "PROMPT": look.get("prompt", ""), "STAT": look.get("stat", ""),
                       "STAT_LABEL": look.get("stat_label", ""), "FOCUS": look.get("focus", "")}

    def pool_files(self):
        import glob
        return sorted({Path(f) for g in self.pool for f in glob.glob(g)})

    def image(self, mobile=False):
        """look.image (look.image_mobile for the phone band), else a capture of the url, cached next to the target."""
        image = (self.look.get("image_mobile") if mobile else None) or self.look.get("image")
        if image:
            return Image.open(self.base / image).convert("RGB")
        cap = self.dir / ("_look_cap_mobile.png" if mobile else "_look_cap.png")
        if not cap.exists():
            if not self.url:
                sys.exit(f"{self.name}: no image or url to build the look from")
            capture(self.url, cap, self.crop_y, mobile)
        return Image.open(cap).convert("RGB")


def eligible(fields, size="16:9"):
    return [b for b, s in BANDS.items() if all(fields.get(k.upper()) for k in s["needs"])
            and (size == "16:9" or "v" in s)]


def build(band, fields, img, accent, out, size="16:9", mark=None):
    pal = palette(accent, BAND_BG[band])
    f = {k: html.escape(v) for k, v in fields.items()}
    f.update(IMG=data_uri(img), MARK=data_uri(mark, "PNG") if mark and Path(mark).exists() else "")
    # the loupe magnifies, but never past 1.2x the source pixels (Ralph's overlay rule: past that it goes soft)
    f.update(LOUPE16=str(int(min(520 * 2.6, img.width * 1.2))), LOUPE9=str(int(min(700 * 3.0, img.width * 1.2))))
    return page_html(band, f, pal, size), out


def cmd_render(a):
    t = Target(a.target)
    fields = t.fields
    img = t.image()
    # a web page: frame its busiest part; a photo: the middle (its busiest part is often texture, like wood grain)
    fields["FOCUS"] = fields["FOCUS"] or ("50% 50%" if t.look.get("image") else busy_focus(img))
    led = ledger(t.ledger_path)
    recent = recent_bands(led, t.name if t.name in led else None)
    prev_accents = [v["accent"] for _, v in sorted(led.items(), key=lambda kv: kv[1]["date"])[-3:]]
    accent = t.look.get("accent") or brand_accent(img)
    near = lambda x, y: np.linalg.norm(np.subtract(hexrgb(x), hexrgb(y))) < 60
    if not t.look.get("accent") and (not accent or any(near(accent, p) for p in prev_accents)):
        accent = next(c for c in ACCENTS if not any(near(c, p) for p in prev_accents))   # the last 3 looks' colours stay unused
    ok_bands = [b for b in eligible(fields, t.size) if b not in recent]
    if a.band:
        if a.band not in BANDS:
            sys.exit(f"unknown band {a.band}; see `looks.py bands`")
        if a.band not in eligible(fields, t.size):
            sys.exit(f"band {a.band} needs look.{', look.'.join(BANDS[a.band]['needs']) or '?'} or has no {t.size} layout")
        if a.band in recent and not a.force:
            sys.exit(f"band {a.band} was used in the last {REPEAT_WINDOW} looks ({recent}); pick another")
        cands = [a.band]
    else:
        never = [b for b in ok_bands if b not in [v["band"] for v in led.values()]]
        cands = (never + [b for b in ok_bands if b not in never])[:a.candidates if not a.auto else len(ok_bands)]
    if not cands:
        sys.exit(f"no band left for {t.size}: every eligible one was used in the last {REPEAT_WINDOW}")
    pages = [build(b, fields, t.image(mobile=True) if b == "phone" else img, accent, t.dir / f"_look_{b}.png",
                   t.size, t.mark) for b in cands]
    reps = render_png(pages, t.size)
    rows = []
    for b, rep in zip(cands, reps):
        s, who = closest(t.dir / f"_look_{b}.png", t)
        rows.append(dict(band=b, fit=fit_ok(rep), shared=round(s, 3), closest=who, report=rep))
        print(f"{b:8s} fit={'ok' if fit_ok(rep) else 'FAIL'}  shared={s:.2f} with {who}  "
              f"title={next((r['size'] for r in rep if r['min'] >= 56), '-')}px")
    if a.band or a.auto:
        good = [r for r in rows if r["fit"] and r["shared"] < LIMIT]
        if not good:
            sys.exit("no candidate passes fit + sameness; shorten the title or set focus / image")
        pick = min(good, key=lambda r: r["shared"])
        Image.open(t.dir / f"_look_{pick['band']}.png").save(t.out)
        led[t.name] = dict(band=pick["band"], accent=accent, date=datetime.datetime.now().isoformat(timespec="seconds"),
                           fit=pick["fit"], shared=pick["shared"], closest=pick["closest"], size=t.size)
        t.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        t.ledger_path.write_text(json.dumps(led, indent=1) + "\n")
        print(f"THUMB {t.out} band={pick['band']} shared={pick['shared']:.2f}")
    else:
        sheet(t.dir, rows, size=t.size)


def sheet(jobdir, rows, prefix="_look_", size="16:9"):
    w, h, cols = (640, 360, 3) if size == "16:9" else (360, 640, 6)
    s = Image.new("RGB", (w * min(cols, len(rows)), (h + 40) * -(-len(rows) // cols)), "white")
    d = ImageDraw.Draw(s)
    for i, r in enumerate(rows):
        x, y = (i % cols) * w, (i // cols) * (h + 40)
        s.paste(Image.open(Path(jobdir) / f"{prefix}{r['band']}.png").resize((w, h)), (x, y))
        d.text((x + 10, y + h + 12), f"{r['band']}  fit {'ok' if r['fit'] else 'FAIL'}  shared {r['shared']:.2f}", fill="black")
    s.save(jobdir / "_looks_sheet.png")
    print("SHEET", jobdir / "_looks_sheet.png")


def cmd_check(a):
    passed = 0
    for arg in a.targets:
        t = Target(arg); errs = []
        led = ledger(t.ledger_path)
        if not t.out.exists():
            errs.append(f"no {t.out.name}")
        elif t.name not in led:
            errs.append(f"not made with looks.py (no entry in {t.ledger_path.name})")
        else:
            s, who = closest(t.out, t)
            if s >= LIMIT:
                errs.append(f"shares {s:.2f} of its frame with {who} (limit {LIMIT})")
            if led[t.name]["band"] in recent_bands(led, t.name):
                errs.append(f"band {led[t.name]['band']} repeats within the last {REPEAT_WINDOW}")
            if not led[t.name]["fit"]:
                errs.append("text did not fit")
        print(f"{t.name}: {'ok' if not errs else '; '.join(errs)}")
        passed += not errs
    print(f"CHECK_{'PASS' if passed == len(a.targets) else 'FAIL'} {passed}/{len(a.targets)}")
    sys.exit(0 if passed == len(a.targets) else 1)


def cmd_control(a):
    import glob
    led = ledger(Path(a.ledger))
    old = [Path(f) for f in sorted(glob.glob(a.pool)) if Path(f).parent.name not in led]
    C = [cells(f) for f in old]
    pairs = [shared(C[i], C[j]) for i, j in itertools.combinations(range(len(C)), 2)]
    flagged = sum(p >= LIMIT for p in pairs)
    print(f"{len(old)} template thumbnails, {flagged}/{len(pairs)} pairs at or over {LIMIT} shared "
          f"(lowest {min(pairs):.2f})")
    ok = len(pairs) >= 10 and flagged / len(pairs) >= 0.95
    print("CONTROL_OK" if ok else "CONTROL_FAIL")
    sys.exit(0 if ok else 1)


def cmd_selftest(a):
    from tempfile import TemporaryDirectory
    g = np.zeros((900, 1440, 3), np.uint8)
    g[..., 0] = np.linspace(30, 220, 1440)[None, :]; g[..., 2] = np.linspace(200, 40, 900)[:, None]
    g[200:500, 300:900] = (250, 250, 250); g[560:640, 300:1200] = (40, 40, 40)
    img = Image.fromarray(g)
    mark = Path(a.mark) if a.mark else None
    real = dict(TOP="HIGGSFIELD CONTENT FACTORY", BIG="1 LINE → FULL VIDEO", BADGE="JUST LAUNCHED",
                PROMPT="What if cats ran the morning news? Make it a 60 second faceless video", STAT="55",
                STAT_LABEL="LANGUAGES", FOCUS="50% 20%")
    absurd = dict(real, BIG="THIS TITLE IS FAR TOO LONG TO EVER FIT ON ANY THUMBNAIL AT A SIZE A PHONE CAN READ OK")
    ok, counts = True, {}
    with TemporaryDirectory() as tmp:
        d = Path(a.out or tmp)
        for size in SIZES:
            bands = [b for b in BANDS if size == "16:9" or "v" in BANDS[b]]
            counts[size] = len(bands)
            for name, fields, want in (("real", real, True), ("absurd", absurd, False)):
                tag = f"{name}{size.replace(':', 'x')}_"
                pages = [build(b, fields, img, "#2f6bff", d / f"{tag}{b}.png", size, mark) for b in bands]
                for b, rep in zip(bands, render_png(pages, size)):
                    good = fit_ok(rep)
                    bad = [r for r in rep if r["overflow"] or r["offcanvas"] or r["covers_image"]]
                    print(f"{size} {name:6s} {b:8s} fit={'ok' if good else 'FAIL'} {bad[:2] if bad and want else ''}")
                    ok &= good if want else (not good)
            if a.out:   # a sheet per size with the real title, to look at
                sheet(d, [dict(band=b, fit=True, shared=0.0) for b in bands], prefix=f"real{size.replace(':', 'x')}_", size=size)
                (d / "_looks_sheet.png").rename(d / f"sheet_{size.replace(':', 'x')}.png")
    print(("SELFTEST_OK " if ok else "SELFTEST_FAIL ") + " ".join(f"{k}={v}" for k, v in counts.items()))
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render"); r.add_argument("target"); r.add_argument("--band"); r.add_argument("--auto", action="store_true")
    r.add_argument("--candidates", type=int, default=3); r.add_argument("--force", action="store_true")
    c = sub.add_parser("check"); c.add_argument("targets", nargs="+")
    k = sub.add_parser("control"); k.add_argument("--pool", default="jobs/*/thumbnail.png"); k.add_argument("--ledger", default="data/looks.json")
    sub.add_parser("bands")
    t = sub.add_parser("selftest"); t.add_argument("--out", help="keep the renders here and write a sheet per size")
    t.add_argument("--mark", default="brand/avatar.png" if Path("brand/avatar.png").exists() else None)
    a = ap.parse_args()
    if a.cmd == "bands":
        for b, s in BANDS.items():
            sizes = "16:9" + (" 9:16" if "v" in s else "")
            print(f"{b:8s} {sizes:10s} needs={','.join(s['needs']) or '-':12s} {s['note']}")
        return
    {"render": cmd_render, "check": cmd_check, "control": cmd_control, "selftest": cmd_selftest}[a.cmd](a)


if __name__ == "__main__":
    main()
