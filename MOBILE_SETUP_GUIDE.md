# Golf Analytics Mobile Dashboard Setup

**Access your 4 validated betting signals from your Android phone**

---

## What You Get

✓ Mobile-optimized dashboard
✓ All 4 signals with edges & confidence levels
✓ API endpoints for data
✓ Zero installation needed on phone

---

## Step 1: Start the Server (On Your PC)

### Option A: Command Line (Recommended)
```bash
cd D:\Projects\luckify-me
python mobile_server.py
```

You should see:
```
GOLF ANALYTICS - MOBILE DASHBOARD SERVER
Starting server on port 8000...
Access from Android phone:
  1. Find your PC's local IP (run 'ipconfig' on Windows)
  2. Open browser on phone: http://YOUR_PC_IP:8000
```

### Option B: Manual (Windows)
1. Open Command Prompt
2. Copy-paste:
```
cd D:\Projects\luckify-me && python mobile_server.py
```
3. Press Enter

---

## Step 2: Find Your PC's Local IP

Open Command Prompt on Windows and run:
```
ipconfig
```

Look for **IPv4 Address** under your network adapter. Usually looks like:
- `192.168.1.100`
- `192.168.0.50`
- `10.0.0.5`

---

## Step 3: Access From Android Phone

1. **Connect to same WiFi** as your PC
2. **Open browser** (Chrome, Firefox, etc.)
3. **Type in address bar:**
```
http://YOUR_PC_IP:8000
```

Example:
```
http://192.168.1.100:8000
```

4. **Press Enter** — Dashboard loads

---

## What You'll See

### Dashboard Home
- **4 Validated Signals** with:
  - Edge % (profit prediction)
  - Sample size (confidence)
  - Ratio (signal strength)
  - Bet size recommendation
  - Confidence level

- **Signals to Avoid** (negative edges)

- **Next Steps** (implementation tasks)

---

## API Endpoints (For Apps)

If building a custom mobile app:

### Get All Signals
```
GET http://YOUR_PC_IP:8000/api/signals

Response:
{
  "transfer_rate": 43.1,
  "signals": [
    {
      "rank": 1,
      "name": "Calm x Mixed x Yellow x Earth",
      "edge": 15.5,
      "sample": 44,
      "ratio": 2.81,
      "confidence": "HIGH",
      "bet": "LARGE"
    },
    ...
  ]
}
```

### Get Status
```
GET http://YOUR_PC_IP:8000/api/status

Response:
{
  "model": "4D Element",
  "transfer_rate": 43.1,
  "signals_validated": 4,
  "last_updated": "2026-03-28",
  "status": "Ready for betting implementation"
}
```

---

## Troubleshooting

### "Connection refused" or "Can't reach server"
- [ ] Server running on PC? (check Command Prompt)
- [ ] Correct IP address? (run `ipconfig` again)
- [ ] Same WiFi network? (phone & PC connected to same router)
- [ ] Firewall blocking? (allow Python through Windows Firewall)

### "Port 8000 already in use"
Edit `mobile_server.py`, change `PORT = 8000` to `PORT = 8001` or higher

### Page loads but looks strange
- [ ] Try refreshing browser (swipe down)
- [ ] Try different browser (Chrome, Firefox)
- [ ] Check internet connection

---

## Using the Dashboard

### View Signals
- Scroll through all 4 validated signals
- Each shows edge %, sample size, and confidence
- Rank 1 = highest edge, Rank 4 = most stable (largest sample)

### Understand the Metrics
- **Edge %:** Predicted profit over baseline
- **Sample (N):** Number of test rounds
- **Ratio:** Combo good/bad vs population
- **Confidence:** HIGH = strong signal, MEDIUM = moderate

### Next Steps Section
Follow the 4 steps to implement betting rules

---

## Keep Server Running

Server must stay running while using phone dashboard:
- [ ] Don't close Command Prompt window
- [ ] Don't turn off PC
- [ ] If closed, restart: `python mobile_server.py`

---

## Advanced: Run at Startup

To auto-start server when PC boots (Windows):

1. Open Notepad
2. Paste:
```batch
@echo off
cd D:\Projects\luckify-me
python mobile_server.py
pause
```
3. Save as `start_dashboard.bat` in D:\Projects\luckify-me
4. Right-click → "Send to" → Desktop (create shortcut)
5. Run shortcut anytime to start server

---

## Security Note

Server is local network only (not internet-accessible). Safe to use on home WiFi. Do NOT expose to public internet (no authentication).

---

## Support

If having issues:
1. Check Command Prompt for error messages
2. Verify IP address is correct
3. Try restarting server
4. Restart phone browser app

File locations:
- Dashboard: `D:\Projects\luckify-me\dashboard.html`
- Server: `D:\Projects\luckify-me\mobile_server.py`
- Full report: `D:\Projects\luckify-me\FINAL_ANALYSIS_REPORT.md`

---

**Status:** Ready to use. Server can handle multiple phone connections simultaneously.
