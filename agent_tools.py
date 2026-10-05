import os
import subprocess
from pathlib import Path
from validators import DocAnalysisRequest, DocAnalysisReport, FileNameValidator, FileSummaryValidator
from openai import OpenAI
from pydantic import ValidationError

# static variable
PROJECT_ROOT = Path(__file__).resolve().parent

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


def analyze_document(args: dict):
    try:
        request = DocAnalysisRequest.model_validate(args)
        file_name = request.file_name
        words = request.words

        # open a file/ find how many times a word occurs in the file
        p = (PROJECT_ROOT / file_name).resolve()
        p.relative_to(PROJECT_ROOT)

        if not p.is_file():
            return f"error: {file_name} is not a file!"

        text = p.read_text(encoding="utf-8")
        split_document = text.lower().replace(".","").split()
        matches = {}

        for current_word in words:
            count = split_document.count(current_word.lower())
            matches[current_word] = count

        report = DocAnalysisReport(
            file_name = file_name,
            matches = matches,
            word_count = len(split_document)
        )

        return report.model_dump_json()
    except (ValidationError, ValueError, OSError) as e:
        return f"error: {e}"

def summarize_file(client: OpenAI, args: dict):
    # will receive a file name, will read the file, provide it to an agent, and return a summary.
    try:
        req = FileNameValidator.model_validate(args)
        filename = req.name
        #makes sure the file exists
        path = (PROJECT_ROOT / filename).resolve()
        #aici punem limita ca agentul poate citi doar fisiere din folderul curent.
        path.relative_to(PROJECT_ROOT)
        #reads the whole file
        text = path.read_text(encoding="utf-8")

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
        #returns JSON with title and summary
        return validated_model_json.model_dump_json()

    except Exception as e:
        return f"error: {e}"