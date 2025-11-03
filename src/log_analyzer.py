import re
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from .pattern_detector import PatternDetector  # Fixed import

class LogAnalyzer:
    def __init__(self):
        self.pattern_detector = PatternDetector()
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def parse_log_file(self, log_content: str) -> List[Dict[str, Any]]:
        """Parse log file and extract structured information"""
        log_entries = []
        
        # Common CI log patterns
        patterns = {
            'error': r'ERROR|Error|error|FAILED|Failed|failed',
            'warning': r'WARNING|Warning|warning',
            'test_failure': r'FAIL|Fail|fail|AssertionError',
            'build_failure': r'Build failed|build failure|compilation error',
            'dependency_error': r'ModuleNotFoundError|ImportError|dependency',
            'timeout': r'TIMEOUT|Timeout|timeout',
            'memory': r'MemoryError|out of memory|OOM',
        }
        
        lines = log_content.split('\n')
        for line_num, line in enumerate(lines, 1):
            entry = {
                'line_number': line_num,
                'content': line.strip(),
                'timestamp': datetime.now().isoformat(),
                'level': 'info',
                'patterns_found': []
            }
            
            for pattern_name, pattern in patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    entry['level'] = 'error' if pattern_name in ['error', 'test_failure', 'build_failure'] else 'warning'
                    entry['patterns_found'].append(pattern_name)
            
            if entry['patterns_found']:
                log_entries.append(entry)
        
        return log_entries
    
    def analyze_ci_logs(self, log_content: str) -> Dict[str, Any]:
        """Main method to analyze CI logs"""
        self.logger.info("Starting CI log analysis...")
        
        log_entries = self.parse_log_file(log_content)
        patterns_detected = self.pattern_detector.detect_patterns(log_entries)
        
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'total_entries_analyzed': len(log_entries),
            'error_count': len([e for e in log_entries if e['level'] == 'error']),
            'warning_count': len([e for e in log_entries if e['level'] == 'warning']),
            'patterns_detected': patterns_detected,
            'log_entries': log_entries,
            'summary': self.generate_summary(log_entries, patterns_detected)
        }
        
        self.logger.info(f"Analysis complete. Found {analysis_result['error_count']} errors and {analysis_result['warning_count']} warnings.")
        
        return analysis_result
    
    def generate_summary(self, log_entries: List[Dict], patterns_detected: Dict) -> Dict:
        """Generate summary of the analysis"""
        total_errors = len([e for e in log_entries if e['level'] == 'error'])
        total_warnings = len([e for e in log_entries if e['level'] == 'warning'])
        
        common_patterns = {}
        for entry in log_entries:
            for pattern in entry['patterns_found']:
                common_patterns[pattern] = common_patterns.get(pattern, 0) + 1
        
        return {
            'total_issues': total_errors + total_warnings,
            'common_patterns': dict(sorted(common_patterns.items(), key=lambda x: x[1], reverse=True)[:5]),
            'most_frequent_error': max(common_patterns, key=common_patterns.get) if common_patterns else None,
            'health_score': max(0, 100 - (total_errors * 10 + total_warnings * 2))
        }

if __name__ == "__main__":
    # Test with sample log
    sample_log = """
    INFO: Starting build process...
    WARNING: Using deprecated dependency
    ERROR: Test failure in test_user_authentication
    FAILED: Build failed due to compilation errors
    INFO: Cleaning up resources
    ERROR: Timeout in integration tests
    """
    
    analyzer = LogAnalyzer()
    result = analyzer.analyze_ci_logs(sample_log)
    print(json.dumps(result, indent=2))