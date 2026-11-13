import asyncio
import datetime
import io
import json
import os
import sys

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def _int_env(name):
    value = os.getenv(name, "").strip()
    return int(value) if value.isdigit() else None


def _int_list_env(name):
    raw = os.getenv(name, "")
    return [int(x) for x in raw.replace(" ", "").split(",") if x.isdigit()]


TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
if not TOKEN:
    sys.exit("DISCORD_TOKEN is not set. Put it in the .env file.")

WELCOME_CHANNEL_ID = _int_env("WELCOME_CHANNEL_ID")
TICKET_LOG_CHANNEL_ID = _int_env("TICKET_LOG_CHANNEL_ID")
TICKET_STAFF_ROLE_IDS = _int_list_env("TICKET_STAFF_ROLE_IDS")
WELCOME_GIF_URL = os.getenv("WELCOME_GIF_URL", "").strip()
BOT_STATUS = os.getenv("BOT_STATUS", "kollbar bot").strip()
WARN_FILE = os.path.join(BASE_DIR, os.getenv("WARN_FILE", "warnings.json"))

intents = discord.Intents.default()
intents.members = True
intents.presences = True


class KollbarBot(commands.Bot):
    async def setup_hook(self):
        # Register persistent views so ticket buttons keep working after a restart.
        self.add_view(TicketView())
        self.add_view(CloseTicketView())


bot = KollbarBot(command_prefix="/", intents=intents)
tree = bot.tree


# --- Load/Save Warnings ---
def load_warnings():
    try:
        with open(WARN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_warnings(warnings_data):
    with open(WARN_FILE, "w", encoding="utf-8") as f:
        json.dump(warnings_data, f, indent=4, ensure_ascii=False)


warnings_data = load_warnings()


def utc_now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


# --- Ready event ---
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name=BOT_STATUS))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")


# --- Welcome system ---
@bot.event
async def on_member_join(member: discord.Member):
    if WELCOME_CHANNEL_ID is None:
        return
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is None:
        return
    embed = discord.Embed(
        title="🎉 خوش آمدید 🎉",
        description=(
            f"{member.mention}\n\n"
            f"خوش آمدی به **𝑹𝒂𝒄𝒊𝒔𝒕𝑪𝒂𝒎𝒑!**\n"
            f"امیدواریم از حضور در سرور ما لذت ببری!\n\n"
            f"👥 تعداد اعضای سرور: **{member.guild.member_count}**"
        ),
        color=discord.Color.green(),
    )
    if WELCOME_GIF_URL:
        embed.set_image(url=WELCOME_GIF_URL)
    embed.set_footer(text=f"کاربر جدید: {member.name}", icon_url=member.display_avatar.url)
    await channel.send(embed=embed)


# --- Ticket system ---
def ticket_channel_name(member: discord.Member) -> str:
    return f"ticket-{member.name.lower().replace(' ', '-')}"


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ایجاد تیکت", style=discord.ButtonStyle.green, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user
        name = ticket_channel_name(member)

        for channel in guild.text_channels:
            if channel.name == name:
                await interaction.response.send_message("شما از قبل یک تیکت باز دارید!", ephemeral=True)
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }
        for role_id in TICKET_STAFF_ROLE_IDS:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        ticket_channel = await guild.create_text_channel(name=name, overwrites=overwrites)

        staff_mentions = " ".join(f"<@&{role_id}>" for role_id in TICKET_STAFF_ROLE_IDS)
        embed = discord.Embed(
            title="تیکت شما باز شد!",
            description=(
                f"سلام {member.mention}!\n{staff_mentions} عزیز به این تیکت دسترسی دارند.\n\n"
                f"برای بستن تیکت، از دکمه زیر استفاده کنید."
            ),
            color=discord.Color.blue(),
        )
        await ticket_channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"تیکت شما در {ticket_channel.mention} باز شد!", ephemeral=True)

        ticket_log_channel = bot.get_channel(TICKET_LOG_CHANNEL_ID) if TICKET_LOG_CHANNEL_ID else None
        if ticket_log_channel:
            embed_log = discord.Embed(
                title="تیکت جدید",
                description=f"کاربر {member.mention} یک تیکت باز کرد: {ticket_channel.mention}",
                color=discord.Color.green(),
            )
            embed_log.set_footer(text=f"ID: {member.id}")
            await ticket_log_channel.send(embed=embed_log)


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="بستن تیکت", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        ticket_log_channel = bot.get_channel(TICKET_LOG_CHANNEL_ID) if TICKET_LOG_CHANNEL_ID else None

        await interaction.response.send_message("تیکت در حال بسته شدن است...", ephemeral=True)

        if ticket_log_channel:
            lines = []
            async for message in channel.history(limit=None, oldest_first=True):
                if not message.author.bot:
                    lines.append(
                        f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] "
                        f"{message.author.name}: {message.content}"
                    )
            transcript = "\n".join(lines) or "No user messages recorded in this ticket."
            file = discord.File(io.BytesIO(transcript.encode("utf-8")), filename=f"{channel.name}.txt")

            embed = discord.Embed(
                title="تیکت بسته شد",
                description=f"تیکت {channel.name} توسط {interaction.user.mention} بسته شد.",
                color=discord.Color.orange(),
            )
            await ticket_log_channel.send(embed=embed, file=file)

        await asyncio.sleep(5)
        await channel.delete()


@tree.command(name="setup_ticket", description="ارسال پیام تیکت با دکمه")
async def setup_ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title="𝑹𝒂𝒄𝒊𝒔𝒕𝑪𝒂𝒎𝒑",
        description="Ba Salam , Jahat Vojod Moshkel Ticket Baz Konid",
        color=discord.Color.green(),
    )
    if WELCOME_GIF_URL:
        embed.set_image(url=WELCOME_GIF_URL)
    await interaction.response.send_message(embed=embed, view=TicketView())


# --- Moderation commands ---
@tree.command(name="say", description="ارسال پیام توسط ربات")
@app_commands.describe(message="پیام برای ارسال")
async def say(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("شما اجازه استفاده از این دستور را ندارید.", ephemeral=True)
        return
    await interaction.channel.send(message)
    await interaction.response.send_message("پیام ارسال شد.", ephemeral=True)


@tree.command(name="kick", description="کیک کردن کاربر")
@app_commands.describe(member="کاربر مورد نظر", reason="دلیل کیک")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("شما اجازه کیک کردن را ندارید.", ephemeral=True)
        return
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} کیک شد. دلیل: {reason or 'نامشخص'}")
    except discord.Forbidden:
        await interaction.response.send_message("ربات دسترسی کافی ندارد.", ephemeral=True)


@tree.command(name="ban", description="بن کردن کاربر")
@app_commands.describe(member="کاربر مورد نظر", reason="دلیل بن")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("شما اجازه بن کردن را ندارید.", ephemeral=True)
        return
    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.mention} بن شد. دلیل: {reason or 'نامشخص'}")
    except discord.Forbidden:
        await interaction.response.send_message("ربات دسترسی کافی ندارد.", ephemeral=True)


# --- Warning system ---
@tree.command(name="warn", description="اخطار دادن به کاربر")
@app_commands.describe(member="کاربر مورد نظر", reason="دلیل اخطار")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "بدون دلیل"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("شما اجازه استفاده از این دستور را ندارید.", ephemeral=True)
        return
    user_id = str(member.id)
    warnings_data.setdefault(user_id, []).append(
        {
            "reason": reason,
            "moderator": str(interaction.user),
            "timestamp": utc_now_iso(),
        }
    )
    save_warnings(warnings_data)
    await interaction.response.send_message(f"{member.mention} اخطار گرفت. دلیل: {reason}")


@tree.command(name="warnings", description="نمایش اخطارهای کاربر")
@app_commands.describe(member="کاربر مورد نظر")
async def warnings_cmd(interaction: discord.Interaction, member: discord.Member):
    user_warnings = warnings_data.get(str(member.id), [])
    if not user_warnings:
        await interaction.response.send_message(f"{member.mention} هیچ اخطاری ندارد.")
        return
    description = "\n".join(
        f"{i + 1}. {w['reason']} - توسط {w['moderator']}" for i, w in enumerate(user_warnings)
    )
    embed = discord.Embed(title=f"اخطارهای {member.name}", description=description, color=discord.Color.orange())
    await interaction.response.send_message(embed=embed)


@tree.command(name="clearwarnings", description="پاک کردن اخطارها")
@app_commands.describe(member="کاربر مورد نظر", count="تعداد اخطار برای پاکسازی (اختیاری)")
async def clearwarnings(interaction: discord.Interaction, member: discord.Member, count: int = None):
    user_id = str(member.id)
    if not warnings_data.get(user_id):
        await interaction.response.send_message(f"{member.mention} اخطاری ندارد.", ephemeral=True)
        return
    if count and count > 0:
        remaining = max(len(warnings_data[user_id]) - count, 0)
        warnings_data[user_id] = warnings_data[user_id][:remaining]
    else:
        warnings_data[user_id] = []
    save_warnings(warnings_data)
    await interaction.response.send_message(f"اخطارهای {member.mention} پاک شدند.")


# --- Bulk role commands (deferred because they can take a while) ---
@tree.command(name="addroleall", description="دادن رول به همه اعضا")
@app_commands.describe(role="رول برای اضافه کردن")
async def addroleall(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("شما اجازه استفاده از این دستور را ندارید.", ephemeral=True)
        return
    await interaction.response.defer()
    for member in interaction.guild.members:
        try:
            await member.add_roles(role)
        except discord.HTTPException:
            pass
    await interaction.followup.send(f"رول {role.name} به همه اضافه شد.")


@tree.command(name="removeroleall", description="حذف رول از همه اعضا")
@app_commands.describe(role="رول برای حذف")
async def removeroleall(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("شما اجازه استفاده از این دستور را ندارید.", ephemeral=True)
        return
    await interaction.response.defer()
    for member in interaction.guild.members:
        try:
            await member.remove_roles(role)
        except discord.HTTPException:
            pass
    await interaction.followup.send(f"رول {role.name} از همه حذف شد.")


# --- Purge messages ---
@tree.command(name="clear", description="پاک کردن پیام‌ها")
@app_commands.describe(amount="تعداد پیام برای پاکسازی (حداکثر 100)")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("شما اجازه استفاده از این دستور را ندارید.", ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    amount = max(1, min(amount, 100))
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"{len(deleted)} پیام پاک شد.", ephemeral=True)


# --- Info commands ---
@tree.command(name="userinfo", description="نمایش اطلاعات کاربر")
@app_commands.describe(member="کاربر مورد نظر (اختیاری)")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    roles = [r.name for r in member.roles if r.name != "@everyone"]
    embed = discord.Embed(title=f"اطلاعات {member}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="نام", value=member.name)
    embed.add_field(name="تگ", value=member.mention)
    embed.add_field(name="حضور آنلاین", value=str(member.status))
    embed.add_field(name="نقش‌ها", value=", ".join(roles) if roles else "ندارد")
    await interaction.response.send_message(embed=embed)


@tree.command(name="serverinfo", description="نمایش اطلاعات سرور")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"اطلاعات {guild.name}", color=discord.Color.green())
    embed.add_field(name="ID", value=guild.id)
    embed.add_field(name="اعضا", value=guild.member_count)
    embed.add_field(name="کانال‌ها", value=len(guild.channels))
    embed.add_field(name="رول‌ها", value=len(guild.roles))
    embed.add_field(name="مالک سرور", value=str(guild.owner))
    await interaction.response.send_message(embed=embed)


if __name__ == "__main__":
    bot.run(TOKEN)
