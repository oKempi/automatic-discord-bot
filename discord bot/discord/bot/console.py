import discord
from discord.ext import commands
import asyncio
import csv
from concurrent.futures import ThreadPoolExecutor
import threading
import time as t
import tracemalloc

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
permissions = discord.Permissions()
permissions.use_application_commands = True

bot = commands.Bot(command_prefix="!", intents=intents, strip_after_prefix=True)
tracemalloc.start()

token = "por favor no"
channel_id = 1188897046632071371

async def send(value, channel_id):
    channel = bot.get_channel(channel_id)
    if channel:
        try:
            await asyncio.wait_for(channel.send(value), timeout=5)
        except asyncio.TimeoutError:
            print("Sending message timed out.")

def input_loop():
    while True:
        t.sleep(5)
        comm = input("Input please: ")
        if comm == "start":
            break
        elif comm == "exit":
            exit()
        else:
            try:
                with open("discord\\bot\\database\\commands.csv", "r") as c:
                    csvReader = csv.reader(c)
                    for row in csvReader:
                        if comm in row:
                            try:
                                val = row[1]
                                print(f"Sending code {val} to channel {channel_id}! (normal ID is: 1188897046632071371)")
                                try:
                                    asyncio.run(send(value=val, channel_id=channel_id))
                                    print("Value sent!")
                                except Exception as e:
                                    print(f"Error occurred, value not sent!; {e}")
                                break
                            except IndexError:
                                print("Nope, out of range")
                                break
                    #print("Not found")
            except FileNotFoundError:
                print("File not found")
                break
            except Exception as e:
                print(f"Exception: {e}")
                break

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.content.isdigit():
        print(f"Received a message with content: {message.content}")

def start_bot():
    bot.run(token=token)

# Run the input loop in a separate thread
input_thread = threading.Thread(target=input_loop)
input_thread.start()

# Run the bot in the main thread
start_bot()

#data_to_send = "Hello from script1"
#
# Create a socket
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect(("localhost", 12345))
#    s.sendall(data_to_send.encode())