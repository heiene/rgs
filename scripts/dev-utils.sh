#!/bin/bash

# RGS Development Utilities
# Enhanced script for Flask + Vue development environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
function print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

function print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

function print_error() {
    echo -e "${RED}❌ $1${NC}"
}

function print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to get installed PostgreSQL service name
function get_postgres_service() {
    local pg_service=$(brew services list | grep postgresql | head -n 1 | awk '{print $1}')
    if [ -z "$pg_service" ]; then
        print_error "No PostgreSQL installation found via brew!"
        print_info "Install with: brew install postgresql"
        exit 1
    fi
    echo "$pg_service"
}

# Function to check if we're in the project root
function check_project_root() {
    if [ ! -f "docker-compose.yml" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        print_error "Please run this script from the project root directory"
        exit 1
    fi
}

# Function to setup environment files
function setup_env_files() {
    print_info "Setting up environment files..."
    
    # Backend .env
    if [ ! -f "backend/.env" ]; then
        print_warning "backend/.env not found, creating basic .env"
        cat > backend/.env << EOF
FLASK_CONFIG=development
FLASK_APP=run.py
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
DEV_DATABASE_URL=postgresql://localhost/rgs_dev
TEST_DATABASE_URL=postgresql://localhost/rgs_test
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
MAX_CONTENT_LENGTH=16777216
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF
        print_status "Created backend/.env with default configuration"
        print_info "Please review and update backend/.env with your specific settings"
    else
        print_status "backend/.env already exists and configured"
    fi
    
    # Frontend .env
    if [ ! -f "frontend/.env" ]; then
        cat > frontend/.env << EOF
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=10000
VITE_APP_TITLE=RGS - Vue Flask App
VITE_ENABLE_DEBUG=true
EOF
        print_status "Created frontend/.env"
    else
        print_info "frontend/.env already exists"
    fi
}

# Function to install dependencies
function install_deps() {
    print_info "Installing dependencies..."
    
    # Backend dependencies
    print_info "Installing Python dependencies..."
    cd backend
    pip install -r requirements.txt
    cd ..
    print_status "Backend dependencies installed"
    
    # Frontend dependencies
    print_info "Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
    print_status "Frontend dependencies installed"
}

# Function to setup database
function setup_database() {
    print_info "Setting up database..."
    
    # Check if databases exist, create if not
    if ! psql -lqt | cut -d \| -f 1 | grep -qw rgs_dev; then
        print_info "Creating development database..."
        createdb rgs_dev
        print_status "Development database created"
    else
        print_info "Development database already exists"
    fi
    
    if ! psql -lqt | cut -d \| -f 1 | grep -qw rgs_test; then
        print_info "Creating test database..."
        createdb rgs_test
        print_status "Test database created"
    else
        print_info "Test database already exists"
    fi
    
    # Run migrations
    cd backend
    if [ ! -d "migrations" ]; then
        print_info "Initializing database migrations..."
        flask db init
        print_status "Database migrations initialized"
    fi
    
    print_info "Running database migrations..."
    flask db upgrade
    print_status "Database migrations completed"
    cd ..
}

# Function to start development environment
function start_dev() {
    check_project_root
    print_info "Starting RGS development environment..."
    
    # Start PostgreSQL
    local pg_service=$(get_postgres_service)
    if ! brew services list | grep "$pg_service" | grep started > /dev/null; then
        print_info "Starting PostgreSQL ($pg_service)..."
        brew services start "$pg_service"
        sleep 3  # Wait for PostgreSQL to start
        print_status "PostgreSQL started"
    else
        print_info "PostgreSQL is already running"
    fi
    
    # Setup database if needed
    setup_database
    
    print_status "Development environment is ready!"
    print_info "Backend:  http://localhost:5000"
    print_info "Frontend: http://localhost:3000 (when started)"
    print_info "Admin:    http://localhost:5000/admin"
    echo ""
    print_info "To start services:"
    print_info "  Backend:  cd backend && flask run"
    print_info "  Frontend: cd frontend && npm run dev"
    print_info "  Or use:   ./scripts/dev-utils.sh serve"
}

# Function to stop development environment
function stop_dev() {
    print_info "Stopping RGS development environment..."
    
    # Kill Flask development server
    if pgrep -f "flask run" > /dev/null; then
        print_info "Stopping Flask server..."
        pkill -f "flask run"
        print_status "Flask server stopped"
    fi
    
    # Kill Vue development server
    if pgrep -f "npm run dev" > /dev/null; then
        print_info "Stopping Vue server..."
        pkill -f "npm run dev"
        print_status "Vue server stopped"
    fi
    
    # Stop PostgreSQL if requested
    if [ "$2" = "--with-db" ]; then
        local pg_service=$(get_postgres_service)
        if brew services list | grep "$pg_service" | grep started > /dev/null; then
            print_info "Stopping PostgreSQL ($pg_service)..."
            brew services stop "$pg_service"
            print_status "PostgreSQL stopped"
        fi
    fi
    
    print_status "Development environment stopped!"
}

# Function to show status
function show_status() {
    print_info "RGS Development Environment Status"
    echo ""
    
    # PostgreSQL status
    local pg_service=$(get_postgres_service)
    print_info "PostgreSQL service: $pg_service"
    if brew services list | grep "$pg_service" | grep started > /dev/null; then
        print_status "PostgreSQL is running"
    else
        print_warning "PostgreSQL is not running"
    fi
    
    # Flask status
    if pgrep -f "flask run" > /dev/null; then
        print_status "Flask server is running (http://localhost:5000)"
    else
        print_warning "Flask server is not running"
    fi
    
    # Vue status
    if pgrep -f "npm run dev" > /dev/null; then
        print_status "Vue server is running (http://localhost:3000)"
    else
        print_warning "Vue server is not running"
    fi
    
    # Database status
    if psql -lqt | cut -d \| -f 1 | grep -qw rgs_dev; then
        print_status "Development database exists"
    else
        print_warning "Development database does not exist"
    fi
}

# Function to serve both frontend and backend
function serve_all() {
    check_project_root
    print_info "Starting both backend and frontend servers..."
    
    # Start backend in background
    print_info "Starting Flask backend..."
    cd backend
    flask run &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend in background
    print_info "Starting Vue frontend..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    print_status "Both servers started!"
    print_info "Backend:  http://localhost:5000"
    print_info "Frontend: http://localhost:3000"
    print_info "Press Ctrl+C to stop both servers"
    
    # Wait for interrupt
    trap "print_info 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
    wait
}

# Function to run tests
function run_tests() {
    check_project_root
    print_info "Running RGS test suite..."
    
    # Backend tests
    print_info "Running backend tests..."
    cd backend
    pytest --cov=app --cov-report=term-missing
    cd ..
    print_status "Backend tests completed"
    
    # Frontend tests (if test script exists)
    if [ -f "frontend/package.json" ] && grep -q '"test"' frontend/package.json; then
        print_info "Running frontend tests..."
        cd frontend
        npm run test
        cd ..
        print_status "Frontend tests completed"
    else
        print_warning "No frontend tests configured"
    fi
    
    print_status "All tests completed!"
}

# Function to setup the entire project
function setup_project() {
    check_project_root
    print_info "Setting up RGS project for development..."
    
    setup_env_files
    install_deps
    start_dev
    
    print_status "Project setup completed!"
    print_info "You can now run: ./scripts/dev-utils.sh serve"
}

# Main command handling
case "$1" in
    "setup")
        setup_project
        ;;
    "start")
        start_dev
        ;;
    "stop")
        stop_dev "$@"
        ;;
    "status")
        show_status
        ;;
    "serve")
        serve_all
        ;;
    "test")
        run_tests
        ;;
    "install")
        install_deps
        ;;
    "db-setup")
        setup_database
        ;;
    *)
        echo "RGS Development Utilities"
        echo ""
        echo "Usage: $0 {command}"
        echo ""
        echo "Commands:"
        echo "  setup      - Complete project setup (env files, deps, database)"
        echo "  start      - Start PostgreSQL and setup database"
        echo "  stop       - Stop development servers"
        echo "  stop --with-db - Stop servers and PostgreSQL"
        echo "  status     - Show status of all services"
        echo "  serve      - Start both backend and frontend servers"
        echo "  test       - Run all tests"
        echo "  install    - Install dependencies"
        echo "  db-setup   - Setup database and run migrations"
        echo ""
        echo "Examples:"
        echo "  $0 setup     # First time setup"
        echo "  $0 serve     # Start both servers"
        echo "  $0 status    # Check what's running"
        exit 1
        ;;
esac 