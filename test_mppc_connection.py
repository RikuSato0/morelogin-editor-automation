#!/usr/bin/python3
import json
import sys
from classes.ubasics import *
from classes.cmppcapi import CMppcApi

def test_mppc_connection():
    print("=== MPPC Connection Test ===")
    
    try:
        # Load configuration
        config = config_import()
        print(f"Config loaded successfully")
        print(f"MPPC Base URL: {config['MppcApi']['base_url']}")
        print(f"MPPC Login: {config['MppcApi']['login']}")
        print(f"MPPC Traflist: {config['MppcApi']['traflist']}")
        
        # Test MPPC API
        mppc = CMppcApi(config)
        
        print("\n=== Testing MPPC Login ===")
        mppc.Login()
        print("Login successful!")
        
        print("\n=== Testing AgentTrafList ===")
        traf_data = mppc.AgentTrafList()
        print(f"Traf data type: {type(traf_data)}")
        print(f"Traf data keys: {list(traf_data.keys()) if isinstance(traf_data, dict) else 'Not a dict'}")
        
        if isinstance(traf_data, dict):
            if 'sites' in traf_data:
                print(f"Number of sites: {len(traf_data['sites'])}")
                if traf_data['sites']:
                    print(f"First site structure: {json.dumps(traf_data['sites'][0], indent=2)}")
                else:
                    print("WARNING: Sites array is empty!")
            else:
                print("WARNING: No 'sites' key found in response!")
                print(f"Available keys: {list(traf_data.keys())}")
        
        print("\n=== Test completed successfully ===")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_mppc_connection()
    sys.exit(0 if success else 1) 