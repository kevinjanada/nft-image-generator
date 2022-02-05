from config import TRAIT_CONFIG
import math
from PIL import Image, ImageDraw
import random
from pprint import pprint

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


def create_bg(img, bg_color):
  bg = ImageDraw.Draw(img)
  bounding_box = [(0, 0), (IMAGE_WIDTH, IMAGE_HEIGHT)]
  bg.rectangle(bounding_box, fill=bg_color, outline="black")
  return img

def main():
  characters = generate_characters()
  for i, c in enumerate(characters):
    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
    img = create_bg(img, WHITE)

    img_char = Image.open("./images_in/character.png")
    img.paste(img_char, (0, 0), img_char)

    for trait in list(trait_distribution.keys()):
      trait_var = c[trait]
      trait_var_img_path = TRAIT_CONFIG[trait]["variations"][trait_var]["image"]
      img_trait_var = Image.open(trait_var_img_path)
      img.paste(img_trait_var, (0, 0), img_trait_var)

    img_out_path = "./images_out/" + f"{i+1}"
    trait_vars = [c[trait] for trait in list(trait_distribution.keys())] 
    for trait_var in trait_vars:
      img_out_path += f"_{trait_var}"
    img_out_path += ".png"

    img.save(img_out_path)

if __name__ == "__main__":
  main()
