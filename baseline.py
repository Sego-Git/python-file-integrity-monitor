import json
import os
import logging

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
    
    if not os.path.exists(baseline_path):
        
        print("ERROR: baseline was not found")
        print("Expected baseline:", baseline_path)
        print("Create a baseline before monitoring")
        
        return None
    
    try:
        
        with open(baseline_path, "r") as file:
            return json.load(file)
    
    except json.JSONDecodeError:
        
        print("EROOR: Baseline file contained invalid JSON")
        print("Baseline:", baseline_path)
        
        logger.error(
            "Baseline_INVALIDE_JSON | %s", baseline_path
        )
        
        return None
    
    
           
# ============================================ 
#Create trusted baseline
# ============================================


def create_baseline(folder_path):
    
    if not validate_folder(folder_path):
        return
    
    current_files = scan_folder(folder_path)
    
    if not current_files:
        print("WARNING: No files found in folder")
        print("Folder:", folder_path)
        return
    
    baseline = {}
    
    for file_path in current_files:
        file_hash = calculate_hash(file_path)
        
        if file_hash is None:
            print("WARNING: Could not calculate hash.")
            print("File:", file_path)
            continue
    
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
    

    
    with open(baseline_path, "w") as file:
        json.dump(baseline, file, indent=4)
    print("Baseline created successfully!")
    print("Folder", folder_path)
    print("Baseline:", baseline_path)
    print("Files trusted:", len(baseline))
    