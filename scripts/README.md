# RGS Scripts 🛠️

This directory contains utility scripts for the RGS (Round Golf System) project. These scripts help with development, testing, database management, and API interaction.

## 📋 Available Scripts

### 🧪 `run-tests.py` - Advanced Test Runner
**Purpose:** Comprehensive test runner with multiple options for different development workflows.

**Basic Usage:**
```bash
# Run all tests
python scripts/run-tests.py

# Run all tests with verbose output
python scripts/run-tests.py -v

# Run with coverage report (HTML output in backend/htmlcov/)
python scripts/run-tests.py --coverage
```

**Module-Specific Testing:**
```bash
# Run specific test modules
python scripts/run-tests.py -m test_auth         # Authentication tests only
python scripts/run-tests.py -m test_models       # Database model tests only  
python scripts/run-tests.py -m test_email_service # Email service tests only
python scripts/run-tests.py -m test_golf_models  # Golf-specific model tests
python scripts/run-tests.py -m test_app          # Basic app functionality tests
```

**Development Workflow Options:**
```bash
# Watch mode - auto-rerun tests when files change (great for TDD)
python scripts/run-tests.py --watch

# Fast mode - skip slow tests for quick feedback
python scripts/run-tests.py --fast

# Clean mode - remove test artifacts before running
python scripts/run-tests.py --clean

# Combine options
python scripts/run-tests.py -m test_auth --watch --coverage
```

**Direct Pytest Access:**
For more granular control, you can also use pytest directly:
```bash
cd backend

# Run specific test class
python -m pytest tests/test_auth.py::TestAuthLogin -v

# Run single test method
python -m pytest tests/test_auth.py::TestAuthLogin::test_login_success -v

# Run tests matching pattern
python -m pytest tests/ -k "login" -v

# Stop on first failure
python -m pytest tests/ -x

# Run only failed tests from last run
python -m pytest tests/ --lf
```

---

### 👤 `create-admin-user.py` - User Management
**Purpose:** Create admin and test users for development and testing.

**Usage:**
```bash
# Create default admin and test users
python scripts/create-admin-user.py

# Creates:
# - admin@rgs.test (password: AdminPass123!) - Admin privileges
# - test@rgs.test (password: TestPass123!) - Regular user
```

**When to Use:**
- Setting up a new development environment
- After resetting the database
- When you need test users for manual API testing

---

### 🌐 `api-test.py` - Interactive API Testing
**Purpose:** Interactive tool for testing API endpoints and workflows.

**Usage:**
```bash
# Interactive mode with menu system
python scripts/api-test.py

# Test specific functionality
python scripts/api-test.py --mode auth        # Authentication endpoints
python scripts/api-test.py --mode users       # User management  
python scripts/api-test.py --mode reset       # Password reset flow
python scripts/api-test.py --mode all         # Run all automated tests

# Use different API URL
python scripts/api-test.py --url http://localhost:5000/api/v1
```

**Features:**
- 🔐 Complete authentication flow testing
- 👥 User registration and management
- 🔄 Password reset functionality testing
- 🎨 Interactive menu for manual testing
- 📊 Detailed request/response logging

---

### 🗄️ `dev-utils.sh` - Database & Development Utilities
**Purpose:** Database management and development environment utilities.

**Setup:**
```bash
# Make executable (first time only)
chmod +x scripts/dev-utils.sh
```

**Database Operations:**
```bash
./scripts/dev-utils.sh start      # Start PostgreSQL database
./scripts/dev-utils.sh stop       # Stop PostgreSQL database  
./scripts/dev-utils.sh restart    # Restart PostgreSQL
./scripts/dev-utils.sh status     # Show database status
```

**Database Management:**
```bash
./scripts/dev-utils.sh reset      # Drop and recreate database (DESTRUCTIVE)
./scripts/dev-utils.sh migrate    # Run pending migrations
./scripts/dev-utils.sh migration "Description"  # Create new migration
```

**Development Setup:**
```bash
./scripts/dev-utils.sh setup      # Complete development environment setup
```

---

## 🚀 Testing Workflows

### **Quick Development Testing**
```bash
# 1. Watch mode for immediate feedback during development
python scripts/run-tests.py --watch

# 2. Test specific area you're working on
python scripts/run-tests.py -m test_auth --watch

# 3. Fast tests for quick validation
python scripts/run-tests.py --fast
```

### **Comprehensive Testing**
```bash
# 1. Full test suite with coverage
python scripts/run-tests.py --coverage

# 2. Check all systems are working
./scripts/dev-utils.sh status
python scripts/api-test.py --mode all

# 3. Manual API validation
python scripts/api-test.py  # Interactive mode
```

### **New Feature Development**
```bash
# 1. Start with tests for the feature you're building
python scripts/run-tests.py -m test_models --watch

# 2. Use API tester to validate endpoints
python scripts/api-test.py --mode auth

# 3. Run full suite before committing
python scripts/run-tests.py --coverage
```

### **Debugging Failed Tests**
```bash
# 1. Run specific failing test with verbose output
python -m pytest tests/test_auth.py::TestAuthLogin::test_login_success -v -s

# 2. Use coverage to see what's not tested
python scripts/run-tests.py --coverage

# 3. Test API manually to understand expected behavior
python scripts/api-test.py
```

---

## 🔧 Test Organization

### **Test Module Structure**
```
backend/tests/
├── test_app.py           # Basic application functionality
├── test_auth.py          # Authentication & authorization  
├── test_models.py        # Core database models (User, Club, Theme)
├── test_golf_models.py   # Golf-specific models (Course, Round, Score)
├── test_email_service.py # Email functionality
├── conftest.py          # Test fixtures and configuration
└── pytest.ini          # Pytest settings
```

### **Test Categories**
- **Unit Tests:** Individual model methods and service functions
- **Integration Tests:** API endpoints and database relationships  
- **Service Tests:** Business logic and external service integration
- **End-to-End Tests:** Complete user workflows

### **Available Test Fixtures**
```python
# In conftest.py - use these in your tests
@pytest.fixture
def app():              # Flask application instance
def client(app):        # Test client for API calls
def test_user(app):     # Regular user with known credentials
def admin_user(app):    # Admin user for privilege testing
def test_club(app):     # Sample golf club
def test_theme(app):    # Sample theme
def auth_headers():     # Authorization headers for API calls
def admin_headers():    # Admin authorization headers
```

---

## 🎯 Common Testing Commands

### **Daily Development**
```bash
# Quick check everything works
python scripts/run-tests.py --fast

# Work on specific feature with immediate feedback
python scripts/run-tests.py -m test_auth --watch

# Test API changes manually
python scripts/api-test.py
```

### **Before Committing**
```bash
# Full test suite
python scripts/run-tests.py

# Check coverage
python scripts/run-tests.py --coverage

# Validate API endpoints
python scripts/api-test.py --mode all
```

### **Setting Up New Environment**
```bash
# 1. Setup database and environment
./scripts/dev-utils.sh setup

# 2. Create test users  
python scripts/create-admin-user.py

# 3. Verify everything works
python scripts/run-tests.py
python scripts/api-test.py --mode all
```

### **Debugging Issues**
```bash
# Check what's not working
./scripts/dev-utils.sh status

# Reset if needed (DESTRUCTIVE)
./scripts/dev-utils.sh reset
python scripts/create-admin-user.py

# Run specific tests with output
python -m pytest tests/test_auth.py -v -s
```

---

## 🆘 Troubleshooting

### **Common Issues & Solutions**

**Database Connection Errors:**
```bash
./scripts/dev-utils.sh status    # Check if PostgreSQL is running
./scripts/dev-utils.sh start     # Start if not running
```

**Test Failures:**
```bash
python scripts/run-tests.py --clean  # Clean test artifacts
./scripts/dev-utils.sh reset          # Reset database (if needed)
python scripts/create-admin-user.py   # Recreate test users
```

**API Connection Issues:**
```bash
# Check Flask server is running
curl http://127.0.0.1:5000/health

# Test API health
python scripts/api-test.py --mode health
```

**Import or Module Errors:**
```bash
cd backend
python -c "import app; print('App imports OK')"
```

---

## 📝 Notes

- **Test Database:** Tests use SQLite in-memory for speed (see `conftest.py`)
- **Test Isolation:** Each test gets fresh database state
- **Environment:** Tests use 'testing' config with faster password hashing
- **Authentication:** Fixtures automatically handle JWT tokens
- **Email:** Email sending disabled in tests (uses mocks)
- **Order Independence:** Tests can run in any order

---

## 🎉 Next Steps

1. **For New Developers:** Start with `./scripts/dev-utils.sh setup` and `python scripts/run-tests.py`
2. **For Feature Development:** Use `--watch` mode for immediate feedback
3. **For API Testing:** Use `python scripts/api-test.py` for manual validation
4. **For Debugging:** Use verbose pytest commands with `-v -s` flags

The testing infrastructure provides comprehensive coverage and fast feedback loops for confident development! 🚀 