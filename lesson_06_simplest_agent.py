import os
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
from pathlib import Path
from pydantic import BaseModel, Field, ValidationError
import json

class FileNameValidator(BaseModel):
    name: str = Field(description="Name of the text file in this project.")

class FileSummaryValidator(BaseModel):
    """This validator can validate the output of an agent, the JSON returned by the summary agent."""

    title: str = Field(description="Generated title for the file.")
    summary: str = Field(description="Summary of the file.")

#starts a new agent and summarizes a file
def summarize_file(client: OpenAI, args: dict):
    # will receive a file name, will read the file, provide it to an agent, and return a summary.
    try:
        req = FileNameValidator.model_validate(args)
        filename = req.name
        #makes sure the file exists
        path = Path(filename).resolve()
        #aici punem limita ca agentul poate citi doar fisiere din folderul curent.
        path.relative_to(Path.cwd().resolve())
        #reads the whole file
        text = path.read_text()

        #starts our agent
        response = client.chat.completions.create(
            model=os.getenv("OPENROUTER_MODEL"),
            messages=[
            {"role": "system",
             "content": "Return ONLY JSON, that contains a title and a short summary. Summarise the file you received, and put it in the JSON response."},
            {"role": "user", "content": f"Please summarize this file for me: {text}"}
        ], response_format={
            "type": "json_schema",
            "json_schema": {"name": "file_summary",
                            "schema": FileSummaryValidator.model_json_schema()
                        }
        }).choices[0].message
        #first, validates llm agent output. sometimes it can be messed up
        validated_model_json = FileSummaryValidator.model_validate_json(response.content)
        #returns json with title and summary
        return validated_model_json.model_dump_json()

    except Exception as e:
        return f"error: {e}"


def run_tests() ->str:
    try:
       result =  subprocess.run(
            ["uv","run","pytest"],
            cwd =  Path.cwd(),
            capture_output = True,
            text = True,
            timeout = 60
        )
       return (result.stdout or "") + " " + (result.stderr or "")
    except Exception as e:
        return f"error: {e}"

def run_tool(client: OpenAI, tool_call):
    tool_name = tool_call.function.name

    if tool_name == "summarize_file":
        args = json.loads(tool_call.function.arguments)
        return summarize_file(client, args)

    if tool_name == "run_tests":
        return run_tests()

    return f"error: unknown tool {tool_name}"

#avem agentul si trebuie sa-i dam instructiuni despre cum sa ruleze o unealta creata de noi.

def complete(client: OpenAI, messages: list[dict], tools: list[dict]):
    response = client.chat.completions.create(
        messages=messages,
        model= os.getenv("OPENROUTER_MODEL"),
        tools = tools,
        tool_choice = "auto"
    ).choices[0].message
    return response

def main():
    load_dotenv()

    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
            )

    #aici o sa definim lista de tools pentru agent
    tools = [
        {
            "type": "function",
            "function": {
                "name": "run_tests",
                "description": "Run uv run pytest. Use this only when the user explicitly asks to run tests or pytest."
            }
        },
        {
            "type": "function",
            "function": {
                "name": "summarize_file",
                "description": "Reads and summarizes a text file in the current project. Use this when the user asks to summarize a file. Pass the file path as the name argument.",
                "parameters": FileNameValidator.model_json_schema()
            }
        }
    ]

    messages = []
    #system.prompt
    messages.append({
        "role": "system",
        "content": "You are a helpful assistant. If the user asks to run tests or pytest, use the run_tests tool. If the user asks to summarize a file, use the summarize_file tool and pass the requested file path as the name argument. Do not use run_tests to list files or to summarize files."
    })
    while True:
        inp = input("you>")
        if inp == "quit":
            break
        messages.append({
            "role": "user",
            "content": inp
        })


        #cerem agentului sa ne raspunda la un mesaj.
        response = complete(client,messages,tools)
        messages.append(response.model_dump(exclude_none=True))

        while response.tool_calls:
            for tool_call in response.tool_calls:
                output = run_tool(client, tool_call)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": output
                })
            response = complete(client, messages, tools)
            messages.append(response.model_dump(exclude_none=True))

        print("agent> ", response)
        print(f"Message count: {len(messages)}")

if __name__ == "__main__":
    try:
        main()
        # print(run_tests())
    except Exception as e:
        print(e)
