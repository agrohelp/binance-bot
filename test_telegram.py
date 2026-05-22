import requests

TOKEN = "8278485823:AAFCrIQf59CMyCkfWXHsib9p-Zfo2OtoH0U"
CHAT_ID = 8851570955

url = f"https://api.telegram.org/bot{TOKEN}/getMe"

r = requests.get(url)

print("Status:", r.status_code)
print("Odpowiedź:", r.text)
