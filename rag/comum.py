"""Coisas comuns aos scripts do pipeline do E1: caminhos, catálogo, texto dos documentos e tokenizador."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CATALOGO = RAIZ / "kb/E1/catalog_E1.jsonl"
PERGUNTAS = RAIZ / "tests/questions_E1.jsonl"
EXPERIENCIAS = RAIZ / "experiments/E1"

# Os tokens contam-se com o tokenizador do bge-m3 (proposta de 30/10), sem tokens especiais.
# A revisão fica fixa para a contagem ser a mesma em qualquer máquina.
TOKENIZADOR = "BAAI/bge-m3"
TOKENIZADOR_REVISAO = "5617a9f61b028005a4858fdac845db406aefb181"


def le_jsonl(caminho):
    return [json.loads(linha) for linha in Path(caminho).read_text(encoding="utf-8").splitlines() if linha.strip()]


def grava_jsonl(caminho, objetos):
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as f:
        for o in objetos:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")


def le_catalogo():
    return le_jsonl(CATALOGO)


def le_documento(entrada):
    """Texto exato do .txt de uma entrada do catálogo (sem converter fins de linha) e o SHA-1 dos bytes."""
    dados = (RAIZ / entrada["text_file"]).read_bytes()
    return dados.decode("utf-8"), hashlib.sha1(dados).hexdigest()


def carrega_tokenizador():
    """Só o tokenizador (cerca de 17 MB na primeira vez, guardado na cache do Hugging Face), sem o modelo."""
    from tokenizers import Tokenizer
    return Tokenizer.from_pretrained(TOKENIZADOR, revision=TOKENIZADOR_REVISAO)


def contador(tokenizador):
    return lambda texto: len(tokenizador.encode(texto, add_special_tokens=False).ids)


def commit_git():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def versao_ollama():
    import urllib.request
    with urllib.request.urlopen("http://127.0.0.1:11434/api/version", timeout=5) as r:
        return json.load(r)["version"]


def prepara_consola():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
