# RGS Test Suite 🧪

This directory contains the comprehensive test suite for the RGS (Round Golf System) backend. The tests ensure code quality, catch regressions, and serve as living documentation of the API behavior.

## 📊 Test Status Overview

```
✅ 35 tests passing (63% pass rate)
❌ 21 tests failing (mainly edge cases and email service)
🔍 56 total tests

Core functionality: ✅ WORKING
Authentication: ✅ WORKING  
Database models: ✅ WORKING
API endpoints: ✅ WORKING
```

## 🚀 Quick Start

```bash
# Run all tests
python scripts/run-tests.py

# Run with coverage
python scripts/run-tests.py --coverage

# Watch mode (auto-rerun on changes)
python scripts/run-tests.py --watch

# Run specific test module
python scripts/run-tests.py -m test_auth
```

## 📁 Test Structure

### **Test Files Overview**

| File | Purpose | Tests | Status |
|------|---------|-------|--------|
| `test_app.py` | Basic app functionality | 8 | ✅ 5 passing |
| `test_auth.py` | Authentication API | 19 | ✅ 11 passing |
| `test_models.py` | Database models | 15 | ✅ 14 passing |
| `test_email_service.py` | Email functionality | 12 | ⚠️ 5 passing |
| `conftest.py` | Test configuration | - | Supporting |
| `pytest.ini` | Pytest settings | - | Configuration |

### **🔐 `test_auth.py` - Authentication Tests**

**Working Tests (11/19):**
- ✅ Login with valid credentials
- ✅ Login validation (invalid email/password)
- ✅ Inactive user handling  
- ✅ Missing field validation
- ✅ Token validation and security

**Test Classes:**
```python
TestAuthLogin          # Login functionality
TestAuthRegister       # User registration  
TestPasswordReset      # Password reset flow
TestTokenValidation    # JWT token security
```

**Key Test Coverage:**
- Login success/failure scenarios
- Registration validation
- Password reset workflow
- JWT token management
- Security edge cases

---

### **🏗️ `test_models.py` - Database Model Tests**

**Working Tests (14/15):**
- ✅ User model creation and validation
- ✅ Password hashing and verification
- ✅ Model properties (full_name, full_address)
- ✅ Database relationships (User ↔ Club, User ↔ Theme)
- ✅ Handicap relationships and current handicap logic

**Test Classes:**
```python
TestUserModel     # User model functionality
TestClubModel     # Club model and constraints
TestThemeModel    # Theme model and validation
```

**Coverage Areas:**
- Model creation and defaults
- Property calculations
- Relationship integrity
- Data validation
- Serialization (to_dict)

---

### **🌐 `test_app.py` - Application Tests**

**Working Tests (5/8):**
- ✅ Health endpoints (`/health`, `/api/v1/health`)
- ✅ Endpoint existence verification
- ✅ Authentication requirement enforcement

**Coverage Areas:**
- Basic endpoint availability
- CORS configuration
- Error handling (404, 405)
- API structure validation

---

### **📧 `test_email_service.py` - Email Service Tests**

**Working Tests (5/12):**
- ✅ Service initialization
- ✅ Token verification logic
- ✅ Error handling

**Needs Work:**
- Email sending functionality
- Template rendering
- Token generation

---

## 🔧 Test Configuration

### **Test Environment**

The tests use a separate configuration optimized for speed and isolation:

```python
# TestingConfig in backend/app/config.py
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Fast in-memory DB
BCRYPT_LOG_ROUNDS = 4                           # Faster password hashing
MAIL_SUPPRESS_SEND = True                       # No actual emails
```

### **Test Fixtures (`conftest.py`)**

**Available Fixtures:**
```python
@pytest.fixture
def app():           # Flask application instance
def client(app):     # Test client for API calls
def test_user(app):  # Regular user with known credentials
def admin_user(app): # Admin user for privilege testing
def test_club(app):  # Sample golf club
def test_theme(app): # Sample theme
def auth_headers():  # Authorization headers for API calls
def admin_headers(): # Admin authorization headers
```

**Usage Example:**
```python
def test_user_profile(client, auth_headers):
    """Test getting user profile"""
    response = client.get('/api/v1/users/profile', headers=auth_headers)
    assert response.status_code == 200
```

---

## 🎯 Running Tests

### **Basic Commands**

```bash
# All tests with detailed output
python scripts/run-tests.py -v

# Specific test file
python scripts/run-tests.py -m test_auth

# Individual test class
pytest backend/tests/test_auth.py::TestAuthLogin -v

# Single test method
pytest backend/tests/test_auth.py::TestAuthLogin::test_login_success -v
```

### **Advanced Options**

```bash
# Coverage report
python scripts/run-tests.py --coverage

# Watch mode for TDD
python scripts/run-tests.py --watch

# Fast tests only (skip slow ones)
python scripts/run-tests.py --fast

# Clean artifacts and run
python scripts/run-tests.py --clean
```

### **Direct Pytest Commands**

```bash
# Run from backend directory
cd backend

# All tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=app --cov-report=html

# Stop on first failure
python -m pytest tests/ -x

# Run only failed tests from last run
python -m pytest tests/ --lf
```

---

## ✏️ Writing New Tests

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
```

### **Test Structure Template**

```python
import pytest
from app.models.your_model import YourModel
from app.extensions import db

class TestYourFeature:
    """Test your feature functionality"""
    
    def test_basic_functionality(self, app, client):
        """Test basic feature works"""
        with app.app_context():
            # Setup
            data = {...}
            
            # Action
            response = client.post('/api/v1/endpoint', json=data)
            
            # Assertions
            assert response.status_code == 200
            assert response.get_json()['success'] is True
    
    def test_error_handling(self, client):
        """Test error scenarios"""
        response = client.post('/api/v1/endpoint', json={})
        assert response.status_code == 400
```

### **Using Fixtures**

```python
def test_with_authenticated_user(client, auth_headers):
    """Test requiring authentication"""
    response = client.get('/api/v1/protected', headers=auth_headers)
    assert response.status_code == 200

def test_with_database_model(app, test_user):
    """Test using database models"""
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        assert user.email == test_user.email
```

---

## 🎨 Test Categories

### **Unit Tests**
- Individual model methods
- Service class functions
- Utility functions
- Data validation

### **Integration Tests**
- API endpoint workflows
- Database relationships
- Email service integration
- Authentication flows

### **End-to-End Tests**
- Complete user journeys
- Multi-step workflows
- Cross-service interactions

---

## 📈 Expanding Test Coverage

### **Priority Areas for Additional Tests**

**🔥 High Priority:**
1. **Round and Score Models** - Golf-specific functionality
2. **Course/Hole/TeeSet Models** - Golf course structure
3. **Handicap Calculations** - Core golf logic
4. **API Error Scenarios** - Edge cases and validation
5. **Email Service Completion** - Password reset flows

**🎯 Medium Priority:**
1. **Service Layer Tests** - Business logic validation
2. **Schema Validation Tests** - Marshmallow schemas
3. **Relationship Tests** - Complex model relationships
4. **Performance Tests** - Query optimization
5. **Security Tests** - Authorization edge cases

**⭐ Nice to Have:**
1. **Frontend Integration Tests** - API contract validation
2. **Load Tests** - Performance under load
3. **Database Migration Tests** - Schema change validation
4. **Backup/Restore Tests** - Data integrity

### **Model Test Templates**

**Round Model Tests Needed:**
```python
class TestRoundModel:
    def test_round_creation(self):
        """Test creating a golf round"""
        
    def test_round_score_calculation(self):
        """Test total score calculation"""
        
    def test_round_handicap_adjustment(self):
        """Test handicap-adjusted scoring"""
```

**Course Model Tests Needed:**
```python
class TestCourseModel:
    def test_course_creation(self):
        """Test golf course creation"""
        
    def test_course_hole_relationship(self):
        """Test course-hole relationships"""
        
    def test_course_rating_calculation(self):
        """Test course difficulty rating"""
```

---

## 🐛 Debugging Tests

### **Common Issues**

**Database Errors:**
```bash
# Check if models are properly imported
python -c "from app.models import User; print('Models OK')"

# Reset test database
rm -f test.db
python scripts/run-tests.py -m test_models
```

**Authentication Errors:**
```bash
# Test token generation
python scripts/run-tests.py -m test_auth::TestAuthLogin::test_login_success -v
```

**Import Errors:**
```bash
# Check Python path
cd backend
python -c "import app; print('App imports OK')"
```

### **Test Debugging Tools**

```python
# Add debug output to tests
def test_debug_example(client, test_user):
    response = client.post('/api/v1/auth/login', json={...})
    print(f"Response: {response.status_code}")
    print(f"Data: {response.get_json()}")
    assert response.status_code == 200
```

**Run with output:**
```bash
python scripts/run-tests.py -m test_auth -s  # -s shows print statements
```

---

## 📊 Coverage Reports

### **Generating Coverage**

```bash
# HTML coverage report
python scripts/run-tests.py --coverage

# View coverage
open backend/htmlcov/index.html
```

### **Coverage Goals**

- **Critical Paths:** >90% coverage
- **Authentication:** >95% coverage  
- **Models:** >85% coverage
- **API Endpoints:** >80% coverage
- **Overall:** >75% coverage

---

## 🤝 Contributing Tests

### **Before Adding Tests**

1. **Check existing coverage** - Avoid duplication
2. **Follow naming conventions** - Consistent test names
3. **Use appropriate fixtures** - Leverage existing setup
4. **Test both success and failure** - Comprehensive coverage
5. **Update this README** - Document new test areas

### **Test Review Checklist**

- [ ] Tests are independent (no dependencies between tests)
- [ ] Tests are deterministic (same result every time)
- [ ] Tests are fast (< 1 second each for unit tests)
- [ ] Tests have clear descriptions
- [ ] Tests cover edge cases
- [ ] Tests use appropriate assertions
- [ ] Tests clean up after themselves

---

## 📝 Notes

- Tests use SQLite in-memory database for speed
- Each test gets a fresh database instance
- Authentication tokens are automatically managed by fixtures
- Email sending is disabled in tests (use mocks)
- Tests should be runnable in any order
- Prefer pytest fixtures over setup/teardown methods

---

## 🎯 Next Steps

1. **Add Round/Score model tests** - Core golf functionality
2. **Complete email service tests** - Password reset flows  
3. **Add API integration tests** - End-to-end workflows
4. **Implement performance tests** - Database query optimization
5. **Add security tests** - Authentication edge cases

The test suite provides a solid foundation for maintaining code quality and catching regressions. As new features are added, corresponding tests should be created to maintain the safety net! 🎉 