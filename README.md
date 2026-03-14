# MINDFORGE 🧠⚡

> **Voice-controlled multi-agent AI system for automating online assignments.**

MINDFORGE uses a fleet of LangChain agents powered by Google Gemini to listen to voice commands, navigate the web via Selenium, solve assignment questions, and submit them — all orchestrated through a sleek real-time React dashboard.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend (Vite)                    │
│  VoiceControl │ AgentStatus │ TaskQueue │ BrowserPreview     │
└────────────────────────┬────────────────────────────────────┘
                         │ REST + WebSocket
┌────────────────────────▼────────────────────────────────────┐
│                  FastAPI Backend (Python)                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Orchestrator Agent (LangChain)          │    │
│  │  ┌──────────────┐ ┌─────────────┐ ┌─────────────┐  │    │
│  │  │ Voice Agent  │ │Browser Agent│ │Assignment   │  │    │
│  │  │ (STT/Intent) │ │ (Selenium)  │ │Agent(Gemini)│  │    │
│  │  └──────────────┘ └─────────────┘ └─────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
            │                    │
   ┌────────▼──────┐   ┌────────▼──────────┐
   │ Selenium Grid │   │  Google Gemini API │
   │ (Chrome)      │   │  (LangChain)       │
   └───────────────┘   └────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Google Chrome
- Docker + Docker Compose (optional)

### 1. Clone & Configure
```bash
git clone <repo-url>
cd MINDFORGE
cp .env.example .env
# Edit .env — add your GEMINI_API_KEY
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Run (Development)
```bash
# Terminal 1 — Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && npm run dev
```

Open **http://localhost:5173**

### 5. Run with Docker (All Services)
```bash
docker-compose up --build
```

---

## Project Structure

```
MINDFORGE/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings (pydantic-settings)
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── agents/              # LangChain multi-agent layer
│   │   ├── orchestrator.py
│   │   ├── browser_agent.py
│   │   ├── voice_agent.py
│   │   └── assignment_agent.py
│   ├── services/            # Core service layer
│   │   ├── voice_service.py
│   │   ├── browser_service.py
│   │   └── gemini_service.py
│   ├── api/                 # REST + WebSocket endpoints
│   │   ├── routes/
│   │   │   ├── voice.py
│   │   │   ├── agents.py
│   │   │   ├── tasks.py
│   │   │   └── health.py
│   │   └── websockets.py
│   ├── models/              # Pydantic schemas
│   ├── utils/               # Shared helpers
│   └── tests/               # Pytest tests
├── frontend/
│   ├── src/
│   │   ├── components/      # VoiceControl, AgentStatus, TaskQueue, BrowserPreview
│   │   ├── pages/           # Dashboard, TaskManager, Settings
│   │   ├── services/        # api.js, websocket.js
│   │   └── store/           # Zustand global state
│   └── package.json
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## Environment Variables

See [`.env.example`](.env.example) for the full list.

| Key | Description |
|-----|-------------|
| `GEMINI_API_KEY` | **Required** — Google Gemini API key |
| `BROWSER_HEADLESS` | `true` for CI / production |
| `VOICE_ENGINE` | `google` or `whisper` |
| `DATABASE_URL` | SQLite (default) or PostgreSQL |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Zustand |
| Backend | FastAPI, Uvicorn, Python 3.11 |
| AI Agents | LangChain, Google Gemini |
| Browser Automation | Selenium 4, webdriver-manager |
| Voice | SpeechRecognition, gTTS / Whisper |
| Real-time | WebSockets (native FastAPI) |
| Containerization | Docker, Docker Compose |

---

## License

MIT
