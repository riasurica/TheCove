# File: dnd_chatbot_rpg.py

import openai
import json
import os

# Initialize OpenAI API (Replace 'your-api-key' with your actual key)
openai.api_key = 'your-api-key'

# Path to save game state
SAVE_FILE = 'game_state.json'


def save_game_state(state):
    """Save the game state to a JSON file."""
    with open(SAVE_FILE, 'w') as file:
        json.dump(state, file)


def load_game_state():
    """Load the game state from a JSON file."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as file:
            return json.load(file)
    return None


def chat_with_gpt(prompt, context=""):
    """Send a prompt to GPT-4 and receive a response."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content.strip()


def character_creation():
    """Interactive character creation."""
    print("Welcome to the world of Dungeons & Dragons!")
    print("Let's create your character.")
    name = input("What is your character's name? ")
    race = input("Choose a race (e.g., Human, Elf, Dwarf, Orc): ")
    char_class = input("Choose a class (e.g., Warrior, Mage, Rogue): ")
    backstory = input("Briefly describe your character's backstory: ")

    character = {
        "name": name,
        "race": race,
        "class": char_class,
        "backstory": backstory,
        "inventory": [],
        "stats": {"strength": 10, "dexterity": 10, "intelligence": 10},
    }
    return character


def main():
    """Main game loop."""
    print("Welcome to the OpenAI D&D RPG!")

    # Load or start a new game
    game_state = load_game_state()
    if game_state:
        print("Loading your saved game...")
        print(f"Welcome back, {game_state['character']['name']}!")
    else:
        print("Starting a new game...")
        character = character_creation()
        game_state = {
            "character": character,
            "story": "You find yourself in a mysterious tavern...",
            "progress": [],
        }
        save_game_state(game_state)

    # Main game loop
    while True:
        print("\nCurrent Story: ", game_state["story"])
        user_input = input("What do you do? (type 'save' to save progress, 'exit' to quit): ")

        if user_input.lower() == "save":
            save_game_state(game_state)
            print("Game saved!")
            continue
        elif user_input.lower() == "exit":
            save_game_state(game_state)
            print("Game saved! Exiting now. See you next time!")
            break

        # Update story via GPT-4
        gpt_prompt = f"""
        You are a Dungeon Master in a D&D world. The player character's name is {game_state['character']['name']}.
        They are a {game_state['character']['race']} {game_state['character']['class']}.
        Their current story is: {game_state['story']}
        They just decided to: {user_input}
        Continue the story with vivid detail and present new choices.
        """
        context = "You are a helpful and imaginative Dungeon Master for a D&D-style game."
        new_story = chat_with_gpt(gpt_prompt, context)

        # Update game state
        game_state["story"] = new_story
        game_state["progress"].append({"input": user_input, "story": new_story})
        save_game_state(game_state)

        print("\n", new_story)


if __name__ == "__main__":
    main()