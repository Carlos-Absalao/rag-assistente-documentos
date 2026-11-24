import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from chunking import dividir  # noqa: E402
from rag import montar_prompt  # noqa: E402


def test_dividir_respeita_tamanho():
    texto = "\n\n".join(["parágrafo " * 30] * 10)
    trechos = dividir(texto, tamanho=400, sobreposicao=50)
    assert len(trechos) > 1
    assert all(len(t) <= 400 for t in trechos)


def test_dividir_texto_curto_vira_um_trecho():
    assert dividir("um\n\ndois", tamanho=100, sobreposicao=10) == ["um\n\ndois"]


def test_sobreposicao_invalida():
    with pytest.raises(ValueError):
        dividir("x", tamanho=10, sobreposicao=10)


def test_prompt_numera_fontes():
    msgs = montar_prompt("Qual a vigência?", [{"arquivo": "a.md", "texto": "1 ano"}])
    assert msgs[0]["role"] == "system"
    assert "[1] (a.md)" in msgs[1]["content"]
