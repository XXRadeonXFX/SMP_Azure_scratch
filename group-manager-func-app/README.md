# Group Manager - Azure Functions Version

## 🎯 Security-Restricted Version
**GET and POST operations only** - PUT and DELETE removed for security

---

## 📋 Available Endpoints

### Health & Testing
- `GET /api/health` - Health check (anonymous)
- `GET /api/azure/test` - Test Azure connection (requires function key)

### Group Operations
- `GET /api/groups/search?search=xxx&top=100` - Search/List groups
- `GET /api/groups/{groupId}/members` - Get group members
- `POST /api/groups` - Create new group

**Security Note:** PUT (modify) and DELETE operations intentionally excluded

---

## 📁 Project Structure

```
group-manager-functions/
├── function_app.py              # Main Functions app with HTTP triggers
├── host.json                    # Functions host configuration
├── local.settings.json          # Local development settings
├── requirements.txt             # Python dependencies
├── services/
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   └── azure_graph_service.py  # MS Graph API integration
├── .gitignore
├── .funcignore
└── README.md
```

---

## 🚀 Local Development Setup

### Prerequisites
1. **Python 3.9-3.11** (Azure Functions requirement)
2. **Azure Functions Core Tools v4**
   ```bash
   # macOS
   brew tap azure/functions
   brew install azure-functions-core-tools@4
   
   # Windows
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```
3. **Azure Credentials** (from your .NET app or Azure Portal)

### Setup Steps

1. **Clone/Download the project**
   ```bash
   cd group-manager-functions
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Activate
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Azure credentials**
   
   Edit `local.settings.json`:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AZURE_TENANT_ID": "your-actual-tenant-id",
       "AZURE_CLIENT_ID": "your-actual-client-id",
       "AZURE_CLIENT_SECRET": "your-actual-client-secret"
     }
   }
   ```

5. **Run locally**
   ```bash
   func start
   ```

   You should see:
   ```
   Functions:
     CreateGroup: [POST] http://localhost:7071/api/groups
     GetGroupMembers: [GET] http://localhost:7071/api/groups/{groupId}/members
     HealthCheck: [GET] http://localhost:7071/api/health
     SearchGroups: [GET] http://localhost:7071/api/groups/search
     TestAzureConnection: [GET] http://localhost:7071/api/azure/test
   ```

---

## 🧪 Testing Locally

### Test 1: Health Check
```bash
curl http://localhost:7071/api/health
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "group-manager-functions",
  "version": "1.0.0"
}
```

### Test 2: Azure Connection (Requires Function Key)
```bash
# Get function key from terminal output (looks like: ?code=xxx)
curl "http://localhost:7071/api/azure/test?code=YOUR_FUNCTION_KEY"
```

**Expected:**
```json
{
  "status": "connected",
  "tenant_id": "...",
  "organization": "Your Org Name",
  "message": "Successfully connected to Azure AD and MS Graph API"
}
```

### Test 3: Search Groups
```bash
curl "http://localhost:7071/api/groups/search?search=AAD&code=YOUR_FUNCTION_KEY"
```

**Expected:**
```json
{
  "groups": [
    {
      "id": "...",
      "displayName": "AAD.TA.DM.DEVOPS.ENGINEER",
      "description": "...",
      "mailEnabled": false,
      "securityEnabled": true
    }
  ],
  "count": 1
}
```

### Test 4: Get Group Members
```bash
curl "http://localhost:7071/api/groups/{GROUP_ID}/members?code=YOUR_FUNCTION_KEY"
```

### Test 5: Create Group
```bash
curl -X POST "http://localhost:7071/api/groups?code=YOUR_FUNCTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AAD.TA.TEST.GROUP",
    "description": "Test Group",
    "type": "Security"
  }'
```

**Expected:**
```json
{
  "message": "Group created successfully",
  "group": {
    "id": "...",
    "displayName": "AAD.TA.TEST.GROUP",
    "description": "Test Group",
    "mailEnabled": false,
    "securityEnabled": true
  }
}
```

---

## ☁️ Deploy to Azure

### Option 1: Deploy via VS Code (Easiest)

1. **Install Azure Functions extension** in VS Code
2. **Open project folder** in VS Code
3. **Sign in to Azure** (Azure icon → Sign in)
4. **Deploy:**
   - Click Azure icon
   - Right-click your subscription
   - Click "Create Function App in Azure (Advanced)"
   - Follow prompts:
     - Name: `group-manager-func-dev`
     - Runtime: Python 3.11
     - Region: Same as your resources
     - Plan: **Consumption** (pay-per-use) or **Premium** (no cold starts)
5. **After creation, right-click the function app → Deploy**

### Option 2: Deploy via Azure CLI

```bash
# Login to Azure
az login

# Create Function App (Consumption Plan)
az functionapp create \
  --resource-group YOUR_RESOURCE_GROUP \
  --name group-manager-func-dev \
  --storage-account YOUR_STORAGE_ACCOUNT \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --os-type Linux

# Set Azure credentials as App Settings
az functionapp config appsettings set \
  --name group-manager-func-dev \
  --resource-group YOUR_RESOURCE_GROUP \
  --settings \
    AZURE_TENANT_ID="your-tenant-id" \
    AZURE_CLIENT_ID="your-client-id" \
    AZURE_CLIENT_SECRET="your-client-secret"

# Deploy
func azure functionapp publish group-manager-func-dev
```

### Get Function URLs After Deployment

```bash
# Get function URLs with keys
func azure functionapp list-functions group-manager-func-dev --show-keys
```

You'll get URLs like:
```
https://group-manager-func-dev.azurewebsites.net/api/groups?code=xxx
```

---

## 💰 Cost Comparison

### Consumption Plan (Recommended for start)
- **First 1M executions:** FREE
- **After that:** $0.20 per million executions
- **Memory:** $0.000016/GB-s
- **Typical monthly cost:** $0-10 for low traffic

**Cold starts:** 3-5 seconds if idle for 20 minutes

### Premium Plan (No cold starts)
- **EP1:** ~$170/month (always warm, 3.5GB RAM)
- **EP2:** ~$340/month (7GB RAM)
- **EP3:** ~$680/month (14GB RAM)

**Use Premium if:**
- Your frontend needs sub-second response
- High traffic (thousands of requests/day)
- Can't tolerate cold starts

---

## ⚠️ Important Notes

### Function Keys (Security)
- **Anonymous:** No key needed (only /health)
- **Function:** Requires function-specific key
- **Admin:** Master key (don't expose!)

**Get keys in Azure Portal:**
- Function App → Functions → Your Function → Function Keys

### Cold Starts (Consumption Plan)
- **What:** 3-5 second delay if function hasn't run for 20 min
- **Solution:** Use Premium Plan OR trigger function every 5 min with ping

### Timeout Limits
- **Consumption:** 5 minutes max
- **Premium:** 30 minutes max (configurable)

Your operations should complete in seconds, so this is fine.

---

## 🔧 Troubleshooting

### "Module not found" error
```bash
# Ensure you're in venv
source .venv/bin/activate

# Reinstall
pip install -r requirements.txt
```

### "Function host is not running"
```bash
# Check Python version
python --version  # Should be 3.9-3.11

# Check Azure Functions Core Tools
func --version  # Should be 4.x
```

### Azure connection fails
- Check credentials in `local.settings.json`
- Verify API permissions granted in Azure Portal
- Test with your .NET app first to confirm credentials work

### Deployment fails
```bash
# Clean and redeploy
rm -rf .python_packages
func azure functionapp publish YOUR_FUNCTION_APP_NAME --build remote
```

---

## 📊 Monitoring

### View Logs (Local)
Logs appear in terminal where you ran `func start`

### View Logs (Azure)
```bash
# Stream logs
func azure functionapp logstream group-manager-func-dev

# Or in Azure Portal
Function App → Log stream
```

### Application Insights (Recommended)
Enable in Azure Portal → Function App → Application Insights
- Track requests, failures, performance
- Set alerts for errors

---

## 🔄 Migration from FastAPI Container Apps

### What Changed:
| FastAPI (Container Apps) | Azure Functions |
|--------------------------|-----------------|
| `@app.get("/groups")` | `@app.route(route="groups", methods=["GET"])` |
| `uvicorn.run()` | `func.FunctionApp()` |
| Always running | Triggered execution |
| Single endpoint per route | Function per endpoint |

### API Compatibility:
**✅ URLs stay same:** `/api/groups/search`, `/api/groups/{id}/members`
**✅ Request/Response format unchanged**
**✅ Frontend needs no changes** (just update base URL)

---

## 🎯 Next Steps

1. **Test locally** with your Azure credentials
2. **Deploy to Consumption Plan** (free tier)
3. **Monitor performance and cold starts**
4. **Upgrade to Premium if needed**
5. **Add Application Insights for monitoring**

---

## 📞 Need Help?

- **Azure Functions Docs:** https://learn.microsoft.com/azure/azure-functions/
- **MS Graph SDK:** https://learn.microsoft.com/graph/sdks/sdks-overview
- **Check cold start impact on your use case first!**

Ready to deploy? 🚀
