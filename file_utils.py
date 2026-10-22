import hashlib
import os
import logging

logger = logging.getLogger(__name__)


# ============================================
# CALCULATE FILE HASH
# ============================================

def calculate_hash(file_path):
    
    try:
        hasher = hashlib.sha256()

        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                hasher.update(chunk)

        return hasher.hexdigest()
    
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
        return {
            "files": [],
            "scan_complete": False,
            "directory_errors": 1
        }
        
    current_files = []
    directory_errors = 0
    
    def handle_walk_error(error):
        nonlocal directory_errors
        directory_errors += 1
        
        print("ERROR: Could not scan a directory.")
        print("Reason:", error)
        
        logger.error(
            "DIRECTORY_SCAN_ERROR | %s | %s",
            error.filename,
            error
        )
        
    for root, directories, files in os.walk(
        folder_path,
        onerror=handle_walk_error
    ):
        for filename in files:
            file_path = os.path.join(root, filename)
            current_files.append(file_path)
    return {
        "files": current_files,
        "scan_complete": directory_errors == 0,
        "directory_errors": directory_errors
    }