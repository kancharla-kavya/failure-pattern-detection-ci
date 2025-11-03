"""
Test package for Failure Pattern Detection in CI Logs
"""

import os
import sys

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Common test data
SAMPLE_CI_LOG = """
INFO: Starting CI pipeline
WARNING: Using deprecated API
ERROR: Test failure in test_user_login
FAILED: 1 test failed
INFO: Generating reports
ERROR: Timeout in integration tests
BUILD: Build completed with errors
"""

SAMPLE_ERROR_LOG = """
ERROR: ModuleNotFoundError: No module named 'nonexistent'
ERROR: SyntaxError: invalid syntax
FAILED: Build failed due to errors
"""

SAMPLE_SUCCESS_LOG = """
INFO: Starting build process
INFO: All tests passed
SUCCESS: Build completed successfully
"""