#!/usr/bin/env python3
"""
RGS Test Runner

Runs the test suite with various options for coverage, specific modules, etc.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add backend to Python path
backend_dir = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_dir))

def run_command(cmd, description):
    """Run a command and handle output"""
    print(f"\n🔧 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=backend_dir)
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"⚠️  Warnings/Errors:\n{result.stderr}")
        
        if result.returncode != 0:
            print(f"❌ Command failed with exit code {result.returncode}")
            return False
        
        print(f"✅ {description} completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run RGS tests')
    parser.add_argument('--module', '-m', help='Run specific test module (e.g., test_auth, test_models)')
    parser.add_argument('--coverage', '-c', action='store_true', help='Run tests with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--fast', '-f', action='store_true', help='Skip slow tests')
    parser.add_argument('--watch', '-w', action='store_true', help='Watch for file changes and re-run tests')
    parser.add_argument('--clean', action='store_true', help='Clean test artifacts before running')
    
    args = parser.parse_args()
    
    print("🧪 RGS Test Runner")
    print("=" * 50)
    
    # Clean artifacts if requested
    if args.clean:
        clean_cmd = "find . -name '*.pyc' -delete && find . -name '__pycache__' -type d -exec rm -rf {} + || true"
        run_command(clean_cmd, "Cleaning test artifacts")
    
    # Build pytest command
    pytest_cmd = "python -m pytest"
    
    # Add verbosity
    if args.verbose:
        pytest_cmd += " -v"
    else:
        pytest_cmd += " -v"  # Always use some verbosity
    
    # Add specific module
    if args.module:
        if not args.module.startswith('test_'):
            args.module = f'test_{args.module}'
        if not args.module.endswith('.py'):
            args.module = f'{args.module}.py'
        pytest_cmd += f" tests/{args.module}"
    else:
        pytest_cmd += " tests/"
    
    # Add markers for fast mode
    if args.fast:
        pytest_cmd += " -m 'not slow'"
    
    # Add other pytest options
    pytest_cmd += " --tb=short"
    pytest_cmd += " --strict-markers"
    pytest_cmd += " --disable-warnings"
    
    # Run with coverage if requested
    if args.coverage:
        coverage_cmd = f"python -m coverage run -m pytest tests/ --tb=short --strict-markers --disable-warnings"
        if args.module:
            coverage_cmd = coverage_cmd.replace("tests/", f"tests/{args.module}")
        
        success = run_command(coverage_cmd, "Running tests with coverage")
        if success:
            run_command("python -m coverage report", "Coverage Report")
            run_command("python -m coverage html", "Generating HTML coverage report")
            print("\n📊 HTML coverage report generated in htmlcov/index.html")
    else:
        # Run regular tests
        if args.watch:
            # Install pytest-watch if needed
            install_cmd = "pip install pytest-watch"
            print("Installing pytest-watch for watch mode...")
            subprocess.run(install_cmd, shell=True, cwd=backend_dir)
            
            pytest_cmd = pytest_cmd.replace("python -m pytest", "ptw --")
            run_command(pytest_cmd, "Running tests in watch mode (Ctrl+C to stop)")
        else:
            success = run_command(pytest_cmd, "Running tests")
            if not success:
                sys.exit(1)
    
    print("\n🎉 Test run completed!")
    print("\nUseful commands:")
    print("  python run-tests.py -m auth     # Run only auth tests")
    print("  python run-tests.py -c          # Run with coverage")
    print("  python run-tests.py -w          # Watch mode")
    print("  python run-tests.py --fast      # Skip slow tests")

if __name__ == '__main__':
    main() 