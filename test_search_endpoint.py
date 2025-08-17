#!/usr/bin/env python3
"""
Test script to make HTTP requests to the Flask app to test search functionality
"""
import requests
import os
import urllib.parse

# Set the environment
os.environ["NFL_BASE_DIR"] = "/tmp/test_nfl"

def test_search_endpoint():
    base_url = "http://127.0.0.1:5000"
    
    # Test searches
    test_cases = [
        {
            "name": "Search for traits - Arm Strength",
            "params": {"traits": "Arm Strength"}
        },
        {
            "name": "Search for traits - Mobility", 
            "params": {"traits": "Mobility"}
        },
        {
            "name": "Search for subroles - Accurate Passer",
            "params": {"subroles": "Accurate Passer"}
        },
        {
            "name": "Search for badges - Cannon Arm",
            "params": {"badges": "Cannon Arm"}
        },
        {
            "name": "Search for multiple traits",
            "params": {"traits": "Arm Strength,Accuracy"}
        },
        {
            "name": "Search for playtype",
            "params": {"playtype": "dropback-pass"}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        print(f"Params: {test_case['params']}")
        
        try:
            response = requests.get(f"{base_url}/search", params=test_case['params'], timeout=5)
            print(f"Status: {response.status_code}")
            
            # Check if we got results
            if "TestPlayer" in response.text:
                print("✅ Found results containing TestPlayer")
                # Count results
                result_count = response.text.count("TestPlayer:")
                print(f"   Found {result_count} results")
            else:
                print("❌ No results found")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_search_endpoint()