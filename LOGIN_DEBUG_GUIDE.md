# Login Debug Guide

## 🔍 **Issue Description**
Users are getting "Invalid credentials" error even when entering valid credentials.

## 🛠️ **Debugging Steps Implemented**

### **1. Enhanced Login Logging**
Added detailed logging to `validate_login()` function in `Atomwalk_sdk_interface/ui/login.py`:

- ✅ **Request Details**: Shows username, API URL, and request format
- ✅ **Response Details**: Shows status code, headers, and response text
- ✅ **Error Handling**: Specific error messages for different failure types
- ✅ **Dual Format Testing**: Tries both JSON and form data formats

### **2. Enhanced Login Flow Logging**
Added logging to `check_login()` method:

- ✅ **Input Validation**: Checks for empty username/password
- ✅ **Token Processing**: Shows token validation results
- ✅ **Success/Failure Paths**: Clear indication of which path is taken

### **3. Standalone API Test Tool**
Created `test_login_api.py` for direct API testing:

- ✅ **Direct API Testing**: Tests API without UI interference
- ✅ **Dual Format Testing**: Tests both JSON and form data
- ✅ **Detailed Output**: Shows all request/response details

## 🔧 **How to Debug**

### **Step 1: Run the Application with Debug Logging**
```bash
python run.py
```

**Look for these log messages:**
```
🔍 Login attempt initiated
👤 Username: [your_username]
🔒 Password length: [length] characters
🔐 Attempting login for username: [username]
🌐 API URL: https://crm.atomwalk.com/rest-auth/login/
📤 Trying JSON format: {'username': '...', 'password': '...'}
📥 JSON Response status code: [status]
📥 JSON Response text: [response]
```

### **Step 2: Run Standalone API Test**
```bash
python test_login_api.py
```

**This will:**
- Test API connectivity
- Try JSON format login
- Try form data format login
- Show detailed response information

### **Step 3: Check Common Issues**

#### **A. Network Connectivity**
- **Look for**: `Connection error` or `Timeout error`
- **Solution**: Check internet connection and firewall settings

#### **B. API Endpoint Issues**
- **Look for**: `404 Not Found` or `500 Internal Server Error`
- **Solution**: Verify API endpoint is correct and server is running

#### **C. Authentication Format**
- **Look for**: Different responses between JSON and form data
- **Solution**: Use the format that works (JSON vs form data)

#### **D. Response Format Issues**
- **Look for**: `No 'key' field in response`
- **Solution**: Check if API response format has changed

#### **E. Credential Issues**
- **Look for**: `401 Unauthorized` or specific error messages
- **Solution**: Verify username/password are correct

## 📊 **Expected vs Actual Behavior**

### **Expected Successful Login:**
```
🔍 Login attempt initiated
👤 Username: valid_user
🔒 Password length: 8 characters
🔐 Attempting login for username: valid_user
🌐 API URL: https://crm.atomwalk.com/rest-auth/login/
📤 Trying JSON format: {'username': 'valid_user', 'password': '********'}
📥 JSON Response status code: 200
✅ Login successful with JSON! Response JSON: {"key": "abc123..."}
🔑 Token received: abc123...
✅ Valid token received, proceeding with login
🎉 Login successful, calling on_login_success
```

### **Common Failure Patterns:**

#### **1. Network Issue:**
```
🌐 Connection error: [error_details]
🔄 No internet connection, allowing offline mode
```

#### **2. API Format Issue:**
```
📥 JSON Response status code: 400
📥 JSON Response text: {"error": "Invalid format"}
🔄 JSON failed, trying form data format...
📥 Form Data Response status code: 200
✅ Login successful with form data!
```

#### **3. Authentication Issue:**
```
📥 JSON Response status code: 401
📥 JSON Response text: {"error": "Invalid credentials"}
❌ Both JSON and form data login failed
```

## 🎯 **Next Steps**

1. **Run the application** and attempt login with valid credentials
2. **Check the console output** for detailed logging messages
3. **Run the standalone test** to isolate API issues
4. **Identify the specific failure point** from the logs
5. **Apply the appropriate fix** based on the error type

## 🔧 **Quick Fixes**

### **If JSON format fails but form data works:**
Update `validate_login()` to use form data by default:
```python
response = requests.post(CLOUD_LOGIN_API, data=login_data)
```

### **If API endpoint has changed:**
Update `CLOUD_LOGIN_API` in `login.py`:
```python
CLOUD_LOGIN_API = "https://new-api-endpoint.com/login/"
```

### **If response format has changed:**
Update the token extraction logic:
```python
# Instead of response_json.get("key")
token = response_json.get("token")  # or whatever the new field name is
```

## 📞 **Support**

If the issue persists after following these debugging steps, please provide:
1. The complete console output from the login attempt
2. The output from `test_login_api.py`
3. The specific error messages you're seeing 