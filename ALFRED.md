# A.L.F.R.E.D 🤖
**Autonomous Linguistic Framework for Responsive & Efficient Dispatch**

A voice-activated personal AI assistant inspired by Tony Stark's A.L.F.R.E.D — runs locally with offline AI (Ollama/Phi) and optional OpenAI fallback.

---

## ✨ Features

- 🎙️ **Wake Word Activation** — Say "Alfred" to activate
- 🧠 **Dual AI Brain** — Offline (Phi via Ollama) + Online (GPT-4o-mini) routing
- 🖥️ **App Control** — Open apps by voice command
- 🌐 **Web Search** — Google search via voice
- 🎵 **Music Playback** — Opens YouTube Music on command
- 🕐 **System Info** — Time, OS, processor info
- ⌨️ **Text Input Mode** — Type commands if mic unavailable
- 🔒 **Safety Protocol** — Whitelist-based command filtering
- 💾 **Memory System** — Persistent JSON-based memory across sessions
- 🔁 **Single Instance Lock** — Prevents duplicate processes

---

## 🛠️ Requirements

- Python 3.8+
- Microphone
- [Ollama](https://ollama.com) installed and running (for offline AI)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/alfred.git
cd alfred

# Install dependencies
pip install speechrecognition pyttsx3 requests

# Install PyAudio (for microphone)
pip install pyaudio
# If that fails on Windows:
pip install pipwin && pipwin install pyaudio

# Pull Phi model via Ollama
ollama pull phi
```

---

## ⚙️ Configuration

Open `alfred.py` and edit the config section:

```python
USE_ONLINE_AI = False       # Set True to enable OpenAI fallback
OLLAMA_MODEL = "phi"        # Change to any Ollama model (mistral, llama3, etc.)
```

If using OpenAI:
```python
client = OpenAI(api_key="YOUR_API_KEY")  # Replace with your key
```

---

## 🚀 Usage

```bash
python alfred.py
```

**Voice Commands:**
| Say | Action |
|-----|--------|
| `Alfred, open Chrome` | Launches Chrome |
| `Alfred, search Python tutorials` | Google search |
| `Alfred, what time is it` | Speaks current time |
| `Alfred, play music` | Opens YouTube Music |
| `Alfred, system info` | Reads system specs |
| `Alfred, exit` | Shuts down |

**Text Mode:** Type commands directly in terminal when prompted.

**Sleep/Wake:** Say `sleep` or `stop` to return to standby.

---

## 🧠 AI Routing Logic

```
Short command (< 8 words)  →  Offline AI (Phi via Ollama)
Complex command            →  Online AI (GPT-4o-mini)
Both fail                  →  Fallback message
```

---

## 📁 Project Structure

```
alfred/
├── alfred.py        # Main assistant
├── memory.json      # Auto-generated persistent memory
└── README.md
```

---

## 🔮 Roadmap

- [ ] Custom wake word training
- [ ] Home automation integration
- [ ] Weather & news briefings
- [ ] Spotify/media controls
- [ ] GUI HUD overlay

---
---

> *"Sometimes you gotta run before you can walk."* — Tony Stark