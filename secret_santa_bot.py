import pathlib
import os
import sys
import re
import pickle
import os.path
import sys
import discord
from generate_pairs import create_pairing
from data_XXXX import penultimate_christmas_dict, previous_christmas_dict, couple_dict, users, id_to_display_name

LONGSTONE_GUILD = 704366096165109770

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
                # "thomas5564"
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
        # TODO cache/store locally members ?
        members = await self.get_longstone_guild().chunk() 
        to_member = find(lambda m: m.name == to, members)
        if(not to_member):
            print(f"Couldn't find the member {to}")
        else:
            print(await to_member.send(text))
    
    async def reply_members(self, message):
        members = await self.get_longstone_guild().chunk()
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
            await self.dm(from_id, f"Le tirage a été effectué, tu dois offrir un cadeau à {id_to_display_name[to_id]}")
            print('sent dm', from_id, to_id, f"Le tirage a été effectué, tu dois offrir un cadeau à {id_to_display_name[to_id]}");
        await self.send_general("Le tirage au sort a été réalisé, vous devriez avoir reçu un message privé de ma part.")
        print('finished secret santa');

def retrieveToken():
    # Check environment variable first
    token = os.getenv('SECRET_SANTA_TOKEN')
    if token:
        return token.strip()
    
    # Fallback to file in parent directory
    with open(pathlib.Path(os.getcwd()).parent / 'tokenSecretSanta') as f:
        return f.readline().strip()

if __name__ == '__main__':
    try:
        token = retrieveToken()
    except OSError as e:
        print("Could not retrieve the token of the bot (", e, ")")
        sys.exit(1)

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = MyClient(intents=intents)
    client.run(retrieveToken())