from config import TRAIT_CONFIG
import math
from PIL import Image, ImageDraw
import random
from pprint import pprint
import requests
from dotenv import load_dotenv
import os

load_dotenv()

PINATA_JWT = os.getenv("PINATA_JWT")

PINATA_BASE_URL="https://api.pinata.cloud"

IMAGE_WIDTH = 631
IMAGE_HEIGHT = 631

WHITE = "#ffffff"

TOTAL_NFT = 100

trait_distribution = {
  "hat": {
    "square": 10,
    "circle": 30,
    "triangle": 60
  },
  "eyes": {
    "glasses": 10,
    "sleepy": 30,
    "wide-eyed": 60,
  },
  "mouth": {
    "smile": 10,
    "shout": 30, 
    "frown": 60,
  },
}

# Keep count while generating
trait_generated_count = {
  "hat": {
    "square": 0,
    "circle": 0,
    "triangle": 0
  },
  "eyes": {
    "glasses": 0,
    "sleepy": 0,
    "wide-eyed": 0,
  },
  "mouth": {
    "smile": 0,
    "shout": 0, 
    "frown": 0,
  },
}

"""
generate character with their traits
"""
def generate_characters():
  trait_keys = trait_distribution.keys()
  characters = []

  for i in range(TOTAL_NFT):
    char = {}
    for trait in list(trait_keys):
      char[trait] = ""
    for trait in trait_keys:
      trait_variations = trait_distribution[trait].keys()
      variation = ""
      can_generate = False
      while can_generate is False:
        variation = random.choice(list(trait_variations))
        trait_max_count = trait_distribution[trait][variation]
        trait_curr_count = trait_generated_count[trait][variation]
        can_generate = trait_curr_count < trait_max_count
      char[trait] = variation
      trait_generated_count[trait][variation] += 1
    
    characters.append(char)

  return characters


"""
generate character image based on character's traits
@return image path
"""
def generate_character_image(character, i):
  img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
  bg = ImageDraw.Draw(img)
  bounding_box = [(0, 0), (IMAGE_WIDTH, IMAGE_HEIGHT)]
  bg.rectangle(bounding_box, fill=WHITE, outline="black")

  img_char = Image.open("./images_in/character.png")
  img.paste(img_char, (0, 0), img_char)

  for trait in list(trait_distribution.keys()):
    trait_var = character[trait]
    trait_var_img_path = TRAIT_CONFIG[trait]["variations"][trait_var]["image"]
    img_trait_var = Image.open(trait_var_img_path)
    img.paste(img_trait_var, (0, 0), img_trait_var)

  img_out_path = "./images_out/" + f"{i+1}"
  trait_vars = [character[trait] for trait in list(trait_distribution.keys())] 
  for trait_var in trait_vars:
    img_out_path += f"_{trait_var}"
  img_out_path += ".png"

  img.save(img_out_path)

  return img_out_path


def upload_image_to_ipfs(img_path):
  headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {PINATA_JWT}"
  }
  files = {"file": open(img_path, "rb")}
  resp = requests.post(f"{PINATA_BASE_URL}/pinning/pinFileToIPFS", headers=headers, files=files)
  return resp.json()["IpfsHash"]

def generate_opensea_metadata():
  pass

def main():
  characters = generate_characters()
  print(characters)
  for i, c in enumerate(characters):
    img_out_path = generate_character_image(c, i)
    ipfs_hash = upload_image_to_ipfs(img_out_path)
    print(ipfs_hash)
    # TODO:
    # bikin metadata
    # upload ke ipfs
    # list metadata disimpen ke file

if __name__ == "__main__":
  main()
