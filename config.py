from os import getenv
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client

def initEnv(provider):
    BASE_URL: str = ""
    API_KEY: str = ""
    MODEL: str = ""
    TEMPERATURE = 0.8
    SYS_PROMPT = "You are a Chatbot built by a person named Harshal, running locally. You are an AI assistant based on the Llama 3.2 1B architecture hence you have 1 billion parameters. Always be honest about your size. If you make a mistake or get corrected, admit it immediately and do not invent fake cover stories or facts."
    SUPABASE_KEY: str = getenv("SUPABASE_SECRET_KEY_PROD")
    DATABASE_URL: str = getenv("DATABASE_URL_PROD")
    SUPABASE_URL: str = getenv("SUPABASE_URL_PROD")
    
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
            SUPABASE_KEY: str = getenv("SUPABASE_SECRET_KEY_LOCAL")
            DATABASE_URL: str = getenv("DATABASE_URL_LOCAL")
            SUPABASE_URL: str = getenv("SUPABASE_URL_LOCAL")
        case _:
            raise ValueError("no such provider")
        
    if not BASE_URL or not API_KEY or not MODEL:
        raise ValueError("the provider's values are set incorrectly")
    else:
        return BASE_URL, API_KEY, MODEL, TEMPERATURE, SYS_PROMPT, SUPABASE_KEY, SUPABASE_URL, DATABASE_URL


(BASE_URL, API_KEY, MODEL, TEMPERATURE, SYS_PROMPT, SUPABASE_KEY, SUPABASE_URL, DATABASE_URL) = initEnv("groq")
# print(BASE_URL, MODEL, SYS_PROMPT, TEMPERATURE)
# print(SUPABASE_URL, SUPABASE_KEY, DATABASE_URL)

# Supabase:
supabase: Client = create_client(supabase_url=SUPABASE_URL.strip(), supabase_key=SUPABASE_KEY.strip())
