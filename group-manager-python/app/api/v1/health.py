"""
Health check endpoints
Matches .NET health check pattern: /hc and /liveness
"""
from fastapi import APIRouter, status
from datetime import datetime
from typing import Dict, Any

router = APIRouter()


@router.get("/hc", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Comprehensive health check endpoint
    Matches .NET endpoint: /hc
    """
    return {
        "status": "Healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "group-manager",
        "checks": {
            "self": "Healthy"
        }
    }


@router.get("/liveness", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict[str, str]:
    """
    Simple liveness check
    Matches .NET endpoint: /liveness
    """
    return {
        "status": "Healthy"
    }
