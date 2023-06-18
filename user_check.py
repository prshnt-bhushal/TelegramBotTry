import csv
import time
from telethon.sync import TelegramClient

# Telegram API credentials
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

# CSV file paths
input_file = 'phone.csv'
output_file = 'users.csv'

# Connect to Telegram
with TelegramClient('session', api_id, api_hash) as client:
    # Read input CSV file
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        # Open output CSV file for writing
        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(['Number'])  # Write header

            # Iterate over numbers in input file
            for row in reader:
                number = row[0]

                # Check if number has an ID in Telegram
                try:
                    entity = client.get_entity(number)
                    writer.writerow([number])  # Write to output file
                    print(f"Number {number} has an ID in Telegram. Stored in output file.")
                except ValueError:
                    print(f"Number {number} does not have an ID in Telegram.")

                # Wait for 2 seconds
                time.sleep(1)
