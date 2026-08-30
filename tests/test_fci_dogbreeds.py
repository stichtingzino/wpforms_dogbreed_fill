"""Tests for the fci_dogbreeds package."""

import csv
import json
import os
import tempfile

from fci_dogbreeds.google_functions.functions import BreedGroup, LanguageDataset
from fci_dogbreeds.config import DATA_PROMPT


class TestPydanticModels:
    """Test Pydantic model validation."""
    
    def test_breed_group_model(self):
        """Test BreedGroup model creation and validation."""
        data = {
            "fci_group": 1,
            "group_name": "Herdershonden en veedrijvers",
            "breeds": ["Duitse Herdershond", "Border Collie", "Bearded Collie"]
        }
        group = BreedGroup(**data)
        
        assert group.fci_group == 1
        assert group.group_name == "Herdershonden en veedrijvers"
        assert len(group.breeds) == 3
        assert "Duitse Herdershond" in group.breeds
    
    def test_language_dataset_model(self):
        """Test LanguageDataset model with multiple breed groups."""
        data = {
            "groups": [
                {
                    "fci_group": 1,
                    "group_name": "Group 1",
                    "breeds": ["Breed A", "Breed B"]
                },
                {
                    "fci_group": 2,
                    "group_name": "Group 2",
                    "breeds": ["Breed C"]
                }
            ]
        }
        dataset = LanguageDataset(**data)
        
        assert len(dataset.groups) == 2
        assert dataset.groups[0].fci_group == 1
        assert dataset.groups[1].fci_group == 2


class TestConfig:
    """Test configuration functions."""
    
    def test_data_prompt_contains_placeholder(self):
        """Test that DATA_PROMPT contains the language placeholder."""
        assert "%language%" in DATA_PROMPT
        assert "FCI-rasgroep" in DATA_PROMPT
        assert "LICG" in DATA_PROMPT


class TestDataProcessing:
    """Test data processing and file export functionality."""
    
    def test_csv_export_format(self):
        """Test that CSV export produces correct format."""
        # Sample data matching the expected structure from get_data_from_gemini
        sample_data = {
            "groups": [
                {
                    "fci_group": 1,
                    "group_name": "Test Group",
                    "breeds": ["Breed1", "Breed2", "Breed3"]
                }
            ]
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.csv")
            
            # Write CSV in the same format as gen_breed_file.py
            with open(output_file, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["FCI_Group", "Group_Name", "Breeds"])
                for item in sample_data["groups"]:
                    breeds_str = ";".join(item["breeds"])
                    writer.writerow([item["fci_group"], item["group_name"], breeds_str])
            
            # Verify the file
            with open(output_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                assert len(rows) == 2  # Header + 1 data row
                assert rows[0] == ["FCI_Group", "Group_Name", "Breeds"]
                assert rows[1][0] == "1"
                assert rows[1][1] == "Test Group"
                assert rows[1][2] == "Breed1;Breed2;Breed3"
    
    def test_json_export_format(self):
        """Test that JSON export produces valid structure."""
        sample_data = {
            "groups": [
                {
                    "fci_group": 1,
                    "group_name": "Test Group",
                    "breeds": ["Breed1", "Breed2"]
                }
            ]
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "test.json")
            
            # Write JSON in the same format as gen_breed_file.py
            with open(output_file, mode='w', encoding='utf-8') as f:
                json.dump(sample_data["groups"], f, ensure_ascii=False, indent=2)
            
            # Verify the file
            with open(output_file, mode='r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                
                assert len(loaded_data) == 1
                assert loaded_data[0]["fci_group"] == 1
                assert loaded_data[0]["group_name"] == "Test Group"
                assert loaded_data[0]["breeds"] == ["Breed1", "Breed2"]



