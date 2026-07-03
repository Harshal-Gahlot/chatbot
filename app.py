from openai import AsyncOpenAI
import chainlit as cl
import sys, traceback, config
from utils import extractUploadedFiles, printError
from config import supabase
import chainlit.data as cl_data
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer

cl_data._data_layer = SQLAlchemyDataLayer(conninfo=config.DATABASE_URL)

# Logging in
@cl.password_auth_callback
async def authentication( email: str, password: str):
    try:
        user_data = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        }).user

        return cl.User(
            identifier=user_data.email,
            metadata={"supabase_id": user_data.id}
        )
    except Exception as e:
        print(e)
        return None

# When chat start
@cl.on_chat_start
async def start_app():
    client = AsyncOpenAI(
        base_url=config.BASE_URL,
        api_key=config.API_KEY
    )
    messages = [ {"role":"system","content":config.SYS_PROMPT}]

    cl.user_session.set("client", client)
    cl.user_session.set("messages", messages)
    print("app started\n")

# Handle Message
@cl.on_message
async def on_new_message( mes: cl.Message):
    try:
        # immediately show loading spinner, in advance, before llm actually starts thinking.
        msg = cl.Message(content="")
        await msg.send()
        client = cl.user_session.get("client")
        messages = cl.user_session.get("messages")

        # extract PDF or txt file if uploaded
        if mes.elements: extractUploadedFiles(mes)                
        
        user_input = {"role": "user", "content": mes.content}
        messages.append(user_input)

        stream = await client.chat.completions.create(model=config.MODEL,
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
        llm_output = {"role": "assistant", "content": msg.content}

        messages.append(llm_output)
        await msg.update()

    except Exception as e:
        msg.content = f"❌ Error: {str(e)}"
        # msg.is_error(True)
        await msg.update()
        exc_type, exc_value, exc_tb = sys.exc_info()

        # change the number [n] in below lines if error lines is not correct
        printError("\nUnder CODE BLOCK", traceback.extract_tb(exc_tb)[0].line)
        print("line number: ",traceback.extract_tb(exc_tb)[0].lineno)
        print("parent function name: ",traceback.extract_tb(exc_tb)[0].name)
        print("child function name: ",traceback.extract_tb(exc_tb)[1].name)
        print("filename:part", "/".join(traceback.extract_tb(exc_tb)[0].filename.split("/")[-2:]))
        printError("ERROR MESSAGE", str(e))

@cl.on_chat_end
def on_chat_end():
    """run when chat ends"""
    printError("", "The user is disconnected!") # just to make this log red color, not an error.

@cl.on_stop
def on_stop():
    """The on_stop decorator is used to define a hook that is called
    when the user clicks the stop button while a task was running."""
    pass
    # print("user stopped the llm mid way")
