# Quick Commands to Access Signals

**One-command access to your golf signals**

---

## Windows: Double-Click Start

**File:** `start_remote.bat` (in project folder)

Just double-click it → Server starts
Access: `http://localhost:8000` on phone (same WiFi)

---

## PowerShell One-Liner

Open PowerShell, paste:

```powershell
cd D:\Projects\luckify-me; python mobile_server.py
```

Press Enter → Server starts

---

## Command Line (CMD)

Open Command Prompt, paste:

```cmd
cd D:\Projects\luckify-me && python mobile_server.py
```

Press Enter → Server starts

---

## Quick Access Shortcut (Windows)

1. Right-click Desktop
2. New → Shortcut
3. Paste:
```
C:\Windows\System32\cmd.exe /k "cd D:\Projects\luckify-me && python mobile_server.py"
```
4. Name it: `Golf Dashboard`
5. Click → Server starts

Now just double-click "Golf Dashboard" on desktop anytime.

---

## Public Access (Ngrok Tunnel)

Have ngrok installed? One command:

```bash
ngrok http 8000
```

Then start server in another window:
```bash
python mobile_server.py
```

Ngrok gives you public URL → share with phone

---

## Auto-Start on Boot

1. Press `Win + R`
2. Type: `shell:startup`
3. Copy `start_remote.bat` to that folder
4. Now server auto-starts when PC boots

---

## Check Server Status

Once running, go to:
- **Local:** `http://localhost:8000`
- **Same WiFi:** `http://192.168.1.100:8000` (your IP)
- **Remote:** Use ngrok URL

---

## Stop Server

Press `Ctrl + C` in the terminal window

---

## TL;DR

**Fastest:**
1. Find `start_remote.bat` in project folder
2. Double-click it
3. Done — server running

**Then on phone:**
1. Open browser
2. Type: `http://your-pc-ip:8000`
3. See all 4 signals

---

## Troubleshooting Commands

Check if Python installed:
```bash
python --version
```

Check if port 8000 available:
```bash
netstat -an | findstr :8000
```

Kill any process on port 8000:
```bash
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F
```

---

## Remember

**3 seconds to start server:**
1. `cd D:\Projects\luckify-me`
2. `python mobile_server.py`
3. Access from phone

That's it. Signals ready.
