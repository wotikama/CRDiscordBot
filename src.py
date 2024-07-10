import requests
import discord
import json
import array
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents(messages=True))
@bot.event 
async def on_ready():
        print("Bot is Up and Ready!")
        try: 
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)
@bot.tree.command(name="deck")
@app_commands.describe(name = "Who do you want to see?")
async def deck(interaction: discord.Interaction, name: str):
        await interaction.response.defer()
        #await interaction.response.send_message(f"{interaction.user.name} said: `{name}`", ephemeral=True)
        header = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }
        url= "https://royaleapi.com/player/search/results?q="
        url +=name
        html_content = requests.get(url, headers=header).text
        soup = BeautifulSoup(html_content, "html.parser")
        response = soup.find_all(class_= "ui attached segment player_search_results__result_container")
        matches = len(response)
        # print(response[0].text.replace(" ", "").replace("Pro", "").replace("SupercellCreator", "").split())
        if matches >5:
            matches=5
        for i in range(0, matches):
            if response[i].text.replace(" ", "").replace("Pro", "").split()[2] != "Banned":
                player_info = response[i].text.replace(" ", "").replace("Pro", "").replace("SupercellCreator", "").split()
                player = player_info[1]
                player_tag = player_info[2].replace("#", "")
                url="https://api.clashroyale.com/v1/players/%23"
                url +=player_tag
                deck = []
                r=requests.get( url, headers={"Accept":"application/json", "authorization":"Bearer <YOU_CR_API_KEY_HERE>"}, params = {"limit":20})
                data=json.dumps(r.json(), indent = 2)
                datajson=json.loads(data)
                for j in datajson['currentDeck']:
                    img_url=j['iconUrls']['medium']
                    deck.append(Image.open(requests.get(img_url, stream=True).raw))
                image = Image.new('RGBA', (deck[0].width + deck[1].width + deck[2].width + deck[3].width + deck[4].width + deck[5].width + deck[6].width + deck[7].width, deck[1].height))
                image.paste(deck[0], (0, 0))
                image.paste(deck[1], (deck[1].width*1, 0))
                image.paste(deck[2], (deck[1].width*2, 0))
                image.paste(deck[3], (deck[1].width*3, 0))
                image.paste(deck[4], (deck[1].width*4, 0))
                image.paste(deck[5], (deck[1].width*5, 0))
                image.paste(deck[6], (deck[1].width*6, 0))
                image.paste(deck[7], (deck[1].width*7, 0))
                if len(response[i].text.replace(" ", "").replace("Pro", "").split()) >= 5:
                    clan = player_info[3]
                    clan_tag = player_info[4].replace("#","")
                    bytes = BytesIO()
                    image.save(bytes, format="PNG")
                    bytes.seek(0)
                    dfile = discord.File(bytes, filename="image.png")
                    player += '   ||  '+clan
                    await interaction.followup.send(player,file=dfile)
                else:
                    bytes = BytesIO()
                    image.save(bytes, format="PNG")
                    bytes.seek(0)
                    dfile = discord.File(bytes, filename="image.png")
                    await interaction.followup.send(player,file=dfile)
bot.run ('YOUR_TOKEN')




