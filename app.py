import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent / "src"))
load_dotenv()

from rag import responder  # noqa: E402

app = FastAPI(title="Assistente RAG de Documentos", version="1.0")


class Pergunta(BaseModel):
    pergunta: str = Field(min_length=3)
    k: int = Field(default=4, ge=1, le=10)


@app.post("/perguntar")
def perguntar(p: Pergunta) -> dict:
    return responder(p.pergunta, p.k)


@app.get("/saude")
def saude() -> dict:
    return {"status": "ok"}
