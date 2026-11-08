"""Os 4 casos de teste das decisões de 20/10 (ponto 6), mais os grupos e as perguntas sem resposta.

Uso, na raiz do repositório: .venv\\Scripts\\python -m pytest
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "rag"))
from metricas import acerta, avalia, resumo  # noqa: E402


def x(doc, start, end):
    return {"doc_id": f"E1-{doc:03d}", "start": start, "end": end}


def test_caso_1_factual():
    trechos = [x(2, 1000, 1300)]
    recuperados = [x(5, 0, 2000), x(2, 1200, 3200), x(2, 900, 2900), x(1, 0, 2000), x(9, 0, 2000)]
    assert not acerta(recuperados[1], trechos[0])  # sobrepõe 100 < 150
    assert acerta(recuperados[2], trechos[0])      # sobrepõe 300
    r = avalia(trechos, recuperados)
    assert r["recall_at_5"] == 1 and r["rr"] == pytest.approx(1 / 3) and r["hit_ranks"] == [3]


def test_caso_2_multi_doc():
    trechos = [x(3, 500, 800), x(7, 2000, 2200)]
    recuperados = [x(7, 1800, 2700), x(1, 0, 900), x(4, 0, 900), x(7, 2600, 3500), x(2, 0, 900)]
    r = avalia(trechos, recuperados)
    assert r["recall_at_5"] == 0.5 and r["rr"] == 1 and r["cobertura_total"] == 0


def test_caso_3_trecho_longo():
    assert acerta(x(4, 600, 1450), x(4, 0, 1500))  # 850 ≥ 0,5 × 850


def test_caso_4_so_toca():
    assert not acerta(x(6, 2200, 3050), x(6, 3000, 3400))  # 50 < 200


def test_mesmo_intervalo_noutro_documento_nao_acerta():
    assert not acerta(x(1, 0, 500), x(2, 0, 500))


def test_grupo_conta_uma_vez():
    trechos = [x(1, 0, 300) | {"group": 1}, x(3, 0, 300) | {"group": 1}]
    assert avalia(trechos, [x(3, 0, 400)])["recall_at_5"] == 1
    assert avalia(trechos, [x(1, 0, 400), x(3, 0, 400)])["recall_at_5"] == 1


def test_so_conta_os_5_primeiros():
    r = avalia([x(1, 0, 300)], [x(9, 0, 10)] * 5 + [x(1, 0, 300)])
    assert r["recall_at_5"] == 0 and r["rr"] == 0


def test_sem_resposta_fica_fora_das_medias():
    rs = [{"type": "factual"} | avalia([x(1, 0, 300)], [x(1, 0, 300)]),
          {"type": "unanswerable"} | avalia([], [x(1, 0, 300)])]
    assert rs[1]["recall_at_5"] is None
    assert resumo(rs) == {"perguntas": 1, "recall_at_5": 1, "mrr_at_5": 1, "recall_at_5_factual": 1, "mrr_at_5_factual": 1}
