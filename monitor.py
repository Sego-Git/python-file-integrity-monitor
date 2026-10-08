import argparse




from baseline import create_baseline, load_baseline
from integrity import check_integrity
from config import load_config
from logger import configure_logging

    
    


# ============================================
# MAIN FUNCTION
# ============================================

def main():
    
    config = load_config()
    
    if config is None:
        print("ERROR: Program cannot start without a valid configuration.")
        return
    
    configure_logging(config)
    
    
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