import unittest
import os
import json 

from baseline import create_baseline, load_baseline
from file_utils import calculate_hash


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