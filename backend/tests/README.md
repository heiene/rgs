# RGS Test Suite 🧪

This directory contains the comprehensive test suite for the RGS (Round Golf System) backend. The tests ensure code quality, catch regressions, and serve as living documentation of the API behavior.

## 📁 Test Organization

### **Test Files Structure**
```
backend/tests/
├── test_app.py           # Basic application functionality & health checks
├── test_auth.py          # Authentication API endpoints & JWT handling
├── test_models.py        # Core database models (User, Club, Theme)
├── test_golf_models.py   # Golf-specific models (Course, Round, Score) 
├── test_email_service.py # Email functionality & templates
├── conftest.py          # Test fixtures and shared configuration
└── pytest.ini          # Pytest settings and options
```

### **Test Categories**

**🔍 Unit Tests**
- Individual model methods and properties
- Service class functions and business logic
- Utility functions and helpers
- Data validation and serialization

**🔗 Integration Tests** 
- API endpoint workflows
- Database relationships and constraints
- Service integration (email, authentication)
- Cross-model interactions

**🌐 End-to-End Tests**
- Complete user authentication flows
- Multi-step API workflows
- Full feature scenarios

---

## 🚀 Running Tests

### **Quick Commands**
```bash
# Run all tests
python scripts/run-tests.py

# Run with verbose output
python scripts/run-tests.py -v

# Run with coverage report (generates HTML in backend/htmlcov/)
python scripts/run-tests.py --coverage

# Watch mode - auto-rerun when files change
python scripts/run-tests.py --watch
```

### **Module-Specific Testing**
```bash
# Test authentication only
python scripts/run-tests.py -m test_auth

# Test database models
python scripts/run-tests.py -m test_models

# Test email functionality
python scripts/run-tests.py -m test_email_service

# Test basic app functionality
python scripts/run-tests.py -m test_app
```

### **Granular Testing with Pytest**
```bash
cd backend

# Run specific test class
python -m pytest tests/test_auth.py::TestAuthLogin -v

# Run single test method
python -m pytest tests/test_auth.py::TestAuthLogin::test_login_success -v

# Run tests matching a pattern
python -m pytest tests/ -k "login" -v

# Stop on first failure
python -m pytest tests/ -x

# Run only failed tests from last run
python -m pytest tests/ --lf

# Run with live output (see print statements)
python -m pytest tests/test_auth.py -s
```

---

## 🔧 Test Configuration

### **Test Environment (`conftest.py`)**
The test suite uses optimized configuration for speed and isolation:

```python
# Automatic test configuration
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Fast in-memory database
BCRYPT_LOG_ROUNDS = 4                           # Faster password hashing
MAIL_SUPPRESS_SEND = True                       # No actual emails sent
```

### **Available Test Fixtures**
Use these fixtures in your tests by adding them as function parameters:

```python
def test_example(client, test_user, auth_headers):
    # Your test code here
    pass
```

**Core Fixtures:**
- `app` - Flask application instance with test config
- `client` - Test client for making API requests
- `db` - Database session for direct database operations

**User & Authentication:**
- `test_user` - Regular user (email: test@example.com, password: testpass123)
- `admin_user` - Admin user with elevated privileges
- `auth_headers` - Authorization headers for authenticated requests
- `admin_headers` - Authorization headers for admin requests

**Golf-Related:**
- `test_club` - Sample golf club for testing
- `test_theme` - Sample theme for testing
- `test_course` - Sample golf course (when implemented)

**Usage Example:**
```python
def test_user_profile(client, auth_headers):
    """Test getting user profile with authentication"""
    response = client.get('/api/v1/auth/me', headers=auth_headers)
    assert response.status_code == 200
    assert 'email' in response.get_json()['user']
```

---

## ✏️ Writing Tests

### **Test Naming Convention**
```python
class TestFeatureName:
    """Test feature description"""
    
    def test_success_scenario(self):
        """Test successful operation"""
        
    def test_failure_scenario(self):
        """Test error handling"""
        
    def test_edge_case(self):
        """Test boundary conditions"""
        
    def test_validation_error(self):
        """Test input validation"""
```

### **Basic Test Structure**
```python
import pytest
from app.models.user import User

class TestUserAuthentication:
    """Test user authentication functionality"""
    
    def test_login_success(self, client, test_user):
        """Test successful login with valid credentials"""
        # Arrange
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        # Act
        response = client.post('/api/v1/auth/login', json=login_data)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert data['user']['email'] == 'test@example.com'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/api/v1/auth/login', json={
            'email': 'wrong@example.com',
            'password': 'wrongpass'
        })
        
        assert response.status_code == 401
        assert 'Invalid credentials' in response.get_json()['error']
```

### **Testing Authenticated Endpoints**
```python
def test_authenticated_endpoint(client, auth_headers):
    """Test endpoint requiring authentication"""
    response = client.get('/api/v1/auth/me', headers=auth_headers)
    assert response.status_code == 200

def test_admin_endpoint(client, admin_headers):
    """Test endpoint requiring admin privileges"""
    response = client.get('/api/v1/users/', headers=admin_headers)
    assert response.status_code == 200
```

### **Testing Database Models**
```python
def test_user_model_creation(app):
    """Test creating user model"""
    with app.app_context():
        user = User(
            email='new@example.com',
            first_name='New',
            last_name='User',
            sex='M'
        )
        user.set_password('testpass123')
        
        assert user.email == 'new@example.com'
        assert user.check_password('testpass123')
        assert not user.check_password('wrongpass')
```

---

## 🎯 Testing Scenarios

### **Authentication Testing**
```python
# Test authentication flows
def test_complete_auth_flow(client, app):
    """Test registration -> login -> protected access"""
    # 1. Register new user
    register_response = client.post('/api/v1/auth/register', json={...})
    assert register_response.status_code == 201
    
    # 2. Login with new user
    login_response = client.post('/api/v1/auth/login', json={...})
    assert login_response.status_code == 200
    token = login_response.get_json()['access_token']
    
    # 3. Access protected endpoint
    headers = {'Authorization': f'Bearer {token}'}
    me_response = client.get('/api/v1/auth/me', headers=headers)
    assert me_response.status_code == 200
```

### **Error Handling Testing**
```python
def test_validation_errors(client):
    """Test API validation error responses"""
    # Missing required fields
    response = client.post('/api/v1/auth/login', json={})
    assert response.status_code == 400
    
    # Invalid email format
    response = client.post('/api/v1/auth/register', json={
        'email': 'invalid-email',
        'password': 'validpass123',
        # ... other fields
    })
    assert response.status_code == 400
```

### **Permission Testing**
```python
def test_user_permissions(client, auth_headers, admin_headers):
    """Test different permission levels"""
    # Regular user cannot access admin endpoint
    response = client.get('/api/v1/users/', headers=auth_headers)
    assert response.status_code == 403
    
    # Admin can access admin endpoint
    response = client.get('/api/v1/users/', headers=admin_headers)
    assert response.status_code == 200
```

---

## 🔍 Debugging Tests

### **Running Specific Failing Tests**
```bash
# Run single failing test with verbose output
python -m pytest tests/test_auth.py::TestAuthLogin::test_login_success -v -s

# Run all tests in a class
python -m pytest tests/test_auth.py::TestAuthLogin -v

# Run tests matching pattern
python -m pytest tests/ -k "login and success" -v
```

### **Adding Debug Output**
```python
def test_debug_example(client, test_user):
    """Test with debug output"""
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    # Debug output (visible with -s flag)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.get_json()}")
    
    assert response.status_code == 200
```

### **Database State Inspection**
```python
def test_database_state(app, test_user):
    """Test with database inspection"""
    with app.app_context():
        from app.models.user import User
        
        # Check user exists in database
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        print(f"User ID: {user.id}, Active: {user.is_active}")
```

---

## 📊 Coverage Analysis

### **Generating Coverage Reports**
```bash
# Run tests with coverage
python scripts/run-tests.py --coverage

# View HTML report
open backend/htmlcov/index.html
```

### **Coverage Goals**
- **Critical Authentication:** >95% coverage
- **Core Models:** >90% coverage
- **API Endpoints:** >85% coverage
- **Service Classes:** >80% coverage
- **Overall Project:** >75% coverage

### **Understanding Coverage**
- **Lines:** Code lines executed during tests
- **Branches:** Conditional paths taken
- **Functions:** Functions called during tests
- **Missing:** Code not covered by any test

---

## 🧹 Test Maintenance

### **Test Isolation**
- Each test gets a fresh database state
- Tests should not depend on other tests
- Use fixtures for common setup

### **Test Performance**
- Keep unit tests fast (< 1 second each)
- Use in-memory database for speed
- Mock external services

### **Test Organization**
- Group related tests in classes
- Use descriptive test names
- Include docstrings for complex tests

---

## 🎪 Advanced Testing

### **Mocking External Services**
```python
from unittest.mock import patch

def test_email_service_mock(client, test_user):
    """Test with mocked email service"""
    with patch('app.services.email_service.EmailService.send_welcome_email') as mock_email:
        response = client.post('/api/v1/auth/register', json={...})
        assert response.status_code == 201
        mock_email.assert_called_once()
```

### **Parameterized Tests**
```python
@pytest.mark.parametrize("email,password,expected_status", [
    ("valid@example.com", "validpass123", 200),
    ("invalid@", "validpass123", 400),
    ("valid@example.com", "short", 400),
])
def test_login_variations(client, email, password, expected_status):
    """Test login with various input combinations"""
    response = client.post('/api/v1/auth/login', json={
        'email': email,
        'password': password
    })
    assert response.status_code == expected_status
```

### **Custom Test Fixtures**
```python
@pytest.fixture
def inactive_user(app):
    """Create an inactive user for testing"""
    with app.app_context():
        from app.models.user import User
        from app.extensions import db
        
        user = User(
            email='inactive@example.com',
            first_name='Inactive',
            last_name='User',
            sex='M',
            is_active=False
        )
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
        return user
```

---

## 🎯 Testing Checklist

### **Before Committing Code**
- [ ] All tests pass: `python scripts/run-tests.py`
- [ ] No coverage regressions: `python scripts/run-tests.py --coverage`
- [ ] New features have tests
- [ ] Tests are properly named and documented

### **When Adding New Features**
- [ ] Write tests first (TDD approach)
- [ ] Test both success and failure scenarios
- [ ] Test edge cases and validation
- [ ] Update this README if adding new test patterns

### **When Debugging Issues**
- [ ] Run specific failing tests: `python -m pytest tests/test_file.py::test_name -v -s`
- [ ] Check test isolation (run tests in different orders)
- [ ] Verify test data and fixtures
- [ ] Check for external dependencies

---

## 📝 Best Practices

1. **Test Naming:** Use descriptive names that explain what is being tested
2. **Test Structure:** Follow Arrange-Act-Assert pattern
3. **Test Independence:** Tests should not depend on each other
4. **Test Data:** Use fixtures for consistent test data
5. **Assertions:** Be specific about what you're testing
6. **Documentation:** Add docstrings for complex test scenarios
7. **Coverage:** Aim for high coverage but focus on critical paths
8. **Performance:** Keep tests fast for quick feedback

The test suite is designed to provide confidence in code changes and catch regressions early. Use it liberally during development! 🚀 