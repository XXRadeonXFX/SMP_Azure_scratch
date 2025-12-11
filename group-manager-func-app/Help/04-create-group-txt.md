**🎯 Let's create a test group and check its members!**

---

## **Step 1: Create a Test Group**

```bash
curl -X POST http://localhost:7071/api/groups \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AAD.TA.TEST.POC.GROUP",
    "description": "Test Group for Azure Functions POC",
    "type": "Security"
  }'
```

**Expected response:**
```json
{
  "message": "Group created successfully",
  "group": {
    "id": "12345678-abcd-1234-abcd-123456789abc",
    "displayName": "AAD.TA.TEST.POC.GROUP",
    "description": "Test Group for Azure Functions POC",
    "mailEnabled": false,
    "securityEnabled": true
  }
}
```

---

## **Step 2: Verify Group Was Created**

```bash
curl "http://localhost:7071/api/groups/search?search=AAD.TA.TEST"
```

You should now see your new group!

---

## **Step 3: Get Group Members**

```bash
# Use the actual group ID from Step 1 response
curl http://localhost:7071/api/groups/12345678-abcd-1234-abcd-123456789abc/members
```

**Expected response:**
```json
{
  "groupId": "12345678-abcd-1234-abcd-123456789abc",
  "members": [],
  "count": 0
}
```

Empty because we just created it!

---

## **⚠️ Adding Users - NOT Implemented (By Design)**

**Sprint 1 security restriction: GET/POST only, no PUT/DELETE/PATCH**

To test with members, you need to **manually add users via Azure Portal:**

1. **Azure Portal** → **Azure Active Directory** → **Groups**
2. Find your group: `AAD.TA.TEST.POC.GROUP`
3. Click **Members** → **Add members**
4. Add yourself or test users
5. Then test the GET members endpoint again!

---

## **🧪 Full Test Sequence:**

```bash
# 1. Create group
curl -X POST http://localhost:7071/api/groups \
  -H "Content-Type: application/json" \
  -d '{"name":"AAD.TA.TEST.POC.GROUP","description":"Test Group","type":"Security"}'

# 2. Search for it (copy the group ID from response)
curl "http://localhost:7071/api/groups/search?search=AAD.TA.TEST"

# 3. Get members (replace GROUP_ID)
curl http://localhost:7071/api/groups/GROUP_ID_HERE/members

# 4. Manually add users in Azure Portal

# 5. Check members again
curl http://localhost:7071/api/groups/GROUP_ID_HERE/members
```

