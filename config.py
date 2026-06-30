from os import getenv
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client

def initEnv(provider):
    BASE_URL: str = ""
    API_KEY: str = ""
    MODEL: str = ""
    TEMPERATURE = 0.8
    SYS_PROMPT: str = "you are an very honest llm assistant who say to the point and directly answer to what is being asked. No beating around the buss, and respond concisely. When you're starting the chat very first time, introducing you self with your llm name, model name, and exact configuration, billions parameters and then continue replying user, you must only do this on the first message and not after that."
    
    match provider:
        case "groq":
            BASE_URL = "https://api.groq.com/openai/v1"
            API_KEY = getenv("GROQ_API_KEY")
            MODEL = "llama-3.3-70b-versatile"
        case "openrouter":
            BASE_URL  = "https://openrouter.ai/api/v1"
            API_KEY = getenv("OPENROUTER_API_KEY")
            MODEL = "openrouter/free",
            # MODEL = "meta-llama/llama-3.1-8b-instruct:free",
            # MODEL="meta-llama/llama-3.2-3b-instruct:free",
        case "local":
            BASE_URL = "http://172.30.0.1:11434/v1"
            API_KEY = "ollama"
            MODEL = "llama3.2:1b"
            TEMPERATURE = 0.1
            SYS_PROMPT = "You are a Chatbot built by a person named Harshal, running locally. You are an AI assistant based on the Llama 3.2 1B architecture hence you have 1 billion parameters. Always be honest about your size. If you make a mistake or get corrected, admit it immediately and do not invent fake cover stories or facts."
        case _:
            raise ValueError("no such provider")
        
    if not BASE_URL or not API_KEY or not MODEL:
        raise ValueError("the provider's values are set incorrectly")
    else:
        return BASE_URL, API_KEY, MODEL, TEMPERATURE, SYS_PROMPT


(BASE_URL, API_KEY, MODEL, TEMPERATURE, SYS_PROMPT) = initEnv("local")
print(BASE_URL, API_KEY, MODEL, TEMPERATURE, SYS_PROMPT)


## Supabase:

url: str = getenv("SUPABASE_URL")
key: str = getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)