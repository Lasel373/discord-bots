import random

def get_response(user_input: str) -> str:
    lowered = user_input.lower()
    if lowered == "":
        return "Nunja, du sagst ja nicht gerade viel!!!!"
    
    if user_input[0] == "$":
        if user_input == "$info":
            return "Hier sind die neusten Steam-Spiele: ..."
        
