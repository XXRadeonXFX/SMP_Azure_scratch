"""
Azure Graph API Service
Handles all MS Graph API operations for group management
"""
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.group import Group
from msgraph.generated.models.reference_create import ReferenceCreate
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class AzureGraphService:
    """Service for interacting with MS Graph API"""
    
    def __init__(self, settings):
        self.settings = settings
        self._credential: Optional[ClientSecretCredential] = None
        self._graph_client: Optional[GraphServiceClient] = None
    
    def _get_credential(self) -> ClientSecretCredential:
        """Get or create Azure AD credential"""
        if not self._credential:
            logger.info("Creating Azure AD credential")
            self._credential = ClientSecretCredential(
                tenant_id=self.settings.AZURE_TENANT_ID,
                client_id=self.settings.AZURE_CLIENT_ID,
                client_secret=self.settings.AZURE_CLIENT_SECRET
            )
        return self._credential
    
    def _get_graph_client(self) -> GraphServiceClient:
        """Get or create MS Graph API client"""
        if not self._graph_client:
            logger.info("Creating MS Graph API client")
            credential = self._get_credential()
            scopes = ["https://graph.microsoft.com/.default"]
            self._graph_client = GraphServiceClient(
                credentials=credential,
                scopes=scopes
            )
        return self._graph_client
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test Azure AD connection"""
        try:
            logger.info("Testing Azure AD connection")
            client = self._get_graph_client()
            
            # Try to get organization info - MUST await the async call
            org_result = await client.organization.get()
            
            if org_result and org_result.value and len(org_result.value) > 0:
                org_info = org_result.value[0]
                return {
                    "status": "connected",
                    "tenant_id": self.settings.AZURE_TENANT_ID,
                    "organization": org_info.display_name if org_info.display_name else "Unknown",
                    "message": "Successfully connected to Azure AD and MS Graph API"
                }
            else:
                return {
                    "status": "connected",
                    "tenant_id": self.settings.AZURE_TENANT_ID,
                    "message": "Connected but could not retrieve organization info"
                }
                
        except Exception as e:
            logger.error(f"Azure AD connection test failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "message": "Failed to connect to Azure AD"
            }
    
    async def search_groups(self, search_term: str = "", top: int = 100) -> List[Dict[str, Any]]:
        """
        Search Azure AD groups
        
        Args:
            search_term: Optional filter by display name
            top: Maximum number of results (default 100)
        
        Returns:
            List of groups with id, displayName, description
        """
        try:
            logger.info(f"Searching groups with term: '{search_term}', top: {top}")
            client = self._get_graph_client()
            
            # Build query configuration
            from msgraph.generated.groups.groups_request_builder import GroupsRequestBuilder
            
            if search_term:
                # Filter by display name containing search term
                filter_query = f"startswith(displayName, '{search_term}')"
                
                query_params = GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
                    filter=filter_query,
                    top=top,
                    select=['id', 'displayName', 'description', 'mailEnabled', 'securityEnabled']
                )
                request_config = GroupsRequestBuilder.GroupsRequestBuilderGetRequestConfiguration(
                    query_parameters=query_params
                )
                result = await client.groups.get(request_configuration=request_config)
            else:
                # Get all groups (up to top limit)
                query_params = GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
                    top=top,
                    select=['id', 'displayName', 'description', 'mailEnabled', 'securityEnabled']
                )
                request_config = GroupsRequestBuilder.GroupsRequestBuilderGetRequestConfiguration(
                    query_parameters=query_params
                )
                result = await client.groups.get(request_configuration=request_config)
            
            groups = []
            if result and result.value:
                for group in result.value:
                    groups.append({
                        "id": group.id,
                        "displayName": group.display_name,
                        "description": group.description if group.description else "",
                        "mailEnabled": group.mail_enabled,
                        "securityEnabled": group.security_enabled
                    })
            
            logger.info(f"Found {len(groups)} groups")
            return groups
            
        except Exception as e:
            logger.error(f"Search groups failed: {str(e)}")
            raise Exception(f"Failed to search groups: {str(e)}")
    
    async def get_group_members(self, group_id: str) -> List[Dict[str, Any]]:
        """
        Get members of a specific group
        
        Args:
            group_id: Azure AD group GUID
        
        Returns:
            List of members with id, displayName, userPrincipalName
        """
        try:
            logger.info(f"Getting members for group: {group_id}")
            client = self._get_graph_client()
            
            # Get group members - MUST await the async call
            result = await client.groups.by_group_id(group_id).members.get()
            
            members = []
            if result and result.value:
                for member in result.value:
                    member_info = {
                        "id": member.id,
                        "displayName": getattr(member, 'display_name', 'N/A'),
                        "type": member.odata_type.split('.')[-1] if member.odata_type else "Unknown"
                    }
                    
                    # Add user-specific fields if it's a user
                    if hasattr(member, 'user_principal_name'):
                        member_info["userPrincipalName"] = member.user_principal_name
                    
                    members.append(member_info)
            
            logger.info(f"Found {len(members)} members in group {group_id}")
            return members
            
        except Exception as e:
            logger.error(f"Get group members failed: {str(e)}")
            raise Exception(f"Failed to get group members: {str(e)}")
    
    async def create_group(self, name: str, description: str, group_type: str) -> Dict[str, Any]:
        """
        Create a new Azure AD group
        
        Args:
            name: Group display name (must start with AAD.TA.)
            description: Group description
            group_type: 'Security' or 'Microsoft365'
        
        Returns:
            Created group information
        """
        try:
            logger.info(f"Creating group: {name}, type: {group_type}")
            client = self._get_graph_client()
            
            # Check if group already exists - MUST await the async call
            from msgraph.generated.groups.groups_request_builder import GroupsRequestBuilder
            
            filter_query = f"displayName eq '{name}'"
            query_params = GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
                filter=filter_query
            )
            request_config = GroupsRequestBuilder.GroupsRequestBuilderGetRequestConfiguration(
                query_parameters=query_params
            )
            existing = await client.groups.get(request_configuration=request_config)
            
            if existing and existing.value and len(existing.value) > 0:
                raise ValueError(f"Group '{name}' already exists")
            
            # Create new group object
            new_group = Group()
            new_group.display_name = name
            new_group.description = description
            new_group.mail_nickname = name.replace('.', '-').replace(' ', '-')
            
            if group_type == "Security":
                new_group.security_enabled = True
                new_group.mail_enabled = False
            else:  # Microsoft365
                new_group.security_enabled = False
                new_group.mail_enabled = True
                new_group.group_types = ["Unified"]
                new_group.visibility = "Public"
            
            # Create the group - MUST await the async call
            created_group = await client.groups.post(new_group)
            
            logger.info(f"Group created successfully: {created_group.id}")
            
            return {
                "id": created_group.id,
                "displayName": created_group.display_name,
                "description": created_group.description,
                "mailEnabled": created_group.mail_enabled,
                "securityEnabled": created_group.security_enabled
            }
            
        except ValueError as e:
            # Re-raise validation errors
            raise e
        except Exception as e:
            logger.error(f"Create group failed: {str(e)}")
            raise Exception(f"Failed to create group: {str(e)}")