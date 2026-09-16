import os
from dotenv import load_dotenv
from openai import OpenAI

#avem agentul si trebuie sa-i dam instructiuni despre cum sa ruleze o unealta de noi.

def main():
    load_dotenv()

    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
            )
    messages = []
    #system.prompt
    messages.append({
        "role": "system",
        "content": "Use run_tests tool when asked to run any tests"
    })
    messages.append({
        "role": "user",
        "content": input("you>")
    })

    #aici o sa definim lista de tools pentru agent
    tools = [
        {
            "type": "function",
            "function": {
                "name": "run_tests",
                "description": "Run uv run pytest."
            }
        }
    ]

    #cerem agentului sa ne raspunda la un mesaj.
    response = client.chat.completions.create(
        messages=messages,
        model= os.getenv("OPENROUTER_MODEL"),
        tools = tools,
        tool_choice = "auto"
    ).choices[0].message
    print(response)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)