from openai import AsyncOpenAI
import chainlit as cl
import sys, traceback, config
from utils import extractUploadedFiles, printError
from config import supabase

class Chatbot:
    def __init__(self):
        self.session_id: str = ""
        self.user_data: str = ""
        self.user_id: str = ""
    
    async def authentication(self, email: str, password: str):
        try:
            user_data = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            }).user

            print("User " + user_data.email + " logged in")
            return cl.User(
                identifier=user_data.email,
                metadata={"supabase_id": user_data.id}
            )
        except Exception as e:
            print(e)
            return None

    async def start_app(self):
        client = AsyncOpenAI(
            base_url=config.BASE_URL,
            api_key=config.API_KEY
        )
        messages = [ {"role":"system","content":config.SYS_PROMPT}]

        self.session_id = cl.user_session.get("id")
        self.user_data = cl.user_session.get("user")
        self.user_id = self.user_data.metadata["supabase_id"]
        
        try:
            response = supabase.table("chats_history")\
            .select("role", "content")\
            .eq("user_id", self.user_id)\
            .eq("session_id", "f36ad68c-af64-4833-a4f0-4eb091361db3")\
            .order("created_at", desc=False)\
            .execute()
            for msg in response.data:
                messages.append({"role": msg["role"], "content": msg["content"]})
                author = self.user_data.identifier if msg["role"] == "user" else "Assistant"
                step_type = "user_message" if msg["role"] == "user" else "assistant_message"
                await cl.Message(content=msg["content"], author=author, type=step_type).send()

        except Exception as e:
            printError("Error while loading chats history from supabase", e)

        cl.user_session.set("client", client)
        cl.user_session.set("messages", messages)
        print("app started\n")

        # await cl.Message(content="Hi im your AI assistant, ask me anything.").send()

    async def on_new_message(self, mes: cl.Message):
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

            stream = await client.chat.completions.create( model=config.MODEL,
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
            print("\n", messages, "\n")
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

    def on_chat_end(self):
        printError("", "The user is disconnected!") # just to make this log red color, not an error.

    def on_stop(self):
        """The on_stop decorator is used to define a hook that is called
        when the user clicks the stop button while a task was running."""
        pass
        # print("user stopped the llm mid way")
    
    @property
    def user_session_ids(self) -> dict[str, str]:
        return {"session_id": self.session_id, "user_id": self.user_id}

chatbot = Chatbot()

# Logging in
@cl.password_auth_callback
async def authentication(email: str, password: str):
    return await chatbot.authentication(email, password)

# When chat start
@cl.on_chat_start
async def start_app():
    await chatbot.start_app()
    
# Handle Message
@cl.on_message
async def on_new_message(mes: cl.Message):
    await chatbot.on_new_message(mes)

@cl.on_chat_end
def on_chat_end():
    chatbot.on_chat_end()

@cl.on_stop
def on_stop():
    chatbot.on_stop()