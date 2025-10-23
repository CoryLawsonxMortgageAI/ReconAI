#!/usr/bin/env python3
"""
Test script for ReconAI
Performs a real scan and validates results
"""

import requests
import json
import time

API_URL = "http://localhost:8000"

def test_scan(target="example.com", scan_type="quick"):
    """Test a reconnaissance scan"""
    print(f"\n{'='*60}")
    print(f"Testing ReconAI Scan")
    print(f"Target: {target}")
    print(f"Scan Type: {scan_type}")
    print(f"{'='*60}\n")
    
    # Prepare scan request
    scan_request = {
        "target": target,
        "scan_type": scan_type,
        "modules": ["domain", "web"]
    }
    
    print("[+] Starting scan...")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_URL}/api/scan",
            json=scan_request,
            timeout=120
        )
        
        if response.status_code == 200:
            elapsed = time.time() - start_time
            print(f"[+] Scan completed in {elapsed:.2f} seconds\n")
            
            results = response.json()
            
            # Display results
            print("="*60)
            print("SCAN RESULTS")
            print("="*60)
            print(f"Scan ID: {results['scan_id']}")
            print(f"Target: {results['target']}")
            print(f"Status: {results['status']}")
            print(f"Timestamp: {results['timestamp']}")
            
            # Domain Intelligence
            if 'domain' in results['results']:
                domain = results['results']['domain']
                print(f"\n[Domain Intelligence]")
                print(f"  IP Addresses: {', '.join(domain.get('ip_addresses', []))}")
                print(f"  Nameservers: {', '.join(domain.get('nameservers', []))}")
                print(f"  Subdomains Found: {len(domain.get('subdomains', []))}")
                
                whois = domain.get('whois', {})
                if 'registrar' in whois:
                    print(f"  Registrar: {whois.get('registrar')}")
            
            # Web Intelligence
            if 'web' in results['results']:
                web = results['results']['web']
                print(f"\n[Web Intelligence]")
                print(f"  Technologies: {', '.join(web.get('technologies', []))}")
                
                sec_headers = web.get('security_headers', {})
                if 'score' in sec_headers:
                    print(f"  Security Headers: {sec_headers.get('score')} (Grade: {sec_headers.get('grade')})")
                
                ssl = web.get('ssl_info', {})
                if 'protocol' in ssl:
                    print(f"  SSL Protocol: {ssl.get('protocol')}")
            
            # AI Analysis
            analysis = results.get('analysis', {})
            print(f"\n{'='*60}")
            print("AI ANALYSIS")
            print(f"{'='*60}")
            print(f"Risk Score: {analysis.get('risk_score', 0)}/100")
            print(f"\nSummary:")
            print(analysis.get('summary', 'No summary available'))
            
            if analysis.get('recommendations'):
                print(f"\nRecommendations:")
                for i, rec in enumerate(analysis['recommendations'][:5], 1):
                    print(f"  {i}. {rec}")
            
            # Save full results
            with open('test_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n[+] Full results saved to test_results.json")
            
            return True
            
        else:
            print(f"[-] Scan failed with status code: {response.status_code}")
            print(f"[-] Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"[-] Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Test with example.com (safe, public domain)
    success = test_scan("example.com", "quick")
    
    if success:
        print(f"\n{'='*60}")
        print("✓ TEST PASSED - ReconAI is working correctly!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print("✗ TEST FAILED")
        print(f"{'='*60}\n")

