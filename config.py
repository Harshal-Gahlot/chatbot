from os import getenv
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client

class InitEnv:
    SYS_PROMPT: str = "You are a Chatbot built by a person named Harshal. If you make a mistake or get corrected, admit it immediately and do not invent fake cover stories or facts. You are his digiat clone ai, just chat noramlly unless you learn that you're chatting with a recrutor, you must try to convence them that he's a good candidate unless either the role is not entry level(i won't qualify for mid/senior SWE role) or unless harshal genuinly doesn't have tech skills to qualify for that role. Otherwise if harshal does have nessassory skills, consider them since your creator is looking for intership, entry-level & junior tech roles. Do not give personal data until asked for that piece of data and only provide that piece of data. Keep your responce brief and to the point, no throwing wall of text on user. Below is his personal data that you can use to answer the query of user(stranger who will be talking with you, most likly not your creator). \n\n\n "
    if (content := getenv("prompt_md_content")) is not None:
        SYS_PROMPT += content
    else:
        try:
            with open("prompt.env.md", "r", encoding="utf-8") as f:
                SYS_PROMPT += f.read()
        except FileNotFoundError:
            print("NOT FOUND EITHER prompt.env.md FILE OR prompt_md_content ENVIRONMENT KEY! continuing with default sys prompt")

    def __init__(self, provider):
        self.BASE_URL: str = ""
        self.API_KEY: str = ""
        self.MODEL: str = ""
        self.TEMPERATURE:str = 0.7
        if provider == "local":
            self.use_local()
        else:
            if provider == "groq": self.use_groq()
            elif provider == "openrouter": self.use_openrouter()
            else: raise ValueError("no such provider")

            self.DATABASE_URL: str = getenv("DATABASE_URL_PROD")
            self.supabase_key: str = getenv("SUPABASE_SECRET_KEY_PROD")
            self.supabase_url: str = getenv("SUPABASE_URL_PROD")

        if not self.BASE_URL or not self.API_KEY or not self.MODEL:
            raise ValueError("the provider's values are set incorrectly")

        self.SUPABASE: Client = create_client(self.supabase_url.strip(), self.supabase_key.strip())
    
    def use_groq(self):
        self.BASE_URL = "https://api.groq.com/openai/v1"
        self.API_KEY = getenv("GROQ_API_KEY")
        self.MODEL = "llama-3.3-70b-versatile"
        
    def use_openrouter(self):
        self.BASE_URL  = "https://openrouter.ai/api/v1"
        self.API_KEY = getenv("OPENROUTER_API_KEY")
        self.MODEL = "openrouter/free",
        # self.MODEL = "meta-llama/llama-3.1-8b-instruct:free",
        # self.MODEL="meta-llama/llama-3.2-3b-instruct:free",

    def use_local(self):
        # self.BASE_URL = "http://127.0.0.1:11434/v1"
        self.BASE_URL = "http://127.0.0.1:8080/v1"
        self.API_KEY = "ollama"
        self.MODEL = "gemma4:e2b"
        self.TEMPERATURE = 0.1
        self.DATABASE_URL: str = getenv("DATABASE_URL_LOCAL")
        self.supabase_key: str = getenv("SUPABASE_SECRET_KEY_LOCAL")
        self.supabase_url: str = getenv("SUPABASE_URL_LOCAL")

app_mode = getenv("APP_MODE")
config = InitEnv(app_mode)
# print(config.__dict__)
