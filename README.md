# Longstone Secret Santa Discord Bot

- generate_pairs.py : algorithm to generate pairs of gifter -> giftee
- secret_santa_bot.py : Discord bot to generate pairs and announce the results on Discord
- data_20xx.json : data needed to run a secret santa draw

*Not* included in the repository : the Discord bot (application) token file (tokenSecretSanta).

## How to run a secret santa

It's a simple 10 steps process. *Hurrah!*

1) Clone this repository 
2) Create a python environment (optional but recommended)
   ```bash
   python -m venv .venv

   #activate the environment
   source .venv/bin/activate #Linux/Mac 
   .venv\Scripts\activate #Windows
   ```
3) Install dependencies 
   ```bash
   pip install -r requirements.txt
   ```

4) Generate the bot token, store it in a file named *tokenSecretSanta* in the parent directory of Longstone_Christmas_DiscordBot or set the environment variable `SECRET_SANTA_TOKEN`.  
   ```bash
   # store in a file
   echo "your_discord_bot_token_here" > ../tokenSecretSanta
   ```
   or 
   ```bash
   # set environment variable
   export SECRET_SANTA_TOKEN="your_discord_bot_token_here"  # Linux/Mac
   setx SECRET_SANTA_TOKEN "your_discord_bot_token_here"  # Windows
   ```
5) Copy the last `data_20xx.json` file and update it for the current year. See below: [Updating data for a new year](#updating-data-for-a-new-year)

6) Start the discord bot  
   ```bash
   cd Longstone_Christmas_DiscordBot
   python secret_santa_bot.py data_20xx.json
   ```  

7) Test that the bot works with discord.  
   Eg. send it the !dm command in a DM message to ask it to send a message to someone : `!dm <userID> Bonjour mon enfant!`

8) Test the secret santa draw without sending messages to users or saving the result  
   Send a DM to the bot with the command : `!testsecretsanta`

9) If the draw works, run draw with `!runsecretsanta`, the result will probably be different from the test draw.  
   
10) Push the `secretsanta.bin` to the repository with a name like `secretsanta20xx.bin`  
   ```bash
   mv secretsanta.bin secretsanta20xx.bin
   git add secretsanta20xx.bin
   git commit -m "secretsanta 20xx results"
   git push
   ``` 

## Bot commands
Commands to make the bot perform an action. Send a DM to the bot.  
This is not protected, anybody can make the bot perform an action!

- !members : list of members on the discord group
- !dm from_user_id message : make the bot send a message to someone
- !speak message : send a message to the general chat
- !data : print all the data used to make a draw
- !testsecretsanta : make a draw but do not send the messages to users, do not save it to secretsanta.bin either
- !runsecretsanta : make a draw and send a message to each member with the person the member must send a gift to. Careful!

## Updating data for a new year
When updating the data for a new year (eg. from 2024 to 2025), make sure to update like the example below.

_list of users participating in the secret santa_

> [!WARNING]
>
>Be careful, the code doesn't check that the data is correct. Make sure :
>- every user_id exists in the discord (*!members*), 
>- in the data, the strings are the discord ids and not the display name (except for *id_to_display_name* value) example : "bylex0802" not "ByLex"
>- the id of an user can change! (check with *!members*)
>- every id in *user* is also in *id_to_display_name*

```json
"users": [
   "bylex0802",
   "romain4956",
   "vivianus3950",
   "_meliz_",
   "cricri7570",
   "Cinducci",
   "lucine2884",
   "barbieguuurl",
   "thomas5564"
],
```

_use the bot !members command to update if needed, if an id changed : must change in all the other variables!_
```json
"id_to_display_name": {
   "thomas5564": "ThomasB",
   "bylex0802": "ByLex",
   "_meliz_": "méliz",
   "barbieguuurl": "BarbieGurl",
   "romain4956": "Romain",
   "vivianus3950": "vivianus3950",
   "Cinducci": "Cinducci",
   "LoloManzo": "Lolomanzo",
   "lucine2884": "Lucine",
   "cricri7570": "Cricri"
},
```
_dict of : gifter -> person who receives the gift from two christmases ago_
```json

"penultimate_christmas_dict": {
   "bylex0802": "LoloManzo",
   "vivianus3950": "Cinducci",
   "_meliz_": "barbieguuurl",
   "cricri7570": "vivianus3950",
   "LoloManzo": "lucine2884",
   "Cinducci": "_meliz_",
   "lucine2884": "cricri7570",
   "barbieguuurl": "thomas5564",
   "thomas5564": "bylex0802"
},
```

_dict of : gifter -> person who receives the gift from last christmases ago_

can be retrieved from secretsanta.bin

```bash
python printsecretsantabin.py secretsanta20xx.bin
```

```json
"previous_christmas_dict": {
   "bylex0802": "vivianus3950",
   "vivianus3950": "barbieguuurl",
   "_meliz_": "lucine2884",
   "cricri7570": "thomas5564",
   "Cinducci": "cricri7570",
   "lucine2884": "bylex0802",
   "barbieguuurl": "_meliz_",
   "thomas5564": "Cinducci"
}
```

_couple data, example:_
```bash
# ! two lines required for each couple:
#   'Him' : 'Her',
#   'Her' : 'Him',
#   or 
#   'Him' : 'Him',
#   'Her' : 'Her',
```

```json
"couple_dict": {
   "bylex0802": "Cinducci",
   "vivianus3950": "lucine2884",
   "Cinducci": "bylex0802",
   "lucine2884": "vivianus3950",
   "_meliz_": "thomas5564",
   "thomas5564": "_meliz_",
   "cricri7570": "LoloManzo",
   "LoloManzo": "cricri7570"
}
```


