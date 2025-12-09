from flask import Flask, jsonify
import requests

app = Flask(__name__)

# ==========================================
# ⚙️ CONFIGURACIÓN DIRECTA (Edita esto aquí)
# ==========================================

# Pon tu ID numérica aquí (sin comillas)
OWNER_ID = 2987464390 

# Pon tu cookie completa aquí (dentro de las comillas)
ROBLOX_COOKIE = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhsKBGR1aWQSEzE5NTQ0NzA3Nzg2NjgyNDM5NjUoAw.iq57vHSIH1sPGqhJA91ac8Q74amgXDUxghhWdj77bPCUYOt3wJAbCZ7sgUzusZjvCaEXIDSa2MUsmw3ifKmsl6OlODnTiJ9iMgwpJ01yUNzX6yQD3E0ntZMgksSBcQ1MlD1qXgvOXIVQCe6Rs5fQY6nfgnldP5xrORyxIoV2WzO2352sdhvTPremArYLMfVWznUOKcIRkaa9QqJKOJmeou-bsOdokyrur1l7C0ZCYYwwrADxiLgXDMmuNbZ6L_MgJTn2H-UbHruc3uUvBTw2yb9ryxk-0hx4vpLhfp339Ydrsq0cMOSzPJPE-mQOc127Rg43MGJURG3T9DcKrntmoSFZgWUw67BpvSZwmfJYejYj0DnZ26bXOcfnBYNq-djd0yFAWDzWIHXb_ot9p8p7VhUEStHNm6UCVNhYPwWm32KWEv5QK7JRYGUfy31SLDb62_JJyteFP4fJqCPHreIpzbXieqn1yFdC7y0zi7OzCqmsbyDm9EqnTI5mf6T8THAf8pTgwbNzYOhldUHE7BjJsWpvbpNfuLPbvxAPsInSBGrPwDtA9N9sU1oOdIwx-XgwkdJhD9J8_4GGeTsKfIcbPuyqQW8sSExa6Kl_CKYiNfhdlGT-7EopUcvIJvSpzr-mgmYlVs_uKB1LDa0c9YIOf3xbmXZasL8_TXlFjJ0d11Iow-czbeFeRuwz11Nn3rb3dQ1FIuTGt242ys4yEOzHrrJrPIA4arETDbvc7hlB0-6WaFO0RDOWPgG_ewevnAqNM5Hemfmdg5aZh489tgMBXlotyo8" 

# ==========================================

@app.route('/')
def home():
    return "API Sniper Funcionando."

@app.route('/check')
def check_status():
    try:
        url = "https://presence.roblox.com/v1/presence/users"
        payload = {"userIds": [OWNER_ID], "minimal": False}
        headers = {
            "Cookie": f".ROBLOSECURITY={ROBLOX_COOKIE}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            user_presence = data['userPresences'][0]
            
            # Tipo 2 = En Juego
            if user_presence['userPresenceType'] == 2:
                place_id = user_presence.get('placeId')
                job_id = user_presence.get('gameId')
                
                if job_id:
                    return jsonify({
                        "action": "teleport",
                        "placeId": place_id,
                        "jobId": job_id,
                        "status": "Playing"
                    })
                else:
                    return jsonify({"action": "stay", "status": "Privado/JoinsOff"})
            else:
                return jsonify({"action": "stay", "status": "Offline/Web"})
        else:
            return jsonify({"error": "Error conectando a Roblox API", "code": response.status_code})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)