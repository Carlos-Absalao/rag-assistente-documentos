"""Indexa documentos de uma pasta no ChromaDB."""
import sys
from pathlib import Path

from chunking import dividir
from store import colecao


def ler_arquivo(caminho: Path) -> str:
    if caminho.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        return "\n\n".join(p.extract_text() or "" for p in PdfReader(caminho).pages)
    return caminho.read_text(encoding="utf-8")


def indexar(pasta: str) -> int:
    col = colecao()
    total = 0
    for arq in sorted(Path(pasta).glob("**/*")):
        if arq.suffix.lower() not in {".md", ".txt", ".pdf"}:
            continue
        trechos = dividir(ler_arquivo(arq))
        col.upsert(
            ids=[f"{arq.name}::{i}" for i in range(len(trechos))],
            documents=trechos,
            metadatas=[{"arquivo": arq.name, "trecho": i} for i in range(len(trechos))],
        )
        total += len(trechos)
        print(f"{arq.name}: {len(trechos)} trechos")
    return total


if __name__ == "__main__":
    print(f"Total indexado: {indexar(sys.argv[1] if len(sys.argv) > 1 else 'data/docs')}")
