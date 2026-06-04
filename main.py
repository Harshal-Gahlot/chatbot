from openai import OpenAI
from llm_error_handling import handle_error
import config

def chat(prompt: str, messages: list[dict[str, str]]):
    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model=config.MODEL,
        temperature=config.TEMPERATURE,
        messages=messages
    )

    response = completion.choices[0].message.content
    print(response)
    messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    client = OpenAI(
        api_key=config.API_KEY,
        base_url=config.BASE_URL
    )
    messages = [ {"role":"system","content":config.SYS_PROMPT}]

    while True:
        user_input = input("User: ")
        if "bye" in user_input.lower().strip().split():
            break
        handle_error(chat, user_input, messages)