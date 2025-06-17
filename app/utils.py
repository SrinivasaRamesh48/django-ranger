import random
import string

# The list from your 'verb' function, which are actually adjectives
ADJECTIVES = [
    "Alert", "Amused", "Annoyed", "Anxious", "Ashamed", "Blue", "Brainy", 
    "Brave", "Bright", "Busy", "Calm", "Careful", "Clean", "Clear", 
    "Clever", "Cloudy", "Crowded", "Curious", "Cute", "Dark", "Dizzy", 
    "Drab", "Dull", "Eager", "Easy", "Elated", "Elegant", "Excited", 
    "Fair", "Famous", "Fancy", "Fine", "Funny", "Gentle", "Gifted", 
    "Good", "Happy", "Healthy", "Helpful", "Hungry", "Jealous", 
    "Jittery", "Jolly", "Joyous", "Kind", "Light", "Lively", "Long", 
    "Lovely", "Lucky", "Modern", "Nervous", "Nice", "Open", "Perfect", 
    "Plain", "Poised", "Proud", "Puzzled", "Quaint", "Real", "Rich", 
    "Selfish", "Shiny", "Silly", "Sleepy", "Smiling", "Smoggy", 
    "Stormy", "Super", "Tame", "Tender", "Tense", "Tired", "Vast", 
    "Weary", "Wicked", "Wild", "Witty"
]

# The list from your 'animal' function
ANIMALS = [
    "Alligator", "Alpaca", "Anteater", "Antelope", "Armadillo", "Badger", 
    "Bear", "Beaver", "Beetle", "Bird", "Bison", "Bluebird", "Boar", 
    "Bobcat", "Buffalo", "Butterfly", "Camel", "Capybara", "Caracal", 
    "Caribou", "Caterpillar", "Cattle", "Cheetah", "Chicken", 
    "Chinchilla", "Cobra", "Coyote", "Crab", "Crane", "Cricket", 
    "Crocodile", "Crow", "Deer", "Dingo", "Dogfish", "Dolphin", "Dove", 
    "Dragonfly", "Duck", "Eagle", "Elephant", "Falcon", "Ferret", "Finch", 
    "Fish", "Fisher", "Flamingo", "Frog", "Gazelle", "Gecko", "Gerbil", 
    "Giraffe", "Goat", "Goldfinch", "Goose", "Gorilla", "Grasshopper", 
    "Gull", "Hamster", "Hare", "Hawk", "Hedgehog", "Heron", "Hornet", 
    "Horse", "Hummingbird", "Hyena", "Iguana", "Impala", "Jackal", 
    "Jaguar", "Jellyfish", "Kangaroo", "Kingbird", "Koala", "Lemur", 
    "Leopard", "Lion", "Lizard", "Llama", "Lobster", "Lynx", "Lyrebird", 
    "Macaque", "Macaw", "Magpie", "Mallard", "Mammoth", "Manatee", 
    "Marmot", "Meerkat", "Mink", "Mongoose", "Moose", "Mouse", "Narwhal", 
    "Newt", "Ocelot", "Opossum", "Orangutan", "Ostrich", "Otter", 
    "Panther", "Parrot", "Panda", "Peafowl", "Pelican", "Penguin", 
    "Pheasant", "Pigeon", "Pony", "Quail", "Rabbit", "Raccoon", "Raven", 
    "Reindeer", "Rhino", "Salamander", "Salmon", "Seahorse", "Seal", 
    "Serval", "Shark", "Sheep", "Shrew", "Skipper", "Sloth", "Snail", 
    "Snake", "Spider", "Squirrel", "Starling", "Stilt", "Swan", 
    "Tamarin", "Termite", "Tiger", "Toad", "Toucan", "Turkey", "Turtle", 
    "Viper", "Vulture", "Wallaby", "Walrus", "Wasp", "Weasel", "Whale", 
    "Wolf", "Wombat", "Worm", "Zebra"
]

def generate_password():
    """
    Generates a memorable password by combining a random adjective, a random animal,
    and a three-digit number. This is the direct Python equivalent of your PHP class.
    
    Returns:
        str: The generated password, e.g., "CalmZebra385".
    """
    
    # random.choice is the Pythonic way to get a random element from a list.
    adjective = random.choice(ADJECTIVES)
    animal = random.choice(ANIMALS)
    
    # This is a more direct way to generate a random string of digits
    # than the str_shuffle(str_repeat(...)) method in PHP.
    number_part = ''.join(random.choices(string.digits, k=3))
    
    # Combine the parts into the final password.
    # The f-string is a modern and readable way to format strings.
    password = f"{adjective}{animal}{number_part}"
    
    return password

# --- Example Usage ---
# In your actual Django code (e.g., in a view or another utility), you would
# import this function and call it like so:
#
# from .utils import generate_password
# new_password = generate_password()
# print(new_password)

# if __name__ == "__main__":
#     # This block allows you to test the function by running the script directly.
#     print("Generated Passwords:")
#     for _ in range(5):
#         print(generate_password())
