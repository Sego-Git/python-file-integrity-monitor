import json
import os
import logging
import re

from config import load_config
from file_utils import calculate_hash, scan_folder, validate_folder

# ============================================
# Generate baseline file name
# ============================================
logger = logging.getLogger(__name__)



def get_baseline_path(folder_path):
    
    folder_name = os.path.basename(os.path.normpath(folder_path))
    
    baseline_filename = folder_name + "_baseline.json"
    
    config = load_config()
    
    if config is None:
        return None
    
    baseline_directory = config["baseline_directory"]
    
    os.makedirs(
        baseline_directory,
        exist_ok = True
    )
    
    return os.path.join(
        baseline_directory,
        baseline_filename
    )
    
    
# ============================================
# Load trusted baseline
# ============================================



def load_baseline(folder_path):

    baseline_path = get_baseline_path(folder_path)

    # Step 1: Make sure we have a valid baseline path.
    if baseline_path is None:
        print("ERROR: Could not determine baseline path.")
        return None

    if not os.path.isfile(baseline_path):
        print("ERROR: Baseline was not found or is not a file.")
        print("Expected baseline:", baseline_path)
        print("Create a baseline before monitoring.")
        return None

    # Step 2: Read the JSON file safely.
    try:
        with open(baseline_path, "r", encoding="utf-8") as file:
            baseline = json.load(file)

    except json.JSONDecodeError:
        print("ERROR: Baseline file contains invalid JSON.")
        print("Baseline:", baseline_path)
        logger.error("BASELINE_INVALID_JSON | %s", baseline_path)
        return None

    except OSError as error:
        print("ERROR: Could not read the baseline file.")
        print("Reason:", error)
        logger.error("BASELINE_READ_ERROR | %s | %s", baseline_path, error)
        return None

    # Step 3: Make sure the baseline is a dictionary.
    if not isinstance(baseline, dict) or not baseline:
        print("ERROR: Baseline must be a non-empty dictionary.")
        logger.error("BASELINE_INVALID_STRUCTURE | %s", baseline_path)
        return None

    # Step 4: Validate every file path and SHA-256 hash.
    for file_path, file_hash in baseline.items():

        if not isinstance(file_path, str) or not file_path.strip():
            print("ERROR: Baseline contains an invalid file path.")
            logger.error("BASELINE_INVALID_PATH | %s", baseline_path)
            return None

        if (
            not isinstance(file_hash, str)
            or re.fullmatch(r"[0-9a-fA-F]{64}", file_hash) is None
        ):
            print("ERROR: Baseline contains an invalid SHA-256 hash.")
            print("File:", file_path)
            logger.error(
                "BASELINE_INVALID_HASH | %s | %s",
                baseline_path,
                file_path
            )
            return None

    # Step 5: Return the trusted data only if every check passes.
    print("Baseline loaded and validated successfully.")
    return baseline

    
           
# ============================================ 
#Create trusted baseline
# ============================================


def create_baseline(folder_path):
    
    if not validate_folder(folder_path):
        return
    
    scan_result = scan_folder(folder_path)
    
    if not scan_result["scan_complete"]:
        print("ERROR: Folder scan was incomplete.")
        print("Directory errors:", scan_result["directory_errors"])
        print("Baseline was not created")
        return
    
    current_files = scan_result["files"]
    
    if not current_files:
        print("WARNING: No files found in folder")
        print("Folder:", folder_path)
        return
    
    baseline = {}
    
    for file_path in current_files:
        file_hash = calculate_hash(file_path)

        if file_hash is None:
            print("ERROR: Could not calculate hash.")
            print("File:", file_path)
            print("Baseline was not created because a file could not be read.")
            return

        baseline[file_path] = file_hash
     
    if not baseline:
        print("ERROR: No valid files found to create a baseline.")
        return
        
    baseline_path = get_baseline_path(folder_path)    
    
    if baseline_path is None:
        print("ERROR: Could not determine baseline path")
        return
    
    with open(baseline_path, "w") as file:
        json.dump(baseline, file, indent=4)
    
    print("Baseline created successfully!")
    print("Folder:", folder_path)
    print("Baseline:", baseline_path)
    
    