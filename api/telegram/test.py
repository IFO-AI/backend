import asyncio
from tel import create_supergroup_and_invite_link
loop = asyncio.get_event_loop()

def crete_telegram_group(title, desc):
    a, b, c = loop.run_until_complete(create_supergroup_and_invite_link(title,desc)) 
    print("Telegram group created")
    print(a,b,c)
    return b