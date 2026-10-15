from os import getenv
from dotenv import load_dotenv

load_dotenv()
load_dotenv(dotenv_path="configs.env")

# Explicitly telling Pyright type definations.
BASE_URL: str | None = ""
API_KEY: str | None = ""

MODEL: str | None = ""
TEMPERATURE: float | None = None
TOP_P: float | None = None
FREQUENCY_PENALTY: float | None = None
PRESENCE_PENALTY: float | None = None

DATABASE_URL: str | None = ""
supabase_key: str | None = ""
supabase_url: str | None = ""

SYS_PROMPT: str = ""

try:
    with open("src/sys_prompt.txt", "r", encoding="utf-8") as f:
        SYS_PROMPT += f.read()
        print("sys prompt part 1 found:", True)
except FileNotFoundError:
    print("NOT FOUND: sys_prompt.txt")


def raise_err(var):
    raise ValueError(f'missing "{var}" environment variable')


def set_prod_db():
    globals().update(
        {
            "DATABASE_URL": getenv("DATABASE_URL_PROD"),
            "supabase_key": getenv("SUPABASE_SECRET_KEY_PROD"),
            "supabase_url": getenv("SUPABASE_URL_PROD"),
        }
    )


def set_local_db():
    globals().update(
        {
            "DATABASE_URL": getenv("DATABASE_URL_LOCAL"),
            "supabase_key": getenv("SUPABASE_SECRET_KEY_LOCAL"),
            "supabase_url": getenv("SUPABASE_URL_LOCAL"),
        }
    )


def use_prod_prompt():
    try:
        if (content := getenv("prompt_md_content")) is not None:
            global SYS_PROMPT
            SYS_PROMPT += content
            print("sys prompt part 2 found:", True)
    except FileNotFoundError:
        raise ValueError("prompt.env.md NOT FOUND")


def use_local_prompt():
    try:
        with open("prompt.env.md", "r", encoding="utf-8") as f:
            global SYS_PROMPT
            SYS_PROMPT += f.read()
            print("sys prompt part 2 found:", True)
    except FileNotFoundError:
        raise ValueError("prompt.env.md NOT FOUND")


def mode(
    model,
    provider,
    db_instance,
    prompt_instance,
    temp,
    top_p,
    frequency_penalty,
    presence_penalty,
):
    global \
        BASE_URL, \
        API_KEY, \
        MODEL, \
        TEMPERATURE, \
        TOP_P, \
        FREQUENCY_PENALTY, \
        PRESENCE_PENALTY

    match provider:
        case "local":
            BASE_URL = "http://127.0.0.1:8080/v1"
            API_KEY = "ollama"
        case "groq":
            BASE_URL = "https://api.groq.com/openai/v1"
            API_KEY = getenv("GROQ_API_KEY")
        case "openrouter":
            BASE_URL = "https://openrouter.ai/api/v1"
            API_KEY = getenv("OPENROUTER_API_KEY")
        case _:
            raise ValueError("no such provider")

    MODEL = model
    TEMPERATURE = float(temp)
    TOP_P = float(top_p)
    FREQUENCY_PENALTY = float(frequency_penalty)
    PRESENCE_PENALTY = float(presence_penalty)

    if db_instance == "prod":
        set_prod_db()
    else:
        set_local_db()
    if prompt_instance == "prod":
        use_prod_prompt()
    else:
        use_local_prompt()


local_models = ["gemma4:e2b", "gemma4:e4b"]
groq_models = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b"]

provider = getenv("PROVIDER")
model = getenv("MODEL")
prompt_instance = getenv("PROMPT_INSTANCE")
db_instance = getenv("DB_INSTANCE")

temp = getenv("TEMPERATURE")
top_p = getenv("TOP_P")
frequency_penalty = getenv("FREQUENCY_PENALTY")
presence_penalty = getenv("PRESENCE_PENALTY")
# max_tokens = getenv("MAX_TOKENS")

if not all([temp and top_p and frequency_penalty and presence_penalty]):
    raise_err("""at least one of the inital Configs values is missing in configs.env: \n
        TEMPERATURE, TOP_P, FREQUENCY_PENALTY, PRESENCE_PENALTY""")
elif not all([db_instance and provider and prompt_instance and model]):
    raise_err("""at least one of the inital Secrate values is missing in .env: \n
        DB_INSTANCE, PROVIDER, PROMPT_INSTANCE, MODEL""")
else:
    mode(
        model=model,
        provider=provider,
        db_instance=db_instance,
        prompt_instance=prompt_instance,
        temp=temp,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

if not BASE_URL:
    raise_err("BASE_URL")
if not API_KEY:
    raise_err("API_KEY")
if not DATABASE_URL:
    raise_err("DATABASE_URL")
if not supabase_key:
    raise_err("supabase_secret_key")
if not supabase_url:
    raise_err("supabase_url")


from supabase import create_client, Client

SUPABASE: Client = create_client(supabase_url.strip(), supabase_key.strip())
#
# to get a list of groq laatest available models directly.
# import requests
# import os
#
# api_key = os.environ.get("GROQ_API_KEY")
# url = "https://api.groq.com/openai/v1/models"
#
# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.json())
