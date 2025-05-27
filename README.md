# RGS - Vue 3 + Flask Application

A modern full-stack web application built with Vue 3 frontend, Flask backend, and PostgreSQL database, following clean architecture principles.

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Vue 3 + Vite + Vue Router + Pinia
- **Backend**: Flask + SQLAlchemy + Marshmallow + JWT
- **Database**: PostgreSQL
- **Testing**: Pytest (backend) + Vitest (frontend)

### Architecture Principles
- **Thin Routes, Fat Services**: Routes handle HTTP concerns only, Services contain business logic
- **API-First Design**: Frontend communicates with backend only through API routes
- **Clean Architecture**: Clear separation of concerns across layers
- **Comprehensive Testing**: 80%+ test coverage with proper fixtures

### Project Structure
```
rgs/
├── backend/                    # Flask backend application
│   ├── app/
│   │   ├── routes/
│   │   │   ├── api/v1/        # JSON API endpoints (THIN)
│   │   │   └── web/           # Admin HTML interfaces
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Marshmallow validation/serialization
│   │   ├── services/          # Business logic (FAT)
│   │   └── templates/         # Jinja2 templates (admin only)
│   ├── tests/                 # Pytest tests
│   └── migrations/            # Database migrations
├── frontend/                  # Vue 3 frontend application
│   ├── src/
│   │   ├── components/        # Reusable Vue components
│   │   ├── views/            # Page-level components
│   │   ├── router/           # Vue Router configuration
│   │   └── store/            # Pinia state management
│   └── public/               # Static assets
├── scripts/                  # Development utilities
└── docs/                     # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ with conda/pip
- Node.js 18+
- PostgreSQL (installed via Homebrew recommended)

### One-Command Setup
```bash
# Make the script executable
chmod +x scripts/dev-utils.sh

# Complete project setup (first time only)
./scripts/dev-utils.sh setup
```

This will:
- ✅ Check/create environment files (.env)
- ✅ Install Python and Node.js dependencies
- ✅ Start PostgreSQL
- ✅ Create databases (rgs_dev, rgs_test)
- ✅ Initialize and run database migrations

### Start Development Servers
```bash
# Start both backend and frontend servers
./scripts/dev-utils.sh serve
```

Access your application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Admin Interface**: http://localhost:5000/admin
- **Health Check**: http://localhost:5000/health

## 🛠️ Development Utilities

The `scripts/dev-utils.sh` script provides comprehensive development environment management:

### Available Commands

#### `setup` - Complete Project Setup
```bash
./scripts/dev-utils.sh setup
```
**First-time setup command that:**
- Checks for `.env` files (creates if missing)
- Installs all dependencies (Python + Node.js)
- Starts PostgreSQL service
- Creates development and test databases
- Initializes database migrations
- Sets up the complete development environment

#### `serve` - Start Development Servers
```bash
./scripts/dev-utils.sh serve
```
**Starts both backend and frontend servers:**
- Flask backend on http://localhost:5000
- Vue frontend on http://localhost:3000
- Press `Ctrl+C` to stop both servers

#### `start` - Start Infrastructure
```bash
./scripts/dev-utils.sh start
```
**Starts PostgreSQL and sets up database:**
- Starts PostgreSQL service via Homebrew
- Creates databases if they don't exist
- Runs database migrations
- Prepares environment for development

#### `stop` - Stop Services
```bash
# Stop development servers only
./scripts/dev-utils.sh stop

# Stop servers AND PostgreSQL
./scripts/dev-utils.sh stop --with-db
```

#### `status` - Check Environment Status
```bash
./scripts/dev-utils.sh status
```
**Shows status of:**
- PostgreSQL service
- Flask backend server
- Vue frontend server
- Database existence

#### `test` - Run Test Suite
```bash
./scripts/dev-utils.sh test
```
**Runs all tests:**
- Backend tests with coverage report
- Frontend tests (if configured)
- Generates HTML coverage report

#### `install` - Install Dependencies
```bash
./scripts/dev-utils.sh install
```
**Installs:**
- Python packages from `backend/requirements.txt`
- Node.js packages from `frontend/package.json`

#### `db-setup` - Database Management
```bash
./scripts/dev-utils.sh db-setup
```
**Database operations:**
- Creates development and test databases
- Initializes Flask-Migrate if needed
- Runs database migrations

## 📋 Manual Development Workflow

If you prefer manual control over the development environment:

### Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Environment file should already exist as .env
# Edit .env with your database credentials if needed

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run tests
pytest --cov=app

# Start development server
flask run
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Environment file should already exist as .env

# Start development server
npm run dev

# Run tests
npm run test
```

### Database Setup
```bash
# Start PostgreSQL
brew services start postgresql

# Create databases
createdb rgs_dev
createdb rgs_test
```

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_app.py -v

# Run tests in watch mode
pytest-watch
```

### Frontend Testing
```bash
cd frontend

# Run tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with UI
npm run test:ui
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Flask Configuration
FLASK_CONFIG=development
FLASK_APP=run.py
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DEV_DATABASE_URL=postgresql://localhost/rgs_dev
TEST_DATABASE_URL=postgresql://localhost/rgs_test

# Security
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

#### Frontend (.env)
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=10000

# App Settings
VITE_APP_TITLE=RGS - Vue Flask App
VITE_ENABLE_DEBUG=true
```

## 🐳 Docker Support (Optional)

Docker configuration is included but not required for development:

```bash
# Start everything with Docker
docker-compose up --build

# Start only PostgreSQL with Docker
docker run -d \
  --name rgs-postgres \
  -e POSTGRES_DB=rgs_dev \
  -e POSTGRES_USER=rgs_user \
  -e POSTGRES_PASSWORD=rgs_password \
  -p 5432:5432 \
  postgres:15-alpine
```

## 📚 API Documentation

### Health Check
```bash
GET /health
```

### Authentication Endpoints
```bash
POST /api/v1/auth/login
POST /api/v1/auth/register
POST /api/v1/auth/refresh
```

### User Endpoints
```bash
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
```

### Admin Web Interface
```bash
GET /admin/           # Dashboard
GET /admin/login      # Login page
GET /admin/upload     # CSV upload
```

## 🔍 Troubleshooting

### Common Issues

#### PostgreSQL Connection Error
```bash
# Check if PostgreSQL is running
./scripts/dev-utils.sh status

# Start PostgreSQL
brew services start postgresql

# Check PostgreSQL logs
brew services list | grep postgresql
```

#### Port Already in Use
```bash
# Check what's using port 5000
lsof -i :5000

# Check what's using port 3000
lsof -i :3000

# Kill process on port
kill $(lsof -ti:5000)
```

#### Database Migration Issues
```bash
# Reset migrations (development only)
rm -rf backend/migrations
cd backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### Dependencies Issues
```bash
# Reinstall backend dependencies
cd backend
pip install -r requirements.txt --force-reinstall

# Reinstall frontend dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 🤝 Development Workflow

### Recommended Development Flow
1. **First time**: `./scripts/dev-utils.sh setup`
2. **Daily development**: `./scripts/dev-utils.sh serve`
3. **Check status**: `./scripts/dev-utils.sh status`
4. **Run tests**: `./scripts/dev-utils.sh test`
5. **Stop everything**: `./scripts/dev-utils.sh stop`

### Git Workflow
- Feature branches for all changes
- Descriptive commit messages
- Run tests before committing
- Pull request reviews required

## 📖 Next Steps

1. **Phase 1**: Backend Foundation & Authentication (Current)
   - ✅ Environment setup
   - ✅ Flask application scaffolding
   - ✅ Testing framework
   - 🔄 User models and authentication

2. **Phase 2**: Core Models & Business Logic
3. **Phase 3**: Admin Interface & Web Routes
4. **Phase 4**: Frontend Integration
5. **Phase 5**: Production & Deployment

See `TODO.md` for detailed development plan and progress tracking.

## 📄 License

This project is licensed under the MIT License.
