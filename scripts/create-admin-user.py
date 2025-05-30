#!/usr/bin/env python3
"""
Create Admin Test User Script

Creates an admin user for development and testing purposes.
Run this from the backend directory: python ../scripts/create-admin-user.py
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from app import create_app
from app.extensions import db
from app.models.user import User


def create_admin_user():
    """Create admin test user"""
    
    # Admin user details
    admin_data = {
        'email': 'admin@rgs.test',
        'password': 'AdminPass123!',
        'first_name': 'Admin',
        'last_name': 'User',
        'sex': 'M',
        'distance_unit': 'meters',
        'timezone': 'Europe/Oslo',
        'country': 'Norway',
        'city': 'Oslo',
        'is_admin': True
    }
    
    print("🚀 Creating admin test user...")
    
    # Create Flask app context
    app = create_app('development')
    
    with app.app_context():
        # Check if admin user already exists
        existing_admin = User.query.filter_by(email=admin_data['email']).first()
        
        if existing_admin:
            print(f"⚠️  Admin user already exists: {admin_data['email']}")
            print(f"   ID: {existing_admin.id}")
            print(f"   Name: {existing_admin.full_name}")
            print(f"   Is Admin: {existing_admin.is_admin}")
            return existing_admin
        
        # Create new admin user
        try:
            admin_user = User(
                email=admin_data['email'],
                first_name=admin_data['first_name'],
                last_name=admin_data['last_name'],
                sex=admin_data['sex'],
                distance_unit=admin_data['distance_unit'],
                timezone=admin_data['timezone'],
                country=admin_data['country'],
                city=admin_data['city'],
                is_admin=admin_data['is_admin']
            )
            
            # Set password
            admin_user.set_password(admin_data['password'])
            
            # Save to database
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print(f"   Email: {admin_user.email}")
            print(f"   Password: {admin_data['password']}")
            print(f"   Name: {admin_user.full_name}")
            print(f"   ID: {admin_user.id}")
            print(f"   Is Admin: {admin_user.is_admin}")
            
            return admin_user
            
        except Exception as e:
            print(f"❌ Failed to create admin user: {str(e)}")
            db.session.rollback()
            return None


def create_test_user():
    """Create regular test user"""
    
    # Regular user details
    user_data = {
        'email': 'test@rgs.test',
        'password': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User',
        'sex': 'M',
        'distance_unit': 'meters',
        'timezone': 'Europe/Oslo',
        'country': 'Norway',
        'city': 'Bergen',
        'is_admin': False
    }
    
    print("\n👤 Creating regular test user...")
    
    # Create Flask app context
    app = create_app('development')
    
    with app.app_context():
        # Check if test user already exists
        existing_user = User.query.filter_by(email=user_data['email']).first()
        
        if existing_user:
            print(f"⚠️  Test user already exists: {user_data['email']}")
            print(f"   ID: {existing_user.id}")
            print(f"   Name: {existing_user.full_name}")
            return existing_user
        
        # Create new test user
        try:
            test_user = User(
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                sex=user_data['sex'],
                distance_unit=user_data['distance_unit'],
                timezone=user_data['timezone'],
                country=user_data['country'],
                city=user_data['city'],
                is_admin=user_data['is_admin']
            )
            
            # Set password
            test_user.set_password(user_data['password'])
            
            # Save to database
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Test user created successfully!")
            print(f"   Email: {test_user.email}")
            print(f"   Password: {user_data['password']}")
            print(f"   Name: {test_user.full_name}")
            print(f"   ID: {test_user.id}")
            print(f"   Is Admin: {test_user.is_admin}")
            
            return test_user
            
        except Exception as e:
            print(f"❌ Failed to create test user: {str(e)}")
            db.session.rollback()
            return None


if __name__ == '__main__':
    print("🔧 RGS Test User Creation Script")
    print("=" * 40)
    
    # Create admin user
    admin = create_admin_user()
    
    # Create test user
    user = create_test_user()
    
    print("\n📋 Summary:")
    print("=" * 40)
    
    if admin:
        print("✅ Admin User Ready")
        print(f"   Login: admin@rgs.test / AdminPass123!")
    
    if user:
        print("✅ Test User Ready")
        print(f"   Login: test@rgs.test / TestPass123!")
    
    print("\n🚀 You can now use these accounts for testing!")
    print("💡 Use these credentials with Postman or your API testing tool")
    print("📖 API Base URL: http://localhost:5000/api/v1") 