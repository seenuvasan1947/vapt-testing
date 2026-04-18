import os, sys, asyncio
from pyrogram import Client

API_ID   = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION  = os.environ['SESSION']
CHAT_ID  = int(os.environ['CHAT_ID'])
target   = os.environ['TARGET_NAME']
dest     = os.environ['TG_DEST']

async def run():
    app = Client("tg_session", api_id=API_ID, api_hash=API_HASH,
                 session_string=SESSION, no_updates=True)
    async with app:
        await app.get_chat(CHAT_ID)  # populate peer cache
        async for msg in app.search_messages(chat_id=CHAT_ID, query=target):
            if msg.document and os.path.basename(msg.document.file_name) == os.path.basename(target):
                print(f"[+] Found: {msg.document.file_name}", flush=True)
                await msg.download(file_name=dest)
                print(f"[+] Downloaded to: {dest}", flush=True)
                sys.exit(0)
    print(f"[-] Not found: {target}", flush=True)
    sys.exit(1)

asyncio.run(run())
