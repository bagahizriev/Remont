# Разработка

## Локальный запуск

### 1-й терминал (веб-приложение)

```bash
uvicorn main:app --reload
```

или

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2-й терминал (сборка CSS)

```bash
npm run watch
```

### 3-й терминал (Telegram бот)

```bash
python bot.py
```

## Настройка для разработки

1. Создайте файл `.env` в корне проекта:
```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789
```

2. Установите зависимости:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm install
```

# Деплой на сервер

## Автоматический деплой (рекомендуется)

Используйте скрипт `deploy.sh` для автоматического деплоя:

1. Отредактируйте `deploy.sh` и укажите:
   - `PROJECT_REPO` - URL вашего Git репозитория
   - `DOMAIN` - ваш домен
   - `BOT_TOKEN` - токен Telegram бота
   - `ADMIN_IDS` - ваши Telegram ID
   - `SSL_EMAIL` - email для Let's Encrypt

2. Запустите на сервере:
   ```bash
   sudo bash deploy.sh
   ```

Скрипт автоматически настроит всё необходимое.

## Ручной деплой

Подробные инструкции по ручному деплою без Docker см. в файле [DEPLOYMENT.md](DEPLOYMENT.md)

### Быстрый старт (для тестирования)

1. Создайте `.env` файл с переменными:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_IDS=123456789
   ```

2. Запустите `./start.sh` для веб-приложения
3. Запустите `./start-bot.sh` для Telegram бота

Или используйте systemd сервисы (см. DEPLOYMENT.md)


