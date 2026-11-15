<div align="center">

# 🤖 kollbar bot

ربات دیسکورد با خوش‌آمدگویی، تیکت با دکمه، مدیریت سرور و سیستم اخطار
<br>
A Discord bot with welcome messages, button tickets, moderation tools and warnings

🎨 **طراح / Designer:** alexanderson

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](#)
[![discord.py](https://img.shields.io/badge/discord.py-2.4%2B-5865F2?logo=discord&logoColor=white)](#)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%20%7C%2024.04-E95420?logo=ubuntu&logoColor=white)](#)
[![systemd](https://img.shields.io/badge/systemd-service-222222)](#)

**[🇮🇷 فارسی](#-راهنمای-فارسی)** • **[🇬🇧 English](#-english-guide)**

</div>

---

## ✨ امکانات

| | قابلیت | توضیح |
|:-:|---|---|
| 👋 | **خوش‌آمدگویی** | پیام embed زیبا برای هر عضو جدید |
| 🎫 | **تیکت با دکمه** | ساخت کانال خصوصی برای هر تیکت + ترنسکریپت خودکار |
| 🛡️ | **مدیریت** | kick، ban، clear، say |
| ⚠️ | **سیستم اخطار** | ثبت، نمایش و پاکسازی اخطار با ذخیره دائمی |
| 🏷️ | **رول دسته‌جمعی** | دادن و گرفتن رول به همه اعضا |
| 📊 | **اطلاعات** | نمایش اطلاعات کاربر و سرور |
| 🚀 | **نصب یک‌خطی** | نصب روی Ubuntu با یک دستور، اجرا بعد از ریبوت |

---

<details open>
<summary><h2>🇮🇷 راهنمای فارسی</h2></summary>

### 📋 پیش‌نیازها

- 🐧 Ubuntu 22.04 یا 24.04 با دسترسی `sudo`
- 🐍 Python نسخه 3.10 یا بالاتر
- 🔑 دسترسی git به این ریپو (کلید SSH یا Personal Access Token)
- 🤖 یک Application در [Discord Developer Portal](https://discord.com/developers/applications) و توکن ربات
- 🏰 سرور Discord که ربات به آن دعوت شده باشد

### 🤖 ساخت ربات در Discord

1. به Developer Portal برو و یک **New Application** بساز.
2. از منوی **Bot** روی **Reset Token** بزن و توکن را کپی کن (همان `DISCORD_TOKEN`).
3. زیر **Privileged Gateway Intents** این دو گزینه را روشن کن:
   - ✅ **Server Members Intent**
   - ✅ **Presence Intent**
4. در **OAuth2 > URL Generator**:
   - Scopes: `bot` و `applications.commands`
   - Permissions: View Channels، Send Messages، Embed Links، Read Message History، Manage Messages، Manage Channels، Manage Roles، Kick Members، Ban Members
5. لینک ساخته‌شده را باز کن و ربات را دعوت کن.
6. در تنظیمات سرور **Roles**، نقش ربات را **بالاتر** از نقش‌هایی بکش که باید به آن‌ها رول بدهد.

> 💡 برای کپی ID کانال‌ها و نقش‌ها، **Developer Mode** را از *User Settings > Advanced* روشن کن، بعد روی آن‌ها راست‌کلیک و **Copy ID** را بزن.

### 🚀 نصب

```bash
git clone git@github.com:<your-username>/kollbar-bot.git
cd kollbar-bot
sudo ./install.sh
```

اسکریپت نصب این کارها را انجام می‌دهد:

1. 📦 نصب پکیج‌های لازم با `apt`
2. 👤 ساخت یک کاربر سیستمی بدون دسترسی لاگین
3. 📁 کپی در `/opt/kollbar-bot` و ساخت virtualenv
4. 🔐 پرسیدن تنظیمات و ذخیره در `.env` (فقط قابل خواندن توسط کاربر ربات)
5. ⚙️ ساخت و اجرای سرویس `kollbar-bot` در systemd

توکن در حین نصب وارد می‌شود و هیچ‌وقت نمایش داده نمی‌شود. ربات بعد از ریبوت سرور هم خودکار بالا می‌آید.

### 🔄 آپدیت

```bash
git pull
sudo ./install.sh
```

`.env` قبلی حفظ می‌شود.

### 🎛️ مدیریت سرویس

```bash
sudo systemctl status kollbar-bot     # وضعیت
sudo systemctl restart kollbar-bot   # ریستارت
sudo systemctl stop kollbar-bot      # توقف
sudo journalctl -u kollbar-bot -f    # لاگ‌های زنده
```

### 🧪 اجرای محلی (توسعه)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # مقادیر را پر کن
python bot.py
```

> ⚠️ اگر توکن را مستقیم داخل `bot.py` بگذاری، به جای `YOUR_BOT_TOKEN_HERE` بنویس و **هرگز آن را commit نکن**.

### ⚙️ تنظیمات (`.env`)

| کلید | توضیح |
|---|---|
| `DISCORD_TOKEN` | توکن ربات (الزامی) |
| `WELCOME_CHANNEL_ID` | کانال پیام خوش‌آمدگویی |
| `TICKET_LOG_CHANNEL_ID` | کانال لاگ تیکت‌ها |
| `TICKET_STAFF_ROLE_IDS` | نقش‌های استاف با کاما جدا شوند |
| `WELCOME_GIF_URL` | لینک GIF برای embedها (خالی = غیرفعال) |
| `BOT_STATUS` | متن وضعیت ربات (پیش‌فرض: `kollbar bot`) |

### 📜 دستورات

| دستور | دسترسی | کاربرد |
|---|---|---|
| `/setup_ticket` | مدیر | ارسال پیام دکمه تیکت |
| `/say <message>` | Manage Messages | ارسال پیام از طرف ربات |
| `/kick <member> [reason]` | Kick Members | کیک کردن کاربر |
| `/ban <member> [reason]` | Ban Members | بن کردن کاربر |
| `/warn <member> [reason]` | Kick Members | ثبت اخطار |
| `/warnings <member>` | همه | نمایش اخطارها |
| `/clearwarnings <member> [count]` | Kick Members | پاک کردن اخطارها |
| `/addroleall <role>` | Manage Roles | دادن رول به همه |
| `/removeroleall <role>` | Manage Roles | گرفتن رول از همه |
| `/clear <amount>` | Manage Messages | پاک کردن تا 100 پیام |
| `/userinfo [member]` | همه | اطلاعات کاربر |
| `/serverinfo` | همه | اطلاعات سرور |

### 📝 نکات مهم

- 💾 اخطارها در `warnings.json` داخل `/opt/kollbar-bot` ذخیره می‌شوند.
- 🧾 وقتی تیکت بسته می‌شود، ترنسکریپت آن به صورت فایل `.txt` در کانال لاگ ارسال می‌شود.
- 🖼️ لینک GIF قدیمی کد از CDN دیسکورد با تاریخ انقضا بود؛ یک GIF جدید آپلود کن.
- 🔑 اگر توکن لو رفت، از Developer Portal ریست کن و `.env` را به‌روز کن.

</details>

---

<details>
<summary><h2>🇬🇧 English Guide</h2></summary>

### 📋 Prerequisites

- 🐧 Ubuntu 22.04 or 24.04 with `sudo` access
- 🐍 Python 3.10 or newer
- 🔑 git access to this repository (SSH key or Personal Access Token)
- 🤖 A Discord application and bot token from the [Developer Portal](https://discord.com/developers/applications)
- 🏰 A Discord server the bot has been invited to

### 🤖 Create the bot in Discord

1. Create a **New Application** in the Developer Portal.
2. Open **Bot**, click **Reset Token** and copy it. This is your `DISCORD_TOKEN`.
3. Under **Privileged Gateway Intents**, enable:
   - ✅ **Server Members Intent**
   - ✅ **Presence Intent**
4. Under **OAuth2 > URL Generator**:
   - Scopes: `bot` and `applications.commands`
   - Permissions: View Channels, Send Messages, Embed Links, Read Message History, Manage Messages, Manage Channels, Manage Roles, Kick Members, Ban Members
5. Open the generated URL and invite the bot to your server.
6. In **Server Settings > Roles**, drag the bot's role **above** any role it must assign.

> 💡 To copy IDs, enable **Developer Mode** (*User Settings > Advanced*), then right-click a channel or role and choose **Copy ID**.

### 🚀 Install

```bash
git clone git@github.com:<your-username>/kollbar-bot.git
cd kollbar-bot
sudo ./install.sh
```

The installer will:

1. 📦 Install the required packages with `apt`
2. 👤 Create a no-login system user `kollbar`
3. 📁 Copy the bot to `/opt/kollbar-bot` and create a virtualenv
4. 🔐 Ask for your settings and save them to `.env` (readable only by the bot user)
5. ⚙️ Create and start the `kollbar-bot` systemd service (starts on boot)

The token is entered hidden and is never printed.

### 🔄 Update

```bash
git pull
sudo ./install.sh
```

Your existing `.env` is kept.

### 🎛️ Manage the service

```bash
sudo systemctl status kollbar-bot     # status
sudo systemctl restart kollbar-bot   # restart
sudo systemctl stop kollbar-bot      # stop
sudo journalctl -u kollbar-bot -f    # live logs
```

### 🧪 Run locally (development)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # fill in the values
python bot.py
```

> ⚠️ To hardcode a token for a quick local test, replace `YOUR_BOT_TOKEN_HERE` in `bot.py`. **Never commit a real token.**

### ⚙️ Configuration (`.env`)

| Key | Description |
|---|---|
| `DISCORD_TOKEN` | Bot token (required) |
| `WELCOME_CHANNEL_ID` | Channel for welcome messages |
| `TICKET_LOG_CHANNEL_ID` | Channel for ticket logs and transcripts |
| `TICKET_STAFF_ROLE_IDS` | Staff roles that can see tickets (comma-separated) |
| `WELCOME_GIF_URL` | GIF for embeds (empty = disabled) |
| `BOT_STATUS` | Bot status text (default: `kollbar bot`) |

### 📜 Commands

| Command | Permission | Description |
|---|---|---|
| `/setup_ticket` | Admin | Posts the ticket button message |
| `/say <message>` | Manage Messages | Sends a message as the bot |
| `/kick <member> [reason]` | Kick Members | Kicks a member |
| `/ban <member> [reason]` | Ban Members | Bans a member |
| `/warn <member> [reason]` | Kick Members | Adds a warning |
| `/warnings <member>` | Everyone | Lists warnings |
| `/clearwarnings <member> [count]` | Kick Members | Clears all, or the last N warnings |
| `/addroleall <role>` | Manage Roles | Gives a role to every member |
| `/removeroleall <role>` | Manage Roles | Removes a role from every member |
| `/clear <amount>` | Manage Messages | Deletes up to 100 messages |
| `/userinfo [member]` | Everyone | Member information |
| `/serverinfo` | Everyone | Server information |

### 📝 Notes

- 💾 Warnings are stored in `warnings.json` inside `/opt/kollbar-bot`.
- 🧾 When a ticket closes, its transcript is posted as a `.txt` file to the log channel.
- 🖼️ The old welcome GIF link was a signed Discord CDN link that has expired. Upload a new GIF and set `WELCOME_GIF_URL`.
- 🔑 Never commit your token. If it leaks, reset it in the Developer Portal and update `.env`.

</details>

---

<div align="center">

🎨 طراحی شده توسط **alexanderson** • Designed by **alexanderson**

</div>
