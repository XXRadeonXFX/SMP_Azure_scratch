"""
Configuration settings for Group Manager Service
Loads from environment variables
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Group Manager Service"
    ENVIRONMENT: str = "development"
    PORT: int = 8080
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:7001"]
    
    # Azure AD Credentials (Required for Azure operations)
    AZURE_TENANT_ID: str = ""
    AZURE_CLIENT_ID: str = ""
    AZURE_CLIENT_SECRET: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    def validate_azure_credentials(self) -> bool:
        """Check if Azure credentials are configured"""
        return bool(
            self.AZURE_TENANT_ID and 
            self.AZURE_CLIENT_ID and 
            self.AZURE_CLIENT_SECRET
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()
