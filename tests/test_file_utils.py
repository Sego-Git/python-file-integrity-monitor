import unittest
import os
import hashlib

from file_utils import calculate_hash, scan_folder, validate_folder
from unittest.mock import patch

#Create a group of test cases related to the file_utils module
class TestFileUtils(unittest.TestCase):
    def test_calculate_hash(self):
        # Create a temporary file for testing
        
        test_file = "tests/test_file.txt"
        with open(test_file, "w") as file:
            file.write("HELLO FIM")
            
        file_hash = calculate_hash(test_file)
        
        expected_hash = hashlib.sha256(
            b"HELLO FIM"
        ).hexdigest()
        
        self.assertEqual(
            file_hash,
            expected_hash
        )
        
        os.remove(test_file)
        
    def test_hash_changes_when_file_change(self):
        test_file = "tests/test_file.txt"
        
        with open(test_file, "w") as file:
            file.write("Original content")
            
        original_hash = calculate_hash(test_file)
        
        with open(test_file, "w") as file:
            file.write("Modified content")
            
        modified_hash = calculate_hash(test_file)
        
        self.assertNotEqual(
            original_hash,
            modified_hash
        )
        
        os.remove(test_file)
        
    def test_hash_nonexistent_file(self):
        
        test_file = "tests/does_not_exist.txt"
        
        file_hash = calculate_hash(test_file)
        
        self.assertIsNone(file_hash)
            
    def test_scan_folder(self):
        
        test_folder = "tests/test_scan"
        
        os.makedirs(test_folder, exist_ok = True)
        
        file1 = os.path.join(test_folder, "file1.txt")
        file2 = os.path.join(test_folder, "file2.txt")
        
        with open(file1, "w") as file:
            file.write("File 1")
        
        with open(file2, "w") as file:
            file.write("File 2")
            
        scan_result = scan_folder(test_folder)
        files = scan_result["files"]
        
        self.assertTrue(scan_result["scan_complete"])
        self.assertEqual(scan_result["directory_errors"], 0)
        
        self.assertEqual(
            len(files),
            2
        )
        
        self.assertIn(
            file1,
            files
        )
        
        self.assertIn(
            file2,
            files
        )
        
        os.remove(file1)
        os.remove(file2)
        os.rmdir(test_folder)
        
    def test_scan_folder_recursive(self):
        
        test_folder = "tests/test_scan_recursive"
        nested_folder = os.path.join(
            test_folder,
            "documets"
        )
        
        os.makedirs(
            nested_folder,
            exist_ok = True
        )
        
        file1 = os.path.join(
            test_folder,
            "file1.txt"
        )
        
        file2 = os.path.join(
            nested_folder,
            "report.txt"
        )
        
        with open(file1, "w") as file:
            file.write("File 1")
        
        with open(file2, "w") as file:
            file.write("Report")
            
        scan_result = scan_folder(test_folder)
        files = scan_result["files"]
        
        self.assertTrue(scan_result["scan_complete"])
        self.assertEqual(scan_result["directory_errors"], 0)
        
        self.assertEqual(
            len(files),
            2
        )
        
        self.assertIn(
            file1,
            files
        )
        
        self.assertIn(
            file2,
            files
        )    
        os.remove(file1)
        os.remove(file2)
        os.rmdir(nested_folder)
        os.rmdir(test_folder)
        
    def test_validate_nonexistent_folder(self):
        
        test_folder = "tests/folder_that_does_not_exist"
        
        result = validate_folder(test_folder)
        
        self.assertFalse(result)
        
    def test_scan_folder_invalid_folder(self):
        
        test_folder = "tests/another_folder_that_does_not_exist"
        
        scan_result = scan_folder(test_folder)

        self.assertEqual(scan_result["files"], [])
        self.assertFalse(scan_result["scan_complete"])
        self.assertEqual(scan_result["directory_errors"], 1)
        
    def test_scan_folder_directory_error(self):
        
        test_folder = "tests/test_scan_error"
        os.makedirs(test_folder, exist_ok=True)
        
        with patch("file_utils.os.walk") as mock_walk:
            
            def simulate_walk_error(folder_path, onerror):
                error = OSError("Simulated directory access error")
                error.filename = folder_path
                onerror(error)
                return iter([])
            mock_walk.side_effect = simulate_walk_error
            
            scan_result = scan_folder(test_folder)
            
            self.assertFalse(scan_result["scan_complete"])
            self.assertEqual(scan_result["directory_errors"], 1)
            self.assertEqual(scan_result["files"], [])
            
            os.rmdir(test_folder)
    