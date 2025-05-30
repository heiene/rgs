# RGS Scripts 🛠️

This directory contains utility scripts for the RGS (Round Golf System) project. These scripts help with development, testing, database management, and API interaction.

## 📋 Available Scripts

### 🧪 `run-tests.py` - Test Runner
**Purpose:** Run the test suite with various options and configurations.

**Usage:**
```bash
# Run all tests
python scripts/run-tests.py

# Run specific test module
python scripts/run-tests.py -m test_auth
python scripts/run-tests.py -m test_models

# Run with coverage report
python scripts/run-tests.py --coverage

# Watch mode (auto-rerun on file changes)
python scripts/run-tests.py --watch

# Fast mode (skip slow tests)
python scripts/run-tests.py --fast

# Verbose output
python scripts/run-tests.py -v

# Clean artifacts before running
python scripts/run-tests.py --clean
```

**Features:**
- 🎯 Module-specific testing
- 📊 Coverage reporting with HTML output
- 🔄 Watch mode for continuous testing
- 🏃‍♂️ Fast mode for quick feedback
- 🧹 Artifact cleanup

---

### 👤 `create-admin-user.py` - User Management
**Purpose:** Create admin and test users for development and testing.

**Usage:**
```bash
# Create default admin and test users
python scripts/create-admin-user.py

# The script creates:
# - admin@rgs.test (password: AdminPass123!)
# - test@rgs.test (password: TestPass123!)
```

**Features:**
- ✅ Creates admin user with full privileges
- ✅ Creates test user for regular operations
- 🔍 Checks for existing users to prevent duplicates
- 📝 Provides detailed feedback with user IDs
- 🔐 Uses secure password hashing

**Requirements:**
- Database must be running and migrated
- Run from project root directory

---

### 🌐 `api-test.py` - API Testing Tool
**Purpose:** Interactive API testing and validation tool.

**Usage:**
```bash
# Interactive mode (recommended)
python scripts/api-test.py

# Test specific functionality
python scripts/api-test.py --mode auth        # Authentication tests
python scripts/api-test.py --mode users       # User management tests
python scripts/api-test.py --mode reset       # Password reset tests
python scripts/api-test.py --mode all         # All tests

# Use different API base URL
python scripts/api-test.py --url http://localhost:5000/api/v1
```

**Features:**
- 🔐 Authentication flow testing
- 👥 User management operations
- 🔄 Password reset functionality
- 🎨 Interactive menu system
- 📊 Detailed request/response logging
- 🌍 Health check verification

**Test Categories:**
- **Authentication:** Login, register, token refresh
- **Users:** Profile management, user operations
- **Password Reset:** Forgot/reset password flow
- **Interactive:** Manual API exploration

---

### 🗄️ `dev-utils.sh` - Database Utilities
**Purpose:** Database development and management utilities.

**Usage:**
```bash
# Make executable (first time)
chmod +x scripts/dev-utils.sh

# Start PostgreSQL database
./scripts/dev-utils.sh start

# Stop PostgreSQL database  
./scripts/dev-utils.sh stop

# Reset database (drop and recreate)
./scripts/dev-utils.sh reset

# Run database migrations
./scripts/dev-utils.sh migrate

# Create new migration
./scripts/dev-utils.sh migration "Add new field"

# Show database status
./scripts/dev-utils.sh status

# Full development setup
./scripts/dev-utils.sh setup
```

**Features:**
- 🚀 One-command database startup
- 🔄 Database reset and migration
- 📊 Status monitoring
- 🏗️ Complete development setup
- 🐳 Docker support (if configured)

---

## 🚀 Quick Start Workflows

### **New Developer Setup**
```bash
# 1. Setup database and environment
./scripts/dev-utils.sh setup

# 2. Create test users
python scripts/create-admin-user.py

# 3. Run tests to verify setup
python scripts/run-tests.py

# 4. Test API functionality
python scripts/api-test.py
```

### **Daily Development**
```bash
# Start database
./scripts/dev-utils.sh start

# Run tests in watch mode while developing
python scripts/run-tests.py --watch

# Test API changes
python scripts/api-test.py --mode auth
```

### **Before Committing**
```bash
# Run full test suite with coverage
python scripts/run-tests.py --coverage

# Verify API endpoints work
python scripts/api-test.py --mode all
```

---

## 📁 Directory Structure

```
scripts/
├── README.md              # This documentation
├── run-tests.py           # Test runner with advanced options
├── create-admin-user.py   # User creation utility
├── api-test.py            # API testing tool
└── dev-utils.sh           # Database and development utilities
```

---

## 🔧 Requirements

### **Python Scripts**
- Python 3.11+
- Flask application dependencies (see `backend/requirements.txt`)
- Database running and migrated

### **Shell Scripts** 
- Bash shell
- PostgreSQL installed
- psql command available

---

## 🆘 Troubleshooting

### **Common Issues**

**Database Connection Errors:**
```bash
# Check if PostgreSQL is running
./scripts/dev-utils.sh status

# Start database if not running
./scripts/dev-utils.sh start
```

**Migration Errors:**
```bash
# Reset database and run fresh migrations
./scripts/dev-utils.sh reset
./scripts/dev-utils.sh migrate
```

**Test Failures:**
```bash
# Clean test artifacts
python scripts/run-tests.py --clean

# Run specific failing test module
python scripts/run-tests.py -m test_auth -v
```

**API Test Connection Issues:**
```bash
# Verify Flask server is running on correct port
curl http://127.0.0.1:5000/health

# Check API health endpoint
python scripts/api-test.py --mode health
```

---

## 🤝 Contributing

When adding new scripts:

1. **Follow naming convention:** `kebab-case.py` or `kebab-case.sh`
2. **Add help documentation:** Use argparse for Python, help text for shell
3. **Update this README:** Document the new script's purpose and usage
4. **Include error handling:** Graceful failures with helpful error messages
5. **Test thoroughly:** Verify script works in clean environment

---

## 📝 Notes

- All Python scripts should be run from the project root directory
- Shell scripts are designed to work from any directory
- Scripts use the backend virtual environment and configuration
- Test scripts use SQLite in-memory database for speed
- API scripts default to `http://127.0.0.1:5000/api/v1` 