import requests

TOKEN = "8278485823:AAFCrIQf59CMyCkfWXHsib9p-Zfo2OtoH0U"
CHAT_ID = 8851570955

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "🔥 Telegram działa! Możesz odpalać bota!"
}

r = requests.post(url, json=payload)

print("Status:", r.status_code)
print("Odpowiedź:", r.text)
