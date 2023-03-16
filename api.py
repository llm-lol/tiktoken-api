# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import tiktoken

app = FastAPI()


class InputData(BaseModel):
    model_name: str
    text: str


class OutputData(BaseModel):
    status: str
    error: Optional[str] = None
    token_count: int


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


@app.post("/token_count", response_model=OutputData)
async def get_token_count(data: InputData):
    try:
        token_count = num_tokens_from_string(data.text, data.model_name)
        return {"status": "success", "token_count": token_count}
    except Exception as e:
        return {"status": "error", "token_count": 0, "error": str(e)}
