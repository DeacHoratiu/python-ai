from pydantic import BaseModel, Field, ConfigDict

class FileNameValidator(BaseModel):
    name: str = Field(description="Name of the text file in this project.")

class FileSummaryValidator(BaseModel):
    """This validator can validate the output of an agent, the JSON returned by the summary agent."""

    title: str = Field(description="Generated title for the file.")
    summary: str = Field(description="Summary of the file.")

class DocAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra = "forbid")

    file_name: str = Field(description="The name of the file to analyze.")
    words: list[str] = Field(description="A list of words to analyze and count.")

class DocAnalysisReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    file_name: str
    word_count: int
    matches: dict[str, int]
