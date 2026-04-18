import os, sys, asyncio, subprocess
from pathlib import Path

BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID   = os.environ['CHAT_ID']
API_ID    = int(os.environ['API_ID'])
API_HASH  = os.environ['API_HASH']
SESSION   = os.environ['SESSION']
basename  = os.environ['SCAN_BASENAME']
result_zips = [z for z in os.environ['RESULT_ZIPS'].strip().split('\n') if z]

def send_bot_api(filepath, caption):
    cmd = ['curl', '-s',
           '-F', f'chat_id={CHAT_ID}',
           '-F', f'caption={caption}',
           '-F', f'document=@{filepath}',
           f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument']
    subprocess.run(cmd)

async def send_pyrogram(filepath, caption):
    from pyrogram import Client
    app = Client('tg_session', api_id=API_ID, api_hash=API_HASH,
                 session_string=SESSION, no_updates=True)
    async with app:
        await app.get_chat(int(CHAT_ID))  # populate peer cache
        await app.send_document(chat_id=int(CHAT_ID), document=filepath, caption=caption)
    print(f"Sent via Pyrogram: {filepath}")

for rzip in result_zips:
    if not rzip or not Path(rzip).exists():
        continue

    size_bytes = Path(rzip).stat().st_size
    size_mb    = size_bytes / (1024 * 1024)
    caption    = f"Results: {basename}"

    if size_bytes <= 52428800:  # 50 MB
        print(f"Sending {Path(rzip).name} ({size_mb:.1f}MB) via Bot API...")
        send_bot_api(rzip, caption)
    else:
        print(f"Sending {Path(rzip).name} ({size_mb:.1f}MB) via Pyrogram...")
        try:
            asyncio.run(send_pyrogram(rzip, caption))
            print(f"Sent via Pyrogram: {size_mb:.1f}MB")
        except Exception as e:
            print(f"Failed to send {rzip}: {e}")
            sys.exit(1)
