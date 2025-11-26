#!/usr/bin/env bash
set -euo pipefail

# --- Конфигурируемые переменные ---
REPO_URL="https://github.com/bagahizriev/Remont.git"
PROJECT_DIR="/var/www/remont"
DOMAIN="comfortholding.ru"
ADDITIONAL_DOMAIN="www.comfortholding.ru"
BOT_TOKEN="8439653071:AAFumKitOJKrGctnL8DrfOjrLXCa7NXUxK8"
ADMIN_IDS="6052363807"
SYSTEM_USER="www-data"

# --- Проверки окружения ---
if [[ "$(id -u)" -ne 0 ]]; then
  echo "Эту установку нужно запускать под root (sudo)." >&2
  exit 1
fi

if [[ -z "$REPO_URL" || -z "$PROJECT_DIR" || -z "$DOMAIN" || -z "$BOT_TOKEN" || -z "$ADMIN_IDS" ]]; then
  echo "Заполните все переменные в верхней части скрипта." >&2
  exit 1
fi

RUN_USER="${SUDO_USER:-root}"

APT_PACKAGES=(
  git python3 python3-venv python3-pip
  nodejs npm sqlite3 nginx ufw
  certbot python3-certbot-nginx
)

echo "[1/10] Установка пакетов..."
export DEBIAN_FRONTEND=noninteractive
apt update
apt install -y "${APT_PACKAGES[@]}"

echo "[2/10] Создание системной директории $PROJECT_DIR..."
mkdir -p "$PROJECT_DIR"
chown "$RUN_USER":"$RUN_USER" "$PROJECT_DIR"

if [[ -d "$PROJECT_DIR/.git" ]]; then
  echo "[3/10] Обновление репозитория..."
  sudo -u "$RUN_USER" git -C "$PROJECT_DIR" pull --ff-only
else
  echo "[3/10] Клонирование репозитория..."
  sudo -u "$RUN_USER" git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

echo "[4/10] Настройка Python окружения..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[5/10] Сборка фронтенда..."
sudo -u "$RUN_USER" npm install
sudo -u "$RUN_USER" npm run build

echo "[6/10] Обновление файла .env..."
cat <<EOF > .env
BOT_TOKEN=${BOT_TOKEN}
ADMIN_IDS=${ADMIN_IDS}
EOF
chown "$SYSTEM_USER":"$SYSTEM_USER" .env || true

# Создаём базу заранее и отдаём права сервисному пользователю
touch applications.db
chown "$SYSTEM_USER":"$SYSTEM_USER" applications.db || true

echo "[7/10] Создание systemd юнитов..."
cat <<EOF >/etc/systemd/system/remont-api.service
[Unit]
Description=Remont FastAPI
After=network.target

[Service]
User=${SYSTEM_USER}
Group=${SYSTEM_USER}
WorkingDirectory=${PROJECT_DIR}
Environment="PYTHONPATH=${PROJECT_DIR}"
ExecStart=${PROJECT_DIR}/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --proxy-headers
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF >/etc/systemd/system/remont-bot.service
[Unit]
Description=Remont Telegram Bot
After=network.target remont-api.service

[Service]
User=${SYSTEM_USER}
Group=${SYSTEM_USER}
WorkingDirectory=${PROJECT_DIR}
EnvironmentFile=${PROJECT_DIR}/.env
ExecStart=${PROJECT_DIR}/venv/bin/python bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now remont-api remont-bot

# Перед стартом сервисов убеждаемся, что весь проект принадлежит SYSTEM_USER,
# чтобы FastAPI и бот могли писать в базу и другие файлы.
chown -R "$SYSTEM_USER":"$SYSTEM_USER" "$PROJECT_DIR"

echo "[8/10] Настройка Nginx..."
STATIC_DIR="${PROJECT_DIR}/static"
cat <<EOF >/etc/nginx/sites-available/remont
server {
    listen 80;
    server_name ${DOMAIN} ${ADDITIONAL_DOMAIN};

    client_max_body_size 20m;

    location /static/ {
        alias ${STATIC_DIR}/;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/remont /etc/nginx/sites-enabled/remont
nginx -t
systemctl reload nginx

echo "[9/10] Настройка фаервола..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo "[10/10] Выпуск Let's Encrypt сертификата..."
domains=(-d "$DOMAIN")
if [[ -n "$ADDITIONAL_DOMAIN" ]]; then
  domains+=(-d "$ADDITIONAL_DOMAIN")
fi
certbot --nginx "${domains[@]}" --agree-tos --no-eff-email -m "admin@${DOMAIN}"

echo "Готово. Приложение и бот работают за Nginx с HTTPS."

