# kollbar bot

یک ربات دیسکورد با سیستم خوش‌آمدگویی، تیکت با دکمه (همراه با ترنскрипت)، دستورات مدیریتی، سیستم اخطار و ابزارهای رول دسته‌جمعی.

<details open>
<summary><h2>🇮🇷 راهنمای فارسی</h2></summary>

## پیش‌نیازها

- سیستم‌عامل Ubuntu 22.04 یا 24.04 با دسترسی `sudo`
- Python نسخه 3.10 یا بالاتر (در Ubuntu 22.04 و 24.04 از قبل نصب است)
- دسترسی git به این ریپو (کلید SSH یا Personal Access Token)
- یک برنامه (Application) در Discord Developer Portal و توکن ربات
- سرور Discord که ربات به آن دعوت شده باشد

## ساخت ربات در Discord

1. به آدرس https://discord.com/developers/applications برو و یک Application جدید بساز.
2. از منوی **Bot** روی **Reset Token** بزن و توکن را کپی کن. این همان `DISCORD_TOKEN` است.
3. در همان صفحه‌ی **Bot** بخش **Privileged Gateway Intents** را پیدا کن و این دو گزینه را روشن کن:
   - **Server Members Intent**
   - **Presence Intent**
4. از منوی **OAuth2 > URL Generator** این موارد را انتخاب کن:
   - Scopes: `bot` و `applications.commands`
   - Bot Permissions: View Channels، Send Messages، Embed Links، Read Message History، Manage Messages، Manage Channels، Manage Roles، Kick Members، Ban Members
5. لینک ساخته‌شده را باز کن و ربات را به سرورت دعوت کن.
6. در تنظیمات سرور Discord، بخش **Roles** را باز کن و نقش ربات را **بالاتر** از نقش‌هایی بکش که باید به آن‌ها رول بدهد (برای `/addroleall`) یا نقش‌های استاف تیکت.

برای کپی کردن ID کانال‌ها و نقش‌ها، ابتدا **Developer Mode** را از **User Settings > Advanced** روشن کن. بعد روی کانال یا نقش راست‌کلیک کن و **Copy ID** را بزن.

## نصب

```bash
git clone git@github.com:alexanderson05/kollbar-bot.git
cd kollbar-bot
sudo ./install.sh
```

اسکریپت نصب این کارها را انجام می‌دهد:
1. پکیج‌های لازم را با `apt` نصب می‌کند.
2. یک کاربر سیستمی به نام `kollbar` بدون دسترسی لاگین می‌سازد.
3. فایل‌های ربات را در `/opt/kollbar-bot` کپی می‌کند و virtualenv می‌سازد.
4. مقادیر تنظیمات را می‌پرسد و در فایل `.env` ذخیره می‌کند (دسترسی فقط برای کاربر ربات).
5. سرویس `kollbar-bot` را در systemd می‌سازد و راه می‌اندازد. بعد از ریبوت سرور هم خودکار بالا می‌آید.

توکن را در حین نصب وارد می‌کنی و نمایش داده نمی‌شود.

## آپدیت ربات

بعد از گرفتن تغییرات جدید از گیت، دوباره همان دستور نصب را اجرا کن. فایل `.env` قبلی حفظ می‌شود.

```bash
git pull
sudo ./install.sh
```

## مدیریت سرویس

```bash
sudo systemctl status kollbar-bot        # وضعیت
sudo systemctl restart kollbar-bot      # ریستارت
sudo systemctl stop kollbar-bot         # توقف
sudo journalctl -u kollbar-bot -f       # دیدن لاگ‌ها به صورت زنده
```

## اجرای محلی برای توسعه

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # و مقادیر را پر کن
python bot.py
```

اگر ترجیح می‌دهی توکن را مستقیم در کد بگذاری، به جای `YOUR_BOT_TOKEN_HERE` داخل `bot.py` توکن را بنویس. فقط برای تست محلی؛ هرگز توکن واقعی را commit نکن.

## تنظیمات (`.env`)

| کلید | توضیح |
|---|---|
| `DISCORD_TOKEN` | توکن ربات (الزامی) |
| `WELCOME_CHANNEL_ID` | ID کانال پیام خوش‌آمدگویی |
| `TICKET_LOG_CHANNEL_ID` | ID کانال لاگ تیکت‌ها |
| `TICKET_STAFF_ROLE_IDS` | ID نقش‌های استاف که به تیکت دسترسی دارند؛ با کاما جدا شوند |
| `WELCOME_GIF_URL` | لینک GIF برای embedها؛ خالی بگذاری یعنی GIF نمایش داده نمی‌شود |
| `BOT_STATUS` | متنی که زیر اسم ربات نمایش داده می‌شود (پیش‌فرض: `kollbar bot`) |

## دستورات

| دستور | دسترسی لازم | توضیح |
|---|---|---|
| `/setup_ticket` | مدیر | ارسال پیام با دکمه ایجاد تیکت |
| `/say <message>` | Manage Messages | ارسال پیام توسط ربات |
| `/kick <member> [reason]` | Kick Members | کیک کردن کاربر |
| `/ban <member> [reason]` | Ban Members | بن کردن کاربر |
| `/warn <member> [reason]` | Kick Members | ثبت اخطار برای کاربر |
| `/warnings <member>` | همه | نمایش اخطارهای کاربر |
| `/clearwarnings <member> [count]` | Kick Members | پاک کردن همه یا تعداد مشخصی از آخرین اخطارها |
| `/addroleall <role>` | Manage Roles | دادن رول به همه اعضا |
| `/removeroleall <role>` | Manage Roles | گرفتن رول از همه اعضا |
| `/clear <amount>` | Manage Messages | پاک کردن تا 100 پیام از کانال |
| `/userinfo [member]` | همه | نمایش اطلاعات کاربر |
| `/serverinfo` | همه | نمایش اطلاعات سرور |

## نکات مهم

- اخطارها در فایل `warnings.json` داخل `/opt/kollbar-bot` ذخیره می‌شوند.
- وقتی تیکت بسته می‌شود، ترنскрипت آن به صورت فایل `.txt` در کانال لاگ تیکت ارسال می‌شود.
- لینک GIF قدیمی کد یک لینک امضاشده‌ی Discord با تاریخ انقضا بود و دیگر کار نمی‌کند. یک GIF جدید آپلود کن و لینکش را در `WELCOME_GIF_URL` بگذار.
- توکن را هرگز در گیت یا در چت عمومی قرار نده. اگر لو رفت، از Developer Portal ریست کن و دوباره `.env` را ویرایش کن یا `install.sh` را اجرا کن.

</details>

---

<details>
<summary><h2>🇬🇧 English Guide</h2></summary>

## Prerequisites

- Ubuntu 22.04 or 24.04 with `sudo` access
- Python 3.10 or newer (included in Ubuntu 22.04 and 24.04)
- git access to this repository (SSH key or Personal Access Token)
- A Discord application and bot token from the Developer Portal
- A Discord server the bot has been invited to

## Create the bot in Discord

1. Go to https://discord.com/developers/applications and create a new application.
2. Open **Bot**, click **Reset Token** and copy the token. This is your `DISCORD_TOKEN`.
3. Under **Privileged Gateway Intents**, turn on:
   - **Server Members Intent**
   - **Presence Intent**
4. Under **OAuth2 > URL Generator**, select:
   - Scopes: `bot` and `applications.commands`
   - Bot Permissions: View Channels, Send Messages, Embed Links, Read Message History, Manage Messages, Manage Channels, Manage Roles, Kick Members, Ban Members
5. Open the generated URL and invite the bot to your server.
6. In Server Settings > **Roles**, drag the bot's role **above** any role it must assign (for `/addroleall`) and above the ticket staff roles.

To copy channel and role IDs, enable **Developer Mode** in User Settings > Advanced, then right-click the item and choose **Copy ID**.

## Install

```bash
git clone git@github.com:alexanderson05/kollbar-bot.git
cd kollbar-bot
sudo ./install.sh
```

The installer will:
1. Install the required packages with `apt`.
2. Create a system user `kollbar` with no login shell.
3. Copy the bot to `/opt/kollbar-bot` and create a virtualenv.
4. Ask for your settings and save them to `.env` (readable only by the bot user).
5. Create and start the `kollbar-bot` systemd service. It starts automatically on boot.

The token is entered hidden and is never printed.

## Update

```bash
git pull
sudo ./install.sh
```

Your existing `.env` is kept.

## Manage the service

```bash
sudo systemctl status kollbar-bot       # status
sudo systemctl restart kollbar-bot     # restart
sudo systemctl stop kollbar-bot        # stop
sudo journalctl -u kollbar-bot -f      # live logs
```

## Run locally for development

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # then fill in the values
python bot.py
```

You can also put your token directly in `bot.py` by replacing `YOUR_BOT_TOKEN_HERE`. Use this only for quick local tests and never commit a real token.

## Configuration (`.env`)

| Key | Description |
|---|---|
| `DISCORD_TOKEN` | Bot token (required) |
| `WELCOME_CHANNEL_ID` | Channel ID for welcome messages |
| `TICKET_LOG_CHANNEL_ID` | Channel ID where ticket logs and transcripts are posted |
| `TICKET_STAFF_ROLE_IDS` | Staff role IDs that can see tickets, comma-separated |
| `WELCOME_GIF_URL` | GIF URL for embeds; leave empty to disable |
| `BOT_STATUS` | Text shown as the bot's status (default: `kollbar bot`) |

## Commands

| Command | Required permission | Description |
|---|---|---|
| `/setup_ticket` | Admin | Posts the ticket button message |
| `/say <message>` | Manage Messages | Sends a message as the bot |
| `/kick <member> [reason]` | Kick Members | Kicks a member |
| `/ban <member> [reason]` | Ban Members | Bans a member |
| `/warn <member> [reason]` | Kick Members | Adds a warning |
| `/warnings <member>` | Everyone | Lists a member's warnings |
| `/clearwarnings <member> [count]` | Kick Members | Clears all warnings, or only the last N |
| `/addroleall <role>` | Manage Roles | Gives a role to every member |
| `/removeroleall <role>` | Manage Roles | Removes a role from every member |
| `/clear <amount>` | Manage Messages | Deletes up to 100 messages in the channel |
| `/userinfo [member]` | Everyone | Shows member information |
| `/serverinfo` | Everyone | Shows server information |

## Notes

- Warnings are stored in `warnings.json` inside `/opt/kollbar-bot`.
- When a ticket closes, its transcript is posted as a `.txt` file to the ticket log channel.
- The welcome GIF link in the original code was a signed Discord CDN link that has expired. Upload a new GIF and set `WELCOME_GIF_URL`.
- Never commit your token. If it leaks, reset it in the Developer Portal and update `.env`.

</details>
