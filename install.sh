#!/usr/bin/env bash
# Installs (or updates) one bot from bots/<name> as a systemd service on Ubuntu.
# Usage: sudo ./install.sh <bot-name>
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Please run with sudo: sudo ./install.sh <bot-name>"
  exit 1
fi

BOT_NAME="${1:-}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "$BOT_NAME" ]]; then
  echo "Usage: sudo ./install.sh <bot-name>"
  echo "Available bots:"
  ls -1 "$REPO_DIR/bots"
  exit 1
fi

SRC_DIR="$REPO_DIR/bots/$BOT_NAME"
if [[ ! -f "$SRC_DIR/bot.py" ]]; then
  echo "Bot '$BOT_NAME' not found (expected $SRC_DIR/bot.py)."
  exit 1
fi

RUN_USER="discordbots"
INSTALL_DIR="/opt/discord-bots/$BOT_NAME"
SERVICE_NAME="discord-$BOT_NAME"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "==> Installing system packages"
apt-get update -y
apt-get install -y python3 python3-venv python3-pip

echo "==> Creating service user"
if ! id -u "$RUN_USER" &>/dev/null; then
  useradd --system --home-dir "/opt/discord-bots" --shell /usr/sbin/nologin "$RUN_USER"
fi

echo "==> Copying bot files to $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -r "$SRC_DIR/." "$INSTALL_DIR/"

echo "==> Setting up Python virtualenv"
if [[ ! -d "$INSTALL_DIR/venv" ]]; then
  python3 -m venv "$INSTALL_DIR/venv"
fi
"$INSTALL_DIR/venv/bin/pip" install --quiet --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install --quiet -r "$INSTALL_DIR/requirements.txt"

ENV_FILE="$INSTALL_DIR/.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "==> Configuration (press Enter to keep the default shown in brackets)"
  TMP_ENV="$(mktemp)"
  while IFS= read -r line; do
    if [[ "$line" =~ ^# || -z "$line" ]]; then
      echo "$line" >> "$TMP_ENV"
      continue
    fi
    key="${line%%=*}"
    default="${line#*=}"
    if [[ "$key" == "DISCORD_TOKEN" ]]; then
      read -rsp "$key (hidden, required): " value; echo
    else
      read -rp "$key [${default}]: " value
      value="${value:-$default}"
    fi
    echo "$key=$value" >> "$TMP_ENV"
  done < "$INSTALL_DIR/.env.example"
  mv "$TMP_ENV" "$ENV_FILE"
  chmod 600 "$ENV_FILE"
else
  echo "==> Existing .env found, keeping it"
fi

chown -R "$RUN_USER:$RUN_USER" "$INSTALL_DIR"

echo "==> Writing systemd service $SERVICE_NAME"
cat > "$SERVICE_FILE" << UNIT
[Unit]
Description=Discord bot: $BOT_NAME
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$RUN_USER
Group=$RUN_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

sleep 3
echo ""
systemctl --no-pager status "$SERVICE_NAME" || true
echo ""
echo "Done. Useful commands:"
echo "  sudo systemctl status $SERVICE_NAME"
echo "  sudo journalctl -u $SERVICE_NAME -f"
echo "  sudo systemctl restart $SERVICE_NAME"
