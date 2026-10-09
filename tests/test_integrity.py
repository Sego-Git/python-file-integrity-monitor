import unittest
import os

from baseline import create_baseline, load_baseline
from integrity import check_integrity
from io import StringIO
from contextlib import redirect_stdout

class TestIntegrity(unittest.TestCase):
    
    def test_modified_file(self):
        
        test_folder = "tests/test_integrity_folder"
        
        os.makedirs(
            test_folder,
            exist_ok = True   
        )
        
        test_file = os.path.join(
            test_folder,
            "file1.txt"
        )
        
        #create the original file
        with open(test_file, "w") as file:
            file.write("Original content")
            
        # Save its trusted hash
        create_baseline(test_folder)
        
        baseline = load_baseline(test_folder)
        
        # Modify the file after creating the baseline
        with open(test_file, "w") as file:
            file.write("Modified content")
            
        # check the file against the original baseline
        output = StringIO()
        
        with redirect_stdout(output):
            check_integrity(test_folder, baseline)
            
        result = output.getvalue()
        
        self.assertIn(
            "Files modified: 1",
            result
        )
        
        self.assertIn(
            "INTEGRITY ISSUES DETECTED",
            result.upper()
        )
        
        # clean up
        baseline_path = os.path.join(
            "baselines",
            "test_integrity_folder_baseline.json"
        )
        
        os.remove(test_file)
        os.rmdir(test_folder)
        os.remove(baseline_path)
        
    def test_added_file(self):
        
        test_folder = "tests/test_added_file_folder"
        
        os.makedirs(
            test_folder,
            exist_ok = True
        )
        
        file1 = os.path.join(
            test_folder,
            "file1.txt"
        )
        
        with open(file1, "w") as file:
            file.write("Trusted content")
        
        # Create the baseline before the new file exists
        create_baseline(test_folder)
        
        baseline = load_baseline(test_folder)
        
        #Add an unexpected file after the baseline is created
        new_file = os.path.join(
            test_folder,
            "unexpected.txt"
        )
        
        with open(new_file, "w") as file:
            file.write("Unexpected content")
            
        # Capture the integrity scan output
        output = StringIO()
        
        with redirect_stdout(output):
            check_integrity(test_folder, baseline)
            
        result = output.getvalue()
        
        # Verify that the added file was detected
        self.assertIn(
            "Files added: 1",
            result
        )
        
        # Clean up test files
        baseline_path = os.path.join(
            "baselines",
            "test_added_file_folder_baseline.json"
        )
        
        os.remove(file1)
        os.remove(new_file)
        os.rmdir(test_folder)
        os.remove(baseline_path)
        
    
    def test_deleted_file(self):
        
        test_folder = "tests/test_deleted_file_folder"
        
        os.makedirs(
            test_folder,
            exist_ok = True
        )
        
        file1 = os.path.join(
            test_folder,
            "file1.txt"
        )
        
        file2 = os.path.join(
            test_folder,
            "file2.txt"
        )
        
        # Create two files before the baseline
        with open(file1, "w") as file:
            file.write("Trusted file 1")
            
        with open(file2, "w") as file:
            file.write("Trusted file 2")
            
        # Save both files in the trusted baseline
        create_baseline(test_folder)
        
        baseline = load_baseline(test_folder)
        
        #Delete one file after creating the baseline
        os.remove(file2)
        
        # Capture the integrity scan output
        output = StringIO()
        
        with redirect_stdout(output):
            check_integrity(test_folder, baseline)
            
        result = output.getvalue()
        
        # Verify that one deleted file was detected
        self.assertIn(
            "Files deleted: 1",
            result
        )
        
        # Clean up
        baseline_path = os.path.join(
            "baselines",
            "test_deleted_file_folder_baseline.json"
        )
        
        os.remove(file1)
        os.rmdir(test_folder)
        os.remove(baseline_path)
        
    
    
    def test_unchanged_file(self):

        test_folder = "tests/test_unchanged_file_folder"

        os.makedirs(test_folder, exist_ok=True)

        test_file = os.path.join(
            test_folder,
            "file1.txt"
        )

        # Create the original file
        with open(test_file, "w") as file:
            file.write("Trusted content")

        # Create and load the trusted baseline
        create_baseline(test_folder)
        baseline = load_baseline(test_folder)

        # Scan without changing the file
        output = StringIO()

        with redirect_stdout(output):
            check_integrity(test_folder, baseline)

        result = output.getvalue()

        # Verify that the file is reported as unchanged
        self.assertIn("Files OK: 1", result)
        self.assertIn("Files modified: 0", result)
        self.assertIn("Files added: 0", result)
        self.assertIn("Files deleted: 0", result)

        # Clean up
        baseline_path = os.path.join(
            "baselines",
            "test_unchanged_file_folder_baseline.json"
        )

        os.remove(test_file)
        os.rmdir(test_folder)
        os.remove(baseline_path)