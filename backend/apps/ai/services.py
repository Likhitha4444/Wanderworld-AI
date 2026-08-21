import logging
import json
import time
from google.genai.errors import ServerError
from .client import GeminiClient
from .exceptions import AIResponseError, AIServiceUnavailableError, AITimeoutError

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.client_wrapper = GeminiClient()
        self.client = self.client_wrapper.get_client()

    def generate(self, prompt: str) -> dict:
        """Generates a structured response from Gemini with retries for transient errors."""
        max_attempts = 3
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            start_time = time.time()
            logger.info(f"AI request started (attempt {attempt}).")
            
            try:
                # Generate content
                response = self.client.models.generate_content(
                    model=self.client_wrapper.model,
                    contents=prompt,
                    config={'response_mime_type': 'application/json'}
                )
                
                duration = time.time() - start_time
                logger.info(f"AI request completed in {duration:.2f} seconds.")
                
                # Parse response
                try:
                    text = response.text.strip()
                    if text.startswith("```json"):
                        text = text[len("```json"):-3].strip()
                    elif text.startswith("```"):
                        text = text[3:-3].strip()
                    
                    data = json.loads(text)
                    return {"status": "success", "data": data}
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse AI response: {e}")
                    raise AIResponseError("Invalid response format from AI.")

            except ServerError as e:
                # Retry on 503 or other server errors
                if e.code == 503 and attempt < max_attempts:
                    wait_time = 2 ** (attempt - 1)
                    logger.warning(f"Gemini API temporarily unavailable (503). Retrying in {wait_time}s (attempt {attempt}/{max_attempts}).")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Gemini API server error: {e}")
                    raise AIServiceUnavailableError("Gemini API is temporarily unavailable.")
            except Exception as e:
                logger.error(f"AI request failed: {e}")
                raise AIServiceUnavailableError("AI service error.")
        
        raise AIServiceUnavailableError("Gemini API is unavailable after multiple retries.")

    def health_check(self) -> bool:
        """Internal health check."""
        try:
            # Check if API key is present
            if not self.client_wrapper.api_key:
                return False
            # We don't make a live call here to avoid unnecessary costs/latency
            return True
        except Exception:
            return False
