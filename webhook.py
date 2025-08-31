import os
from flask import Flask, request, jsonify
from db import mark_user_paid
import hmac, hashlib

app = Flask(__name__)
LEMON_SECRET = os.getenv("LEMON_WEBHOOK_SECRET")

def verify_lemon(payload, signature):
    mac = hmac.new(LEMON_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)

@app.route("/webhook", methods=["POST"])
def lemon_webhook():
    sig = request.headers.get("x-ls-signature", "")
    body = request.get_data()
    if not verify_lemon(body, sig):
        return jsonify({"ok": False}), 400
    data = request.json
    ev = data.get("event", {})
    if ev.get("type") in ["order.paid", "checkout.completed"]:
        metadata = ev.get("data", {}).get("metadata", {})
        telegram_id = metadata.get("telegram_id")
        email = metadata.get("email")
        if telegram_id:
            mark_user_paid(telegram_id, email=email)
    return jsonify({"ok": True})
