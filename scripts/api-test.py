#!/usr/bin/env python3
"""
RGS API Testing Script

Manual testing script for RGS API endpoints.
Provides a convenient way to test APIs without Postman.
"""
import requests
import json
import sys
from typing import Dict, Any, Optional


class RGSAPITester:
    """API testing helper class"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000/api/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        
    def set_auth_token(self, token: str):
        """Set authentication token for requests"""
        self.access_token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
    
    def request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict[str, Any]:
        """Make API request"""
        url = f"{self.base_url}{endpoint}"
        
        print(f"\n🔗 {method.upper()} {url}")
        if data:
            print(f"📤 Data: {json.dumps(data, indent=2)}")
        if params:
            print(f"🔍 Params: {params}")
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params
            )
            
            print(f"📊 Status: {response.status_code}")
            
            try:
                result = response.json()
                print(f"📥 Response: {json.dumps(result, indent=2)}")
                return result
            except json.JSONDecodeError:
                print(f"📥 Response (text): {response.text}")
                return {"error": "Invalid JSON response"}
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {str(e)}")
            return {"error": str(e)}
    
    def login(self, email: str, password: str) -> bool:
        """Login and set auth token"""
        data = {"email": email, "password": password}
        result = self.request("POST", "/auth/login", data)
        
        if result.get("success") and result.get("access_token"):
            self.set_auth_token(result["access_token"])
            print("✅ Login successful!")
            return True
        else:
            print("❌ Login failed!")
            return False
    
    def register(self, email: str, password: str, first_name: str, last_name: str) -> bool:
        """Register new user"""
        data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        result = self.request("POST", "/auth/register", data)
        
        if result.get("success"):
            if result.get("access_token"):
                self.set_auth_token(result["access_token"])
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            return False


def test_auth_endpoints(api: RGSAPITester):
    """Test authentication endpoints"""
    print("\n" + "="*50)
    print("🔐 TESTING AUTHENTICATION ENDPOINTS")
    print("="*50)
    
    # Test login with admin user
    print("\n1. Testing Admin Login")
    success = api.login("admin@rgs.test", "AdminPass123!")
    
    if success:
        # Test get current user
        print("\n2. Testing Get Current User")
        api.request("GET", "/auth/me")
        
        # Test token refresh
        print("\n3. Testing Token Refresh")
        api.request("POST", "/auth/refresh")


def test_user_endpoints(api: RGSAPITester):
    """Test user management endpoints"""
    print("\n" + "="*50)
    print("👥 TESTING USER ENDPOINTS")
    print("="*50)
    
    # Test get all users (admin only)
    print("\n1. Testing Get All Users")
    api.request("GET", "/users")
    
    # Test get user by ID
    print("\n2. Testing Get User by ID")
    api.request("GET", "/users/1")
    
    # Test user search
    print("\n3. Testing User Search")
    api.request("GET", "/users/search", params={"q": "admin"})


def test_password_reset(api: RGSAPITester):
    """Test password reset functionality"""
    print("\n" + "="*50)
    print("🔑 TESTING PASSWORD RESET")
    print("="*50)
    
    # Test forgot password
    print("\n1. Testing Forgot Password")
    api.request("POST", "/auth/forgot-password", {"email": "test@rgs.test"})
    
    print("\n💡 Note: Check your email configuration to see if the reset email was sent")
    print("   The reset token would be in the email for testing reset-password endpoint")


def interactive_mode(api: RGSAPITester):
    """Interactive testing mode"""
    print("\n" + "="*50)
    print("🎮 INTERACTIVE MODE")
    print("="*50)
    
    while True:
        print("\nAvailable commands:")
        print("1. login <email> <password>")
        print("2. register <email> <password> <first_name> <last_name>")
        print("3. get <endpoint>")
        print("4. post <endpoint> <json_data>")
        print("5. put <endpoint> <json_data>")
        print("6. delete <endpoint>")
        print("7. quit")
        
        command = input("\n🎯 Enter command: ").strip().split()
        
        if not command:
            continue
            
        if command[0] == "quit":
            break
        elif command[0] == "login" and len(command) >= 3:
            api.login(command[1], command[2])
        elif command[0] == "register" and len(command) >= 5:
            api.register(command[1], command[2], command[3], command[4])
        elif command[0] == "get" and len(command) >= 2:
            api.request("GET", command[1])
        elif command[0] in ["post", "put"] and len(command) >= 3:
            try:
                data = json.loads(" ".join(command[2:]))
                api.request(command[0].upper(), command[1], data)
            except json.JSONDecodeError:
                print("❌ Invalid JSON data")
        elif command[0] == "delete" and len(command) >= 2:
            api.request("DELETE", command[1])
        else:
            print("❌ Invalid command or missing parameters")


def main():
    """Main testing function"""
    print("🚀 RGS API Testing Tool")
    print("=" * 50)
    
    # Initialize API tester
    api = RGSAPITester()
    
    # Check if server is running
    try:
        response = requests.get("http://127.0.0.1:5000/health")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("⚠️  Server responded but may have issues")
    except requests.exceptions.RequestException:
        print("❌ Server is not running!")
        print("💡 Start the server with: flask run")
        return
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print("\nSelect testing mode:")
        print("1. auth - Test authentication endpoints")
        print("2. users - Test user management endpoints")
        print("3. reset - Test password reset")
        print("4. interactive - Interactive mode")
        print("5. all - Run all tests")
        
        mode = input("\n🎯 Enter mode (1-5): ").strip()
    
    if mode in ["1", "auth"]:
        test_auth_endpoints(api)
    elif mode in ["2", "users"]:
        # Need to login first for user endpoints
        if api.login("admin@rgs.test", "AdminPass123!"):
            test_user_endpoints(api)
    elif mode in ["3", "reset"]:
        test_password_reset(api)
    elif mode in ["4", "interactive"]:
        interactive_mode(api)
    elif mode in ["5", "all"]:
        test_auth_endpoints(api)
        test_user_endpoints(api)
        test_password_reset(api)
    else:
        print("❌ Invalid mode selected")


if __name__ == "__main__":
    main() 