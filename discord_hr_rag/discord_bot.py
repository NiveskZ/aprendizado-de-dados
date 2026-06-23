import os
import re
import discord
from dotenv import load_dotenv
from agent import conversar

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"HR Buddy conectado como: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    eh_mencao = client.user in message.mentions
    eh_dm = isinstance(message.channel, discord.DMChannel)
    if not (eh_mencao or eh_dm):
        return

    texto = re.sub(rf"<@!?{client.user.id}>", "", message.content).strip()
    if not texto:
        await message.reply("Oi! Como posso te ajudar com questões de RH?")
        return

    session_id = str(message.channel.id)  # equivalente ao chat.id do Telegram
    async with message.channel.typing():
        resposta = conversar(texto, session_id)
        if not resposta.strip():
            resposta = "Desculpa, tive um problema para gerar a resposta. Pode repetir a pergunta?"
    await message.reply(resposta)

if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))