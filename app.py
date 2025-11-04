from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from src.log_analyzer import LogAnalyzer
from src.utils import save_analysis_result

app = Flask(__name__)
analyzer = LogAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_logs():
    try:
        if 'log_file' in request.files:
            file = request.files['log_file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            log_content = file.read().decode('utf-8')
        else:
            log_content = request.json.get('log_content', '')
        
        if not log_content:
            return jsonify({'error': 'No log content provided'}), 400
        
        # Analyze logs
        result = analyzer.analyze_ci_logs(log_content)
        
        # Save result
        filename = save_analysis_result(result)
        
        return jsonify({
            'success': True,
            'result': result,
            'download_url': f'/download/{filename}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_result(filename):
    try:
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'Failure Pattern Detection'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Changed to debug=True for development
