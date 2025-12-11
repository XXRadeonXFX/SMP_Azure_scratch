# 🚀 QUICK START - Azure Functions

## 5-Minute Setup

### 1. Install Azure Functions Core Tools
```bash
# macOS
brew tap azure/functions
brew install azure-functions-core-tools@4

# Windows
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

### 2. Setup Project
```bash
cd group-manager-functions
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Azure Credentials

Edit `local.settings.json`:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_TENANT_ID": "YOUR_TENANT_ID",
    "AZURE_CLIENT_ID": "YOUR_CLIENT_ID",
    "AZURE_CLIENT_SECRET": "YOUR_CLIENT_SECRET"
  }
}
```

### 4. Run
```bash
func start
```

### 5. Test
```bash
# Health check
curl http://localhost:7071/api/health

# Test Azure (use code from terminal output)
curl "http://localhost:7071/api/azure/test?code=YOUR_CODE"
```

---

## ✅ Success Criteria

You should see:
1. ✅ Functions start without errors
2. ✅ 5 functions listed in terminal
3. ✅ Health check returns 200 OK
4. ✅ Azure test shows "connected"

---

## 📦 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check (no auth) |
| GET | `/api/azure/test` | Test connection (requires key) |
| GET | `/api/groups/search` | List/search groups |
| GET | `/api/groups/{id}/members` | Get group members |
| POST | `/api/groups` | Create new group |

**Note:** PUT and DELETE removed for security

---

## 🐛 Common Issues

**"func: command not found"**
- Install Azure Functions Core Tools (step 1)

**"Python version mismatch"**
- Use Python 3.9, 3.10, or 3.11
- Check: `python --version`

**"Module not found"**
- Activate venv: `source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt`

**"Azure connection failed"**
- Check credentials in `local.settings.json`
- Verify they match your working .NET app

---

## 💡 Next Steps

Once working locally:
1. **Deploy to Azure** (see README.md)
2. **Choose plan:** Consumption ($0-10/mo) or Premium ($170/mo)
3. **Monitor cold starts** if using Consumption

---

## ⚠️ Important Decision

**Cold Starts on Consumption Plan:**
- First request after 20 min idle = 3-5 sec delay
- **If this is acceptable:** Use Consumption (cheap!)
- **If you need instant response:** Use Premium Plan

**Test it first before deploying!**

Ready to deploy? See full deployment guide in README.md 🚀
