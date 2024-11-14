import spacy    
from random import choice


nlp = spacy.load("en_core_web_sm")


responses = {
    "greeting": ["Hello!", "Hi There!", "Meowdy!", "Ahoy", "Ahoy, matey!", "Hello there"],
    "farewell": ["Goodbye!", "See you later!", "Take care!"],
    "help": ["I can help answer questions or just chat! How can I assist you?"],
    "age": ["I'm just a few lines of code, so I don't have an age!"],
    "name": ["I'm Bob! Your Pirate Python chatbot, here to help!"],
}


def get_response(intent):
    return choice(responses.get(intent, ["I'm not sure how to respond to that."]))


def detect_intent(text):
    doc = nlp(text.lower())
    
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
    else:
        return "unknown"


def chat():
    print("Hello! I'm Bob, your friendly pirate! How can I help today? Type 'quit' to exit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Chatbot: Goodbye!")
            break
        intent = detect_intent(user_input)
        response = get_response(intent)
        print(f"Bob {response}")
            

if __name__ == "__main__":
    chat()
