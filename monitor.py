import argparse
import logging


from config import load_config
from baseline import create_baseline, load_baseline
from integrity import check_integrity


# ============================================
# DEFAULT CONFIGURATION
# ============================================

DEFAULT_CONFIG = {
    "log_file": "fim.log",
    "log_level": "INFO",
    "baseline_directory": "baselines"
}


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