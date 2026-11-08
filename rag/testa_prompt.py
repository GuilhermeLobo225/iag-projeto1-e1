#!/usr/bin/env python3
"""Teste do prompt de geração com 2 perguntas inventadas (não são das 15), antes de o congelar.

Uma tem resposta na base (o compostor doméstico é gratuito para quem adere ao projeto, E1-002) e outra não
(o preço de uma reparação num Repair Café de Guimarães). Recupera os 5 primeiros excertos com o melhor embedding
do teste (Qwen3-Embedding 8B na A) e mostra a resposta de cada LLM com as verificações automáticas.

Uso, na raiz do repositório (com o Ollama a correr):
  .venv\\Scripts\\python rag/testa_prompt.py
"""
import comum
import embeddings
import geracao
import indice

PERGUNTAS = ["Em Guimarães, tenho de pagar o compostor se quiser fazer compostagem em casa?",
             "Quanto custa uma reparação no Repair Café de Guimarães?"]
EMBEDDING, CONFIG = "qwen3-embedding-8b", "A"


def main():
    comum.prepara_consola()
    por_id = {x["chunk_id"]: x for x in comum.le_jsonl(comum.EXPERIENCIAS / f"excertos_{CONFIG}.jsonl")}
    col = indice.cliente().get_collection(indice.nome_colecao(EMBEDDING, CONFIG))
    contextos = [[por_id[r["chunk_id"]] for r in indice.pesquisa(col, v, 5)]
                 for v in embeddings.embeda(EMBEDDING, PERGUNTAS, "query")]
    for pergunta, excertos in zip(PERGUNTAS, contextos):
        print(f"\n##### {pergunta}\nExcertos: {', '.join(x['chunk_id'] for x in excertos)}")
        for modelo in geracao.LLMS:
            r = geracao.responde(modelo, pergunta, excertos)
            v = geracao.verifica(r["answer"], excertos)
            print(f"\n=== {modelo} ({r['tokens_in']} tokens de entrada, {r['tokens_out']} de saída, {r['latency_s']} s, "
                  f"fim: {r['done_reason']}) | abstenção {v['abstained']} | citados {v['cited_doc_ids']} | "
                  f"fora dos excertos {v['citations_outside_context']} | mal escritas {v['malformed_citations']}")
            print(r["answer"].strip())


if __name__ == "__main__":
    main()
