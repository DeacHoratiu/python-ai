import os
from agent_tools import summarize_file, analyze_document, run_tests
from validators import FileNameValidator, DocAnalysisRequest
from dotenv import load_dotenv
from openai import OpenAI
import json


def run_tool(client: OpenAI, tool_call):
    tool_name = tool_call.function.name

    if tool_name == "summarize_file":
        args = json.loads(tool_call.function.arguments)
        return summarize_file(client, args)

    if tool_name == "run_tests":
        return run_tests()

    if tool_name == "analyze_document":
        args = json.loads(tool_call.function.arguments)
        return analyze_document(args)

    return f"error: unknown tool {tool_name}"

def tool_add(name, description, parameters=None):
    function = {
        "name": name,
        "description": description
    }

    if parameters is not None:
        function["parameters"] = parameters

    tool = {
        "type": "function",
        "function": function
    }

    return tool

##Here we have the agent, and we need to pass instructions how to run a tool.

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

    ## here we define a list of tools for the agent
    tools = [
            tool_add("run_tests","Run uv run pytest. Use this only when the user explicitly asks to run tests or pytest."),
            tool_add("summarize_file","Reads and summarizes a text file in the current project. Use this when the user asks to summarize a file. Pass the file path as the name argument.",FileNameValidator.model_json_schema()),
            tool_add("analyze_document","Analyzes a project file and counts how many times the provided words appear.",DocAnalysisRequest.model_json_schema())

    ]

    messages = []
    ## system.prompt
    messages.append({
        "role": "system",
        "content": "You are a helpful assistant. If the user asks to run tests or pytest, use the run_tests tool. If the user asks to summarize a file, use the summarize_file tool and pass the requested file path as the name argument. Do not use run_tests to list files or to summarize files. If the user asks to analyze a document or count words in a file, use analyze_document."
    })
    while True:
        inp = input("you>")
        if inp == "quit":
            break
        messages.append({
            "role": "user",
            "content": inp
        })


        ##ask for response
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
