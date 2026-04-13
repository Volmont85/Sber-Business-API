sber-overnight-bot/

app/
    main.py
    config.py
    sber_client.py
    overnight_service.py
    storage.py
    telegram_logger.py

requirements.txt
Dockerfile
README.md


17:00 МСК
   ↓
cron запускает job
   ↓
Redis проверяет запуск сегодня
   ↓
OAuth token
   ↓
проверка баланса
   ↓
если > 1 300 000
   ↓
amount = balance − 300 000
   ↓
получение автокотировки
   ↓
создание заявления overnight
   ↓
Telegram уведомление
