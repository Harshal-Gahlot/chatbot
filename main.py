from openai import OpenAI
import config

client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)

messages = [ {"role":"system","content":config.SYS_PROMPT}]

def chat(prompt: str):
    completion = client.chat.completions.create(
        model=config.MODEL,
        temperature=config.TEMPERATURE,
        messages=messages
    )

    response = completion.choices[0].message.content

    print(response)
    messages.append({"role": "user", "content": prompt})
    messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if "bye" in user_input.lower().strip().split():
            break
        chat(user_input)