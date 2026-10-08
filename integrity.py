import logging
import os

from file_utils import calculate_hash, scan_folder
from logger import log_event






# ============================================
#Check file integrity
# ============================================


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
    
    
    # Check current files
    for file_path in current_files:
        current_hash = calculate_hash(file_path)
        
        if current_hash is None:
            print("WARNONG: Could not calculate the hash")
            print("File:", file_path)
            
            log_event(
                "ERROR",
                "HASH_CALCULATION_FAILED",
                file_path
            )
            
            continue
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
