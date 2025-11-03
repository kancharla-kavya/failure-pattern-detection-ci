import pytest
from src.pattern_detector import PatternDetector

class TestPatternDetector:
    def setup_method(self):
        self.detector = PatternDetector()
    
    def test_detect_test_failures(self):
        log_entries = [
            {'content': 'FAIL test_login', 'line_number': 1, 'level': 'error', 'patterns_found': []},
            {'content': 'Test failed: user_creation', 'line_number': 2, 'level': 'error', 'patterns_found': []}
        ]
        
        result = self.detector.detect_patterns(log_entries)
        
        assert 'test_failures' in result
        assert len(result['test_failures']) == 2
    
    def test_get_suggestions(self):
        detected_patterns = {
            'test_failures': [{'content': 'FAIL test', 'line_number': 1, 'pattern': 'FAIL.*test'}],
            'build_errors': [{'content': 'Build failed', 'line_number': 2, 'pattern': 'Build failed'}]
        }
        
        suggestions = self.detector.get_pattern_suggestions(detected_patterns)
        
        assert len(suggestions) > 0
        assert any('test' in suggestion.lower() for suggestion in suggestions)