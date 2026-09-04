from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

API_KEY = "AIzaSyAe_aOVT1gSfmHKBrorFvX4fRwN5nODXVA"

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
        "clientType": "CLIENT_TYPE_ANDROID"
    }
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        data = r.json()
        return data.get("idToken")
    return None

def set_king_rank(id_token):
    url = "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating1"
    rating_data = {
        "cars": 100000, "car_fix": 100000, "car_collided": 100000,
        "car_exchange": 100000, "car_trade": 100000, "car_wash": 100000,
        "slicer_cut": 100000, "drift_max": 100000, "drift": 100000,
        "cargo": 100000, "delivery": 100000, "taxi": 100000,
        "levels": 100000, "gifts": 100000, "fuel": 100000,
        "offroad": 100000, "speed_banner": 100000, "reactions": 100000,
        "police": 100000, "run": 100000, "real_estate": 100000,
        "t_distance": 100000, "treasure": 100000, "block_post": 100000,
        "push_ups": 100000, "burnt_tire": 100000, "passanger_distance": 100000,
        "time": 10000000000, "race_win": 3000
    }
    body = {"data": json.dumps({"RatingData": rating_data})}
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json",
        "User-Agent": "UnityPlayer/2022.3.62f2 (UnityWebRequest/1.0, libcurl/8.10.1-DEV)"
    }
    r = requests.post(url, json=body, headers=headers)
    return r.status_code, r.text

@app.route('/king_rank', methods=['POST'])
def king_rank():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"ok": False, "message": "Email/пароль обязательны"}), 400
    token = login(email, password)
    if not token:
        return jsonify({"ok": False, "message": "Ошибка авторизации"}), 401
    status, text = set_king_rank(token)
    if status == 200:
        return jsonify({"ok": True, "message": "Кинг ранг установлен!"})
    else:
        return jsonify({"ok": False, "message": f"Ошибка: {text[:200]}"}), status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
