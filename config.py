from os import getenv
from dotenv import load_dotenv
load_dotenv()

# BASE_URL:str = "https://openrouter.ai/api/v1"
BASE_URL:str = "https://api.groq.com/openai/v1"
API_KEY:str = getenv("GROQ_API_KEY")

MODEL: str = "llama-3.3-70b-versatile"
# MODEL:str = "openrouter/free",
# model="meta-llama/llama-3.1-8b-instruct:free",
# model="meta-llama/llama-3.2-3b-instruct:free",

TEMPERATURE = 0.8

SYS_PROMPT:str = "you are an very honest llm assistant who say to the point and directly answer to what is being asked. No beating around the buss, and respond concisely. You always start that chat by introducing you self with your llm name, model name, and exact configuration, billions parameters and then continue replying user."
