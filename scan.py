#!/usr/bin/env python3
"""
Nexula Scan - GitHub Action
Scans repositories for AI/ML security vulnerabilities
"""
import os
import sys
import requests
import time
import json

# Get inputs from environment
API_KEY = os.getenv('INPUT_API-KEY')
SCAN_TYPE = os.getenv('INPUT_SCAN-TYPE', 'unified')
FAIL_ON_CRITICAL = os.getenv('INPUT_FAIL-ON-CRITICAL', 'true').lower() == 'true'
FAIL_ON_HIGH = os.getenv('INPUT_FAIL-ON-HIGH', 'false').lower() == 'true'

# API Configuration
API_URL = os.getenv('NEXULA_API_URL', 'https://api.nexula.one')
GITHUB_WORKSPACE = os.getenv('GITHUB_WORKSPACE', '.')

def set_output(name, value):
    """Set GitHub Action output"""
    print(f"::set-output name={name}::{value}")

def print_banner():
    """Print Nexula banner"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███╗   ██╗███████╗██╗  ██╗██╗   ██╗██╗      █████╗    ║
║   ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██║     ██╔══██╗   ║
║   ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██║     ███████║   ║
║   ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██║     ██╔══██║   ║
║   ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████╗██║  ██║   ║
║   ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ║
║                                                           ║
║            AI/ML Security Scanner                        ║
║            10 Specialized Scanners                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")

def trigger_scan():
    """Trigger scan via Nexula API"""
    print(f"\n📡 Connecting to Nexula API...")
    print(f"   Scan Type: {SCAN_TYPE}")
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Create project from GitHub repo
    repo_name = os.getenv('GITHUB_REPOSITORY', 'unknown-repo')
    
    try:
        # Trigger scan
        response = requests.post(
            f'{API_URL}/api/v1/scanner/scan/{SCAN_TYPE}/1',  # Using project_id=1 for now
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to start scan: {response.status_code}")
            print(f"   Response: {response.text}")
            sys.exit(1)
        
        data = response.json()
        scan_id = data.get('id')
        
        print(f"✅ Scan started successfully!")
        print(f"   Scan ID: {scan_id}")
        
        return scan_id
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        sys.exit(1)

def poll_scan_results(scan_id):
    """Poll for scan results"""
    print(f"\n⏳ Waiting for scan to complete...")
    
    headers = {'Authorization': f'Bearer {API_KEY}'}
    max_attempts = 360  # 1 hour max (10s intervals)
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get(
                f'{API_URL}/api/v1/scanner/scan/run/{scan_id}',
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"⚠️  Failed to get scan status: {response.status_code}")
                time.sleep(10)
                attempt += 1
                continue
            
            data = response.json()
            status = data.get('status')
            progress = data.get('progress', 0)
            
            if status == 'completed':
                return data
            elif status == 'failed':
                error = data.get('error_message', 'Unknown error')
                print(f"\n❌ Scan failed: {error}")
                sys.exit(1)
            else:
                # Show progress
                print(f"   Progress: {progress}% - {status}...", end='\r')
                time.sleep(10)
                attempt += 1
                
        except requests.exceptions.RequestException as e:
            print(f"\n⚠️  Error checking status: {e}")
            time.sleep(10)
            attempt += 1
    
    print(f"\n❌ Scan timeout after {max_attempts * 10} seconds")
    sys.exit(1)

def print_results(results):
    """Print scan results"""
    print(f"\n\n{'='*60}")
    print(f"📊 SCAN RESULTS")
    print(f"{'='*60}\n")
    
    total = results.get('total_findings', 0)
    critical = results.get('critical_count', 0)
    high = results.get('high_count', 0)
    medium = results.get('medium_count', 0)
    low = results.get('low_count', 0)
    
    print(f"Total Findings: {total}")
    print(f"")
    print(f"  🔴 Critical: {critical}")
    print(f"  🟠 High:     {high}")
    print(f"  🟡 Medium:   {medium}")
    print(f"  🟢 Low:      {low}")
    print(f"")
    
    scan_id = results.get('id')
    scan_url = f"https://cloud.nexula.one/scans/{scan_id}"
    
    print(f"📄 View detailed results:")
    print(f"   {scan_url}")
    print(f"\n{'='*60}\n")
    
    # Set outputs
    set_output('scan-id', scan_id)
    set_output('findings-count', total)
    set_output('critical-count', critical)
    set_output('high-count', high)
    set_output('scan-url', scan_url)
    
    return critical, high

def main():
    """Main execution"""
    print_banner()
    
    # Validate API key
    if not API_KEY:
        print("❌ Error: NEXULA_API_KEY is required")
        print("   Get your free API key at: https://nexula.one")
        sys.exit(1)
    
    # Trigger scan
    scan_id = trigger_scan()
    
    # Poll for results
    results = poll_scan_results(scan_id)
    
    # Print results
    critical, high = print_results(results)
    
    # Check if should fail
    if FAIL_ON_CRITICAL and critical > 0:
        print(f"❌ Build failed: {critical} critical vulnerabilities found")
        sys.exit(1)
    
    if FAIL_ON_HIGH and high > 0:
        print(f"❌ Build failed: {high} high severity vulnerabilities found")
        sys.exit(1)
    
    print("✅ Scan completed successfully!")
    sys.exit(0)

if __name__ == '__main__':
    main()
