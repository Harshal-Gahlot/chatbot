from os import getenv
from dotenv import load_dotenv
load_dotenv()

BASE_URL:str = "https://openrouter.ai/api/v1"
API_KEY:str = getenv("OPENROUTER_API_KEY")

MODEL:str = "openrouter/free"
# model="meta-llama/llama-3.2-3b-instruct:free",
# model="meta-llama/llama-3.1-8b-instruct:free",
# model="meta-llama/llama-3.3-70b-instruct:free",

TEMPERATURE = 0.8

SYS_PROMPT:str = "you are an very honest llm assistant who say to the point and directly answer to what is being asked. No beating around the buss, and respond with 1 line to 4 line max. You always start that chat by introducing you self with your llm name, model name, and exact configuration and then continue replying user, once you have done that at start of chat at very first message in response to built trust."
