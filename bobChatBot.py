import spacy    
from random import choice
import re  


nlp = spacy.load("en_core_web_sm")


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

# Initialize memory with a default name key
memory = {"name": None}



def get_response(intent):
    return choice(responses.get(intent, ["I'm not sure how to respond to that."]))



def detect_intent(text):
    text = text.lower()  # Convert input to lowercase for case-insensitive matching
    doc = nlp(text)
    
    if "my name is" in text:  
        return "remember_name"
    if any(token.lemma_ in ["hello", "hi", "hey"] for token in doc):
        return "greeting"
    elif any(token.lemma_ in ["bye", "goodbye", "see you"] for token in doc):
        return "farewell"
    elif any(token.lemma_ in ["help", "assist", "welp"] for token in doc):
        return "help"  
    elif any(token.lemma_ in ["age", "old", "elder"] for token in doc):
        return "age" 
    elif any(token.lemma_ in ["name", "who", "you are"] for token in doc):
        return "name" 
    elif any(token.lemma_ in ["joke", "funny"] for token in doc):
        return "joke"
    elif any(token.lemma_ in ["fact", "tell", "story"] for token in doc):
        return "fact"
    elif any(token.lemma_ in ["anchor", "cannon", "sail"] for token in doc):
        return "command"
    else:
        return "unknown"



def tell_joke():
    return choice(pirate_jokes)



def tell_fact():
    return choice(pirate_facts)



def pirate_commands(text):
    if "anchor" in text:
        return "The anchor be raised! We're ready to set sail!"
    elif "cannon" in text:
        return "BOOM! The cannons be fired! Enemy ship defeated!"
    elif "sail" in text:
        return "Hoist the sails! We're off to find treasure!"
    else:
        return "Arrr, I don't know that command!"



def update_memory(text):
    # Use a regular expression to extract the name after "my name is"
    match = re.search(r"my name is (.+)", text.lower())
    if match:
        name = match.group(1).strip()  
        memory["name"] = name  
        return f"Ahoy, {name.capitalize()}! I'll remember yer name!"
    return "Arrr, I couldn't catch yer name, matey."



def chat():
    print("Hello! I'm Bob, your friendly pirate! How can I help today? Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Chatbot: Goodbye!")
            break

       
        intent = detect_intent(user_input)

     
        if intent == "remember_name":
            response = update_memory(user_input)
        elif intent == "greeting" and memory["name"]:
            response = f"Ahoy, {memory['name'].capitalize()}! How can I help ye today?"
        elif intent == "joke":
            response = tell_joke()
        elif intent == "fact":
            response = tell_fact()
        elif intent == "command":
            response = pirate_commands(user_input)
        elif intent in responses:
            response = get_response(intent)
        else:
            response = "Arrr, I don't understand that, matey."

        print(f"Bob: {response}")



if __name__ == "__main__":
    chat()
