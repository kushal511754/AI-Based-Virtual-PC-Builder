# Server Crash Prevention - Quick Reference

## Start Server

### Fast Start
```bash
python run.py
```

### Production Start (Recommended)
```bash
python run_production.py
```

## What Was Fixed

**5 Critical Issues Resolved:**

1. **Waitress Configuration** - Added production-ready threading, timeouts, and memory limits
2. **JSON Parsing** - Safe handling of malformed/None requests in all routes
3. **Error Handlers** - Added global exception handler to prevent uncaught crashes
4. **Route Protection** - Try-catch blocks in all endpoints with proper logging
5. **Signal Handling** - Graceful shutdown with proper signal handling

## Files Modified

- `run.py` - ✓ Updated Waitress config
- `run_production.py` - ✓ NEW: Production runner
- `server/app.py` - ✓ Error handlers + safety configs
- `server/routes/builder.py` - ✓ Safe JSON parsing + error logging
- `server/routes/compatibility.py` - ✓ Error logging
- `requirements.txt` - ✓ Added waitress explicitly

## Verification

```bash
# Quick verification
python -c "from server.app import create_app; app = create_app(); print('SUCCESS')"

# Run stability tests
python test_server_stability.py
```

## If You See Errors

1. Check `server.log` for details
2. Restart: `python run_production.py`
3. Check network/port: `netstat -an | findstr :5000` (Windows)

## Server Features Now

- Automatic logging to `server.log`
- Handles up to 10 concurrent requests
- 16MB max request size
- 120-second request timeout
- Graceful shutdown (Ctrl+C)
- Global error recovery
- Safe JSON parsing in all endpoints

## No More Crashes!

The server is now production-ready with comprehensive crash prevention.
