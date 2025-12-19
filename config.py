import os
from dotenv import load_dotenv

class Config:
    """Configuration manager for Azure OpenAI API credentials"""
    
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Azure OpenAI configuration
        self.azure_api_key = os.getenv('AZURE_OPENAI_API_KEY', '')
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '')
        self.deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME', 'gpt-4-vision')
        
        # Validate configuration
        self._validate()
    
    def _validate(self):
        """Validate that required configuration is present"""
        if not self.azure_api_key:
            print("WARNING: AZURE_OPENAI_API_KEY not set in .env file")
        if not self.azure_endpoint:
            print("WARNING: AZURE_OPENAI_ENDPOINT not set in .env file")
    
    def is_configured(self):
        """Check if all required configuration is present"""
        return bool(self.azure_api_key and self.azure_endpoint)