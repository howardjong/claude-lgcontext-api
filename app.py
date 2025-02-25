import os
import logging
import uuid
import signal
import sys
from flask import Flask, request, jsonify, render_template, redirect, url_for
from claude_handler import create_claude_assistant, query_claude
from logger import setup_logger

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Setup logging
logger = setup_logger()

# Initialize Claude assistant
claude_config = None

def init_claude():
    global claude_config
    try:
        claude_config = create_claude_assistant()
        logger.info("Claude assistant initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Claude assistant: {e}")
        return None

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Shutdown signal received, cleaning up...")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

@app.before_first_request
def before_first_request():
    """Initialize services before first request"""
    global claude_config
    if claude_config is None:
        init_claude()

@app.route('/')
def index():
    """Redirect root URL to status dashboard"""
    return redirect(url_for('status'))

@app.route('/start', methods=['GET'])
def start():
    """Initialize a new conversation thread"""
    try:
        thread_id = str(uuid.uuid4())
        logger.info(f"New conversation thread created: {thread_id}")
        return jsonify({"thread_id": thread_id})
    except Exception as e:
        logger.error(f"Error creating conversation thread: {e}")
        return jsonify({"error": "Failed to create conversation thread"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with thread tracking"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        thread_id = data.get('thread_id')
        message = data.get('message')

        if not thread_id:
            return jsonify({"error": "Missing thread_id"}), 400
        if not message:
            return jsonify({"error": "Missing message"}), 400

        logger.info(f"Received message for thread {thread_id}: {message}")

        if not claude_config:
            init_claude()
            if not claude_config:
                return jsonify({'error': 'Claude assistant not initialized'}), 500

        response = query_claude(message, claude_config)
        logger.info(f"Generated response for thread {thread_id}")

        return jsonify({
            "response": response,
            "thread_id": thread_id
        })

    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """Legacy webhook endpoint for Voiceflow compatibility"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Invalid request format'}), 400

        question = data['question']
        logger.info(f"Received question via webhook: {question}")

        if not claude_config:
            init_claude()
            if not claude_config:
                return jsonify({'error': 'Claude assistant not initialized'}), 500

        response = query_claude(question, claude_config)
        logger.info("Claude response generated successfully")

        return jsonify({
            'output': response
        })

    except Exception as e:
        logger.error(f"Error processing webhook request: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/status')
def status():
    """Status monitoring dashboard"""
    try:
        if not claude_config:
            init_claude()
        return render_template('dashboard.html', 
                            claude_status=bool(claude_config),
                            anthropic_key=bool(os.environ.get('ANTHROPIC_API_KEY')))
    except Exception as e:
        logger.error(f"Error rendering status page: {e}")
        return jsonify({'error': 'Failed to render status page'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        if not claude_config:
            init_claude()
        return jsonify({
            'status': 'healthy',
            'claude_assistant': bool(claude_config),
            'anthropic_api': bool(os.environ.get('ANTHROPIC_API_KEY'))
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize Claude before starting
    init_claude()
    # ALWAYS serve the app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)