from flask import Flask, request, jsonify
import unicodedata
from telethon import TelegramClient, errors, events
import asyncio
import os
import random
from datetime import datetime

# Telegram API credentials
api_id = '25686279'
api_hash = '585e642db1018af44e670f344fb616ef'
phone_number = '+639644135150'

# Initialize Flask app
app = Flask(name)

# Session name for TelegramClient
client = TelegramClient('session_name_itsmerjc', api_id, api_hash)

# Start the Telegram client
async def start_client():
    await client.start(phone=phone_number)

# Luhn algorithm
def luhn_residue(digits):
    sum_digits = 0
    for i, digit in enumerate(reversed(digits)):
        n = int(digit)
        if i % 2 == 0:  # Double every second digit
            n = n * 2
            if n > 9:
                n = n - 9
        sum_digits += n
    return (10 - (sum_digits % 10)) % 10

# Generate a credit card number
def generate_card_number(bin_format):
    digits = list(bin_format)
    while len(digits) < 15:
        digits.append(str(random.randint(0, 9)))
    check_digit = luhn_residue(digits)
    digits.append(str(check_digit))
    return ''.join(digits)

# Generate random expiry date
def generate_expiry_date():
    current_year = datetime.now().year % 100
    current_month = datetime.now().month
    future_year = random.randint(current_year, current_year + 7)
    if future_year == current_year:
        month = random.randint(current_month, 12)
    else:
        month = random.randint(1, 12)
    return f"{str(month).zfill(2)}|{str(future_year).zfill(2)}"

# Generate random CVV
def generate_cvv():
    return str(random.randint(0, 999)).zfill(3)

# Generate card details
def generate_card(bin_format):
    card_number = generate_card_number(bin_format)
    expiry_date = generate_expiry_date()
    cvv = generate_cvv()
    return f"{card_number}|{expiry_date}|{cvv}"

# Read BINs from a text file
def read_bin_list(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        bins = file.readlines()
    return [bin_format.strip() for bin_format in bins]

# Write BINs to a text file
def write_bin_list(filename, bins):
    with open(filename, 'w') as file:
        for bin_format in bins:
            file.write(bin_format + '\n')

# Endpoint to set BINs
@app.route('/setbin', methods=['POST'])
async def set_bin():
    bin_data = request.json.get('bins', '')
    bin_list = [bin.strip() for bin in bin_data.split(',') if bin.strip()]
    
    if bin_list:
        write_bin_list('kido.txt', bin_list)
        return jsonify({"message": "BIN list has been updated", "bins": bin_list}), 200
    else:
        return jsonify({"error": "Please provide valid BIN numbers."}), 400

# Endpoint to generate and send cards
@app.route('/generate', methods=['POST'])
async def generate_and_send_cards():
    chat_id = request.json.get('chat_id', 'bmb0H9EiKU0YzZl')  # Default chat ID
    bin_file = 'kido.txt'
    bin_list = read_bin_list(bin_file)

    results = []
    for bin_format in bin_list:
        card_details = generate_card(bin_format)
        full_command = f"$avs {card_details}"
        
        try:
            sent_message = await client.send_message(chat_id, full_command)
            results.append({"status": "sent", "message": full_command})
            await asyncio.sleep(20)  # Delay between sends
            await delete_message(chat_id, sent_message.id)
        except errors.FloodWaitError as e:
            return jsonify({"error": f"Flood wait for {e.seconds} seconds."}), 429
        except Exception as e:
            results.append({"status": "error", "message": str(e)})
    
    return jsonify({"results": results}), 200

# Function to delete a message
async def delete_message(chat_id, message_id):
    try:
        await client.delete_messages(chat_id, message_id)
        print(f"Deleted message with ID: {message_id}")
    except Exception as e:
        print(f"Failed to delete message: {e}")

# Main function to run the bot
if name == 'main':
    asyncio.run(start_client())
    app.run(port=5000)
