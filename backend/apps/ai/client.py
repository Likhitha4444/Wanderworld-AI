import os
import logging
from django.conf import settings
from google import genai
from .exceptions import AIConfigurationError, AIAuthenticationError

logger = logging.getLogger(__name__)

class GeminiClient:
    _instance = None

    def __new__(cls):
        instance = super(GeminiClient, cls).__new__(cls)
        # We need to make sure _initialize is called every time if it's not initialized
        # but in tests we want to reset it.
        # Let's bypass singleton in tests if explicitly needed.
        if cls._instance is None:
            cls._instance = instance
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Read from settings to be more Django-ish, or os.environ
        api_key = os.environ.get('GEMINI_API_KEY')
        
        # Test hook to force failure
        if api_key == 'FORCE_MISSING':
            api_key = None
            
        print(f"DEBUG: _initialize called, api_key is {api_key}")
        
        if not api_key:
            logger.error("GEMINI_API_KEY is not configured.")
            raise AIConfigurationError("Gemini API Key is missing.")
        
        self.api_key = api_key
        self.model = 'gemini-3.6-flash'
        
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to initialize Gemini Client: {e}")
            raise AIAuthenticationError("Failed to initialize Gemini Client.")

    def get_client(self):
        return self.client

def reset_gemini_client():
    GeminiClient._instance = None
