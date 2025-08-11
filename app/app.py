#!/usr/bin/env python3
"""
AI-Augmented DevOps Demo Application
A simple Flask web service for demonstrating DevSecOps pipeline
"""

from flask import Flask, jsonify, request, render_template_string
import os
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI-Augmented DevOps Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        .status { padding: 20px; margin: 20px 0; border-radius: 5px; }
        .healthy { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
        .info { background: #d1ecf1; border: 1px solid #bee5eb; color: #0c5460; }
        .endpoint { margin: 20px 0; padding: 15px; background: #f8f9fa; border-left: 4px solid #007bff; }
        code { background: #f1f3f4; padding: 2px 4px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI-Augmented DevOps Pipeline</h1>
        <div class="status healthy">
            <strong>✅ Service Status:</strong> Running and healthy!
        </div>
        <div class="info">
            <strong>🚀 Version:</strong> {{ version }}<br>
            <strong>🕐 Uptime:</strong> {{ uptime }}<br>
            <strong>🐳 Container:</strong> {{ container_info }}
        </div>
        
        <div class="endpoint">
            <h3>API Endpoints:</h3>
            <p><code>GET /</code> - This web interface</p>
            <p><code>GET /api/health</code> - Health check endpoint</p>
            <p><code>GET /api/status</code> - Detailed service status</p>
            <p><code>POST /api/upload</code> - Simulate file upload processing</p>
        </div>
        
        <div class="info">
            <strong>💡 Demo Features:</strong><br>
            • Pre-commit hooks with secret scanning<br>
            • Automated vulnerability scanning with Trivy<br>
            • Kubernetes policy enforcement with Kyverno<br>
            • Runtime anomaly detection with ML<br>
            • Explainable AI incident reporting
        </div>
    </div>
</body>
</html>
"""

# Application start time for uptime calculation
START_TIME = time.time()

@app.route('/')
def home():
    """Main web interface"""
    uptime_seconds = int(time.time() - START_TIME)
    uptime_str = f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"
    
    container_info = os.environ.get('HOSTNAME', 'localhost')
    
    return render_template_string(
        HTML_TEMPLATE,
        version="1.0.0",
        uptime=uptime_str,
        container_info=container_info
    )

@app.route('/api/health')
def health_check():
    """Health check endpoint for Kubernetes probes"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI-Augmented DevOps is running!',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/status')
def detailed_status():
    """Detailed status endpoint with metrics"""
    uptime_seconds = int(time.time() - START_TIME)
    
    return jsonify({
        'service': 'ai-devops-demo',
        'version': '1.0.0',
        'status': 'running',
        'uptime_seconds': uptime_seconds,
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'container_id': os.environ.get('HOSTNAME', 'localhost'),
        'features': {
            'pre_commit_hooks': True,
            'vulnerability_scanning': True,
            'policy_enforcement': True,
            'anomaly_detection': True,
            'explainable_ai': True
        }
    })

@app.route('/api/upload', methods=['POST'])
def simulate_upload():
    """Simulate file upload processing for demo purposes"""
    try:
        # Simulate processing time
        processing_time = 0.5
        time.sleep(processing_time)
        
        # Log the upload attempt
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        logger.info(f"Upload simulation from {client_ip}")
        
        return jsonify({
            'status': 'success',
            'message': 'File processed successfully',
            'processing_time_seconds': processing_time,
            'ai_analysis': {
                'security_scan': 'clean',
                'content_type': 'image/jpeg',
                'malware_detected': False,
                'confidence': 0.97
            }
        })
    
    except Exception as e:
        logger.error(f"Upload processing error: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Processing failed',
            'error': str(e)
        }), 500

@app.route('/api/simulate-anomaly')
def simulate_anomaly():
    """Endpoint to simulate an anomaly for testing monitoring"""
    logger.warning("🚨 SIMULATED ANOMALY: Unusual traffic pattern detected")
    
    return jsonify({
        'status': 'anomaly_detected',
        'message': 'Simulated anomaly for testing purposes',
        'anomaly_type': 'traffic_spike',
        'ai_confidence': 0.85,
        'recommended_action': 'Review traffic patterns and scale resources'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting AI-Augmented DevOps Demo on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
