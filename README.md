# discord-bots

A collection of Discord bots. Each bot lives in `bots/<name>/` and is installed on Ubuntu
with one command as a systemd service that starts on boot.

## Prerequisites

- Ubuntu 22.04 or 24.04 (or any Debian-based system with `apt` and systemd)
- Python 3.10 or newer (included in Ubuntu 22.04+)
- `sudo` access on the server
- A Discord application and bot token for each bot (see each bot's README)

## Install a bot

```bash
git clone git@github.com:alexanderson05/discord-bots.git
cd discord-bots
sudo ./install.sh kollbar
```

The installer will:
1. Install Python, venv, and pip with `apt`.
2. Create a system user `discordbots` with no login shell.
3. Copy the bot to `/opt/discord-bots/<name>` and create a virtualenv.
4. Ask for the bot's settings and save them to `.env` (mode 600).
5. Create and start the `discord-<name>` systemd service.

Run the same command again to update a bot after pulling new code. Existing `.env` files are kept.

## Manage a bot

```bash
sudo systemctl status discord-kollbar
sudo journalctl -u discord-kollbar -f
sudo systemctl restart discord-kollbar
```

## Add a new bot

1. Create `bots/<newbot>/` containing:
   - `bot.py` (entry point, reads settings from `.env`)
   - `requirements.txt`
   - `.env.example` (the installer prompts for each line here)
   - `README.md`
2. Run `sudo ./install.sh <newbot>`.

## Bots

| Name | Description |
|---|---|
| [kollbar](bots/kollbar/README.md) | Welcome messages, tickets, moderation, warnings |

## Security

- Never commit `.env` files or tokens. `.gitignore` already excludes them.
- If a token is ever exposed, reset it in the Discord Developer Portal and re-run the installer.
