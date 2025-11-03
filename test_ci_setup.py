#!/usr/bin/env python3
"""
CI Setup Verification Test
"""

def test_ci_environment():
    """Test that basic Python environment works"""
    try:
        # Test basic imports
        import sys
        import os
        import pytest
        
        # Test project imports
        from src.log_analyzer import LogAnalyzer
        from src.pattern_detector import PatternDetector
        
        # Test basic functionality
        analyzer = LogAnalyzer()
        result = analyzer.analyze_ci_logs("ERROR: Test error\nWARNING: Test warning")
        
        assert result['error_count'] == 1
        assert result['warning_count'] == 1
        
        print("✅ CI environment test passed!")
        return True
        
    except Exception as e:
        print(f"❌ CI environment test failed: {e}")
        return False

if __name__ == "__main__":
    test_ci_environment()