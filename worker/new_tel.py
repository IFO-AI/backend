import asyncio
from telethon import TelegramClient, events


from environment import Config


# Get the environment variables
api_id = Config.get("TELEGRAM_API_ID")
api_hash = Config.get("TELEGRAM_API_HASH")


async def main():
    async with TelegramClient('ifo_session_name', api_id, api_hash) as client:
        data = await client.get_me()
        print(data)
        @client.on(events.ChatAction()) # Match any group invite link format
        async def handle_invite_link(event):
            print(event)
            link = event.message.text.strip()
            print(link)
            try:
                pass
                # await client(ImportChatInviteRequest(link.split('/')[-1]))  # Join the group using the invite hash
                # chat = await client.get_entity(event.chat_id)  # Get chat information
                # initial_members = await client(GetParticipantsRequest(chat, filter=chat.participants.admin.id))  # Get initial admin(s)

                # # Function to send welcome message to new members
                # async def send_welcome_message(new_member):
                #     if new_member not in initial_members.users:  # Check if user wasn't already an admin
                #         try:
                #             await client.send_message(new_member.id, "Welcome to the group! ")
                #         except Exception as e:
                #             print(f"Error sending message to {new_member.id}: {e}")

                # @client.on(events.UpdateNewChatMembers(**{'chat_id': chat.id}))
                # async def handle_new_members(event):
                #     for new_member in event.new_members:
                #         await send_welcome_message(new_member)

            except Exception as e:
                print(f"Error processing invite link: {e}")

        await client.start()
        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
