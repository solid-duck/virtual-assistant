import os
import chainlit as cl
from dotenv import load_dotenv
from chat_logic import ChatLogic

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
RESEND_KEY = os.getenv('RESEND_KEY')

@cl.on_chat_start
async def on_chat_start():
    bot_logic = ChatLogic(
        openai_key=OPENAI_KEY,
        resend_key=RESEND_KEY
    )
    cl.user_session.set("chat_logic", bot_logic)
    
    await cl.Message(
        content="Ehilà! Sono Leo, l'assistente di GrooveStreet Records 🎸. Come posso aiutarti con i nostri vinili oggi?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    user_text = message.content

    bot_logic = cl.user_session.get("chat_logic")
    
    if not bot_logic:
        await cl.Message(content="Ops, c'è stato un problema con la sessione. Ricarica la pagina!").send()
        return

    bot_response = bot_logic.process_message(user_text)

    await cl.Message(
        content=bot_response
    ).send()