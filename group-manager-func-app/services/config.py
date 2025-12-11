"""
Configuration management for Azure Functions
Loads from environment variables / local.settings.json
"""
import os
from typing import Optional
from functools import lru_cache


class Settings:
    """Application settings loaded from environment"""
    
    def __init__(self):
        # Azure AD Credentials
        self.AZURE_TENANT_ID = os.environ.get("AZURE_TENANT_ID", "")
        self.AZURE_CLIENT_ID = os.environ.get("AZURE_CLIENT_ID", "")
        self.AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET", "")
        
        # Validation
        if not self.AZURE_TENANT_ID:
            raise ValueError("AZURE_TENANT_ID environment variable is required")
        if not self.AZURE_CLIENT_ID:
            raise ValueError("AZURE_CLIENT_ID environment variable is required")
        if not self.AZURE_CLIENT_SECRET:
            raise ValueError("AZURE_CLIENT_SECRET environment variable is required")
    
    def validate_credentials(self) -> bool:
        """Check if all Azure credentials are configured"""
        return bool(
            self.AZURE_TENANT_ID and 
            self.AZURE_CLIENT_ID and 
            self.AZURE_CLIENT_SECRET
        )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
