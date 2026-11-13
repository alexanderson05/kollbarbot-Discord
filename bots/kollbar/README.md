# kollbar bot

A Discord bot with welcome messages, a button-based ticket system with transcripts,
moderation commands (kick, ban, say, clear), a warning system, and bulk role tools.

## Setup

Install with the repository's installer (from the repo root):

```bash
sudo ./install.sh kollbar
```

The installer asks for the bot token and IDs, then runs the bot as a systemd service
that starts on boot.

## Manual run (for development)

```bash
cd bots/kollbar
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in the values
python bot.py
```

## Commands

| Command | Who can use it | Description |
|---|---|---|
| `/setup_ticket` | anyone with permission to post | Posts the ticket button message |
| `/say <message>` | Manage Messages | Sends a message as the bot |
| `/kick <member> [reason]` | Kick Members | Kicks a member |
| `/ban <member> [reason]` | Ban Members | Bans a member |
| `/warn <member> [reason]` | Kick Members | Adds a warning |
| `/warnings <member>` | everyone | Lists a member's warnings |
| `/clearwarnings <member> [count]` | Kick Members | Clears all, or the last N warnings |
| `/addroleall <role>` | Manage Roles | Gives a role to every member |
| `/removeroleall <role>` | Manage Roles | Removes a role from every member |
| `/clear <amount>` | Manage Messages | Deletes up to 100 messages in the channel |
| `/userinfo [member]` | everyone | Shows member info |
| `/serverinfo` | everyone | Shows server info |

## Discord setup (before running the installer)

1. Go to https://discord.com/developers/applications and create an application.
2. Open **Bot**, click **Reset Token** and copy it. This is the `DISCORD_TOKEN`.
3. In **Bot > Privileged Gateway Intents**, turn on **Server Members Intent** and **Presence Intent**.
4. In **OAuth2 > URL Generator**, select the scopes `bot` and `applications.commands`, and these permissions:
   View Channels, Send Messages, Embed Links, Read Message History, Manage Messages,
   Manage Channels, Manage Roles, Kick Members, Ban Members.
5. Open the generated URL and invite the bot to your server.
6. In Discord server settings > Roles, drag the bot's role **above** any role it has to assign
   (for `/addroleall`) or any ticket staff role it has to see.

Turn on **Developer Mode** (User Settings > Advanced) to copy channel and role IDs.

## Notes

- Warnings are stored in `warnings.json` inside the install folder (`/opt/discord-bots/kollbar`).
- Ticket transcripts are posted as a `.txt` file to the ticket log channel when a ticket closes.
- The welcome GIF link from the original code was a signed Discord CDN link that expires.
  Upload a new GIF and set `WELCOME_GIF_URL` to a fresh link, or leave it empty.
