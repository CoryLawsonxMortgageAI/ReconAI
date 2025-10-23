#!/usr/bin/env python3
"""
Comprehensive test script for Person Intelligence module
Tests multiple scenarios and validates all functionality
"""

import asyncio
import json
from modules.person_intel import PersonIntelligence


async def test_all_scenarios():
    """Test person intelligence with various scenarios"""
    
    person_intel = PersonIntelligence()
    
    test_cases = [
        {
            "name": "Test Case 1: California with DOB",
            "person": "Michael Johnson",
            "state": "CA",
            "dob": "1975-06-15"
        },
        {
            "name": "Test Case 2: Texas without DOB",
            "person": "Sarah Williams",
            "state": "TX",
            "dob": None
        },
        {
            "name": "Test Case 3: Florida with DOB",
            "person": "Robert Brown",
            "state": "FL",
            "dob": "1988-03-22"
        },
        {
            "name": "Test Case 4: Illinois without state",
            "person": "Jennifer Davis",
            "state": None,
            "dob": None
        },
        {
            "name": "Test Case 5: Pennsylvania with middle name",
            "person": "James Michael Wilson",
            "state": "PA",
            "dob": "1992-11-08"
        }
    ]
    
    results_summary = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"{test_case['name']}")
        print(f"Person: {test_case['person']}")
        print(f"State: {test_case['state'] or 'Not specified'}")
        print(f"DOB: {test_case['dob'] or 'Not specified'}")
        print(f"{'='*70}\n")
        
        try:
            # Run the scan
            results = await person_intel.scan(
                test_case["person"],
                state=test_case["state"],
                dob=test_case["dob"]
            )
            
            # Validate results structure
            assert "target" in results, "Missing 'target' field"
            assert "timestamp" in results, "Missing 'timestamp' field"
            assert "identity" in results, "Missing 'identity' field"
            assert "criminal_records" in results, "Missing 'criminal_records' field"
            assert "court_cases" in results, "Missing 'court_cases' field"
            assert "professional_info" in results, "Missing 'professional_info' field"
            assert "social_media" in results, "Missing 'social_media' field"
            assert "public_records" in results, "Missing 'public_records' field"
            
            # Count data points
            criminal_sources = len(results.get("criminal_records", []))
            court_sources = len(results.get("court_cases", []))
            social_platforms = len([k for k, v in results.get("social_media", {}).items() if v])
            property_sources = len(results.get("property_records", []))
            business_sources = len(results.get("business_registrations", []))
            
            total_sources = criminal_sources + court_sources + social_platforms + property_sources + business_sources
            
            # Print summary
            print(f"✅ Test Passed!")
            print(f"   - Criminal Record Sources: {criminal_sources}")
            print(f"   - Court Record Sources: {court_sources}")
            print(f"   - Social Media Platforms: {social_platforms}")
            print(f"   - Property Record Sources: {property_sources}")
            print(f"   - Business Record Sources: {business_sources}")
            print(f"   - Total Data Sources: {total_sources}")
            
            # Parse name validation
            parsed_name = results["identity"]["parsed_name"]
            print(f"   - Name Parsed: {parsed_name['first_name']} {parsed_name['last_name']}")
            
            results_summary.append({
                "test_case": test_case["name"],
                "status": "PASSED",
                "total_sources": total_sources,
                "criminal_sources": criminal_sources,
                "court_sources": court_sources,
                "error": None
            })
            
        except Exception as e:
            print(f"❌ Test Failed!")
            print(f"   Error: {str(e)}")
            results_summary.append({
                "test_case": test_case["name"],
                "status": "FAILED",
                "error": str(e)
            })
    
    # Print final summary
    print(f"\n{'='*70}")
    print("FINAL TEST SUMMARY")
    print(f"{'='*70}\n")
    
    passed = sum(1 for r in results_summary if r["status"] == "PASSED")
    failed = sum(1 for r in results_summary if r["status"] == "FAILED")
    
    print(f"Total Tests: {len(results_summary)}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {failed} ❌")
    print(f"Success Rate: {(passed/len(results_summary)*100):.1f}%\n")
    
    for result in results_summary:
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"{status_icon} {result['test_case']}: {result['status']}")
        if result["status"] == "PASSED":
            print(f"   Total Sources: {result['total_sources']}")
        else:
            print(f"   Error: {result['error']}")
    
    print(f"\n{'='*70}\n")
    
    # Save results to file
    with open("test_results_comprehensive.json", "w") as f:
        json.dump(results_summary, f, indent=2)
    
    print("✅ Test results saved to: test_results_comprehensive.json")
    
    return passed == len(results_summary)


if __name__ == "__main__":
    success = asyncio.run(test_all_scenarios())
    exit(0 if success else 1)

