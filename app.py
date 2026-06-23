from openai import AsyncOpenAI
import chainlit as cl
import sys, traceback, config
from utils import extractUploadedFiles, printError

# When chat start
@cl.on_chat_start
async def start_app():
    print("app started")
    client = AsyncOpenAI(
        base_url=config.BASE_URL,
        api_key=config.API_KEY
    )
    messages = [ {"role":"system","content":config.SYS_PROMPT}]

    cl.user_session.set("client", client)
    cl.user_session.set("messages", messages)
    # await cl.Message(content="Hi im your AI assistant, ask me anything.").send()
    
# Handle Message
@cl.on_message
async def main(mes: cl.Message):
    try:
        # immediately show loading spinner, in advance, before llm actually starts thinking.
        msg = cl.Message(content="")
        await msg.send()

        client = cl.user_session.get("client")
        messages = cl.user_session.get("messages")

        # extract PDF or txt file if uploaded
        if mes.elements: extractUploadedFiles(mes)                
        
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
        exc_type, exc_value, exc_tb = sys.exc_info()

        printError("\nUnder CODE BLOCK", traceback.extract_tb(exc_tb)[1].line)
        print("line number: ",traceback.extract_tb(exc_tb)[1].lineno)
        print("function name: ",traceback.extract_tb(exc_tb)[1].name)
        print("filename:part", "/".join(traceback.extract_tb(exc_tb)[1].filename.split("/")[-2:]))
        printError("ERROR MESSAGE", str(e))


@cl.on_chat_end
def on_chat_end():
    printError("", "The user is disconnected!") # just to make this log red color, not an error.

@cl.on_stop
def on_stop():
    """The on_stop decorator is used to define a hook that is called
    when the user clicks the stop button while a task was running."""
    pass
    # print("user stopped the llm mid way")