import os
import logging
from flask import Flask, request, jsonify, render_template, redirect, url_for
from claude_handler import create_claude_assistant, query_claude
from logger import setup_logger

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Setup logging
logger = setup_logger()

# Initialize Claude assistant
try:
    claude_config = create_claude_assistant()
    logger.info("Claude assistant initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Claude assistant: {e}")
    claude_config = None

@app.route('/')
def index():
    """Redirect root URL to status dashboard"""
    return redirect(url_for('status'))

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Voiceflow webhook requests"""
    try:
        data = request.get_json()

        if not data or 'question' not in data:
            return jsonify({'error': 'Invalid request format'}), 400

        question = data['question']
        logger.info(f"Received question: {question}")

        if not claude_config:
            return jsonify({'error': 'Claude assistant not initialized'}), 500

        response = query_claude(question, claude_config)
        logger.info(f"Claude response generated successfully")

        return jsonify({
            'response': response,
            'status': 'success'
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
    return render_template('dashboard.html', 
                         claude_status=bool(claude_config),
                         anthropic_key=bool(os.environ.get('ANTHROPIC_API_KEY')))

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'claude_assistant': bool(claude_config),
        'anthropic_api': bool(os.environ.get('ANTHROPIC_API_KEY'))
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)