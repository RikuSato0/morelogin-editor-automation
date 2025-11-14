#!/usr/bin/python3
import json
import sys
from classes.ubasics import *
from classes.cbrowsermorelogin import CBrowserMoreLogin

def test_morelogin_permissions():
    print("=== MoreLogin API Permissions Test ===")
    
    try:
        # Load configuration
        config = config_import()
        print(f"Config loaded successfully")
        print(f"MoreLogin Base URL: {config['Browser']['base_url']}")
        print(f"MoreLogin API ID: {config['Browser']['api_id']}")
        print(f"MoreLogin Group ID: {config['Browser']['group_id']}")
        
        # Test MoreLogin API
        browser = CBrowserMoreLogin(config)
        
        print("\n=== Testing Profile List ===")
        try:
            profiles = browser.ProfileList()
            print(f"Found {len(profiles)} existing profiles")
            for profile in profiles[:3]:  # Show first 3
                print(f"  - {profile['name']} (ID: {profile['id']})")
        except Exception as e:
            print(f"ERROR listing profiles: {e}")
        
        print("\n=== Testing Proxy List ===")
        try:
            proxies = browser.ProxyList()
            print(f"Found {len(proxies)} existing proxies")
            for proxy in proxies[:3]:  # Show first 3
                print(f"  - {proxy['name']} (ID: {proxy['id']})")
        except Exception as e:
            print(f"ERROR listing proxies: {e}")
        
        print("\n=== Testing Profile Creation ===")
        try:
            # Try to create a test profile
            test_profile_id = browser.ProfileCreate(
                name="TEST_PERMISSION_PROFILE",
                proxyId=proxies[0]['id'] if proxies else 1,
                operatorSystemId=1,  # Windows
                browserTypeId=1,     # Chrome
                kernelVersion=133,   # Latest
                openUrl="https://www.google.com"
            )
            print(f"Profile creation result: {test_profile_id}")
            
            if test_profile_id:
                print("✅ Profile creation successful!")
                
                print("\n=== Testing Profile Start ===")
                start_result = browser.ProfileStart(test_profile_id)
                print(f"Profile start result: {start_result}")
                
                if start_result:
                    print("✅ Profile start successful!")
                    
                    print("\n=== Testing Profile Close ===")
                    close_result = browser.ProfileClose(test_profile_id)
                    print(f"Profile close result: {close_result}")
                    
                    if close_result:
                        print("✅ Profile close successful!")
                    else:
                        print("❌ Profile close failed!")
                else:
                    print("❌ Profile start failed - This is the main issue!")
                    
                print("\n=== Testing Profile Delete ===")
                delete_result = browser.ProfileDelete([test_profile_id])
                print(f"Profile delete result: {delete_result.ok if hasattr(delete_result, 'ok') else delete_result}")
                
            else:
                print("❌ Profile creation failed!")
                
        except Exception as e:
            print(f"ERROR during profile operations: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n=== Test completed ===")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_morelogin_permissions()
    sys.exit(0 if success else 1) 