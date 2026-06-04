from openai import OpenAI
import config

client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)

response = client.chat.completions.create(
    messages=[
        {"role":"system","content":config.SYS_PROMPT},
        {"role":"user","content":"hi"},
    ],
    model=config.MODEL,
    temperature=config.TEMPERATURE
)
print(response.choices[0].message.content)