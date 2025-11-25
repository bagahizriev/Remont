# Быстрый старт: Автоматический деплой

## Подготовка

1. **Откройте файл `deploy.sh`** и отредактируйте следующие переменные:

```bash
PROJECT_REPO="https://github.com/ваш-username/Remont.git"  # URL вашего репозитория
DOMAIN="your-domain.com"                                    # Ваш домен
BOT_TOKEN="your_telegram_bot_token_here"                   # Токен от @BotFather
ADMIN_IDS="123456789"                                       # Ваш Telegram ID (узнайте у @userinfobot)
SSL_EMAIL="your-email@example.com"                         # Email для Let's Encrypt
```

2. **Убедитесь, что:**
   - Домен указывает на IP вашего сервера (A-запись)
   - У вас есть доступ к серверу с правами sudo
   - Telegram бот создан и у вас есть токен

## Запуск деплоя

На сервере выполните:

```bash
# Скачайте скрипт (если ещё не скачан)
# Или скопируйте его на сервер

# Сделайте скрипт исполняемым
chmod +x deploy.sh

# Запустите деплой
sudo bash deploy.sh
```

## Что делает скрипт

1. ✅ Обновляет систему и устанавливает зависимости
2. ✅ Создаёт пользователя `remont`
3. ✅ Клонирует проект из репозитория
4. ✅ Создаёт виртуальное окружение Python
5. ✅ Устанавливает зависимости (Python и Node.js)
6. ✅ Собирает Tailwind CSS
7. ✅ Создаёт `.env` файл с вашими настройками
8. ✅ Настраивает systemd сервисы для веб-приложения и бота
9. ✅ Настраивает Nginx как reverse proxy
10. ✅ Устанавливает SSL сертификат через Let's Encrypt

## После деплоя

Проверьте статус сервисов:

```bash
sudo systemctl status remont-web
sudo systemctl status remont-bot
```

Просмотр логов:

```bash
sudo journalctl -u remont-web -f
sudo journalctl -u remont-bot -f
```

Откройте ваш сайт в браузере: `https://your-domain.com`

## Обновление проекта

Для обновления проекта после изменений:

```bash
cd /srv/remont
sudo -u remont git pull
sudo -u remont /srv/remont/venv/bin/pip install -r requirements.txt
sudo -u remont npm install
sudo -u remont npm run build
sudo systemctl restart remont-web
sudo systemctl restart remont-bot
```

## Устранение проблем

### Сервисы не запускаются

```bash
# Проверьте логи
sudo journalctl -u remont-web -n 50
sudo journalctl -u remont-bot -n 50

# Проверьте .env файл
sudo cat /srv/remont/.env
```

### SSL не установился

```bash
# Попробуйте установить вручную
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### Бот не отвечает

1. Проверьте, что `BOT_TOKEN` правильный в `.env`
2. Проверьте, что бот запущен: `sudo systemctl status remont-bot`
3. Проверьте логи: `sudo journalctl -u remont-bot -f`

