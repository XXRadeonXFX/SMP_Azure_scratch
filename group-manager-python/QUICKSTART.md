# 🚀 QUICK START - Step 1 Testing

## Fastest Way to Test (5 minutes)

### 1. Download & Setup
```bash
cd group-manager-python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run
```bash
python -m uvicorn app.main:app --reload --port 8080
```

### 3. Test in Browser
Open these URLs:
- http://localhost:8080 (Root)
- http://localhost:8080/hc (Health Check)
- http://localhost:8080/docs (API Docs)

### 4. Test with Curl
```bash
curl http://localhost:8080/hc
```

---

## ✅ Success Criteria

You should see:
1. ✅ Application starts without errors
2. ✅ Health check returns `{"status": "Healthy"}`
3. ✅ Swagger UI shows at /docs
4. ✅ No import or dependency errors

---

## ⚠️ Common Issues

**"Port 8080 in use"?**
- Your .NET service might be running
- Use different port: `--port 8081`

**"Module not found"?**
- Activate venv: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

---

## 🎯 When Ready

Once all tests pass, tell me:
**"Step 1 works! Ready for Step 2"**

And I'll add Azure AD authentication + MS Graph API integration! 🔐
