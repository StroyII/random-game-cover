from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import textwrap
from io import BytesIO
import requests
import random
import math
import os

# Environment
load_dotenv()
API_KEY = os.getenv("RAWG_API_KEY")
API_URL = "https://api.rawg.io/api"
PAGE_SIZE = 40
FILENAME = "cover.png"
BACKUPGAMENAME = "Yo-kai Watch Dance: Just Dance Special Version"
BACKUPGAMEIMAGE = "https://static.wikia.nocookie.net/justdance/images/c/c3/Youkaiwatchdance.png"

def getGamePage(url:str,key:str,page:int=1,numerByPage:int=1)->dict:
    """
    Function to fetch the RAWG api
    """
    complete_url = url + "/games?key=" + key
    response = requests.get(complete_url, {"page":page,"page_size":numerByPage})
    data = response.json()

    return data

def saveImagePng(image_url:str, filename:str, game_name:str):
    """
    Function to save an image in png 
    """
    response = requests.get(image_url)

    image = Image.open(BytesIO(response.content)).convert("RGBA")

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    band_height = 120
    overlay_draw.rectangle([(0, image.height - band_height), (image.width, image.height)],fill=(0, 0, 0, 150))

    image = Image.alpha_composite(image, overlay)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("fonts/comicsansms.ttf", 48)
    except:
        font = ImageFont.load_default()

    wrapped_name = "\n".join(textwrap.wrap(game_name, width=30))

    draw.text((40, image.height - band_height + 30),wrapped_name,font=font,fill=(255, 255, 255, 255))

    image.save("cover/"+filename, "PNG")

def chooseRandomGame(max_try:int=20)->dict:
    """
    Function to choose a random game
    """
    
    # Choose a random page in the api
    numberOfGame = getGamePage(API_URL,API_KEY)["count"]
    total_page = math.ceil(numberOfGame / PAGE_SIZE)

    for i in range(max_try):
        random_page = random.randint(1, total_page)
        games = getGamePage(API_URL,API_KEY,random_page,PAGE_SIZE)["results"]

        valid_games = [g for g in games if g.get("background_image")]

        if valid_games:
            return random.choice(valid_games)

    return None

# Fetch a random game in the page
choosen_game = chooseRandomGame(20)

if choosen_game:
    game_name = choosen_game["name"]
    image_url = choosen_game["background_image"]
else:
    game_name = BACKUPGAMENAME
    image_url = BACKUPGAMEIMAGE
    
saveImagePng(image_url,FILENAME,game_name)
