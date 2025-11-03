import re
from typing import List, Dict, Any
from collections import defaultdict

class PatternDetector:
    def __init__(self):
        self.patterns = {
            'test_failures': [
                r'FAIL.*test',
                r'Test.*failed',
                r'AssertionError',
                r'expected.*but got'
            ],
            'build_errors': [
                r'Build failed',
                r'compilation error',
                r'SyntaxError',
                r'TypeError'
            ],
            'dependency_issues': [
                r'ModuleNotFoundError',
                r'ImportError',
                r'package not found',
                r'dependency conflict'
            ],
            'resource_issues': [
                r'MemoryError',
                r'out of memory',
                r'TIMEOUT',
                r'disk space'
            ],
            'network_issues': [
                r'Connection refused',
                r'Network is unreachable',
                r'SSL error',
                r'DNS lookup failed'
            ],
            'configuration_errors': [
                r'Configuration error',
                r'missing configuration',
                r'invalid setting'
            ]
        }
    
    def detect_patterns(self, log_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect failure patterns in log entries"""
        detected_patterns = defaultdict(list)
        
        for entry in log_entries:
            content = entry['content']
            line_number = entry['line_number']
            
            for pattern_category, pattern_list in self.patterns.items():
                for pattern in pattern_list:
                    if re.search(pattern, content, re.IGNORECASE):
                        detected_patterns[pattern_category].append({
                            'line_number': line_number,
                            'content': content,
                            'pattern': pattern
                        })
                        break  # Avoid multiple matches for same line
        
        # Convert to regular dict and add statistics
        result = dict(detected_patterns)
        result['statistics'] = {
            'total_patterns_detected': sum(len(patterns) for patterns in detected_patterns.values()),
            'pattern_counts': {category: len(patterns) for category, patterns in detected_patterns.items()},
            'most_common_category': max(detected_patterns.keys(), 
                                      key=lambda x: len(detected_patterns[x])) if detected_patterns else None
        }
        
        return result
    
    def get_pattern_suggestions(self, detected_patterns: Dict[str, Any]) -> List[str]:
        """Get suggestions based on detected patterns"""
        suggestions = []
        
        if detected_patterns.get('test_failures'):
            suggestions.extend([
                "Review recent code changes in test files",
                "Check test environment configuration",
                "Verify test data integrity"
            ])
        
        if detected_patterns.get('build_errors'):
            suggestions.extend([
                "Check syntax errors in recent commits",
                "Verify compiler/interpreter version compatibility",
                "Review build configuration files"
            ])
        
        if detected_patterns.get('dependency_issues'):
            suggestions.extend([
                "Update dependency versions",
                "Check virtual environment setup",
                "Verify package repository connectivity"
            ])
        
        if detected_patterns.get('resource_issues'):
            suggestions.extend([
                "Increase resource allocation",
                "Optimize memory usage",
                "Add timeout handling"
            ])
        
        if not suggestions:
            suggestions.append("No specific patterns detected. Review logs manually.")
        
        return suggestions