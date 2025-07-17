# app/services.py

import random
import string
from django.conf import settings
from cryptography.fernet import Fernet

# --- Password Generation Service ---

_verbs = [
    "alert", "amused", "annoyed", "anxious", "ashamed", "blue", "brainy", "brave",
    "bright", "busy", "calm", "careful", "clean", "clear", "clever", "cloudy",
    "crowded", "curious", "cute", "dark", "dizzy", "drab", "dull", "eager",
    "easy", "elated", "elegant", "excited", "fair", "famous", "fancy", "fine",
    "funny", "gentle", "gifted", "good", "happy", "healthy", "helpful", "hungry",
    "jealous", "jittery", "jolly", "joyous", "kind", "light", "lively", "long",
    "lovely", "lucky", "modern", "nervous", "nice", "open", "perfect", "plain",
    "poised", "proud", "puzzled", "quaint", "real", "rich", "selfish", "shiny",
    "silly", "sleepy", "smiling", "smoggy", "stormy", "super", "tame", "tender",
    "tense", "tired", "vast", "weary", "wicked", "wild", "witty",
]

_animals = [
    "Alligator", "Alpaca", "Anteater", "Antelope", "Armadillo", "Badger", "Bear",
    "Beaver", "Beetle", "Bird", "Bison", "Bluebird", "Boar", "Bobcat", "Buffalo",
    "Butterfly", "Camel", "Capybara", "Caracal", "Caribou", "Caterpillar",
    "Cattle", "Cheetah", "Chicken", "Chinchilla", "Cobra", "Coyote", "Crab",
    "Crane", "Cricket", "Crocodile", "Crow", "Deer", "Dingo", "Dogfish",
    "Dolphin", "Dove", "Dragonfly", "Duck", "Eagle", "Elephant", "Falcon",
    "Ferret", "Finch", "Fish", "Fisher", "Flamingo", "Frog", "Gazelle", "Gecko",
    "Gerbil", "Giraffe", "Goat", "Goldfinch", "Goose", "Gorilla", "Grasshopper",
    "Gull", "Hamster", "Hare", "Hawk", "Hedgehog", "Heron", "Hornet", "Horse",
    "Hummingbird", "Hyena", "Iguana", "Impala", "Jackal", "Jaguar", "Jellyfish",
    "Kangaroo", "Kingbird", "Koala", "Lemur", "Leopard", "Lion", "Lizard",
    "Llama", "Lobster", "Lynx", "Lyrebird", "Macaque", "Macaw", "Magpie",
    "Mallard", "Mammoth", "Manatee", "Marmot", "Meerkat", "Mink", "Mongoose",
    "Moose", "Mouse", "Narwhal", "Newt", "Ocelot", "Opossum", "Orangutan",
    "Ostrich", "Otter", "Panther", "Parrot", "Panda", "Peafowl", "Pelican",
    "Penguin", "Pheasant", "Pigeon", "Pony", "Quail", "Rabbit", "Raccoon",
    "Raven", "Reindeer", "Rhino", "Salamander", "Salmon", "Seahorse", "Seal",
    "Serval", "Shark", "Sheep", "Shrew", "Skipper", "Sloth", "Snail", "Snake",
    "Spider", "Squirrel", "Starling", "Stilt", "Swan", "Tamarin", "Termite",
    "Tiger", "Toad", "Toucan", "Turkey", "Turtle", "Viper", "Vulture",
    "Wallaby", "Walrus", "Wasp", "Weasel", "Whale", "Wolf", "Wombat", "Worm", "Zebra"
]

def generate_random_password():
    """
    Generates a random password by combining a verb, an animal, and 3 numbers.
    This is a direct translation of the RandomPasswordGeneratorController.
    """
    verb = random.choice(_verbs).capitalize()
    animal = random.choice(_animals)
    numbers = "".join(random.choices(string.digits, k=3))
    
    return f"{verb}{animal}{numbers}"





# --- Encryption Service ---# Initialize the Fernet encryption key. This should be securely stored and managed.
# For production,

"""

# NOTE: The key should be generated once and stored securely in your settings.
# To generate a key: from cryptography.fernet import Fernet; Fernet.generate_key()
# _fernet = Fernet(settings.ENCRYPTION_KEY)

def encrypt_string(text: str) -> str:
   #Encrypts a string using Fernet symmetric encryption.
    # return _fernet.encrypt(text.encode()).decode()
    print(f"Encrypting '{text}'")
    return f"encrypted_{text}" # Placeholder

def decrypt_string(token: str) -> str:
   #Decrypts a token.
    # return _fernet.decrypt(token.encode()).decode()
    print(f"Decrypting '{token}'")
    return token.replace("encrypted_", "") # Placeholder


"""




