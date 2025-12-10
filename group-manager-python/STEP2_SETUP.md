# 🔐 Step 2: Azure AD + MS Graph Setup

## What We Added:
✅ Azure AD authentication service  
✅ MS Graph API client  
✅ Connection test endpoint  
✅ Credential validation  

---

## 📋 Prerequisites

You need Azure AD credentials. You can either:
- **Option A:** Use your existing .NET app credentials (from `.env` file)
- **Option B:** Create new Azure AD App Registration

---

## 🔑 Getting Azure Credentials

### Option A: Use Existing Credentials (Easiest)

Your .NET app already has these credentials in the `.env` file:

```bash
# From your existing .env file
AZURE_TENANT_ID=...
AZURE_CLIENT_ID=...  (AzureAd:Admin:ClientId in your .NET config)
AZURE_CLIENT_SECRET=...  (AzureAd:Admin:ClientSecret in your .NET config)
```

Copy these to your Python `.env` file!

### Option B: Create New App Registration

1. **Go to Azure Portal** → Azure Active Directory → App Registrations
2. **Click "New registration"**
   - Name: `GroupManager-Python-Dev`
   - Supported account types: "Single tenant"
   - Click "Register"

3. **Copy Application (client) ID**
   - This is your `AZURE_CLIENT_ID`

4. **Copy Directory (tenant) ID**
   - This is your `AZURE_TENANT_ID`

5. **Create Client Secret**
   - Go to "Certificates & secrets"
   - Click "New client secret"
   - Description: `Python Service Secret`
   - Expiry: 6 months (or your preference)
   - Click "Add"
   - **Copy the VALUE immediately** (you can't see it again!)
   - This is your `AZURE_CLIENT_SECRET`

6. **Grant API Permissions**
   - Go to "API permissions"
   - Click "Add a permission"
   - Select "Microsoft Graph"
   - Select "Application permissions"
   - Add these permissions:
     - `Group.ReadWrite.All`
     - `Directory.ReadWrite.All`
     - `GroupMember.ReadWrite.All`
   - Click "Grant admin consent" (requires admin)

---

## ⚙️ Configuration

1. **Create `.env` file** (if not exists)
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials**
   ```bash
   # Application Configuration
   ENVIRONMENT=development
   PORT=8080
   
   # CORS Origins
   CORS_ORIGINS=http://localhost:3000;http://localhost:7001
   
   # Azure AD Configuration
   AZURE_TENANT_ID=your-tenant-id-here
   AZURE_CLIENT_ID=your-client-id-here
   AZURE_CLIENT_SECRET=your-client-secret-here
   
   # Logging
   LOG_LEVEL=INFO
   ```

3. **Restart the application**
   ```bash
   # Stop the current server (Ctrl+C)
   # Start it again
   python -m uvicorn app.main:app --reload --port 8080
   ```

---

## 🧪 Testing Step 2

### Test 1: Verify Azure Configuration

Check if credentials are loaded:
```bash
curl http://localhost:8080/
```

The app should start without errors.

### Test 2: Test Azure Connection

**Important:** This will actually connect to Azure AD!

```bash
curl http://localhost:8080/azure/test
```

**Expected Success Response:**
```json
{
  "status": "connected",
  "tenant_id": "your-tenant-id",
  "organization": "Your Organization Name",
  "message": "Successfully connected to Azure AD and MS Graph API"
}
```

**If Credentials Are Wrong:**
```json
{
  "status": "failed",
  "error": "...",
  "message": "Failed to connect to Azure AD. Check your credentials."
}
```

### Test 3: Check API Documentation

Open http://localhost:8080/docs

You should see:
- ✅ Health endpoints
- ✅ Azure test endpoint (NEW!)

---

## ⚠️ Troubleshooting

### Error: "Failed to connect to Azure AD"

**Check these:**

1. **Credentials are correct**
   ```bash
   # Print your .env file (remove before committing!)
   cat .env
   ```

2. **No extra spaces or quotes**
   ```bash
   # WRONG:
   AZURE_TENANT_ID="abc-123"
   AZURE_TENANT_ID= abc-123
   
   # CORRECT:
   AZURE_TENANT_ID=abc-123
   ```

3. **API Permissions granted**
   - Go to Azure Portal → Your App → API permissions
   - All permissions should show "Granted for [Your Org]"
   - If not, click "Grant admin consent"

4. **Client secret hasn't expired**
   - Go to Azure Portal → Your App → Certificates & secrets
   - Check if secret is still valid
   - Create new one if expired

5. **Using correct credentials**
   - Make sure you're using `AzureAd:Admin:ClientId` and `AzureAd:Admin:ClientSecret`
   - NOT the web app credentials

### Error: "Insufficient privileges"

You need admin consent for the API permissions. Ask your Azure AD admin to:
1. Go to your App Registration
2. Go to "API permissions"
3. Click "Grant admin consent for [Your Organization]"

### Error: "Module not found: msgraph"

```bash
pip install -r requirements.txt
```

---

## ✅ Step 2 Checklist

- [ ] Azure credentials obtained
- [ ] `.env` file configured
- [ ] Application starts without errors
- [ ] `/azure/test` endpoint returns "connected"
- [ ] Organization name displayed correctly

---

## 🎯 When Ready for Step 3

Once `/azure/test` returns **"status": "connected"**, tell me:

**"Step 2 works! Ready for Step 3"**

And I'll add the GET endpoints to list groups and members! 🚀

---

## 📝 Notes

- **Don't commit `.env` file!** (already in `.gitignore`)
- Same credentials work for both .NET and Python services
- MS Graph SDK handles token refresh automatically
- Connection test calls Azure AD once per app startup
