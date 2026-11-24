"""Divisão de texto em trechos com sobreposição, respeitando parágrafos."""
from __future__ import annotations


def dividir(texto: str, tamanho: int = 800, sobreposicao: int = 150) -> list[str]:
    if sobreposicao >= tamanho:
        raise ValueError("sobreposicao deve ser menor que tamanho")
    paragrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    trechos: list[str] = []
    atual = ""
    for p in paragrafos:
        if len(atual) + len(p) + 2 <= tamanho:
            atual = f"{atual}\n\n{p}" if atual else p
            continue
        if atual:
            trechos.append(atual)
            atual = atual[-sobreposicao:] + "\n\n" + p if sobreposicao else p
        else:
            atual = p
        # parágrafo maior que o limite: corta em janelas
        while len(atual) > tamanho:
            trechos.append(atual[:tamanho])
            atual = atual[tamanho - sobreposicao :]
    if atual:
        trechos.append(atual)
    return trechos
