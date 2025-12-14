import pathlib
import os
import sys
import re
import pickle
import os.path
import sys
import json
import discord
from generate_pairs import create_pairing

LONGSTONE_GUILD = 704366096165109770

# Global variables for data
users = []
id_to_display_name = {}
penultimate_christmas_dict = {}
previous_christmas_dict = {}
couple_dict = {}

def load_data(json_file):
    """Load secret santa data from JSON file"""
    global users, id_to_display_name, penultimate_christmas_dict, previous_christmas_dict, couple_dict
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    users = data.get('users', [])
    id_to_display_name = data.get('id_to_display_name', {})
    penultimate_christmas_dict = data.get('penultimate_christmas_dict', {})
    previous_christmas_dict = data.get('previous_christmas_dict', {})
    couple_dict = data.get('couple_dict', {})

# https://tomayko.com/blog/2004/cleanest-python-find-in-list-function
def find(f, seq):
  """Return first item in sequence where f(item) == True."""
  for item in seq:
    if f(item): 
      return item

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # members = self.get_all_members()
        # await self.guilds[0].leave()
        try:
            self.get_longstone_guild()
        except Exception:
            print(f"Not connected to the longstone guild! (LONGSTONE_GUILD)")
    
    def get_longstone_guild(self):
        guild = find(lambda guild: guild.id == LONGSTONE_GUILD, self.guilds)
        if not guild:
            raise Exception("Not connected to the longstone guild! " + 
                             f"(id {LONGSTONE_GUILD})")
        return guild
    
    def get_longstone_members(self):
        guild = self.get_longstone_guild()

        if (not guild.members):
            return []
        return guild.members
    

    def get_longstone_member(self, member_name):
        members = self.get_longstone_members()
            
        if (not members):
            print("No members in guild")
            return None
        
        to_member = find(lambda m: m.name == member_name or
                            m.display_name == member_name, members)
        return to_member

        

    async def on_message(self, message):
        # do not respond to own messages
        if message.author == client.user:
            return
        
        # only respond if in the longstone guild
        # ! message.guild is None when receiving a DM
        # if not message.guild or message.guild.id != LONGSTONE_GUILD:
        #     print("ignore non-longstone message", message)
        #     return

        if isinstance(message.channel, discord.DMChannel):
            print('private message')
        
        print(f'Message from {message.author}: {message.content}. {message.channel}')

        if message.content.startswith('!members'):
            await self.reply_members(message)

        elif message.content.startswith('!dm'):
            match = re.match(r'!dm (.+?) (.+)', message.content)
            if match:
                to = match.group(1)
                text = match.group(2)
                await self.dm(to, text)
        
        elif message.content.startswith('!speak'):
            match = re.match(r'!speak (.+)', message.content)
            if match:
                text  = match.group(1)
                await self.send_general(text)
        
        elif message.content.startswith('!data'):
            await self.reply_data(message)
        
        elif message.content.startswith('!testsecretsanta'):
            await self.test_secretsanta(message)

        elif message.content.startswith('!runsecretsanta'):
            await self.runsecretsanta()

    async def send_general(self, text):
        await self.get_longstone_guild().system_channel.send(text)

    async def dm(self, to, text):

        member = self.get_longstone_member(to)

        if(not member):
            print(f"Couldn't find the member {to}")
            return None
        try:
            dm_message = await member.send(text)
            print(f"DM sent to {to}: {text}")
            return dm_message
        except discord.Forbidden:
            print(f"Cannot send DM to {to} - user has DMs disabled or bot is blocked")
            return None
        except Exception as e:
            print(f"Error sending DM to {to}: {e}")
            return None
    
    async def reply_members(self, message):

        guild = self.get_longstone_guild()

        if (not guild.members):
            print("No members in guild")
            return None
        
        members = guild.members
        print("members:")
        print([(member.name, member.display_name) for member in members])
        print()
        reply = "Members found : \n\n" + \
            ',\n'.join([f'("{discord.utils.escape_markdown(member.name)}", "{discord.utils.escape_markdown(member.display_name)}")' for member in members])
        await message.reply(reply)
    
    async def reply_data(self, message):
        reply = f"users : {users}" + \
        "\n\n" + \
        f"id_to_display_name : {id_to_display_name}" + \
        "\n\n" + \
        f"couple_dict : {couple_dict}" + \
        "\n\n" + \
        f"penultimate_christmas_dict : {penultimate_christmas_dict}" + \
        "\n\n" + \
        f"previous_christmas_dict : {previous_christmas_dict}"
        await message.reply(discord.utils.escape_markdown(reply))
    
    async def test_secretsanta(self, message):
        print()
        print("Testing secret santa")

        pairings = create_pairing(
            users,
            couple_dict,
            penultimate_christmas_dict,
            previous_christmas_dict)

        await self.reply_data(message)

        print("pairings generated")
        print(pairings)

        reply = f"pairings generated: {pairings}"
        await message.reply(discord.utils.escape_markdown(reply))


    async def runsecretsanta(self):
        print()
        print("Running secret santa")
        # todo : should validate that the data from data_20xx.py is correct, including checking that every user id exists
        pairings = create_pairing(
            users,
            couple_dict,
            penultimate_christmas_dict,
            previous_christmas_dict)
        
        print("pairings generated")
        print(pairings)
        
        # backup
        print("saving pairings")
        with open('secretsanta.bin', 'wb') as file:
            pickle.dump(pairings, file)


        # send secret santa to everybody
        print('sending dms')
        for (from_id, to_id) in pairings:
            message = f"Le tirage a été effectué, tu dois offrir un cadeau à {id_to_display_name[to_id]}"
            dm = await self.dm(from_id, message)
            print(f"DM to {from_id} : {dm}")
            
        await self.send_general("Le tirage au sort a été réalisé, vous devriez avoir reçu un message privé de ma part.")
        print('finished secret santa')

def retrieveToken():
    # Check environment variable first
    token = os.getenv('SECRET_SANTA_TOKEN')
    if token:
        return token.strip()
    
    # Fallback to file in parent directory
    with open(pathlib.Path(os.getcwd()).parent / 'tokenSecretSanta') as f:
        return f.readline().strip()

if __name__ == '__main__':
    # Check for JSON file argument
    if len(sys.argv) < 2:
        print("Usage: python secret_santa_bot.py <data_file.json>")
        print("Example: python secret_santa_bot.py data_2025.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    # Load data from JSON file
    try:
        load_data(json_file)
        print(f"Data loaded successfully from {json_file}")
        print(f"Participants: {len(users)} users")
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{json_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data from '{json_file}': {e}")
        sys.exit(1)
    
    # Retrieve bot token
    try:
        token = retrieveToken()
    except OSError as e:
        print("Could not retrieve the token of the bot (", e, ")")
        sys.exit(1)

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = MyClient(intents=intents)
    client.run(token)