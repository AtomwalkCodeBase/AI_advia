# ADVIA Proxy Listener Flow Documentation

## Corrected Flow Sequence

The proxy listener now follows the proper application flow:

### 1. Application Startup
```
🚀 Application started
🔄 Syncing proxy configuration...
```

### 2. Login Process
```
✅ Login successful! Showing SDK selection...
```

### 3. SDK Selection
```
✅ SDK selected: ADVIA
🔄 Starting selected SDK...
```

### 4. SDK Status Handling
The system now properly handles different SDK statuses:

#### ✅ SDK Success (True)
```
✅ ADVIA SDK started successfully. System is ready.
📊 Loading ADVIA dashboard...
✅ ADVIA dashboard loaded successfully.
```

#### ⚠️ SDK Issues (False)
```
⚠️ ADVIA SDK encountered issues during processing.
🔄 ADVIA SDK had issues, activating proxy listener as backup...
🛡️ Activating ADVIA Proxy Listener (Backup Mode)...
🕐 ADVIA Proxy Listener is now active, waiting for manual file drop.
📂 ADVIA Proxy is in standby for manual file drop or backup modes.
```

#### ℹ️ No Files (None)
```
ℹ️ ADVIA SDK found no files to process.
🔄 ADVIA SDK found no files, activating proxy listener for manual file drop...
🛡️ Activating ADVIA Proxy Listener (Backup Mode)...
🕐 ADVIA Proxy Listener is now active, waiting for manual file drop.
📂 ADVIA Proxy is in standby for manual file drop or backup modes.
```

#### ❌ SDK Failure
```
❌ ADVIA SDK failed to start.
🔄 ADVIA SDK failed, activating proxy listener as backup...
🛡️ Activating ADVIA Proxy Listener (Backup Mode)...
🕐 ADVIA Proxy Listener is now active, waiting for manual file drop.
📂 ADVIA Proxy is in standby for manual file drop or backup modes.
```

## Key Changes Made

### 1. Fixed Automatic Startup Issue
- **Problem**: Proxy listener was starting automatically on module import
- **Solution**: Removed the automatic print statement and execution from `proxy_listener.py`
- **Result**: Proxy listener only starts when explicitly called via `activate_proxy()`

### 2. Improved Flow Logic
- **Enhanced**: Better status handling in `main_launcher.py`
- **Added**: Specific handling for different SDK return values (True, False, None)
- **Clarified**: Clear logging messages for each step of the process

### 3. Threading Support
- **Added**: Proxy listener now runs in background threads
- **Benefit**: Non-blocking operation that doesn't interfere with the main application

## Proxy Listener Activation Conditions

The ADVIA proxy listener is **ONLY** activated when:

1. **ADVIA SDK is selected** (not other SDKs)
2. **AND** one of these conditions is met:
   - SDK returns `False` (processing issues)
   - SDK returns `None` (no files to process)
   - SDK fails to start
   - SDK encounters an exception

## Other SDKs

For non-ADVIA SDKs (IOT, CUSTOM, TEST):
- No proxy listener is activated
- Only error messages are shown
- User must check configuration manually

## Files Modified

1. **`advia_proxy/proxy_listener.py`**
   - Removed automatic startup code
   - Added threading support
   - Improved `activate_proxy()` function

2. **`Atomwalk_sdk_interface/main_launcher.py`**
   - Enhanced SDK status handling
   - Added detailed logging
   - Improved flow control logic

## Testing

The corrected flow has been tested and verified:
- ✅ Proxy listener no longer starts on import
- ✅ Only activates when ADVIA SDK fails
- ✅ Proper threading implementation
- ✅ Clear logging and status messages 