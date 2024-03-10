import aiohttp
from telethon import TelegramClient, events
from telethon.tl.functions.channels import CreateChannelRequest, EditBannedRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import ChatBannedRights
from telethon.errors import SessionPasswordNeededError
from datetime import timedelta, datetime

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

api_id = ''  # Your API ID
api_hash = ''  # Your API Hash
phone = ''  # Your phone number, including the country code
secret_key_base58 = '' # Your secret key in base58 format
public_key = '' # Your public key


async def create_keypair():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:3000/create-keypair') as response:
            if response.status == 200:
                data = await response.json()
                return data['keypair']
            else:
                # Handle error
                return None


async def send_tokens(destination_wallet, secret_key_base58, mint):
    async with aiohttp.ClientSession() as session:
        payload = {'destinationWallet': destination_wallet, 'secretKeyBase58': secret_key_base58, 'mint': mint}
        async with session.post('http://localhost:3000/send-tokens', json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data['tx']
            else:
                # Handle error
                return None


async def create_ata(owner, secret_key_base58, mint):
    async with aiohttp.ClientSession() as session:
        payload = {'owner': owner, 'secretKeyBase58': secret_key_base58, 'mint': mint}
        async with session.post('http://localhost:3000/create-ata', json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data['accountInfo']
            else:
                # Handle error
                return None


async def create_and_send_token(destination_wallet, secret_key_base58):
    async with aiohttp.ClientSession() as session:
        payload = {
            'destinationWallet': destination_wallet,
            'secretKeyBase58': secret_key_base58
        }
        async with session.post('http://localhost:3000/create-and-send-token', json=payload) as response:
            if response.status == 200:
                data = await response.json()
                return data  # Assuming data contains the 'transactionId' and 'mint'
            else:
                # Handle error
                return None


async def create_supergroup_and_invite_link(client, title, description):
    # Connect to the client
    await client.connect()
    
    # Ensure you're authorized
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
    
    # # Create the supergroup
    # result = await client(CreateChannelRequest(
    #     title=title,
    #     about=description,
    #     megagroup=True  # Set True to create a supergroup
    # ))
    # print(result)
    # channel = result.chats[0]
    # print(f'Supergroup "{title}" created with ID: {channel.id}')

    # API HIT TO CREATE A TOKEN
    # token_creation_response = await create_and_send_token(public_key, secret_key_base58)
    # print(f"Token created and sent to {public_key}: Transaction ID {token_creation_response['transactionId']}, Mint {token_creation_response['mint']}")

    # Generate an invite link
    invite_link_result = await client(ExportChatInviteRequest(
        peer=2122726039,
        # peer=channel.id,
        legacy_revoke_permanent=True,
        request_needed=False,
        usage_limit=0
    ))
    print(invite_link_result)
    print(f'Invite link: {invite_link_result.link}')

    # return channel.id, invite_link_result.link, token_creation_response['mint']
    return 2122726039, invite_link_result.link, 'CgVkauhXeUtmy7x7RULzFkJL7jpM1bSN7p44Z4yDjaEX'


async def fetch_all_users(client, channel_id):
    offset = 0
    limit = 100
    all_participants = []

    while True:
        participants = await client(GetParticipantsRequest(
            channel_id, ChannelParticipantsSearch(''), offset, limit, hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
    
    return all_participants

async def main():
    title = "IFO Project"
    description = "An IFO Project for the Solana Hackathon."
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Create the supergroup and get its invite link
        res = await create_supergroup_and_invite_link(client, title, description)
        mint = res[2]
        print(f"mint: {mint}")

        # Fetch and print all users in the group
        channel_username = '2122726039'  # Replace with your group's username or ID
        all_users = await fetch_all_users(client, channel_username)
        for user in all_users:
            print(user.id, user.first_name, user.username)

        # Setup listener for new members joining
        @client.on(events.ChatAction())
        async def handler(event):
            print("Event detected:", event)
            if event.user_joined:
                print(f"{event.user_id} - {event.get_user()} has joined the group.")
            elif event.user_left:
                print(f"{event.user_id} has left the group.")


            # # Check if the event is someone joining
            # if event.user_joined or event.user_added:
            #     new_user = await event.get_user()
            #     username = new_user.username if new_user.username else new_user.first_name
            #     print(f"{username} has joined the group!")

            #     # Create keypair for the new user
            #     keypair = await create_keypair()
            #     print(f"Keypair created for {username}: {keypair['publicKey']}")

            #     # SEND AN API HIT TO SEND TOKENS TO THE USER
            #     await create_ata(keypair['publicKey'], secret_key_base58, mint)
            #     await create_ata(public_key, secret_key_base58, mint)

            #     tx = await send_tokens(keypair['publicKey'], secret_key_base58, mint)
            #     print(f"Tokens sent to {username}: Transaction ID {tx}")

            #     # Restricting the new user's ability to send messages for 30 seconds
            #     rights = ChatBannedRights(
            #         until_date=datetime.now() + timedelta(seconds=30),  # Restriction duration of 30 seconds
            #         send_messages=True,
            #         view_messages=True
            #     )

            #     await client(EditBannedRequest(
            #         channel=event.chat_id,
            #         participant=new_user.id,
            #         banned_rights=rights
            #     ))
            #     print(f"Restrictions applied to {username} for 30 seconds.")

            #     # Send a welcome message to the new user
            #     welcome_message = f"""
            #         Welcome to the group, {username}!

            #         100 tokens have been sent to your wallet on Solana.
            #         Here is your public key: {keypair['publicKey']}
            #         Here is your private key: {keypair['privateKey']}

            #         Please keep your private key safe and do not share it with anyone.
            #     """
            #     await client.send_message(new_user.id, welcome_message)
            #     print(f"Sent welcome message to {username}.")

        print("Listening for new members...")
        await client.run_until_disconnected()


import asyncio
asyncio.run(main())
