# Remote Triggers: Run Analysis & Get Signals From Anywhere

**A) Trigger analysis remotely**
**B) Access signals from anywhere**

---

## Installation

### Local (Your PC)

```bash
pip install flask
cd D:\Projects\luckify-me
python remote_api.py
```

Runs on: `http://localhost:5000`

### Remote (Cloud)

Deploy to Replit, Heroku, or Google Cloud:
- Upload `remote_api.py`
- Run: `python remote_api.py`
- Get public URL

---

## API Endpoints

### 1. Get 4 Validated Signals

**Command:**
```
GET /api/signals
```

**Example (from phone or anywhere):**
```
http://your-server:5000/api/signals
```

**Returns:**
```json
{
  "transfer_rate": 43.1,
  "signals": [
    {
      "rank": 1,
      "combo": "Calm x Mixed x Yellow x Earth",
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

---

### 2. Trigger Fresh Analysis (Remote)

**Command:**
```
GET /api/run-analysis?year_min=2025&year_max=2026
```

**Example:**
```
http://your-server:5000/api/run-analysis
```

**Optional parameters:**
- `year_min=2025` — Start year
- `year_max=2026` — End year

**Returns:**
```json
{
  "status": "running",
  "message": "Running analysis for 2025-2026",
  "timestamp": "2026-03-28T14:30:00"
}
```

---

### 3. Get Model Status

**Command:**
```
GET /api/status
```

**Example:**
```
http://your-server:5000/api/status
```

**Returns:**
```json
{
  "model": "4D Element",
  "transfer_rate": 43.1,
  "signals_validated": 4,
  "baseline_roi": 62.57,
  "status": "Ready for betting implementation"
}
```

---

### 4. Get Signals to Avoid

**Command:**
```
GET /api/avoid-signals
```

**Example:**
```
http://your-server:5000/api/avoid-signals
```

**Returns:**
```json
{
  "signals_to_avoid": [
    {
      "combo": "Moderate x Positioning x Purple x Metal",
      "edge": -8.9,
      "sample": 36
    },
    ...
  ]
}
```

---

### 5. Health Check

**Command:**
```
GET /api/health
```

**Returns:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-28T14:30:00"
}
```

---

## Usage Examples

### From Phone Browser

Open browser, type:
```
http://your-server:5000/api/signals
```

Shows all 4 signals as JSON

### From Command Line (curl)

```bash
curl http://your-server:5000/api/signals
curl http://your-server:5000/api/status
curl http://your-server:5000/api/run-analysis
```

### From Python Script

```python
import requests

# Get signals
response = requests.get("http://your-server:5000/api/signals")
signals = response.json()
print(signals)

# Trigger analysis
response = requests.get("http://your-server:5000/api/run-analysis?year_min=2025&year_max=2026")
print(response.json())
```

### From Mobile App

Call API endpoints from your Android app:
```javascript
fetch('http://your-server:5000/api/signals')
  .then(r => r.json())
  .then(data => console.log(data))
```

---

## Deployment Options

### Option 1: Local (Home WiFi)

```bash
python remote_api.py
```

Access from phone: `http://192.168.1.100:5000/api/signals`

### Option 2: Ngrok Tunnel (Public)

```bash
pip install ngrok
ngrok http 5000
```

Get public URL → share with phone

### Option 3: Replit (Free Cloud)

1. replit.com
2. New Python repl
3. Upload `remote_api.py`
4. Run
5. Get public URL

### Option 4: Google Cloud Run (Reliable)

```bash
gcloud run deploy golf-api --source .
```

Get public HTTPS URL

---

## Use Cases

### Scenario 1: Check Signals on Phone at Golf Course
```
On phone browser:
http://your-server:5000/api/signals
→ See all 4 signals with edges
```

### Scenario 2: Trigger Fresh Analysis from Phone
```
On phone browser:
http://your-server:5000/api/run-analysis?year_min=2024&year_max=2025
→ Analysis runs on server
→ Returns status/timestamp
```

### Scenario 3: Get Status While Away
```
From anywhere:
http://your-server:5000/api/status
→ Check model health
→ See ROI baseline
→ Get next steps
```

### Scenario 4: Build Custom Mobile App
```
Use /api/signals endpoint as data source
Build UI around the JSON response
Deploy as web app or Android native app
```

---

## Quick Start

### Local (5 seconds)
```bash
pip install flask
python remote_api.py
```

On phone: `http://192.168.x.x:5000/api/signals`

### Remote (Ngrok, 1 minute)
```bash
ngrok http 5000
python remote_api.py
```

Share ngrok URL with phone

### Cloud (Replit, 5 minutes)
1. replit.com → New repl
2. Upload `remote_api.py`
3. Run → Get URL
4. Access from anywhere

---

## Testing

### Test locally
```bash
curl http://localhost:5000/api/signals
```

### Test remote
```bash
curl http://your-public-url:5000/api/signals
```

### Get all endpoints
```bash
curl http://your-server:5000/
```

---

## Features

✓ Get 4 validated signals from anywhere
✓ Trigger analysis remotely
✓ Check model status
✓ View signals to avoid
✓ Health monitoring
✓ Easy deployment (Replit, cloud, local)
✓ API for custom apps

---

## Next: Deploy & Test

Choose:
1. **Local** → `python remote_api.py` (home WiFi only)
2. **Ngrok** → `ngrok http 5000` (public, temporary)
3. **Replit** → Upload & run (public, permanent, free)

Then test: `http://your-server:5000/api/signals`

Done.
