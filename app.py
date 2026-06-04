from openai import AsyncOpenAI
import chainlit as cl
from llm_error_handling import handle_error
import sys, traceback, config

@cl.on_chat_start
def start_app():
    print("app started")
    client = AsyncOpenAI(
        base_url=config.BASE_URL,
        api_key=config.API_KEY
    )
    messages = [ {"role":"system","content":config.SYS_PROMPT}]

    cl.user_session.set("client", client)
    cl.user_session.set("messages", messages)

@cl.on_message
async def main(mes: cl.Message):
    try:
        # immediately show loading spinner, in advance, before llm actually starts thinking.
        msg = cl.Message(content="")
        await msg.send()

        client = cl.user_session.get("client")
        messages = cl.user_session.get("messages")
        messages.append({"role": "user", "content": mes.content})

        stream = await client.chat.completions.create(
            model=config.MODEL,
            temperature=config.TEMPERATURE,
            messages=messages,
            stream=True
        )

        async for chunk in stream:
            # walrus/assignment expression operator
            if token := chunk.choices[0].delta.content or "":
                # Adds fancy UI loading as token are streamed in from network.
                await msg.stream_token(token)

        # update the content fr:
        messages.append({"role": "assistant", "content": msg.content})
        await msg.update()


    except Exception as e:
        msg.content = f"❌ Error: {str(e)}"
        await msg.update()


        RED = "\033[31m"
        RESET = "\033[0m"
        exc_type, exc_value, exc_tb = sys.exc_info()

        print("\nUnder CODE BLOCK: ",RED,traceback.extract_tb(exc_tb)[1].line, RESET)
        print("line number: ",traceback.extract_tb(exc_tb)[1].lineno)
        print("function name: ",traceback.extract_tb(exc_tb)[1].name)
        print("filename:part", "/".join(traceback.extract_tb(exc_tb)[1].filename.split("/")[-2:]))
        print("ERROR MESSAGE:",RED, str(e), RESET)