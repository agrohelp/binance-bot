# Binance EMA 15m Trading Bot (Python)

## Opis projektu

Projekt to prosty bot tradingowy w Pythonie, który pobiera dane świecowe 15‑minutowe z Binance, oblicza średnie kroczące EMA (szybką i wolną), generuje sygnały BUY/SELL/WAIT oraz wysyła powiadomienia e‑mail przy zmianie sygnału. Bot działa w pętli i odświeża dane co 1 minutę.

## Funkcje

- Pobieranie świec 15m z publicznego API Binance
- Obliczanie EMA 7 i EMA 25
- Generowanie sygnałów BUY / SELL / WAIT
- Wysyłanie powiadomień Gmail przy zmianie sygnału
- Przechowywanie danych w pliku `.env`
- Działanie non stop w pętli co 60 sekund

## Struktura projektu

binance_bot/
│
├── main.py
├── strategy_ema.py
├── notify.py
├── .env
├── .gitignore
└── README.md

## Wymagania

Python 3.10 lub nowszy  
Biblioteki:

pip install requests python-dotenv

Kod

## Konfiguracja pliku .env

Utwórz plik `.env` w katalogu projektu i dodaj:

BINANCE_API_KEY=twoj_klucz
BINANCE_SECRET_KEY=twoj_klucz

GMAIL_USER=twoj_email@gmail.com
GMAIL_PASS=haslo_aplikacji
TO_EMAIL=twoj_email@gmail.com

Kod

Hasło Gmail to hasło aplikacji generowane w panelu Google (App Passwords).

## Uruchomienie bota

W terminalu:

python main.py

Kod

Bot będzie:

- pobierał świeczki 15m
- aktualizował EMA
- wyświetlał sygnał w konsoli
- wysyłał e‑mail przy zmianie sygnału

## Bezpieczeństwo

- Plik `.env` musi być dodany do `.gitignore`
- Nie commitować kluczy API ani haseł
- Repozytorium może być publiczne, jeśli `.env` jest ignorowany

## Rozszerzenia (opcjonalnie)

- Dodanie RSI
- Dodanie MACD
- Powiadomienia Telegram
- Paper trading
- Automatyczne zlecenia Binance