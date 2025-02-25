import unittest
import json
import os
from app import app

class TestClaudeService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Ensure ANTHROPIC_API_KEY is set for testing
        os.environ['ANTHROPIC_API_KEY'] = 'test_key'
        
    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        
    def test_status_dashboard(self):
        response = self.app.get('/status')
        self.assertEqual(response.status_code, 200)
        
    def test_webhook_missing_question(self):
        response = self.app.post('/webhook',
                               json={})
        self.assertEqual(response.status_code, 400)
        
    def test_webhook_valid_request(self):
        response = self.app.post('/webhook',
                               json={'question': 'Test question'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertEqual(data['status'], 'success')

if __name__ == '__main__':
    unittest.main()
