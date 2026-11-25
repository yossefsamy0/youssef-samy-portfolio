import os
import discord
from collections import defaultdict, deque
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

if not DISCORD_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Set DISCORD_TOKEN and OPENAI_API_KEY in your environment.")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
ai = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are a careful assistant for beginner programming and robotics learners. "
    "Explain concepts clearly. For electronics, ask for missing board and voltage details "
    "when needed, and emphasize checking wiring and power limits before connecting hardware."
)
history = defaultdict(lambda: deque(maxlen=12))


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot or client.user not in message.mentions:
        return

    prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
    prompt = prompt.replace(f"<@!{client.user.id}>", "").strip()
    if not prompt:
        await message.reply("اكتب سؤالك بعد منشن البوت.")
        return

    channel_history = history[message.channel.id]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(channel_history)
    messages.append({"role": "user", "content": prompt})

    async with message.channel.typing():
        try:
            response = ai.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.4,
                max_tokens=700,
            )
            answer = response.choices[0].message.content or "لم أتمكن من إنشاء رد."
            channel_history.append({"role": "user", "content": prompt})
            channel_history.append({"role": "assistant", "content": answer})
            await message.reply(answer[:1900], mention_author=False)
        except Exception as exc:
            print(f"AI request failed: {exc}")
            await message.reply("حصلت مشكلة أثناء معالجة السؤال. حاول مرة أخرى لاحقًا.")


client.run(DISCORD_TOKEN)
