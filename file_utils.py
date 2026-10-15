import hashlib
import os
import logging

logger = logging.getLogger(__name__)


# ============================================
# CALCULATE FILE HASH
# ============================================

def calculate_hash(file_path):
    
    try:
        
        with open(file_path, "rb") as file:
            file_content = file.read()
            
        return hashlib.sha256(file_content).hexdigest()
    
    except FileNotFoundError:
        
        print("ERROR: File not found:", file_path)
        
        logger.error("FILE_NOT_FOUND | %s", file_path)
        
        return None
    except PermissionError:
        
        print("ERROR: Permission denied:", file_path)
        
        logger.error("PERMISSION_DENIED | %s", file_path)
        
        return None
    
    except OSError as error: 
        
        print("ERROR: Could not read file:", file_path)
        print("Reason:", error)
        
        logger.error("FILE_READ_ERROR | %s | %s", file_path, error)
        
        return None
    
    
def validate_folder(folder_path):
    if not os.path.exists(folder_path):
        
        print("ERROR: Folder does not exist.")
        print("Folder:", folder_path)
        
        return False
    
    if not os.path.isdir(folder_path):
        
        print("ERROR: The specified path is not a folder.")
        print("Path:", folder_path)
        return False
    return True
    
# ============================================
# SCAN FOLDER
# ============================================

def scan_folder(folder_path):
    
    if not validate_folder(folder_path):
        return []
    
    current_file = []
    
    for root, directories, files in os.walk(folder_path):
        
        for filename in files:
            
            file_path = os.path.join(root, filename)
            
            current_file.append(file_path)
            
    return current_file