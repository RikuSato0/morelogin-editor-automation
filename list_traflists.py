#!/usr/bin/python3
import json
import sys
from classes.ubasics import *
from classes.cmppcapi import CMppcApi

def list_traflists():
    print("=== Listing Available Traflists ===")
    
    try:
        # Load configuration
        config = config_import()
        mppc = CMppcApi(config)
        
        print("Logging in to MPPC API...")
        mppc.Login()
        print("Login successful!")
        
        print("\n=== Searching for traflists ===")
        # Try to search for traflists
        try:
            search_results = mppc.AgentTrafListSearch('')
            print(f"Search results: {json.dumps(search_results, indent=2)}")
        except Exception as e:
            print(f"Search failed: {e}")
        
        print("\n=== Testing common traflist patterns ===")
        # Test some common traflist patterns
        test_patterns = [
            'mppc_adzjtn_us',  # Original from settings
            'mppc_adzjtn_ca',  # Current setting
            'mppc_',
            'adzjtn',
            'us',
            'ca'
        ]
        
        for pattern in test_patterns:
            try:
                print(f"\nTesting pattern: {pattern}")
                traf_data = mppc.AgentTrafListSearch(pattern)
                if 'traflists' in traf_data and traf_data['traflists']:
                    print(f"Found {len(traf_data['traflists'])} traflists with pattern '{pattern}':")
                    for traf in traf_data['traflists']:
                        print(f"  - {traf.get('uid', 'N/A')}: {traf.get('name', 'N/A')}")
                        
                        # Test if this traflist has sites
                        try:
                            # Temporarily change traflist
                            original_traflist = mppc.traflist
                            mppc.traflist = traf.get('uid', '')
                            site_data = mppc.AgentTrafList()
                            site_count = len(site_data.get('sites', []))
                            print(f"    Sites: {site_count}")
                            if site_count > 0:
                                print(f"    *** HAS ACTIVE SITES - USE THIS TRAFLIST ***")
                        except Exception as e:
                            print(f"    Error testing sites: {e}")
                        finally:
                            mppc.traflist = original_traflist
                else:
                    print(f"No traflists found with pattern '{pattern}'")
            except Exception as e:
                print(f"Error testing pattern '{pattern}': {e}")
        
        print("\n=== Test completed ===")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = list_traflists()
    sys.exit(0 if success else 1) 