#!/bin/bash

# Simple RGS Development Utilities
# Basic start, stop, and status for development environment

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
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

# Get PostgreSQL service name
function get_postgres_service() {
    local pg_service=$(brew services list | grep postgresql | head -n 1 | awk '{print $1}')
    if [ -z "$pg_service" ]; then
        print_error "No PostgreSQL installation found via brew!"
        print_info "Install with: brew install postgresql"
        exit 1
    fi
    echo "$pg_service"
}

# Start development environment
function start_dev() {
    print_info "Starting development environment..."
    
    # Start PostgreSQL
    local pg_service=$(get_postgres_service)
    if ! brew services list | grep "$pg_service" | grep started > /dev/null; then
        print_info "Starting PostgreSQL ($pg_service)..."
        brew services start "$pg_service"
        sleep 3
        print_status "PostgreSQL started"
    else
        print_info "PostgreSQL is already running"
    fi
    
    print_status "Development environment ready!"
    print_info "You can now start:"
    print_info "  Backend:  cd backend && flask run"
    print_info "  Frontend: cd frontend && npm run dev"
}

# Stop development environment
function stop_dev() {
    print_info "Stopping development environment..."
    
    # Stop Flask server
    if pgrep -f "flask run" > /dev/null; then
        print_info "Stopping Flask server..."
        pkill -f "flask run"
        print_status "Flask server stopped"
    fi
    
    # Stop Vue server
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

# Show status
function show_status() {
    print_info "Development Environment Status"
    echo ""
    
    # PostgreSQL status
    local pg_service=$(get_postgres_service)
    print_info "PostgreSQL ($pg_service):"
    if brew services list | grep "$pg_service" | grep started > /dev/null; then
        print_status "Running"
    else
        print_warning "Not running"
    fi
    
    # Flask status
    print_info "Flask Backend:"
    if pgrep -f "flask run" > /dev/null; then
        print_status "Running (http://localhost:5000)"
    else
        print_warning "Not running"
    fi
    
    # Vue status
    print_info "Vue Frontend:"
    if pgrep -f "npm run dev" > /dev/null; then
        print_status "Running (http://localhost:3000)"
    else
        print_warning "Not running"
    fi
}

# Main command handling
case "$1" in
    "start")
        start_dev
        ;;
    "stop")
        stop_dev "$@"
        ;;
    "status")
        show_status
        ;;
    *)
        echo "Simple RGS Development Utilities"
        echo ""
        echo "Usage: $0 {start|stop|status}"
        echo ""
        echo "Commands:"
        echo "  start              - Start PostgreSQL"
        echo "  stop               - Stop Flask and Vue servers"
        echo "  stop --with-db     - Stop servers and PostgreSQL"
        echo "  status             - Show status of all services"
        echo ""
        echo "Examples:"
        echo "  $0 start           # Start PostgreSQL"
        echo "  $0 status          # Check what's running"
        echo "  $0 stop            # Stop servers only"
        echo "  $0 stop --with-db  # Stop everything including PostgreSQL"
        exit 1
        ;;
esac 