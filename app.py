from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# CONFIGURACIÓN: El servidor buscará estas variables en el entorno de Render
OWNER_ID = os.environ.get('OWNER_ID')
ROBLOX_COOKIE = os.environ.get('ROBLOX_COOKIE')

@app.route('/')
def home():
    return "API de Vigilancia Activa. Usa /check para consultar."

@app.route('/check')
def check_status():
    if not ROBLOX_COOKIE or not OWNER_ID:
        return jsonify({"error": "Faltan variables de entorno (Cookie o ID)"})

    try:
        # 1. Consultar presencia del Owner
        url = "https://presence.roblox.com/v1/presence/users"
        payload = {"userIds": [int(OWNER_ID)], "minimal": False}
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
                job_id = user_presence.get('gameId') # ID del Servidor
                
                if job_id:
                    # Si hay JobID, los joins están ON y es público
                    return jsonify({
                        "action": "teleport",
                        "placeId": place_id,
                        "jobId": job_id,
                        "status": "Playing"
                    })
                else:
                    # Jugando pero joins OFF o Privado
                    return jsonify({"action": "stay", "status": "Privado/JoinsOff"})
            else:
                return jsonify({"action": "stay", "status": "Offline/Web"})
        else:
            return jsonify({"error": "Error conectando a Roblox API"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)