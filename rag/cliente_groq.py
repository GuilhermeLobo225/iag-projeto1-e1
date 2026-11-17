"""Cliente mínimo da API do Groq (compatível com a da OpenAI), para o juiz gpt-oss-120b.

- A chave lê-se do .env (GROQ_API_KEY) e nunca se escreve em código, em logs nem na cache.
- Limites do nível gratuito: 30 pedidos/min, 1 000 pedidos/dia, 8 000 tokens/min e 200 000 tokens/dia. Os
  cabeçalhos x-ratelimit-* de cada resposta dizem o que resta (pedidos do dia e tokens do minuto); o limite diário
  de tokens só aparece na mensagem do erro 429.
- Espera pelo menos INTERVALO s entre pedidos (fica abaixo dos 30/min) e, se os tokens do minuto não chegarem para
  o pedido seguinte, espera pelo reset. No 429 espera o retry-after; se o 429 for de um limite diário, levanta
  LimiteDiario, para a corrida parar de forma limpa.
- Cada resposta fica em cache/groq/<sha1 do pedido>.json (fora do git): o mesmo pedido nunca se paga duas vezes.
- Cada pedido pago fica em cache/groq/uso.jsonl: hora, tokens de entrada, de saída e de raciocínio.
"""
import hashlib
import json
import os
import re
import time
from datetime import datetime

import httpx
from dotenv import load_dotenv

import comum

URL = "https://api.groq.com/openai/v1/chat/completions"
CACHE = comum.RAIZ / "cache/groq"
INTERVALO = 2.5  # segundos entre pedidos
LIMITES = {"pedidos_min": 30, "pedidos_dia": 1000, "tokens_min": 8000, "tokens_dia": 200000}

_ultimo = 0.0
estado = {}  # os últimos cabeçalhos de limites, sem a chave


class LimiteDiario(Exception):
    pass


class RespostaInvalida(Exception):
    """O Groq valida o JSON contra o esquema e devolve 400 (json_validate_failed) quando o modelo falha."""


def _chave():
    load_dotenv(comum.RAIZ / ".env")
    chave = os.environ.get("GROQ_API_KEY")
    if not chave:
        raise RuntimeError("falta GROQ_API_KEY no .env")
    return chave


def _segundos(v):
    """'7.66s', '2m59.56s', '1h2m3s' ou '120ms' → segundos."""
    if not v:
        return 0.0
    if v.endswith("ms"):
        return float(v[:-2]) / 1000
    total = 0.0
    for n, u in re.findall(r"([\d.]+)([hms])", v):
        total += float(n) * {"h": 3600, "m": 60, "s": 1}[u]
    return total


def _limpa(msg):
    return re.sub(r"organization `[^`]*`", "organization `…`", msg)  # não guarda o id da organização


def uso_hoje():
    """Tokens e pedidos pagos hoje (pela hora local), a partir de cache/groq/uso.jsonl."""
    caminho, hoje = CACHE / "uso.jsonl", datetime.now().date().isoformat()
    linhas = [x for x in comum.le_jsonl(caminho) if x["hora"].startswith(hoje)] if caminho.exists() else []
    return {"pedidos": len(linhas), "tokens": sum(x["tokens_total"] for x in linhas)}


def pede(corpo, tokens_previstos=5000):
    """Resposta da API ao corpo dado (dict no formato da OpenAI). Devolve (resposta, veio_da_cache)."""
    global _ultimo
    sha = hashlib.sha1(json.dumps(corpo, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    caminho = CACHE / f"{sha}.json"
    if caminho.exists():
        return json.loads(caminho.read_text(encoding="utf-8"))["resposta"], True
    CACHE.mkdir(parents=True, exist_ok=True)
    falhas = 0
    while True:
        espera = INTERVALO - (time.monotonic() - _ultimo)
        if estado.get("tokens_restantes_min") is not None and estado["tokens_restantes_min"] < tokens_previstos:
            espera = max(espera, estado["tokens_reset_s"] - (time.monotonic() - estado["quando"]) + 0.5)
        if espera > 0:
            time.sleep(espera)
        _ultimo = time.monotonic()
        try:
            r = httpx.post(URL, headers={"Authorization": f"Bearer {_chave()}"}, json=corpo, timeout=300)
        except httpx.TransportError:
            falhas += 1
            if falhas > 3:
                raise
            time.sleep(10)
            continue
        h = r.headers
        if "x-ratelimit-remaining-tokens" in h:
            estado.update({"quando": time.monotonic(), "pedidos_restantes_dia": int(h.get("x-ratelimit-remaining-requests", -1)),
                           "pedidos_limite_dia": int(h.get("x-ratelimit-limit-requests", -1)),
                           "tokens_restantes_min": int(h["x-ratelimit-remaining-tokens"]),
                           "tokens_limite_min": int(h.get("x-ratelimit-limit-tokens", -1)),
                           "tokens_reset_s": _segundos(h.get("x-ratelimit-reset-tokens"))})
        if r.status_code == 429:
            msg = _limpa(r.json().get("error", {}).get("message", ""))
            if "per day" in msg or "(TPD)" in msg or "(RPD)" in msg:
                raise LimiteDiario(msg)
            time.sleep(float(h.get("retry-after", 10)) + 0.5)
            continue
        if r.status_code >= 500:
            falhas += 1
            if falhas > 3:
                r.raise_for_status()
            time.sleep(15)
            continue
        if r.status_code == 400 and "json_validate_failed" in r.text:
            with open(CACHE / "uso.jsonl", "a", encoding="utf-8", newline="\n") as f:  # gastou tokens, mas não há contagem
                f.write(json.dumps({"hora": datetime.now().isoformat(timespec="seconds"), "pedido": sha,
                                    "erro": "json_validate_failed", "tokens_total": 0}) + "\n")
            raise RespostaInvalida(_limpa(r.text[:300]))
        if r.status_code != 200:
            raise RuntimeError(f"Groq: erro {r.status_code}: {_limpa(r.text[:500])}")
        dados = r.json()
        u = dados.get("usage", {})
        caminho.write_text(json.dumps({"hora": datetime.now().isoformat(timespec="seconds"), "resposta": dados},
                                      ensure_ascii=False) + "\n", encoding="utf-8")
        with open(CACHE / "uso.jsonl", "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps({"hora": datetime.now().isoformat(timespec="seconds"), "pedido": sha,
                                "tokens_in": u.get("prompt_tokens"), "tokens_out": u.get("completion_tokens"),
                                "tokens_raciocinio": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
                                "tokens_total": u.get("total_tokens", 0)}) + "\n")
        return dados, False
