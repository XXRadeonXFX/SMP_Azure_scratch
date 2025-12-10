# Group Manager Service - Python Port

## Sprint 1, Step 1: Foundation Setup ✅

This is the basic FastAPI setup with health check endpoints.

---

## 📁 Project Structure

```
group-manager-python/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration settings
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           └── health.py       # Health check endpoints
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### Option 1: Local Python (Recommended for Development)

1. **Install Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Create virtual environment**
   ```bash
   cd group-manager-python
   python -m venv venv
   
   # Activate (Linux/Mac)
   source venv/bin/activate
   
   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults work for Step 1)
   ```

5. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload --port 8080
   ```

6. **Test it!**
   - Open browser: http://localhost:8080
   - Health check: http://localhost:8080/hc
   - Liveness: http://localhost:8080/liveness
   - API docs: http://localhost:8080/docs

---

### Option 2: Docker

1. **Build the image**
   ```bash
   cd group-manager-python
   docker build -t group-manager-python:step1 .
   ```

2. **Run the container**
   ```bash
   docker run -p 8080:8080 group-manager-python:step1
   ```

3. **Test it!**
   - Health check: http://localhost:8080/hc
   - Liveness: http://localhost:8080/liveness

---

## 🧪 Testing Step 1

### Test 1: Root Endpoint
```bash
curl http://localhost:8080/
```

**Expected response:**
```json
{
  "service": "Group Manager Service",
  "version": "1.0.0",
  "status": "running"
}
```

### Test 2: Health Check
```bash
curl http://localhost:8080/hc
```

**Expected response:**
```json
{
  "status": "Healthy",
  "timestamp": "2024-12-09T...",
  "service": "group-manager",
  "checks": {
    "self": "Healthy"
  }
}
```

### Test 3: Liveness Check
```bash
curl http://localhost:8080/liveness
```

**Expected response:**
```json
{
  "status": "Healthy"
}
```

### Test 4: API Documentation
Open in browser: http://localhost:8080/docs

You should see:
- Interactive Swagger UI
- List of available endpoints
- Try out functionality

---

## ✅ Step 1 Checklist

- [x] FastAPI application setup
- [x] Configuration management (environment variables)
- [x] Health check endpoints (/hc, /liveness)
- [x] CORS middleware configured
- [x] Logging configured
- [x] Docker containerization
- [x] API documentation (auto-generated)

---

## 🎯 What's Next?

**Step 2:** Azure AD Authentication + MS Graph API Setup
- Add Azure authentication
- Connect to MS Graph API
- Test connection to Azure AD

---

## 📝 Notes

- Port 8080 matches .NET service internal port
- Health check endpoints match .NET pattern
- CORS configured for React frontend (localhost:3000)
- Non-root user in Docker for security
- Auto-reload enabled in development mode

---

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Find process using port 8080
lsof -i :8080  # Mac/Linux
netstat -ano | findstr :8080  # Windows

# Kill the process or use different port
python -m uvicorn app.main:app --reload --port 8081
```

**Import errors?**
```bash
# Make sure you're in the project root and venv is activated
cd group-manager-python
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Docker build fails?**
```bash
# Clean up and rebuild
docker system prune -a
docker build --no-cache -t group-manager-python:step1 .
```

---

## 📞 Ready for Step 2?

Once all tests pass, confirm with me and we'll move to:
- **Step 2:** Azure AD + MS Graph Integration 🔐
