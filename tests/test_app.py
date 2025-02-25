import unittest
import json
import os
from unittest.mock import patch, MagicMock
from app import app

class TestClaudeService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        os.environ['ANTHROPIC_API_KEY'] = 'test_key'

        # Mock config for testing
        self.mock_config = {
            "model": "claude-3-5-sonnet-20241022",
            "instructions": "Test instructions",
            "knowledgeContent": "Test content"
        }

    @patch('app.claude_config')
    def test_health_endpoint(self, mock_config):
        mock_config.return_value = True
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    @patch('app.claude_config')
    def test_status_dashboard(self, mock_config):
        mock_config.return_value = True
        response = self.app.get('/status')
        self.assertEqual(response.status_code, 200)

    def test_start_conversation(self):
        response = self.app.get('/start')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('thread_id', data)
        self.assertTrue(len(data['thread_id']) > 0)

    def test_chat_missing_thread_id(self):
        response = self.app.post('/chat',
                              json={'message': 'Test message'})
        self.assertEqual(response.status_code, 400)

    def test_chat_missing_message(self):
        response = self.app.post('/chat',
                              json={'thread_id': 'test-thread'})
        self.assertEqual(response.status_code, 400)

    @patch('app.query_claude')
    @patch('app.claude_config')
    def test_chat_valid_request(self, mock_config, mock_query):
        mock_config.return_value = True
        mock_query.return_value = "This is a mock response from Claude"

        # First get a thread_id
        start_response = self.app.get('/start')
        thread_id = json.loads(start_response.data)['thread_id']

        # Then test the chat endpoint
        response = self.app.post('/chat',
                              json={
                                  'thread_id': thread_id,
                                  'message': 'Test question'
                              })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertIn('thread_id', data)
        self.assertEqual(data['thread_id'], thread_id)
        self.assertEqual(data['response'], "This is a mock response from Claude")

    def test_webhook_missing_question(self):
        response = self.app.post('/webhook',
                              json={})
        self.assertEqual(response.status_code, 400)

    @patch('app.query_claude')
    @patch('app.claude_config')
    def test_webhook_valid_request(self, mock_config, mock_query):
        mock_config.return_value = True
        mock_query.return_value = "This is a mock webhook response"

        response = self.app.post('/webhook',
                              json={'question': 'Test question'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('output', data)
        self.assertEqual(data['output'], "This is a mock webhook response")

if __name__ == '__main__':
    unittest.main()