# Argos 👁️

> "I observe. I interpret. I act."

Argos is not a chatbot.

It is a system-aware AI entity designed to understand intent and interact with its environment.

---

## 🧠 Capabilities

- Natural language understanding (Gemini)
- Telegram-based interaction
- System monitoring (CPU, RAM, Disk)
- Modular architecture

---

## ⚙️ Setup

```bash
git clone https://github.com/Rafaeldo367/argos-ai.git
cd argos-ai

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
nano .env

python main.py
