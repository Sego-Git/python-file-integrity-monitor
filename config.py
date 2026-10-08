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

            config = json.load(file)

    except json.JSONDecodeError:

        print("ERROR: Configuration file contains invalid JSON.")
        print("Configuration:", CONFIG_FILE)

        return None

    required_keys = [
        "log_file",
        "log_level",
        "baseline_directory"
    ]
    
    allowed_log_levels = [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    ]

    for key in required_keys:

        if key not in config:

            print("ERROR: Missing configuration setting.")
            print("Missing setting:", key)

            return None

    if config["log_level"].upper() not in allowed_log_levels:
            
        print("ERROR: Invalid log level.")
        print("Allowed levels:", ",".join(allowed_log_levels))
        return None
    
    if not config["log_file"]:
        
        print("ERROR: Log file path cannot be empty.")
        return None
    
    if not config["baseline_directory"]:
        
        print("ERROR: Baseline directory cannot be empty.")
        return None
        
    return config