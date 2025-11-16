import random
import unicodedata
import re


# ---------------- Problemas base -----------------
PROBLEMAS = {
    "alto_tempo_espera": 3,           # peso base
    "cancelamentos_frequentes": 4,
    "inseguranca": 5,
    "preco_inconsistente": 2,
    "motorista_desconhece_rota": 3,
}

# ---------------- Soluções -----------------
SOLUCOES = {
    "alto_tempo_espera": [
        "Otimizar algoritmo de alocação",
        "Incentivar motoristas em horários críticos",
        "Usar previsão preditiva de demanda"
    ],
    "cancelamentos_frequentes": [
        "Incentivos temporários e penalidades graduais",
        "Melhores estimativas de rota e tempo",
        "Treinamento rápido de motoristas"
    ],
    "inseguranca": [
        "Implementar botão de emergência",
        "Rotas seguras",
        "Aumentar monitoramento e suporte 24/7"
    ],
    "preco_inconsistente": [
        "Ajustar modelo de precificação com oferta/demanda",
        "Considerar clima e eventos",
        "Alertas de preço para usuários"
    ],
    "motorista_desconhece_rota": [
        "Integração com APIs de mapas",
        "Treinamento rápido",
        "Sugestões de rotas no app"
    ]
}

# ---------------- Descrições gerais -----------------
DESCRICOES = {
    "alto_tempo_espera": "demora espera tempo de espera motorista demora chegada lenta",
    "cancelamentos_frequentes": "cancelar cancelamentos motorista cancela recusa corrida",
    "inseguranca": "assalto perigoso inseguro risco medo seguranca",
    "preco_inconsistente": "preco tarifa variacao promocao valor inconsistente",
    "motorista_desconhece_rota": "rota desconhece perdida nao sabe o caminho gps mapa",
}

# ---------------- SINÔNIMOS EXTENSOS (sua lista completa) -----------------
SINONIMOS = {

    # ALTO TEMPO DE ESPERA
    "tempo de espera": "alto_tempo_espera",
    "demora": "alto_tempo_espera",
    "muito tempo": "alto_tempo_espera",
    "ta demorando": "alto_tempo_espera",
    "tá demorando": "alto_tempo_espera",
    "espera muito": "alto_tempo_espera",
    "demorando muito": "alto_tempo_espera",
    "fila grande": "alto_tempo_espera",
    "fila enorme": "alto_tempo_espera",
    "fila demorando": "alto_tempo_espera",
    "demora para chegar": "alto_tempo_espera",
    "demorou para chegar": "alto_tempo_espera",
    "espera longa": "alto_tempo_espera",
    "cadê o motorista": "alto_tempo_espera",
    "motorista demorando": "alto_tempo_espera",
    "aguardando muito": "alto_tempo_espera",
    "tempo alto": "alto_tempo_espera",
    "demorando demais": "alto_tempo_espera",

    # CANCELAMENTOS
    "cancelamento": "cancelamentos_frequentes",
    "cancelou": "cancelamentos_frequentes",
    "motorista cancela": "cancelamentos_frequentes",
    "motorista cancelou": "cancelamentos_frequentes",
    "cancelou a corrida": "cancelamentos_frequentes",
    "recusou corrida": "cancelamentos_frequentes",
    "motorista recusou": "cancelamentos_frequentes",
    "recusou": "cancelamentos_frequentes",
    "nao apareceu": "cancelamentos_frequentes",
    "não apareceu": "cancelamentos_frequentes",
    "desistiu": "cancelamentos_frequentes",
    "motorista desistiu": "cancelamentos_frequentes",
    "cancelam muito": "cancelamentos_frequentes",
    "cancelando toda hora": "cancelamentos_frequentes",
    "fica cancelando": "cancelamentos_frequentes",

    # INSEGURANÇA
    "assalto": "inseguranca",
    "assaltaram": "inseguranca",
    "risco de assalto": "inseguranca",
    "perigoso": "inseguranca",
    "perigo": "inseguranca",
    "zona perigosa": "inseguranca",
    "local perigoso": "inseguranca",
    "area perigosa": "inseguranca",
    "área perigosa": "inseguranca",
    "medo": "inseguranca",
    "riscos": "inseguranca",
    "inseguro": "inseguranca",
    "inseguranca": "inseguranca",
    "não é seguro": "inseguranca",
    "nao e seguro": "inseguranca",
    "violento": "inseguranca",
    "violencia": "inseguranca",
    "tentativa de assalto": "inseguranca",
    "perigo na rota": "inseguranca",

    # MOTORISTA PERDIDO
    "nao conhece a rota": "motorista_desconhece_rota",
    "não conhece a rota": "motorista_desconhece_rota",
    "nao sabe a rota": "motorista_desconhece_rota",
    "não sabe a rota": "motorista_desconhece_rota",
    "se perdeu": "motorista_desconhece_rota",
    "motorista perdido": "motorista_desconhece_rota",
    "perdido": "motorista_desconhece_rota",
    "errou o caminho": "motorista_desconhece_rota",
    "erro de rota": "motorista_desconhece_rota",
    "gps bugou": "motorista_desconhece_rota",
    "gps falhou": "motorista_desconhece_rota",
    "pegou caminho errado": "motorista_desconhece_rota",
    "nao sabe o caminho": "motorista_desconhece_rota",
    "não sabe o caminho": "motorista_desconhece_rota",
    "nao conhece o caminho": "motorista_desconhece_rota",
    "motorista desinformado": "motorista_desconhece_rota",
    "confundiu a rota": "motorista_desconhece_rota",
}


# ---------------- NORMALIZADOR -----------------
def limpar(texto: str):
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFKD', texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return re.sub(r"\s+", " ", texto)


# ---------------- INTERPRETAÇÃO DO PROBLEMA -----------------
def identificar_problema(texto):
    t = limpar(texto)

    # 1) Verifica sinônimos primeiro
    for chave, problema in SINONIMOS.items():
        if chave in t:
            return problema

    # 2) fallback via bag-of-words (leve)
    melhor = None
    melhor_score = 0

    for problema, desc in DESCRICOES.items():
        score = sum(1 for p in desc.split() if p in t)
        if score > melhor_score:
            melhor_score = score
            melhor = problema

    return melhor if melhor_score > 0 else None


# ---------------- IA PRINCIPAL -----------------
class IAMobilidade:

    def analisar(self, lista):
        contagem = {}
        nao_identificados = []

        # Conta quantos problemas aparecem
        for item in lista:
            problema = identificar_problema(item)
            if problema:
                contagem[problema] = contagem.get(problema, 0) + 1
            else:
                nao_identificados.append(item)

        # Se nada foi identificado
        if not contagem:
            return (
                "Nenhum problema identificado.\n\n"
                + ("Itens não identificados:\n" + "\n".join(f"- {x}" for x in nao_identificados)
                    if nao_identificados else "")
            )

        # Calcula prioridade = peso base × frequência
        ranking = []
        for problema, freq in contagem.items():
            peso = PROBLEMAS[problema]
            ranking.append((peso * freq, problema))

        ranking.sort(reverse=True)

        # Seleciona top 2
        melhores = [p for _, p in ranking[:2]]

        # Sorteia solução para cada um dos dois melhores
        solucoes_finais = [random.choice(SOLUCOES[p]) for p in melhores]

        # -------------------------
        # FORMATA RESULTADO PRA TEXTO
        # -------------------------
        texto = "Sugestões Prioritárias:\n"
        for p, s in zip(melhores, solucoes_finais):
            texto += f"- {p.replace('_', ' ').title()}: {s}\n"

        if nao_identificados:
            texto += "\nItens não identificados:\n"
            texto += "\n".join(f"- {x}" for x in nao_identificados)

        return texto
