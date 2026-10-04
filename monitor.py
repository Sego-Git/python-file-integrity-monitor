import hashlib
import json
import os
import argparse
import logging
from datetime import datetime


# ============================================
# DEFAULT CONFIGURATION
# ============================================

DEFAULT_CONFIG = {
    "log_file": "fim.log",
    "log_level": "INFO",
    "baseline_directory": "baselines"
}


# ============================================
# LOAD CONFIGURATION
# ============================================

def load_config():

    config_path = "config.json"

    if not os.path.exists(config_path):

        print("WARNING: Configuration file was not found.")
        print("Using default configuration.")

        return DEFAULT_CONFIG

    try:

        with open(config_path, "r") as file:

            config = json.load(file)

        return config

    except json.JSONDecodeError:

        print("WARNING: Configuration file contains invalid JSON.")
        print("Using default configuration.")

        return DEFAULT_CONFIG

    except OSError:

        print("WARNING: Could not read the configuration file.")
        print("Using default configuration.")

        return DEFAULT_CONFIG


# ============================================
# LOGGING CONFIGURATION
# ============================================

config = load_config()

log_level = getattr(
    logging,
    config["log_level"].upper(),
    logging.INFO
)

logging.basicConfig(
    filename=config["log_file"],
    level=log_level,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Calculate SHA-256 hash
def calculate_hash(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return hashlib.sha256(file_content).hexdigest() 

# Load trusted baseline
def load_baseline(folder_path):
    
    baseline_path = get_baseline_path(folder_path)
    
    if not os.path.exists(baseline_path):
        
        print("ERROR: baseline was not found")
        print("Expected baseline:", baseline_path)
        print("Create a baseline before monitoring")
        
        return None
    
    with open(baseline_path, "r") as file:
        return json.load(file)
    

#Log security events
def log_event(level, event, file_path, file_hash=None):
    
    log_message = event + "|" + file_path
    
    if file_hash is not None:
        log_message = (
            log_message
            + " | SHA-256: "
            + file_hash
        )
        
    if level == "INFO":
        logger.info(log_message)
    elif level == "WARNING":
        logger.warning(log_message)
    elif level == "ERROR":
        logger.error(log_message)
    elif level == "CRITICAL":
        logger.critical(log_message)
    
    
    
#Scan the monitored folder
def scan_folder(folder_path):

    print("DEBUG - Folder being scanned:", folder_path)
    print("DEBUG - Absolute path:", os.path.abspath(folder_path))
    print("DEBUG - Folder exists:", os.path.exists(folder_path))
    print("DEBUG - Is directory:", os.path.isdir(folder_path))

    current_files = []

    for root, directories, files in os.walk(folder_path):

        print("DEBUG - Root:", root)
        print("DEBUG - Files found:", files)

        for filename in files:

            file_path = os.path.join(root, filename)

            current_files.append(file_path)

    print("DEBUG - Current files:", current_files)

    return current_files
            
            

# Generate baseline fine name
def get_baseline_path(folder_path):
    
    folder_name = os.path.basename(os.path.normpath(folder_path))
    
    baseline_filename = folder_name + "_baseline.json"
    
    return os.path.join(
        config["baseline_directory"],
        baseline_filename
    )
            
#Create trusted baseline

def create_baseline(folder_path):
    
    if not os.path.exists(folder_path):
        print("ERROR: Folder does not exist.")
        print("Folder:", folder_path)
        
        return
    
    if not os.path.isdir(folder_path):
        print("ERROR: The specified path is not a folder")
        print("Path:", folder_path)
        
        return
    
    current_files = scan_folder(folder_path)
    baseline = {}
    for file_path in current_files:
        file_hash = calculate_hash(file_path)
        baseline[file_path] = file_hash
        
    baseline_path = get_baseline_path(folder_path)    
    
    os.makedirs(
    config["baseline_directory"],
    exist_ok=True
)
    
    with open(baseline_path, "w") as file:
        json.dump(baseline, file, indent=4)
    print("Baseline created successfully!")
    print("Folder", folder_path)
    print("Baseline:", baseline_path)
    print("Files trusted:", len(baseline))

#Check file integrity
def check_integrity(folder_path, baseline):
    
    if not os.path.exists(folder_path):
        print("ERROR: folder does not exist.")
        print("Folder:", folder_path)
        
        return
    
    if not os.path.isdir(folder_path):
        print("ERROR: The specified path is not a folder")
        print("Path:", folder_path)
        
        return
    
    #Get all files currently in the folder
    current_files = scan_folder(folder_path)
    
    files_ok = 0
    files_modified = 0
    files_added = 0
    files_deleted = 0
    
    
    print("DEBUG - Current files:", current_files)
    # Check current files
    for file_path in current_files:
        current_hash = calculate_hash(file_path)
        # New file
        if file_path not in baseline:
            print("WARNING: New file detected")
            print("File: ", file_path)
            print("SHA-256:", current_hash)
            log_event("WARNING", "FILE_ADDED", file_path, current_hash)
            files_added += 1
            
        # Modified file
        elif current_hash != baseline[file_path]:
            print("WARNING: File has been modified!")
            print("File:", file_path)
            print("Trusted SHA-256:", baseline[file_path])
            print("Current SHA-256:", current_hash)
            
            
            log_event("WARNING", "FILE_MODIFIED", file_path, current_hash)
            files_modified += 1
            
            
        # No chang
        else:
            print("File is unchanged:", file_path)
            files_ok += 1
        
# check deleted files
    for file_path in baseline:
        if file_path not in current_files:
            print("WARNING: File has been deleted!")
            print("File:", file_path)
            log_event("WARNING", "FILE_DELETED", file_path)
            files_deleted += 1
            
    print()
    print("=====================================")
    print("INTEGRITY SCAN SUMMARY")
    print("=====================================")

    print("Files scanned:", len(current_files))
    print("Files OK:", files_ok)
    print("Files modified:", files_modified)
    print("Files added:", files_added)
    print("Files deleted:", files_deleted)

    if files_modified > 0 or files_added > 0 or files_deleted > 0:
        
        print("Status: WARNING - Integrity issues detected!")
        
    else:
        
        print("Status: SECURE")
        
    print("=====================================")



# ============================================
# MAIN FUNCTION
# ============================================

def main():

    parser = argparse.ArgumentParser(description = "Python File Integrity Monitor")
    
    subparsers = parser.add_subparsers(dest = "command")
    
    
    #**** CREATE BASELINE COMMAND ****
    
    baseline_parser = subparsers.add_parser(
        "create-baseline",
        help = "Create a trusted file integrity baseline"
    )
    
    baseline_parser.add_argument(
       "folder",
       help = "Folder to create the baseline for" 
    )
    
    
    #**** SCAN COMMAND ****
    
    scan_parser = subparsers.add_parser(
        "scan",
        help = "Check the integrity of a folder"
    )

    scan_parser.add_argument(
        "folder",
        help = "Folder to scan"
    )
    
    
    # *** READ COMMAND-LINE ARGUMENTS ***
    
    
    args = parser.parse_args()
    
    # *** CREATE BASELINE MODE ***
    
    if args.command == "create-baseline":
        
        create_baseline(args.folder)
        
    # *** SCAN MODE ***
        
    elif args.command == "scan":
        
        baseline = load_baseline(args.folder)
        
        if baseline is None:
            return
        
        check_integrity(args.folder, baseline)

    


# ============================================
# START THE PROGRAM
# ============================================


main()