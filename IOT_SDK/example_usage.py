#!/usr/bin/env python3
"""
Example usage of the updated IOT SDK for expense claim API
This script demonstrates how to use the IOT SDK to submit sensor data as expense claims
"""

from main import start_sdk, submit_new_claim, update_existing_claim
import time

def example_basic_usage():
    """Basic usage example - submit a new claim"""
    print("=" * 60)
    print("🔬 IOT SDK - Basic Usage Example")
    print("=" * 60)
    
    # Submit a new expense claim with sensor data (no authentication)
    success = submit_new_claim(use_auth=False)
    
    if success:
        print("✅ Basic claim submission successful!")
    else:
        print("❌ Basic claim submission failed!")

def example_with_project():
    """Example with project ID"""
    print("\n" + "=" * 60)
    print("🏢 IOT SDK - With Project ID Example")
    print("=" * 60)
    
    # Submit claim with project ID (no authentication)
    project_id = "PROJ-001"
    success = submit_new_claim(project_id=project_id, use_auth=False)
    
    if success:
        print(f"✅ Claim submission with project {project_id} successful!")
    else:
        print(f"❌ Claim submission with project {project_id} failed!")

def example_with_authentication():
    """Example with authentication (if you have a token)"""
    print("\n" + "=" * 60)
    print("🔐 IOT SDK - With Authentication Example")
    print("=" * 60)
    
    # Submit claim with authentication (if you have a token)
    success = submit_new_claim(use_auth=True)
    
    if success:
        print("✅ Claim submission with authentication successful!")
    else:
        print("❌ Claim submission with authentication failed!")
        print("💡 Make sure you have set AUTH_TOKEN in config.py")

def example_with_master_claim():
    """Example with master claim ID"""
    print("\n" + "=" * 60)
    print("📋 IOT SDK - With Master Claim ID Example")
    print("=" * 60)
    
    # Submit claim with master claim ID (no authentication)
    master_claim_id = "MCLAIM-2024-001"
    success = submit_new_claim(master_claim_id=master_claim_id, use_auth=False)
    
    if success:
        print(f"✅ Claim submission with master claim {master_claim_id} successful!")
    else:
        print(f"❌ Claim submission with master claim {master_claim_id} failed!")

def example_update_claim():
    """Example updating an existing claim"""
    print("\n" + "=" * 60)
    print("✏️ IOT SDK - Update Existing Claim Example")
    print("=" * 60)
    
    # Update an existing claim (no authentication)
    claim_id = "CLAIM-2024-001"
    success = update_existing_claim(claim_id, use_auth=False)
    
    if success:
        print(f"✅ Claim update for {claim_id} successful!")
    else:
        print(f"❌ Claim update for {claim_id} failed!")

def example_continuous_monitoring():
    """Example of continuous monitoring with periodic submissions"""
    print("\n" + "=" * 60)
    print("🔄 IOT SDK - Continuous Monitoring Example")
    print("=" * 60)
    
    print("Starting continuous monitoring...")
    print("Press Ctrl+C to stop")
    
    try:
        count = 0
        while True:
            count += 1
            print(f"\n📊 Reading #{count} - {time.strftime('%H:%M:%S')}")
            
            success = submit_new_claim(use_auth=False)
            
            if success:
                print(f"✅ Reading #{count} submitted successfully")
            else:
                print(f"❌ Reading #{count} failed")
            
            # Wait 30 seconds before next reading
            print("⏳ Waiting 30 seconds for next reading...")
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n🛑 Continuous monitoring stopped by user")

def example_custom_parameters():
    """Example with all custom parameters"""
    print("\n" + "=" * 60)
    print("⚙️ IOT SDK - Custom Parameters Example")
    print("=" * 60)
    
    # Use all custom parameters
    project_id = "PROJ-002"
    master_claim_id = "MCLAIM-2024-002"
    
    success = start_sdk(
        is_edit_mode=False,
        master_claim_id=master_claim_id,
        project_id=project_id,
        use_auth=False
    )
    
    if success:
        print(f"✅ Custom claim submission successful!")
        print(f"   Project: {project_id}")
        print(f"   Master Claim: {master_claim_id}")
    else:
        print(f"❌ Custom claim submission failed!")

def main():
    """Run all examples"""
    print("🚀 IOT SDK Expense Claim Examples")
    print("This demonstrates how to use the IOT SDK with your expense claim API format")
    
    # Run examples
    example_basic_usage()
    example_with_project()
    example_with_authentication()
    example_with_master_claim()
    example_update_claim()
    example_custom_parameters()
    
    # Ask user if they want to run continuous monitoring
    print("\n" + "=" * 60)
    response = input("🔄 Would you like to run continuous monitoring? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        example_continuous_monitoring()
    
    print("\n🎉 All examples completed!")

if __name__ == "__main__":
    main() 