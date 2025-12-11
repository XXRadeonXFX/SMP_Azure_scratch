## 🧪 **How to Test:**

### **Step 1: Restart Functions**
```bash
# Stop (Ctrl+C) and restart
func start
```

### **Step 2: Get Your User ID**
**From Azure Portal:**
1. Azure Active Directory → Users
2. Find yourself
3. Copy your **Object ID** (e.g., `12345678-abcd-1234-abcd-123456789abc`)

### **Step 3: Create a Test Group**
```bash
curl -X POST http://localhost:7071/api/groups \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AAD.TA.TEST.MEMBER.GROUP",
    "description": "Test Group for Member Operations",
    "type": "Security"
  }'
```

Copy the `group.id` from response!

### **Step 4: Add Yourself to the Group**
```bash
# Replace GROUP_ID and YOUR_USER_ID
curl -X POST http://localhost:7071/api/groups/GROUP_ID/members \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "YOUR_USER_ID"
  }'
```

### **Step 5: Verify Member Was Added**
```bash
curl http://localhost:7071/api/groups/GROUP_ID/members
```


---

