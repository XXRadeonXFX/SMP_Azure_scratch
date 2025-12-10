"""
Azure connectivity test endpoints
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.services.azure_auth import AzureAuthService, get_azure_auth_service

router = APIRouter()


@router.get("/azure/test")
async def test_azure_connection(
    auth_service: AzureAuthService = Depends(get_azure_auth_service)
) -> Dict[str, Any]:
    """
    Test Azure AD and MS Graph API connectivity
    
    This endpoint verifies:
    - Azure AD authentication works
    - MS Graph API is accessible
    - Credentials are valid
    """
    result = await auth_service.test_connection()
    return result
