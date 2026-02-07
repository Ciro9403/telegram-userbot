import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import InviteHashExpired, InviteHashInvalid

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

app = Client("userbot", api_id=api_id, api_hash=api_hash)

LINKS_FILE = "links.txt"

async def check_link(link: str):
    try:
        chat = await app.join_chat(link)
        await app.leave_chat(chat.id)
        return "VALIDO"
    except InviteHashExpired:
        return "SCADUTO / BANNATO"
    except InviteHashInvalid:
        return "NON VALIDO"
    except Exception as e:
        return f"ERRORE: {str(e)}"

@app.on_message(filters.regex(r"https?://t\.me/\S+"))
async def monitor_links(client, message):
    link = message.matches[0].group(0)

    with open(LINKS_FILE, "a") as f:
        f.write(link + "\n")

    print(f"[TROVATO] {link}")

@app.on_message(filters.command("checklinks"))
async def check_all(client, message):
    if not os.path.exists(LINKS_FILE):
        await message.reply("Nessun link salvato.")
        return

    with open(LINKS_FILE, "r") as f:
        links = [l.strip() for l in f.readlines()]

    report = "🔍 **Report link privati**\n\n"

    for link in links:
        status = await check_link(link)
        report += f"- {link} → **{status}**\n"

    await message.reply(report)

app.run()
