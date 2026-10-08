import json
import os

CONFIG_FILE = "config.json"

def load_config():
    
    if not os.path.exists(CONFIG_FILE):
        
        print("ERROR: Configuration file not found.")
        print("Expected configuration:", CONFIG_FILE)
        
        return None
    
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecoderError:
        print("ERROR: Configuration file contains invalid JSON")
        print("Configuration:", CONFIG_FILE)
        
        return None