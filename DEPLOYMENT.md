# Инструкция по деплою проекта Remont

## Требования

- Python 3.8+
- Node.js 14+ и npm
- Система на базе Linux (Ubuntu/Debian рекомендуется)

## Быстрый деплой (автоматический скрипт)

Для автоматического деплоя используйте скрипт `deploy.sh`:

1. Отредактируйте скрипт `deploy.sh` и укажите:
    - `PROJECT_REPO` - URL вашего Git репозитория
    - `DOMAIN` - ваш домен
    - `BOT_TOKEN` - токен Telegram бота
    - `ADMIN_IDS` - ваши Telegram ID (через запятую)
    - `SSL_EMAIL` - ваш email для Let's Encrypt

2. Запустите скрипт на сервере:
    ```bash
    sudo bash deploy.sh
    ```

Скрипт автоматически:

- Установит все зависимости
- Создаст пользователя и директории
- Клонирует проект из репозитория
- Настроит виртуальное окружение
- Установит зависимости Python и Node.js
- Соберёт Tailwind CSS
- Создаст .env файл
- Настроит systemd сервисы для веб-приложения и бота
- Настроит Nginx как reverse proxy
- Установит SSL сертификат через Let's Encrypt

## Ручной деплой

Если вы предпочитаете деплоить вручную, следуйте инструкциям ниже.

## Подготовка к деплою

### 1. Установка зависимостей на сервере

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка Node.js и npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Клонирование проекта

```bash
cd /opt  # или другая директория по вашему выбору
git clone <your-repo-url> Remont
cd Remont
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
nano .env
```

Добавьте следующие переменные:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321
```

Где:

- `BOT_TOKEN` - токен вашего Telegram бота (получите у @BotFather)
- `ADMIN_IDS` - список ID администраторов через запятую (узнайте свой ID у @userinfobot)

### 4. Установка зависимостей проекта

```bash
# Создание виртуального окружения Python
python3 -m venv venv
source venv/bin/activate

# Установка Python зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Установка Node.js зависимостей
npm install

# Сборка Tailwind CSS
npm run build
```

## Варианты запуска

### Вариант 1: Запуск через systemd (рекомендуется)

#### Настройка systemd сервисов

1. Отредактируйте файлы `remont-web.service` и `remont-bot.service`:
    - Замените `/path/to/Remont` на реальный путь к проекту
    - При необходимости измените `User=www-data` на вашего пользователя

2. Скопируйте сервисы в systemd:

```bash
sudo cp remont-web.service /etc/systemd/system/
sudo cp remont-bot.service /etc/systemd/system/
```

3. Перезагрузите systemd и запустите сервисы:

```bash
sudo systemctl daemon-reload
sudo systemctl enable remont-web.service
sudo systemctl enable remont-bot.service
sudo systemctl start remont-web.service
sudo systemctl start remont-bot.service
```

4. Проверка статуса:

```bash
sudo systemctl status remont-web.service
sudo systemctl status remont-bot.service
```

5. Просмотр логов:

```bash
sudo journalctl -u remont-web.service -f
sudo journalctl -u remont-bot.service -f
```

### Вариант 2: Запуск через скрипты

Сделайте скрипты исполняемыми:

```bash
chmod +x start.sh start-bot.sh
```

Запуск веб-приложения:

```bash
./start.sh
```

В отдельном терминале или через screen/tmux запустите бота:

```bash
./start-bot.sh
```

### Вариант 3: Запуск через screen/tmux

```bash
# Установка screen (если не установлен)
sudo apt install screen -y

# Запуск веб-приложения
screen -S remont-web
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
# Нажмите Ctrl+A, затем D для отсоединения

# Запуск бота
screen -S remont-bot
source venv/bin/activate
python bot.py
# Нажмите Ctrl+A, затем D для отсоединения
```

## Настройка веб-сервера (опционально)

### Nginx как reverse proxy

Установите Nginx:

```bash
sudo apt install nginx -y
```

Создайте конфигурацию:

```bash
sudo nano /etc/nginx/sites-available/remont
```

Добавьте:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/Remont/static;
    }
}
```

Активируйте конфигурацию:

```bash
sudo ln -s /etc/nginx/sites-available/remont /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Настройка SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Обновление приложения

```bash
cd /path/to/Remont
git pull
source venv/bin/activate
pip install -r requirements.txt
npm install
npm run build

# Если используете systemd
sudo systemctl restart remont-web.service
sudo systemctl restart remont-bot.service
```

## Проверка работоспособности

1. Проверьте, что веб-приложение доступно:

    ```bash
    curl http://localhost:8000
    ```

2. Проверьте, что бот отвечает на команды в Telegram

3. Проверьте логи на наличие ошибок

## Резервное копирование

Рекомендуется настроить автоматическое резервное копирование базы данных:

```bash
# Создайте скрипт для бэкапа
nano /path/to/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp /path/to/Remont/applications.db "$BACKUP_DIR/backup_$DATE.db"
# Удаление старых бэкапов (старше 30 дней)
find "$BACKUP_DIR" -name "backup_*.db" -mtime +30 -delete
```

Добавьте в crontab:

```bash
crontab -e
# Добавьте строку для ежедневного бэкапа в 2:00
0 2 * * * /path/to/backup.sh
```

## Устранение неполадок

### Приложение не запускается

1. Проверьте логи: `sudo journalctl -u remont-web.service -n 50`
2. Убедитесь, что порт 8000 свободен: `sudo netstat -tulpn | grep 8000`
3. Проверьте права доступа к файлам и директориям

### Бот не работает

1. Проверьте логи: `sudo journalctl -u remont-bot.service -n 50`
2. Убедитесь, что `.env` файл содержит правильный `BOT_TOKEN`
3. Проверьте, что бот запущен в Telegram (@BotFather)

### Проблемы с базой данных

1. Убедитесь, что у процесса есть права на запись в директорию проекта
2. Проверьте, что файл `applications.db` существует и доступен
