**🔐 Zscaler Solutions for Corporate VDI/WSL:**

---

## 🎯 **Option 1: Contact IT (Best Solution)**

Ask your IT team to:

1. **Whitelist localhost/127.0.0.1** in Zscaler:
   - Add `localhost` to bypass list
   - Add `127.0.0.1` to bypass list
   - Whitelist ports `7071` (or all `7000-8000` for development)

2. **Disable Zscaler for local development** (if they allow)

---

## 🛠️ **Option 2: Bypass Proxy (Try This First)**

### **In WSL Terminal:**
```bash
# Set environment variables
export NO_PROXY="localhost,127.0.0.1"
export no_proxy="localhost,127.0.0.1"
export HTTP_PROXY=""
export HTTPS_PROXY=""
export http_proxy=""
export https_proxy=""

# Then start Functions
func start
```

### **Make it permanent:**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export NO_PROXY="localhost,127.0.0.1"' >> ~/.bashrc
echo 'export no_proxy="localhost,127.0.0.1"' >> ~/.bashrc
echo 'export HTTP_PROXY=""' >> ~/.bashrc
echo 'export HTTPS_PROXY=""' >> ~/.bashrc

source ~/.bashrc
```

---

## 🔧 **Option 3: Use WSL IP Instead of Localhost**

### **Get WSL IP:**
```bash
hostname -I | awk '{print $1}'
```

### **Bind Functions to WSL IP:**

**Edit `host.json`:**
```json
{
  "version": "2.0",
  "extensions": {
    "http": {
      "routePrefix": "api"
    }
  },
  "host": {
    "address": "0.0.0.0"
  }
}
```

**Start Functions:**
```bash
func start --host 0.0.0.0 --port 7071
```

**Access from Windows:**
```
http://172.x.x.x:7071/api/health
```

---

## 💡 **Option 4: Disable Zscaler Temporarily**

**Windows System Tray:**
1. Right-click Zscaler icon (usually in taskbar)
2. Select "Disable Zscaler for X minutes"
3. Choose duration (usually 15-60 mins)

*Note: This requires admin permissions or IT policy allowing it.*

---

## 🚀 **Option 5: Use Mac for Local Dev (Recommended)**

Since it already works on your Mac M1:

**Development Workflow:**
```bash
# On Mac (local development)
✅ Write code
✅ Test locally with func start
✅ Git push

# On VDI WSL (deployment only)
✅ Git pull
✅ Deploy to Azure (az functionapp deployment)
✅ Test in Azure
```

---

## 📝 **Option 6: Configure Zscaler Client**

**If you have Zscaler admin access:**

1. Open Zscaler Client
2. Go to **Settings**
3. Look for **Local Proxy Bypass** or **PAC File**
4. Add exceptions:
   ```
   localhost
   127.0.0.1
   *.local
   ```

---

## 🎯 **Recommended Approach:**

**For now (Quick Fix):**
```bash
# On Mac - do all local development
func start  # Works perfectly!

# Test everything on Mac first
```

**Long-term (Proper Fix):**
1. **Contact IT** - Request localhost bypass in Zscaler
2. Provide justification: "Need localhost access for Azure Functions local development"
3. Show them this is standard development practice

**Alternative (If IT says no):**
- Develop on Mac ✅
- Deploy to Azure from VDI
- Test in Azure environment

---

## ✅ **Quick Test to See What Works:**

```bash
# Test 1: Check if proxy is interfering
curl -v http://localhost:7071/api/health 2>&1 | grep -i proxy

# Test 2: Try with NO_PROXY
NO_PROXY="localhost,127.0.0.1" curl http://localhost:7071/api/health

# Test 3: Try 127.0.0.1 instead
curl http://127.0.0.1:7071/api/health

# Test 4: Check WSL IP
hostname -I
curl http://172.x.x.x:7071/api/health  # Use your actual IP
```

---

**Bottom line: Zscaler is blocking localhost traffic. Best solution = IT whitelists it OR use Mac for local dev!** 🔐