import json
import yaml
from datetime import datetime
from typing import Any, Dict

def save_analysis_result(result: Dict[str, Any], filename: str = None) -> str:
    """Save analysis result to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_result_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    return filename

def load_analysis_result(filename: str) -> Dict[str, Any]:
    """Load analysis result from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def format_terminal_output(result: Dict[str, Any]) -> str:
    """Format analysis result for terminal output"""
    output = []
    output.append("=" * 50)
    output.append("CI LOG ANALYSIS RESULTS")
    output.append("=" * 50)
    
    summary = result.get('summary', {})
    output.append(f"Total Issues: {summary.get('total_issues', 0)}")
    output.append(f"Errors: {result.get('error_count', 0)}")
    output.append(f"Warnings: {result.get('warning_count', 0)}")
    output.append(f"Health Score: {summary.get('health_score', 0)}/100")
    
    output.append("\nDETECTED PATTERNS:")
    patterns = result.get('patterns_detected', {})
    for category, items in patterns.items():
        if category != 'statistics' and items:
            output.append(f"  {category.upper()}: {len(items)} occurrences")
    
    output.append("\nRECOMMENDATIONS:")
    # Add recommendations based on patterns
    
    output.append("=" * 50)
    return "\n".join(output)