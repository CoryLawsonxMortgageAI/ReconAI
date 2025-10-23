#!/usr/bin/env python3
"""
Test script for Person Intelligence module
"""

import asyncio
import json
from modules.person_intel import PersonIntelligence


async def test_person_scan():
    """Test person intelligence gathering"""
    
    person_intel = PersonIntelligence()
    
    # Test with a common name (for demonstration)
    test_cases = [
        {
            "name": "John Smith",
            "state": "CA",
            "dob": None
        },
        {
            "name": "Jane Doe",
            "state": "NY",
            "dob": "1980-01-15"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {test_case['name']}")
        print(f"State: {test_case['state']}")
        print(f"{'='*60}\n")
        
        results = await person_intel.scan(
            test_case["name"],
            state=test_case["state"],
            dob=test_case["dob"]
        )
        
        print(json.dumps(results, indent=2))
        print(f"\n{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(test_person_scan())

