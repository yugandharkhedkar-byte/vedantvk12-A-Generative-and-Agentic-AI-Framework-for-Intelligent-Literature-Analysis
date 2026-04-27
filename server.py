# File: server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from coordinator import CoordinatorAgent
import os

app = Flask(__name__)
CORS(app)  # Allow React to talk to this server

# Initialize the AI System
ai_system = CoordinatorAgent()

@app.route('/api/generate', methods=['POST'])
def generate_research():
    data = request.json
    topic = data.get('topic')
    
    print(f"\n🚀 API Request Received: {topic}")
    
    # 1. Run the AI Workflow
    result = ai_system.generate_full_report_data(topic)
    
    return jsonify(result)

# ✅ FIXED ROUTE HERE (IMPORTANT CHANGE)
@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join('generated_reports', filename)

    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(
        'generated_reports', 
        filename, 
        as_attachment=True,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    print("⚡ Server running on http://localhost:5000")
    app.run(debug=True, port=5000)