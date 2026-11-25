# Discord AI Assistant

A starter Discord bot for a programming and robotics help community. It responds when mentioned and keeps a short per-channel conversation context in memory.

## Features
- Responds to direct mentions only.
- Uses an OpenAI-compatible chat completion through the official Python SDK.
- Keeps a small in-memory context per channel.
- Reads credentials from environment variables; no secrets are stored in source control.

## Setup
1. Create a Discord application and bot in the Discord Developer Portal.
2. Enable the Message Content Intent if your bot configuration requires it.
3. Create an API key with your model provider.
4. Copy `.env.example` to `.env` and fill in your own values.
5. Install dependencies and run:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python bot.py
```

## Safety and operating notes
- Never commit `.env` or share bot/API tokens.
- Set spending limits with your model provider and monitor usage.
- The bot's answers can be wrong; users should verify wiring, voltage, and code before applying them to hardware.
- Context is in memory only and is cleared when the bot restarts.

## Status
Starter implementation. Live deployment and real-server testing require the owner's Discord application and API credentials.
