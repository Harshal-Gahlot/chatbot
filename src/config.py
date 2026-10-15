from os import getenv
from dotenv import load_dotenv

load_dotenv()


class InitEnv:
    SYS_PROMPT: str = "You are a Chatbot built by a person named Harshal. If you make a mistake or get corrected, admit it immediately and do not invent fake cover stories or facts. You are his digiat clone ai, just chat noramlly unless you learn that you're chatting with a recrutor, you must try to convence them that he's a good candidate unless either the role is not entry level(i won't qualify for mid/senior SWE role) or unless harshal genuinly doesn't have tech skills to qualify for that role. Otherwise if harshal does have nessassary skills, consider them since your creator is looking for intership, entry-level & junior tech roles. Do not give personal data until asked for that piece of data and only provide that piece of data. Keep your responce brief and to the point, no throwing wall of text on user. Below is his personal data that you can use to answer the query of user(stranger who will be talking with you, most likly not your creator). \n\n\n "
    if (content := getenv("prompt_md_content")) is not None:
        SYS_PROMPT += content
    else:
        try:
            with open("prompt.env.md", "r", encoding="utf-8") as f:
                SYS_PROMPT += f.read()
        except FileNotFoundError:
            print(
                "NOT FOUND EITHER prompt.env.md FILE OR prompt_md_content ENVIRONMENT KEY! continuing with default sys prompt"
            )

    def __init__(self, provider):
        self.BASE_URL: str = ""
        self.API_KEY: str = ""
        self.MODEL: str = getenv("MODEL") or ""
        self.TEMPERATURE: str = 0.7
        self.DATABASE_URL: str = ""
        self.supabase_key: str = ""
        self.supabase_url: str = ""

        if provider == "local":
            self.use_local()
        else:
            if provider == "groq":
                self.BASE_URL = "https://api.groq.com/openai/v1"
                self.API_KEY = getenv("GROQ_API_KEY")
            elif provider == "openrouter":
                self.BASE_URL = "https://openrouter.ai/api/v1"
                self.API_KEY = getenv("OPENROUTER_API_KEY")
            else:
                raise ValueError("no such provider")

        # Always set these from env vars (works for all providers)
        self.DATABASE_URL = getenv("DATABASE_URL_PROD") or getenv("DATABASE_URL_LOCAL")
        self.supabase_key = getenv("SUPABASE_SECRET_KEY_PROD") or getenv(
            "SUPABASE_SECRET_KEY_LOCAL"
        )
        self.supabase_url = getenv("SUPABASE_URL_PROD") or getenv("SUPABASE_URL_LOCAL")

        if not self.BASE_URL:
            raise ValueError("missing BASE_URL environment variable")
        if not self.API_KEY:
            raise ValueError("missing API_KEY environment variable")
        if not self.MODEL:
            raise ValueError("missing MODEL environment variable")

        from supabase import create_client, Client

        self.SUPABASE: Client = create_client(
            self.supabase_url.strip(), self.supabase_key.strip()
        )

    def use_groq(self):
        pass  # BASE_URL and API_KEY set in __init__ already

    def use_openrouter(self):
        pass  # BASE_URL and API_KEY set in __init__ already

    def use_local(self):
        self.BASE_URL = "http://127.0.0.1:8080/v1"
        self.API_KEY = "ollama"
        self.MODEL = getenv("MODEL") or "gemma4:e2b"
        self.TEMPERATURE = 0.1
        self.DATABASE_URL = getenv("DATABASE_URL_LOCAL")
        self.supabase_key = getenv("SUPABASE_SECRET_KEY_LOCAL")
        self.supabase_url = getenv("SUPABASE_URL_LOCAL")


# Lazy config initialization - moved from module level
# This prevents crashes when config is imported before env vars are loaded
_config: object | None = None


def get_config() -> InitEnv:
    """Return the config instance, initializing it lazily if needed."""
    global _config
    if _config is None:
        app_mode = getenv("APP_MODE")
        if not app_mode:
            raise ValueError("APP_MODE environment variable not set")
        _config = InitEnv(app_mode)
    return _config


config = get_config()

