import unittest
import os
import json 

from baseline import create_baseline, load_baseline
from file_utils import calculate_hash
from unittest.mock import patch


class TestBaseline(unittest.TestCase):
    
    def test_create_baseline(self):
        
        test_folder = "tests/test_baseline_folder"
        
        os.makedirs(
            test_folder,
            exist_ok = True
        )
        
        test_file = os.path.join(
            test_folder,
            "file1.txt"
        )
        
        with open(test_file, "w") as file:
            file.write("Hello dear Baseline")
            
        create_baseline(test_folder)
        
        baseline_path = os.path.join(
            "baselines",
            "test_baseline_folder_baseline.json"
        )
        
        self.assertTrue(
            os.path.exists(baseline_path)
        )
        
        with open(baseline_path, "r") as file:
            
            baseline = json.load(file)
            
        self.assertIn(
            test_file,
            baseline
        )
        
        expected_hash = calculate_hash(test_file)
        
        self.assertEqual(
            baseline[test_file],
            expected_hash
        )
        
        os.remove(test_file)
        os.rmdir(test_folder)
        os.remove(baseline_path)
        
    def test_load_baseline(self):
        test_folder = "tests/test_load_baseline_folder"
        
        os.makedirs(test_folder, exist_ok=True)
        
        test_file = os.path.join(
            test_folder,
            "file1.txt"
        )
        
        with open(test_file,"w") as file:
            file.write("Hello Load Baseline")
            
        create_baseline(test_folder)
        
        loaded_baseline = load_baseline(test_folder)
        
        self.assertIsNotNone(loaded_baseline)
        
        self.assertIn(
            test_file,
            loaded_baseline
        )
        
        os.remove(test_file)
        os.rmdir(test_folder)
        
        baseline_path = os.path.join(
            "baselines",
            "test_load_baseline_folder_baseline.json"
        )
        
        os.remove(baseline_path)
        
    def test_laod_missing_baseline(self):
        
        test_folder =  "tests/folder_without_baseline"
        
        os.makedirs(
            test_folder,
            exist_ok = True
        )
        
        loaded_baseline = load_baseline(test_folder)
        
        self.assertIsNone(loaded_baseline)
        
        os.rmdir(test_folder)
        
    def test_laod_invalid_json_baseline(self):
        
        test_folder = "tests/test_invalid_baseline_folder"
        
        os.makedirs(
            test_folder,
            exist_ok = True
        )
        
        baseline_path = os.path.join(
            "baselines",
            "test_invalid_baseline_folder_baseline.json"
        )
        
        with open(baseline_path, "w") as file:
            file.write("This is not valid JSON!!")
            
        loaded_baseline = load_baseline(test_folder)
        
        self.assertIsNone(loaded_baseline)
        
        os.remove(baseline_path)
        os.rmdir(test_folder)
        
    def test_load_invalid_structure_baseline(self):
        test_folder = "tests/test_invalid_structure_folder"
        
        os.makedirs(test_folder, exist_ok=True)
        
        baseline_path = os.path.join(
            "baselines",
            "test_invalid_structure_folder_baseline.json"
        )
        
        with open(baseline_path, "w") as file:
            json.dump(["file1.txt", "file2.txt"], file)
            
        loaded_baseline = load_baseline(test_folder)
        
        self.assertIsNone(loaded_baseline)
        
        os.remove(baseline_path)
        os.rmdir(test_folder)
        
    def test_load_invalid_hash_baseline(self):
        
        test_folder = "tests/test_invalid_hash_folder"
        
        os.makedirs(test_folder, exist_ok=True)
        
        baseline_path = os.path.join(
            "baselines",
            "test_invalid_hash_folder_baseline.json"
        )
        
        invalid_baseline = {
            os.path.join(test_folder, "file1.txt"): "hello"
        }
        
        with open(baseline_path, "w") as file:
            json.dump(invalid_baseline, file)
            
        loaded_baseline = load_baseline(test_folder)
        
        self.assertIsNone(loaded_baseline)
        
        os.remove(baseline_path)
        os.rmdir(test_folder)
        
    
    def test_load_empty_baseline(self):
        
        test_folder = "tests/test_empty_baseline_folder"
        
        os.makedirs(test_folder, exist_ok=True)
        
        baseline_path = os.path.join(
            "baselines",
            "test_empty_baseline_folder_baseline.json"
        )
        
        with open(baseline_path, "w") as file:
            json.dump({}, file)
            
        loaded_baseline = load_baseline(test_folder)
        
        self.assertIsNone(loaded_baseline)
        
        os.remove(baseline_path)
        os.rmdir(test_folder)
        
    def test_load_invalid_path_baseline(self):
        
        test_folder = "tests/test_invalid_path_folder"
        
        os.makedirs(test_folder, exist_ok=True)
        
        baseline_path = os.path.join(
            "baselines",
            "test_invalid_path_folder_baseline.json"
        )
        
        invalid_baseline = {
            "": "a" * 64
        }
        
        with open(baseline_path, "w") as file:
            json.dump(invalid_baseline, file)
            
        loaded_baseline = load_baseline(test_folder)
        
        self.assertIsNone(loaded_baseline)
        
        os.remove(baseline_path)
        os.rmdir(test_folder)
        
        
    
    def test_load_hash_with_invalid_characters(self):

        test_folder = "tests/test_invalid_hash_chars_folder"

        os.makedirs(test_folder, exist_ok=True)

        baseline_path = os.path.join(
            "baselines",
            "test_invalid_hash_chars_folder_baseline.json"
        )

        invalid_baseline = {
            os.path.join(test_folder, "file1.txt"): "g" * 64
        }

        with open(baseline_path, "w") as file:
            json.dump(invalid_baseline, file)

        loaded_baseline = load_baseline(test_folder)

        self.assertIsNone(loaded_baseline)

        os.remove(baseline_path)
        os.rmdir(test_folder)
        
    
    def test_create_baseline_fails_if_file_cannot_be_hashed(self):
        test_folder = "tests/test_unreadable_file_folder"
        os.makedirs(test_folder, exist_ok=True)

        test_file = os.path.join(test_folder, "file1.txt")

        with open(test_file, "w") as file:
            file.write("test content")

        baseline_path = os.path.join(
            "baselines",
            "test_unreadable_file_folder_baseline.json"
        )

        # Remove an old result from a previous test run, if present.
        if os.path.exists(baseline_path):
            os.remove(baseline_path)

        # Simulate a file that cannot be hashed.
        with patch("baseline.calculate_hash", return_value=None):
            create_baseline(test_folder)

        # A baseline must not be created.
        self.assertFalse(os.path.exists(baseline_path))

        # Clean up the test file and folder.
        os.remove(test_file)
        os.rmdir(test_folder)

