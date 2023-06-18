import csv
import tracemalloc
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.channels import InviteToChannelRequest

tracemalloc.start()

async def process_phone_numbers(client, phone_numbers, group_link, channel_link):
    for phone_number in phone_numbers:
        try:
            await client(InviteToChannelRequest(channel=group_link, users=[phone_number]))
            await client(InviteToChannelRequest(channel=channel_link, users=[phone_number]))
            print(f"Contact {phone_number} Added to group")
            await asyncio.sleep(1)  # Introduce a 1-second delay between API calls
        except ValueError as e:
            print(f'Skipping {phone_number} because {e}')
            continue
        except Exception as e:
            print(f'Error occurred for {phone_number}: {e}')
            continue

async def create_telegram_group(api_id, api_hash, phone_file, group_link, channel_link):
    # List to store InputPhoneContact objects
    phone_contacts = []

    # Read the phone numbers from the CSV file
    with open(phone_file, 'r') as file:
        csv_reader = csv.reader(file)
        phone_numbers = [row[0] for row in csv_reader]

    # Create InputPhoneContact objects for each phone number
    for phone_number in phone_numbers:
        phone_contact = InputPhoneContact(
            client_id=0,
            phone=phone_number,
            first_name='First Name',
            last_name='Last Name'
        )
        phone_contacts.append(phone_contact)

    # Initialize the Telegram client
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Import contacts
        client(ImportContactsRequest(contacts=phone_contacts))
        print(phone_numbers)

        batch_size = 20
        num_batches = len(phone_numbers) // batch_size + 1

        for i in range(num_batches):
            start = i * batch_size
            end = (i + 1) * batch_size 
            batch_numbers = phone_numbers[start:end]

            await process_phone_numbers(client, batch_numbers, group_link, channel_link)

# Example usage
api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone_file_path = 'phone.csv'
group_invite_link = 'your_group_invite_link'
channel_link = 'your_channel_link'

# Run the async function in an event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(create_telegram_group(api_id, api_hash, phone_file_path, group_invite_link, channel_link))
