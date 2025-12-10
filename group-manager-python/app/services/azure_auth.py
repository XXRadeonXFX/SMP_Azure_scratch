"""
Azure AD Authentication Service
Handles authentication with Azure AD and MS Graph API
"""
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class AzureAuthService:
    """Service for Azure AD authentication and MS Graph API access"""
    
    def __init__(self):
        self._credential: Optional[ClientSecretCredential] = None
        self._graph_client: Optional[GraphServiceClient] = None
    
    def get_credential(self) -> ClientSecretCredential:
        """Get or create Azure AD credential"""
        if not self._credential:
            logger.info("Creating Azure AD credential")
            self._credential = ClientSecretCredential(
                tenant_id=settings.AZURE_TENANT_ID,
                client_id=settings.AZURE_CLIENT_ID,
                client_secret=settings.AZURE_CLIENT_SECRET
            )
        return self._credential
    
    def get_graph_client(self) -> GraphServiceClient:
        """Get or create MS Graph API client"""
        if not self._graph_client:
            logger.info("Creating MS Graph API client")
            credential = self.get_credential()
            scopes = ["https://graph.microsoft.com/.default"]
            self._graph_client = GraphServiceClient(
                credentials=credential,
                scopes=scopes
            )
        return self._graph_client
    
    async def test_connection(self) -> dict:
        """Test Azure AD connection and MS Graph API access"""
        try:
            logger.info("Testing Azure AD connection")
            client = self.get_graph_client()
            
            # Try to get organization info as a test
            org = await client.organization.get()
            
            if org and org.value and len(org.value) > 0:
                org_info = org.value[0]
                return {
                    "status": "connected",
                    "tenant_id": settings.AZURE_TENANT_ID,
                    "organization": org_info.display_name if org_info.display_name else "Unknown",
                    "message": "Successfully connected to Azure AD and MS Graph API"
                }
            else:
                return {
                    "status": "connected",
                    "tenant_id": settings.AZURE_TENANT_ID,
                    "message": "Connected but could not retrieve organization info"
                }
                
        except Exception as e:
            logger.error(f"Azure AD connection test failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "message": "Failed to connect to Azure AD. Check your credentials."
            }


# Global instance
azure_auth_service = AzureAuthService()


def get_azure_auth_service() -> AzureAuthService:
    """Dependency injection for Azure auth service"""
    return azure_auth_service
