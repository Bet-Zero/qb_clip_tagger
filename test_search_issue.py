#!/usr/bin/env python3
"""
Test script to reproduce the search issue with traits, subroles, and badges
"""
import os
import json
import tempfile
import importlib
from pathlib import Path

def test_search_issue():
    """Test the search functionality for traits, subroles, and badges"""
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmp_dir:
        base = Path(tmp_dir) / "NFLFilm"
        base.mkdir()
        
        # Set environment and reload modules
        os.environ["NFL_BASE_DIR"] = str(base)
        
        # Import modules
        import sys
        sys.path.insert(0, os.getcwd())
        
        config = importlib.import_module("config")
        importlib.reload(config)
        tag_utils = importlib.import_module("tag_utils")
        importlib.reload(tag_utils)
        search_clips = importlib.import_module("search_clips")
        importlib.reload(search_clips)
        
        # Create a test clip
        clip_dir = Path(tmp_dir) / "watch"
        clip_dir.mkdir()
        clip_path = clip_dir / "test.mp4"
        clip_path.write_text("test data")
        
        # Test data with traits, subroles, and badges
        test_data = {
            "player": ["Mahomes"],
            "side": ["Offense"],
            "playtype": ["dropback-pass"],
            "outcome": ["Completion"],
            "traits": ["Arm Strength,Accuracy"],  # Note: comma-separated string
            "roles": ["Pocket Passer"],
            "subroles": ["Accurate Passer,Deep Ball Thrower"],  # Note: comma-separated string
            "badges": ["Cannon Arm,Surgeon"],  # Note: comma-separated string
            "context": ["1Q"],
            "situation": ["clean-pocket"],
            "quality": ["Good"],
        }
        
        print("Test data being processed:")
        print(json.dumps(test_data, indent=2))
        
        # Process the clip
        tag_utils.process_clip_tags(str(clip_path), test_data)
        
        # Check what was actually saved
        log_path = base / "Mahomes" / "tag_log.json"
        with open(log_path) as f:
            saved_data = json.load(f)
        
        print("\nSaved data in log:")
        print(json.dumps(saved_data, indent=2))
        
        # Load logs and test search
        logs = search_clips.load_logs()
        print(f"\nLoaded {len(logs)} log entries")
        
        if logs:
            entry = logs[0]
            print("\nFirst log entry:")
            print(json.dumps(entry, indent=2))
            
            # Test various search filters
            test_filters = [
                {
                    "name": "Search for traits",
                    "filters": {
                        "player": None,
                        "side": None,
                        "playtype": None,
                        "outcome": None,
                        "context": None,
                        "situation": None,
                        "quality": None,
                        "traits": ["Arm Strength"],
                        "roles": [],
                        "subroles": [],
                        "badges": [],
                    }
                },
                {
                    "name": "Search for subroles",
                    "filters": {
                        "player": None,
                        "side": None,
                        "playtype": None,
                        "outcome": None,
                        "context": None,
                        "situation": None,
                        "quality": None,
                        "traits": [],
                        "roles": [],
                        "subroles": ["Accurate Passer"],
                        "badges": [],
                    }
                },
                {
                    "name": "Search for badges",
                    "filters": {
                        "player": None,
                        "side": None,
                        "playtype": None,
                        "outcome": None,
                        "context": None,
                        "situation": None,
                        "quality": None,
                        "traits": [],
                        "roles": [],
                        "subroles": [],
                        "badges": ["Cannon Arm"],
                    }
                },
            ]
            
            for test_case in test_filters:
                print(f"\n{test_case['name']}:")
                print(f"Filter: {test_case['filters']}")
                matches = search_clips.matches(entry, test_case['filters'])
                print(f"Matches: {matches}")
                
                # Debug the matching process
                for key, val in test_case['filters'].items():
                    if not val:
                        continue
                    if isinstance(val, list):
                        entry_val = entry.get(key, [])
                        subset_check = set(val).issubset(set(entry_val))
                        print(f"  {key}: filter={val}, entry={entry_val}, issubset={subset_check}")
                    else:
                        entry_val = entry.get(key, "")
                        equals_check = str(entry_val) == str(val)
                        print(f"  {key}: filter={val}, entry={entry_val}, equals={equals_check}")

if __name__ == "__main__":
    test_search_issue()