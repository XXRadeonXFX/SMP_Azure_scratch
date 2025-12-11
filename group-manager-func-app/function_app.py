"""
Azure Functions App - Group Manager
GET and POST endpoints only (security restricted)
"""
import azure.functions as func
import logging
import json
from typing import Optional

# Import our services
from services.azure_graph_service import AzureGraphService
from services.config import get_settings

# Initialize Function App
app = func.FunctionApp()

# Initialize services
settings = get_settings()
graph_service = AzureGraphService(settings)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.function_name(name="HealthCheck")
@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    logger.info('Health check requested')
    
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "service": "group-manager-functions",
            "version": "1.0.0"
        }),
        mimetype="application/json",
        status_code=200
    )


@app.function_name(name="TestAzureConnection")
@app.route(route="azure/test", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
async def test_azure_connection(req: func.HttpRequest) -> func.HttpResponse:
    """Test Azure AD connection"""
    logger.info('Azure connection test requested')
    
    try:
        result = await graph_service.test_connection()
        
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200 if result.get("status") == "connected" else 500
        )
    except Exception as e:
        logger.error(f"Azure connection test failed: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "status": "failed",
                "error": str(e)
            }),
            mimetype="application/json",
            status_code=500
        )


@app.function_name(name="SearchGroups")
@app.route(route="groups/search", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
async def search_groups(req: func.HttpRequest) -> func.HttpResponse:
    """
    Search/List Azure AD groups
    Query params:
    - search: Optional search term (filters by display name)
    - top: Optional limit (default 100)
    """
    logger.info('Search groups requested')
    
    try:
        # Get query parameters
        search_term = req.params.get('search', '')
        top = int(req.params.get('top', 100))
        
        # Search groups using Graph API
        groups = await graph_service.search_groups(search_term, top)
        
        return func.HttpResponse(
            json.dumps({
                "groups": groups,
                "count": len(groups)
            }),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Search groups failed: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "message": "Failed to search groups"
            }),
            mimetype="application/json",
            status_code=500
        )


@app.function_name(name="GetGroupMembers")
@app.route(route="groups/{groupId}/members", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
async def get_group_members(req: func.HttpRequest) -> func.HttpResponse:
    """
    Get members of a specific Azure AD group
    Path param: groupId (GUID)
    """
    logger.info('Get group members requested')
    
    try:
        # Get group ID from route
        group_id = req.route_params.get('groupId')
        
        if not group_id:
            return func.HttpResponse(
                json.dumps({"error": "Group ID is required"}),
                mimetype="application/json",
                status_code=400
            )
        
        # Get group members from Graph API
        members = await graph_service.get_group_members(group_id)
        
        return func.HttpResponse(
            json.dumps({
                "groupId": group_id,
                "members": members,
                "count": len(members)
            }),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logger.error(f"Get group members failed: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "message": "Failed to get group members"
            }),
            mimetype="application/json",
            status_code=500
        )


@app.function_name(name="CreateGroup")
@app.route(route="groups", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
async def create_group(req: func.HttpRequest) -> func.HttpResponse:
    """
    Create a new Azure AD group
    Request body:
    {
        "name": "AAD.TA.DM.DEVOPS.ENGINEER",
        "description": "DevOps Engineers Group",
        "type": "Security" or "Microsoft365"
    }
    """
    logger.info('Create group requested')
    
    try:
        # Parse request body
        req_body = req.get_json()
        
        # Validate required fields
        name = req_body.get('name')
        description = req_body.get('description')
        group_type = req_body.get('type', 'Security')
        
        if not name:
            return func.HttpResponse(
                json.dumps({
                    "error": "Group name is required",
                    "propertyName": "name"
                }),
                mimetype="application/json",
                status_code=400
            )
        
        if not description:
            return func.HttpResponse(
                json.dumps({
                    "error": "Group description is required",
                    "propertyName": "description"
                }),
                mimetype="application/json",
                status_code=400
            )
        
        # Validate group name format (must start with AAD.TA.)
        if not name.startswith("AAD.TA."):
            return func.HttpResponse(
                json.dumps({
                    "error": "Group name must start with 'AAD.TA.' (case sensitive)",
                    "propertyName": "name"
                }),
                mimetype="application/json",
                status_code=400
            )
        
        # Validate group type
        if group_type not in ["Security", "Microsoft365"]:
            return func.HttpResponse(
                json.dumps({
                    "error": "Group type must be 'Security' or 'Microsoft365'",
                    "propertyName": "type"
                }),
                mimetype="application/json",
                status_code=400
            )
        
        # Create group using Graph API
        created_group = await graph_service.create_group(name, description, group_type)
        
        return func.HttpResponse(
            json.dumps({
                "message": "Group created successfully",
                "group": created_group
            }),
            mimetype="application/json",
            status_code=201
        )
        
    except ValueError as e:
        # Validation errors
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=400
        )
    except Exception as e:
        logger.error(f"Create group failed: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "message": "Failed to create group"
            }),
            mimetype="application/json",
            status_code=500
        )
@app.function_name(name="AddGroupMember")
@app.route(route="groups/{groupId}/members", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
async def add_group_member(req: func.HttpRequest) -> func.HttpResponse:
    """Add a member to a group"""
    logger.info('Add group member requested')
    
    try:
        group_id = req.route_params.get('groupId')
        req_body = req.get_json()
        user_id = req_body.get('userId')
        
        if not group_id or not user_id:
            return func.HttpResponse(
                json.dumps({"error": "groupId and userId are required"}),
                mimetype="application/json",
                status_code=400
            )
        
        result = await graph_service.add_group_member(group_id, user_id)
        
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=201
        )
        
    except Exception as e:
        logger.error(f"Add member failed: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )