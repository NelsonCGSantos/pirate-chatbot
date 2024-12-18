import spacy
from random import choice
import re
import time
from datetime import datetime

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Responses
responses = {
    "greeting": [
        "Ahoy, matey!", "Shiver me timbers, it's good to see ye!",
        "Ahoy there, landlubber!", "Greetings from the high seas!"
    ],
    "farewell": [
        "Fair winds and following seas!", "Until we meet again on the open waters!",
        "Goodbye, ye scallywag!", "Arrr, take care!"
    ],
    "help": [
        "Aye, I can help ye navigate these troubled waters! What d'ye need?",
        "I be here to assist ye, sailor!"
    ],
    "age": [
        "Old enough to sail the seas, but young enough to find treasure!",
        "Age? I've lost count o' the years sailin' these waters."
    ],
    "name": [
        "I be Bob, the saltiest chatbot to sail the Python seas!",
        "Call me Cap'n Bob, at yer service!"
    ],
}

pirate_jokes = [
    "Why couldn't the pirate play cards? Because he was sittin' on the deck!",
    "What's a pirate's favorite letter? Ye'd think it be R, but me first love be the C!",
    "Why do pirates make great singers? Because they hit the high C's!"
]

pirate_facts = [
    "Did ye know Blackbeard once set fire to his own beard to scare his enemies?",
    "Pirates wore eye patches to see in the dark below deck.",
    "Most pirates didn't actually bury their treasure—it'd be bad business!"
]

# Emojis for responses
emoji_responses = {
    "greeting": "☠️",
    "farewell": "🏴‍☠️",
    "joke": "😂",
    "fact": "📜",
    "help": "🛂",
}

# Memory for user details
memory = {"name": None, "color": None, "game": None}

# Utility Functions
def typing_simulation():
    print("Bob is thinkin'...", end="", flush=True)
    time.sleep(1.5)
    print("\r", end="")

def time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good mornin', sailor!"
    elif 12 <= hour < 18:
        return "Good afternoon, matey!"
    else:
        return "Good evenin', scallywag!"

def pirate_mood():
    moods = ["cheerful", "grumpy", "curious"]
    return choice(moods)

def mood_response(base_response):
    mood = pirate_mood()
    if mood == "cheerful":
        return f"{base_response} Har har har!"
    elif mood == "grumpy":
        return f"{base_response} Arrr, I'm feelin' grumpy today!"
    elif mood == "curious":
        return f"{base_response} What else d’ye want to know?"
    return base_response

def add_emoji(response, intent):
    emoji = emoji_responses.get(intent, "")
    return f"{response} {emoji}"

def easter_eggs(user_input):
    if "open sesame" in user_input.lower():
        return "Bob: Ye found the secret treasure! Congratulations, matey!"
    elif "parley" in user_input.lower():
        return "Bob: Parley, ye say? Aye, let's talk it out, sailor."
    return None

def show_memory():
    if not any(memory.values()):
        return "I don't know much about ye yet, matey!"
    details = [f"Yer {key} be {value}" for key, value in memory.items() if value]
    return "Arrr, here's what I know about ye: " + ", ".join(details)

def get_response(intent):
    return choice(responses.get(intent, ["I'm not sure how to respond to that."]))

def detect_intent(text):
    text = text.lower()
    doc = nlp(text)

    if "my name is" in text:
        return "remember_name"
    if "favorite color" in text:
        return "favorite_color"
    if "favorite game" in text:
        return "favorite_game"
    if "what do you know" in text:
        return "show_memory"

    if any(token.lemma_ in ["hello", "hi", "hey"] or token.text.lower() in ["hello", "hi", "hey"] for token in doc):
        return "greeting"
    elif any(token.lemma_ in ["bye", "goodbye"] or token.text.lower() in ["bye", "goodbye"] for token in doc):
        return "farewell"
    elif any(token.lemma_ in ["help", "assist"] or token.text.lower() in ["help", "assist"] for token in doc):
        return "help"
    elif any(token.lemma_ in ["joke", "funny"] or token.text.lower() in ["joke", "funny"] for token in doc):
        return "joke"
    elif any(token.lemma_ in ["fact", "story"] or token.text.lower() in ["fact", "story"] for token in doc):
        return "fact"
    elif any(token.lemma_ in ["old", "age"] or token.text.lower() in ["old", "age"] for token in doc):
        return "age"
    elif any(token.lemma_ in ["who", "name", "you"] or token.text.lower() in ["who", "name", "you"] for token in doc):
        return "name"
    
    return "unknown"

def update_memory(text):
    if "my name is" in text:
        name = re.search(r"my name is (.+)", text).group(1).strip()
        memory["name"] = name.capitalize()
        return f"Ahoy, {name.capitalize()}! I'll remember yer name!"
    elif "my favorite color is" in text:
        color = re.search(r"my favorite color is (.+)", text).group(1).strip()
        memory["color"] = color
        return f"Arrr, {color} be a fine color, matey! I'll remember that."
    elif "my favorite game is" in text:
        game = re.search(r"my favorite game is (.+)", text).group(1).strip()
        memory["game"] = game
        return f"Ah, {game}! A grand game for a sailor like yerself!"
    return "Arrr, I couldn't catch that, matey."

def tell_joke():
    return mood_response(choice(pirate_jokes))

def tell_fact():
    return mood_response(choice(pirate_facts))

def chat():
    print(f"{time_greeting()} I'm Bob, yer friendly pirate bot! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Bob: Goodbye, matey! 🏴‍☠️")
            break
        
        typing_simulation()
        easter_response = easter_eggs(user_input)
        if easter_response:
            print(easter_response)
            continue
        
        intent = detect_intent(user_input)
        if intent == "remember_name" or intent == "favorite_color" or intent == "favorite_game":
            response = update_memory(user_input)
        elif intent == "show_memory":
            response = show_memory()
        elif intent == "greeting" and memory["name"]:
            response = f"Ahoy, {memory['name']}! How can I help ye today?"
        elif intent == "joke":
            response = tell_joke()
        elif intent == "fact":
            response = tell_fact()
        else:
            response = add_emoji(get_response(intent), intent)
        
        print(f"Bob: {response}")

if __name__ == "__main__":
    chat()
