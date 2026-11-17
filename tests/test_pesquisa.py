"""O exemplo do RRF das decisões de 20/10 (ponto 7.4) e o BM25 num caso pequeno.

Uso, na raiz do repositório: .venv\\Scripts\\python -m pytest
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "rag"))
from bm25 import BM25  # noqa: E402
from pesquisa import rrf  # noqa: E402


def lista(ids):
    return [{"rank": r, "chunk_id": c, "doc_id": "E1-001", "start": 0, "end": 1} for r, c in enumerate(ids, start=1)]


def test_exemplo_de_20_10():
    # denso [c7, c2, c9, c4, c1] e BM25 [c2, c5, c7, c8, c3]: c2 (1/62 + 1/61) fica à frente de c7 (1/61 + 1/63)
    f = rrf(lista(["c7", "c2", "c9", "c4", "c1"]), lista(["c2", "c5", "c7", "c8", "c3"]))
    assert [x["chunk_id"] for x in f[:2]] == ["c2", "c7"]
    assert f[0]["score"] == pytest.approx(1 / 62 + 1 / 61, abs=1e-6)
    assert f[1]["score"] == pytest.approx(1 / 61 + 1 / 63, abs=1e-6)


def test_empate_resolvido_pela_densa():
    # c4 (4.º na densa) e c8 (4.º no BM25) empatam com 1/64; ganha o que está na densa
    f = [x["chunk_id"] for x in rrf(lista(["c7", "c2", "c9", "c4", "c1"]), lista(["c2", "c5", "c7", "c8", "c3"]))]
    assert f.index("c4") < f.index("c8")


def test_bm25_prefere_o_texto_com_os_termos():
    b = BM25(["O óleo alimentar usado vai para o oleão.", "As pilhas vão para o pilhão.", "Texto sem nada a ver."])
    assert b.topo("Onde ponho o óleo alimentar?", 3)[0][0] == 0
    assert all(i != 2 for i, _ in b.topo("óleo alimentar", 3))  # pontuação 0 fica de fora
