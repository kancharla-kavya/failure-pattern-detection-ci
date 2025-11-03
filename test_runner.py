#!/usr/bin/env python3
"""
Simple test runner to verify everything works
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("🧪 Testing Failure Pattern Detection Project...")
    print("=" * 50)
    
    try:
        # Test imports
        from src.log_analyzer import LogAnalyzer
        from src.pattern_detector import PatternDetector
        print("✅ All imports successful")
        
        # Test LogAnalyzer
        analyzer = LogAnalyzer()
        sample_log = """
        INFO: Starting CI pipeline
        WARNING: Using deprecated API
        ERROR: Test failure in test_user_login
        FAILED: Build completed with errors
        """
        
        result = analyzer.analyze_ci_logs(sample_log)
        print(f"✅ LogAnalyzer test passed")
        print(f"   - Errors found: {result['error_count']}")
        print(f"   - Warnings found: {result['warning_count']}")
        print(f"   - Health score: {result['summary']['health_score']}")
        
        # Test PatternDetector
        detector = PatternDetector()
        log_entries = [
            {
                'content': 'FAIL test_example',
                'line_number': 1,
                'level': 'error',
                'patterns_found': [],
                'timestamp': '2024-01-01T00:00:00'
            }
        ]
        patterns = detector.detect_patterns(log_entries)
        print(f"✅ PatternDetector test passed")
        print(f"   - Patterns detected: {patterns['statistics']['total_patterns_detected']}")
        
        print("=" * 50)
        print("🎉 All basic tests passed! You can now run pytest.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()