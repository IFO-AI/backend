# import asyncio
# from telethon import TelegramClient, events
# from api.helper.environment import Config
# from api.helper.tel import create_supergroup_and_invite_link
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# api_id = Config.get("TELEGRAM_API_ID")
# api_hash = Config.get("TELEGRAM_API_HASH")
# def crete_telegram_group(title, desc):
#     client = TelegramClient('ifo_session_name', api_id, api_hash) 
#     a, b, c = loop.run_until_complete( create_supergroup_and_invite_link(client,title,desc)) 
#     print("Telegram group created")
#     print(a,b,c)
#     return b