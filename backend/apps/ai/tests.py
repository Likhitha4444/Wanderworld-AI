from django.test import TestCase
from unittest.mock import MagicMock, patch
from .services import GeminiService
from .exceptions import AIConfigurationError
from .client import reset_gemini_client

class AIServiceTests(TestCase):
    
    def test_health_check_with_key(self):
        with patch('os.environ.get') as mock_get:
            with patch('apps.ai.client.genai.Client') as mock_client:
                def side_effect(key, default=None):
                    if key == 'GEMINI_API_KEY': return 'fake-key'
                    return default
                mock_get.side_effect = side_effect
                mock_client.return_value = MagicMock()
                
                # Reset the singleton for testing
                reset_gemini_client()
                
                service = GeminiService()
                self.assertTrue(service.health_check())

    def test_health_check_without_key(self):
        # Reset the singleton for testing
        reset_gemini_client()
        
        # We need to ensure that when _initialize runs, it gets None for GEMINI_API_KEY
        import os
        
        # We need to make sure the environment is empty, or patch os.environ.get
        # The singleton issue is tricky.
        
        with patch('os.environ.get', return_value=None):
            # This should raise AIConfigurationError when initializing
            with self.assertRaises(AIConfigurationError):
                GeminiService()
