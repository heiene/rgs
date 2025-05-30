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

## 🚀 Manual Setup (Complete Instructions)

### Prerequisites
- Python 3.11+ with conda/pip
- Node.js 18+
- PostgreSQL (install via Homebrew: `brew install postgresql`)

### 1. Database Setup
```bash
# Start PostgreSQL service
brew services start postgresql

# Create development and test databases
createdb rgs_dev
createdb rgs_test
```

### 2. Backend Setup
```bash
cd backend

# Install the backend package in development mode
pip install -e .

# Your .env file should already exist with configuration like:
# FLASK_CONFIG=development
# FLASK_APP=run.py
# FLASK_DEBUG=True
# SECRET_KEY=your-secret-key
# DEV_DATABASE_URL=postgresql://localhost/rgs_dev
# TEST_DATABASE_URL=postgresql://localhost/rgs_test

# Initialize database migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations to database
flask db upgrade

# Run tests to verify setup
pytest tests/

# Start Flask development server
flask run
```

### 3. Frontend Setup
```bash
cd frontend

# Install Node.js dependencies
npm install

# Create .env file (if it doesn't exist)
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=10000
VITE_APP_TITLE=RGS - Vue Flask App
VITE_ENABLE_DEBUG=true
EOF

# Start Vue development server
npm run dev
```

### 4. Access Your Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Admin Interface**: http://localhost:5000/admin
- **Health Check**: http://localhost:5000/health

## 🛠️ Development Utilities (Simplified)

For easier development workflow, use the simplified `scripts/dev-utils.sh` script:

### Make Script Executable
```bash
chmod +x scripts/dev-utils.sh
```

### Available Commands

#### `start` - Start PostgreSQL
```bash
./scripts/dev-utils.sh start
```
**What it does:**
- Starts PostgreSQL service via Homebrew
- Shows instructions for manually starting Flask and Vue

#### `status` - Check Environment Status
```bash
./scripts/dev-utils.sh status
```
**Shows status of:**
- PostgreSQL service
- Flask backend server (if running)
- Vue frontend server (if running)

#### `stop` - Stop Services
```bash
# Stop development servers only
./scripts/dev-utils.sh stop

# Stop servers AND PostgreSQL
./scripts/dev-utils.sh stop --with-db
```
**What it does:**
- Stops Flask backend (if running)
- Stops Vue frontend (if running)
- Optionally stops PostgreSQL with `--with-db` flag

### Simple Daily Workflow
```bash
# 1. Start PostgreSQL
./scripts/dev-utils.sh start

# 2. Check what's running
./scripts/dev-utils.sh status

# 3. Start backend (in one terminal)
cd backend && flask run

# 4. Start frontend (in another terminal)
cd frontend && npm run dev

# 5. When done, stop everything
./scripts/dev-utils.sh stop --with-db
```

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_app.py -v
```

### Frontend Testing
```bash
cd frontend

# Run tests
npm run test

# Run tests in watch mode
npm run test:watch
```

## 🔧 Configuration

### Backend Environment Variables (.env)
```bash
# Flask Configuration
FLASK_CONFIG=development
FLASK_APP=run.py
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database URLs
DEV_DATABASE_URL=postgresql://localhost/rgs_dev
TEST_DATABASE_URL=postgresql://localhost/rgs_test

# Optional: Additional settings
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend Environment Variables (.env)
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=10000

# App Settings
VITE_APP_TITLE=RGS - Vue Flask App
VITE_ENABLE_DEBUG=true
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

# Check PostgreSQL installation
brew services list | grep postgresql
```

#### Port Already in Use
```bash
# Check what's using port 5000 (Flask)
lsof -i :5000

# Check what's using port 3000 (Vue)
lsof -i :3000

# Kill process on specific port
kill $(lsof -ti:5000)
```

#### Database Issues
```bash
# Check if databases exist
psql -l | grep rgs

# Recreate databases if needed
dropdb rgs_dev && createdb rgs_dev
dropdb rgs_test && createdb rgs_test
```

#### Migration Issues
```bash
# Reset migrations (development only)
cd backend
rm -rf migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
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

## 🤝 Development Workflow

### Git Workflow
- Feature branches for all changes
- Descriptive commit messages
- Run tests before committing
- Pull request reviews required

### Recommended Daily Flow
1. `./scripts/dev-utils.sh start` - Start PostgreSQL
2. `cd backend && flask run` - Start backend
3. `cd frontend && npm run dev` - Start frontend
4. Develop and test
5. `./scripts/dev-utils.sh stop --with-db` - Stop everything

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
