import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.log_analyzer import LogAnalyzer

class TestLogAnalyzer:
    def setup_method(self):
        self.analyzer = LogAnalyzer()
    
    def test_parse_log_file_basic(self):
        """Test basic log file parsing"""
        sample_log = """
        INFO: Starting tests
        ERROR: Test failure
        WARNING: Deprecated feature
        """
        
        result = self.analyzer.parse_log_file(sample_log)
        assert len(result) == 2  # Should find error and warning
        
        # Check error entry
        error_entries = [e for e in result if e['level'] == 'error']
        assert len(error_entries) == 1
        assert 'error' in error_entries[0]['patterns_found']
        
        # Check warning entry
        warning_entries = [e for e in result if e['level'] == 'warning']
        assert len(warning_entries) == 1
        assert 'warning' in warning_entries[0]['patterns_found']
    
    def test_parse_log_file_empty(self):
        """Test parsing empty log"""
        result = self.analyzer.parse_log_file("")
        assert len(result) == 0
    
    def test_analyze_ci_logs(self):
        """Test complete CI log analysis"""
        sample_log = "ERROR: Build failed\nWARNING: Some warning\nINFO: Normal message"
        
        result = self.analyzer.analyze_ci_logs(sample_log)
        
        assert result['error_count'] == 1
        assert result['warning_count'] == 1
        assert 'summary' in result
        assert 'patterns_detected' in result
        assert result['summary']['total_issues'] == 2
    
    def test_generate_summary(self):
        """Test summary generation"""
        log_entries = [
            {
                'line_number': 1,
                'content': 'ERROR: Test failure',
                'level': 'error',
                'patterns_found': ['error'],
                'timestamp': '2024-01-01T00:00:00'
            },
            {
                'line_number': 2,
                'content': 'WARNING: Deprecation warning',
                'level': 'warning',
                'patterns_found': ['warning'],
                'timestamp': '2024-01-01T00:00:01'
            }
        ]
        
        patterns_detected = {'test_failures': [{'content': 'test', 'line_number': 1}]}
        
        summary = self.analyzer.generate_summary(log_entries, patterns_detected)
        
        assert summary['total_issues'] == 2
        assert summary['health_score'] == 100 - (1 * 10 + 1 * 2)  # 88
        assert 'common_patterns' in summary