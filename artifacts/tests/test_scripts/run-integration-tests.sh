#!/bin/bash
# Integration Testing Setup Script for Unix-like systems

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_status() {
    local message=$1
    local status=${2:-info}
    
    case $status in
        success)
            echo -e "${GREEN}✓ $message${NC}"
            ;;
        error)
            echo -e "${RED}✗ $message${NC}"
            ;;
        warning)
            echo -e "${YELLOW}⚠ $message${NC}"
            ;;
        *)
            echo -e "${BLUE}ℹ $message${NC}"
            ;;
    esac
}

print_section() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
}

# Main script
print_section "Integration Testing Setup & Execution"

# Check Python
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_status "Python 3 is not installed" error
    exit 1
fi
print_status "Python found: $(python3 --version)" success

# Check backend
print_status "Checking backend at http://localhost:8001..."
if ! python3 -c "import requests; requests.get('http://localhost:8001/health', timeout=2)" 2>/dev/null; then
    print_status "Backend is not responding" error
    echo ""
    print_status "Please start the backend with:" warning
    echo "  cd apps/backend"
    echo "  python3 -m uvicorn main:app --host 127.0.0.1 --port 8001"
    exit 1
fi
print_status "Backend is running" success

# Check database
print_status "Checking database..."
if [ -f "apps/data/task_management.db" ]; then
    size=$(du -h apps/data/task_management.db | cut -f1)
    print_status "Database exists ($size)" success
else
    print_status "Database does not exist yet (will be created on backend startup)" warning
fi

# Check/seed database
print_status "Checking if database needs seeding..."
db_status=$(python3 -c "
import sqlite3
from pathlib import Path
db_path = Path('apps/data/task_management.db')
if db_path.exists():
    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        user_count = cur.fetchone()[0]
        conn.close()
        print('HAS_DATA' if user_count > 0 else 'EMPTY')
    except:
        print('ERROR')
else:
    print('NO_DB')
" 2>/dev/null)

if [ "$db_status" == "EMPTY" ] || [ "$db_status" == "NO_DB" ]; then
    print_status "Seeding database with test data..." warning
    cd apps/backend
    python3 seed_data.py
    cd ../..
else
    print_status "Database already contains test data" success
fi

# Check frontend
print_status "Checking frontend setup..."
if [ ! -d "apps/frontend/node_modules" ]; then
    print_status "Frontend dependencies not installed" warning
    print_status "Installing frontend dependencies..."
    cd apps/frontend
    npm install
    cd ../..
fi
print_status "Frontend dependencies are installed" success

# Run tests
print_section "Running Integration Tests"

cd apps/frontend
npm test -- persistence-integration.spec.ts
test_result=$?

# Summary
print_section "Test Summary"
if [ $test_result -eq 0 ]; then
    print_status "Integration testing completed successfully!" success
else:
    print_status "Integration testing had failures. See output above." error
fi

exit $test_result
