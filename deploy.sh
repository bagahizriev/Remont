#!/bin/bash

set -e

# ---------------------------
# Конфигурация проекта
# ---------------------------
PROJECT_USER="remont"
PROJECT_DIR="/srv/remont"
PROJECT_REPO="https://github.com/bagahizriev/Remont.git"  # ЗАМЕНИТЕ НА ВАШ РЕПОЗИТОРИЙ
DOMAIN="your-domain.com"  # ЗАМЕНИТЕ НА ВАШ ДОМЕН
PYTHON_VERSION="3.12"
VENV_DIR="$PROJECT_DIR/venv"
BOT_TOKEN="your_telegram_bot_token_here"  # ЗАМЕНИТЕ НА ВАШ ТОКЕН
ADMIN_IDS="123456789"  # ЗАМЕНИТЕ НА ВАШИ TELEGRAM ID (через запятую)
SSL_EMAIL="your-email@example.com"  # ЗАМЕНИТЕ НА ВАШ EMAIL

# ---------------------------
# Обновление системы
# ---------------------------
echo "Обновляем пакеты..."
sudo apt update && sudo apt upgrade -y

# Устанавливаем необходимые пакеты
sudo apt install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv python$PYTHON_VERSION-dev \
                    build-essential nginx git curl certbot python3-certbot-nginx nodejs npm

# ---------------------------
# Создание пользователя
# ---------------------------
if id "$PROJECT_USER" &>/dev/null; then
    echo "Пользователь $PROJECT_USER уже существует"
else
    echo "Создаём пользователя $PROJECT_USER..."
    sudo adduser --disabled-password --gecos "" $PROJECT_USER
fi

# ---------------------------
# Создание директории проекта
# ---------------------------
echo "Создаём директорию проекта..."
sudo mkdir -p $PROJECT_DIR
sudo chown -R $PROJECT_USER:$PROJECT_USER $PROJECT_DIR

# ---------------------------
# Клонирование проекта
# ---------------------------
if [ -n "$PROJECT_REPO" ] && [ ! -d "$PROJECT_DIR/.git" ]; then
    echo "Клонируем проект из репозитория..."
    sudo -u $PROJECT_USER git clone $PROJECT_REPO $PROJECT_DIR
elif [ -n "$PROJECT_REPO" ]; then
    echo "Проект уже клонирован. Обновляем из репозитория..."
    sudo -u $PROJECT_USER git -C $PROJECT_DIR pull
fi

# ---------------------------
# Настройка виртуального окружения
# ---------------------------
if [ ! -d "$VENV_DIR" ]; then
    echo "Создаём виртуальное окружение..."
    sudo -u $PROJECT_USER python$PYTHON_VERSION -m venv $VENV_DIR
fi

echo "Обновляем pip..."
sudo -u $PROJECT_USER $VENV_DIR/bin/pip install --upgrade pip

# Установка зависимостей
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "Устанавливаем зависимости..."
    sudo -u $PROJECT_USER $VENV_DIR/bin/pip install -r $PROJECT_DIR/requirements.txt
fi

# ---------------------------
# Настройка .env
# ---------------------------
ENV_FILE="$PROJECT_DIR/.env"
echo "Создаём .env файл..."

sudo -u $PROJECT_USER tee $ENV_FILE > /dev/null <<EOL
BOT_TOKEN=$BOT_TOKEN
ADMIN_IDS=$ADMIN_IDS
EOL

# ---------------------------
# Установка npm-зависимостей и сборка Tailwind CSS
# ---------------------------
echo "Устанавливаем npm-зависимости и собираем Tailwind CSS..."
cd $PROJECT_DIR
sudo -u $PROJECT_USER npm install
sudo -u $PROJECT_USER npm run build

# ---------------------------
# Настройка прав доступа
# ---------------------------
echo "Настраиваем права доступа..."
sudo chmod -R 755 $PROJECT_DIR/static
sudo chmod -R 755 $PROJECT_DIR/templates

# Создаём директорию для базы данных (если нужно)
sudo -u $PROJECT_USER touch $PROJECT_DIR/applications.db || true
sudo chmod 644 $PROJECT_DIR/applications.db || true

# ---------------------------
# Systemd сервис для веб-приложения (FastAPI)
# ---------------------------
WEB_SERVICE="/etc/systemd/system/remont-web.service"
echo "Настройка systemd сервиса для веб-приложения..."

sudo tee $WEB_SERVICE > /dev/null <<EOL
[Unit]
Description=Remont Web Application (FastAPI)
After=network.target

[Service]
Type=simple
User=$PROJECT_USER
Group=$PROJECT_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable remont-web
sudo systemctl start remont-web

# ---------------------------
# Systemd сервис для Telegram бота
# ---------------------------
BOT_SERVICE="/etc/systemd/system/remont-bot.service"
echo "Настройка systemd сервиса для Telegram бота..."

sudo tee $BOT_SERVICE > /dev/null <<EOL
[Unit]
Description=Remont Telegram Bot
After=network.target

[Service]
Type=simple
User=$PROJECT_USER
Group=$PROJECT_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable remont-bot
sudo systemctl start remont-bot

# ---------------------------
# Nginx
# ---------------------------
echo "Настройка Nginx..."

NGINX_CONF="/etc/nginx/sites-available/remont"

sudo tee $NGINX_CONF > /dev/null <<EOL
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    client_max_body_size 50M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }

    location /static/ {
        alias $PROJECT_DIR/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL

sudo ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# ---------------------------
# SSL через Let's Encrypt
# ---------------------------
echo "Настройка SSL..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m $SSL_EMAIL

# Перезапускаем сервисы после настройки SSL
sudo systemctl restart remont-web
sudo systemctl restart remont-bot
sudo systemctl restart nginx

# ---------------------------
# Завершение
# ---------------------------
echo ""
echo "=========================================="
echo "Развертывание завершено!"
echo "=========================================="
echo "Доступ к проекту: https://$DOMAIN"
echo "Telegram бот должен быть запущен"
echo ""
echo "Проверка статуса сервисов:"
echo "  sudo systemctl status remont-web"
echo "  sudo systemctl status remont-bot"
echo ""
echo "Просмотр логов:"
echo "  sudo journalctl -u remont-web -f"
echo "  sudo journalctl -u remont-bot -f"
echo ""
echo "ВАЖНО: Убедитесь, что вы заменили следующие значения в скрипте:"
echo "  - PROJECT_REPO (URL вашего репозитория)"
echo "  - DOMAIN (ваш домен)"
echo "  - BOT_TOKEN (токен Telegram бота)"
echo "  - ADMIN_IDS (ваши Telegram ID)"
echo "  - SSL_EMAIL (ваш email для Let's Encrypt)"
echo "=========================================="

