# for non-web/terminal based LLMs, you can use the following code to interact
# with the model in a chat-like manner. This code sets up a simple command-line
# interface where the user can input prompts, and the model will respond
# accordingly. The conversation continues until the user types "bye".
from openai import OpenAI
from llm_error_handling import handle_error


def _import_config():
    import config

    return config


def chat(prompt: str, messages: list[dict[str, str]]):
    messages.append({"role": "user", "content": prompt})

    config = _import_config()
    completion = client.chat.completions.create(
        model=config.MODEL, temperature=config.TEMPERATURE, messages=messages
    )

    response = completion.choices[0].message.content
    print(response)
    messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    config = _import_config()
    client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
    messages = [{"role": "system", "content": config.SYS_PROMPT}]

    while True:
        user_input = input("User: ")
        if "bye" in user_input.lower().strip().split():
            break
        handle_error(chat, user_input, messages)

