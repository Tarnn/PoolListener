#!/usr/bin/env python3
"""
Test Runner for Enhanced Pool Listener
Runs all tests with proper error handling
"""

import sys
import subprocess
import os
from pathlib import Path

def run_tests():
    """Run all tests with proper setup"""
    
    print("🧪 Enhanced Pool Listener Test Suite")
    print("=" * 60)
    
    # Set up environment
    project_root = Path(__file__).parent
    src_path = project_root / "src"
    
    # Add src to Python path
    env = os.environ.copy()
    env['PYTHONPATH'] = str(src_path)
    
    # Set test environment variables
    test_env = {
        'INFURA_API_KEY': 'test_key_12345678901234567890',
        'TOKEN_ADDRESS': '0x1234567890123456789012345678901234567890',
        'SENDER_EMAIL': 'test@example.com',
        'RECEIVER_EMAIL': 'receiver@example.com',
        'EMAIL_PASSWORD': 'test_password',
        'NOTIFICATION_URLS': 'discord://test_webhook'
    }
    
    env.update(test_env)
    
    try:
        # Run pytest with proper configuration
        result = subprocess.run([
            sys.executable, '-m', 'pytest', 
            'tests/', '-v', '--tb=short', '--no-header'
        ], env=env, cwd=project_root, capture_output=False)
        
        if result.returncode == 0:
            print("\n✅ All tests passed! 🎉")
            print("Ready to test real notifications!")
        else:
            print(f"\n❌ Tests failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 