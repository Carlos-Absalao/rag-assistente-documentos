"""Recuperação + geração."""
from __future__ import annotations

import os

SISTEMA = (
    "Você é um assistente que responde em português usando APENAS o contexto fornecido. "
    "Cite as fontes no formato [n]. Se a resposta não estiver no contexto, diga: "
    "'Não encontrei essa informação nos documentos.'"
)


def montar_prompt(pergunta: str, trechos: list[dict]) -> list[dict]:
    contexto = "\n\n".join(f"[{i + 1}] ({t['arquivo']})\n{t['texto']}" for i, t in enumerate(trechos))
    return [
        {"role": "system", "content": SISTEMA},
        {"role": "user", "content": f"Contexto:\n{contexto}\n\nPergunta: {pergunta}"},
    ]


def recuperar(pergunta: str, k: int = 4) -> list[dict]:
    from store import colecao

    res = colecao().query(query_texts=[pergunta], n_results=k)
    return [
        {"texto": doc, "arquivo": meta["arquivo"], "trecho": meta["trecho"], "score": round(1 - dist, 3)}
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


def responder(pergunta: str, k: int = 4) -> dict:
    from openai import OpenAI

    trechos = recuperar(pergunta, k)
    client = OpenAI(base_url=os.getenv("LLM_BASE_URL"), api_key=os.getenv("LLM_API_KEY", "ollama"))
    resp = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "llama3.1"),
        messages=montar_prompt(pergunta, trechos),
        temperature=0.1,
    )
    return {
        "resposta": resp.choices[0].message.content,
        "fontes": [{k: t[k] for k in ("arquivo", "trecho", "score")} for t in trechos],
    }
