import random
import unicodedata
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64


# ============================================================
# -------------------- FUZZY MATCH ---------------------------
# ============================================================

def similar(a, b):
    """Calcula similaridade aproximada entre strings."""
    a, b = a.lower(), b.lower()
    matches, i, j = 0, 0, 0

    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            matches += 1
            j += 1
        i += 1

    return (matches / len(b)) * 100 if b else 0


def fuzzy_contains(text, keyword, threshold=70):
    """Verifica se existe palavra similar dentro do texto."""
    return any(similar(w, keyword) >= threshold for w in text.split())


# ============================================================
# ----------------------- DADOS -------------------------------
# ============================================================

PROBLEMAS = {
    "alto_tempo_espera": 1,
    "cancelamentos_frequentes": 4,
    "inseguranca": 5,
    "preco_inconsistente": 2,
    "motorista_desconhece_rota": 1,
    "stress_saude": 2,
    "falta_de_suporte": 3,
}

SOLUCOES = {
    "alto_tempo_espera": [
        "Otimizar algoritmo de alocação",
        "Incentivar motoristas em horários críticos",
        "Usar previsão preditiva de demanda",
        "Implementar fila inteligente por proximidade real e não apenas raio geográfico",
        "Criar zonas de alta demanda com bônus automático para motoristas",
        "Exibir no app a previsão de tempo de espera antes do pedido ser confirmado",
        "Redistribuir motoristas ociosos para áreas de baixa cobertura",
        "Implementar roteamento dinâmico para que motoristas finalizando corridas recebam corridas próximas",
        "Ajustar tarifas automaticamente para atrair mais motoristas a regiões críticas",
        "Criar pontos de espera sugeridos com dados históricos de chamada",
    ],

    "cancelamentos_frequentes": [
        "Incentivos temporários e penalidades graduais",
        "Melhores estimativas de rota e tempo",
        "Treinamento rápido de motoristas",
        "Melhorar comunicação em tempo real entre motorista e passageiro",
        "Identificar padrões de cancelamento e agir com políticas específicas",
        "Criar sistema de bloqueio temporário para motoristas com cancelamentos excessivos",
        "Mostrar informações detalhadas da corrida antes de o motorista aceitá-la",
        "Ajustar penalidades de cancelamento conforme o motivo relatado",
        "Apertar regras para evitar pedidos duplicados",
        "Enviar notificações preventivas quando o tempo de chegada exceder o previsto",
    ],

    "inseguranca": [
        "Implementar botão de emergência",
        "Rotas seguras",
        "Aumentar monitoramento e suporte 24/7",
        "Gravação de áudio ativa durante corridas para auditoria",
        "Verificação reforçada de motoristas com checagem anual",
        "Compartilhamento automático de rota com contato de confiança",
        "Detecção automática de paradas incomuns com alerta para suporte",
        "Botão de emergência dedicado para motoristas",
        "Implementar rating específico de segurança separado da avaliação geral",
        "Mapear zonas de risco e ajustar rotas automaticamente",
    ],

    "preco_inconsistente": [
        "Ajustar modelo de precificação com oferta/demanda",
        "Considerar clima e eventos",
        "Alertas de preço para usuários",
        "Transparentizar fatores que influenciam o preço",
        "Mostrar histórico de preço da mesma rota",
        "Implantar limites máximos para tarifa dinâmica",
        "Criar assinatura mensal com preços estáveis",
        "Mostrar alternativas mais baratas próximas",
        "Relatórios semanais para motoristas otimizarem estratégia",
        "Correção automática para tarifas fora do padrão",
    ],

    "motorista_desconhece_rota": [
        "Integração com APIs de mapas",
        "Treinamento rápido",
        "Sugestões de rotas no app",
        "Criar sistema de navegação interno ao app",
        "Enviar trechos críticos da rota antes da corrida",
        "Mapear áreas com histórico de erros de navegação",
        "Permitir referência enviada pelo passageiro",
        "Atualizações frequentes de mapa",
        "Sugestão automática de rotas alternativas",
        "Modo de simulação de trajeto para novos motoristas",
    ],

    "stress_saude": [
        "Criar pausas programadas obrigatórias",
        "Oferecer suporte psicológico mensal",
        "Implementar flexibilidade inteligente",
        "Alertas de fadiga com base em horas dirigidas",
        "Programa de bem-estar com dicas de saúde",
        "Parcerias com academias e clínicas",
        "Monitoramento de carga de trabalho",
        "Campanhas sobre ergonomia e postura",
        "Suporte 24/7 para motoristas",
        "Assistente no app com recomendações pessoais",
    ],

    "falta_de_suporte": [
        "Ampliar atendimento humano 24/7",
        "Criar chatbot inteligente",
        "Treinamento contínuo para equipe",
        "Painel para rastrear solicitações",
        "Atendimento prioritário para casos críticos",
        "Central para motoristas iniciantes",
        "Programa de mentoria",
        "Tutoriais interativos",
        "Feedback pós-atendimento",
        "Expandir suporte local em regiões críticas",
    ],
}

DESCRICOES = {
    "alto_tempo_espera": 
        "atraso demora esperando lentidao tempo_espera espera_longa demorado",
    "cancelamentos_frequentes": 
        "cancelamento cancelou recusou desistencias cancela muito interrupcao",
    "inseguranca": 
        "assalto perigoso risco medo inseguro violencia tentativa comportamento",
    "preco_inconsistente": 
        "preco tarifa variacao preco_alto preco_baixo oscilando inconsistente",
    "motorista_desconhece_rota": 
        "rota_errada perdido caminho_errado gps_bug confusa trajeto_errado",
    "stress_saude": 
        "mal cansado exausto estressado sobrecarregado mal_estar desgaste",
    "falta_de_suporte": 
        "sem_suporte sem_ajuda ninguem_responde atendimento_ruim sem_retorno",
}

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
    "cancelou": "cancelamentos_frequentes",
    "canceloou": "cancelamentos_frequentes",
    "cancelaram": "cancelamentos_frequentes",
    "motorista cancelou": "cancelamentos_frequentes",
    "recusou": "cancelamentos_frequentes",
    "recusa corrida": "cancelamentos_frequentes",
    "desistencia": "cancelamentos_frequentes",

    # INSEGURANÇA
    "assalto": "inseguranca",
    "assaltaram": "inseguranca",
    "perigoso": "inseguranca",
    "perigo": "inseguranca",
    "inseguro": "inseguranca",
    "risco": "inseguranca",
    "violencia": "inseguranca",
    "medo": "inseguranca",

    # PREÇO
    "preco alto": "preco_inconsistente",
    "preço alto": "preco_inconsistente",
    "tarifa alta": "preco_inconsistente",
    "caro": "preco_inconsistente",
    "aumentou": "preco_inconsistente",
    "subiu": "preco_inconsistente",

    # ROTA
    "perdido": "motorista_desconhece_rota",
    "perdida": "motorista_desconhece_rota",
    "nao sabe o caminho": "motorista_desconhece_rota",
    "não sabe o caminho": "motorista_desconhece_rota",
    "gps bugou": "motorista_desconhece_rota",
    "gps errado": "motorista_desconhece_rota",

    # STRESS / SAÚDE
    "to mal": "stress_saude",
    "tô mal": "stress_saude",
    "tô cansado": "stress_saude",
    "to cansado": "stress_saude",
    "estressado": "stress_saude",
    "exausto": "stress_saude",
    "sobrecarregado": "stress_saude",
    "mal estar": "stress_saude",

    # FALTA DE SUPORTE
    "sem suporte": "falta_de_suporte",
    "sem ajuda": "falta_de_suporte",
    "ninguem responde": "falta_de_suporte",
    "atendimento ruim": "falta_de_suporte",
    "nao respondem": "falta_de_suporte",
    "não respondem": "falta_de_suporte",
    "preciso de ajuda": "falta_de_suporte",
}




# ============================================================
# ------------------ FUNÇÕES DE APOIO ------------------------
# ============================================================

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return re.sub(r"\s+", " ", texto)


def avaliar_descricoes(texto, problema, lista_descricoes):
    """Retorna score baseado em matches e fuzzy."""
    score = 0
    for termo in lista_descricoes.split():
        if termo in texto or fuzzy_contains(texto, termo):
            score += 1
    return score


def melhor_problema_por_descricoes(texto):
    """Seleciona o problema com maior score."""
    melhor, melhor_score = None, 0

    for problema, descricao in DESCRICOES.items():
        score = avaliar_descricoes(texto, problema, descricao)
        if score > melhor_score:
            melhor, melhor_score = problema, score

    return melhor if melhor_score > 0 else None


def problema_por_sinonimos(texto):
    """Verifica sinônimos diretamente."""
    for chave, problema in SINONIMOS.items():
        if chave in texto or fuzzy_contains(texto, chave):
            return problema
    return None


# ============================================================
# ------------------ IDENTIFICADOR PRINCIPAL -----------------
# ============================================================

def identificar_problema(texto):
    texto = normalizar(texto)

    problema = problema_por_sinonimos(texto)
    if problema:
        return problema

    return melhor_problema_por_descricoes(texto)


# ============================================================
# ---------------------- IA PRINCIPAL -------------------------
# ============================================================

class IAMobilidade:

    def analisar(self, lista):
        contagem = {}
        nao_identificados = []

        for item in lista:
            problema = identificar_problema(item)
            if problema:
                contagem[problema] = contagem.get(problema, 0) + 1
            else:
                nao_identificados.append(item)

        if not contagem:
            return self._saida_nenhum(nao_identificados)

        return self._saida_com_problemas(contagem, nao_identificados)

    # ----------------- Saídas formatadas -----------------

    def _saida_nenhum(self, nao_identificados):
        texto = "Nenhum problema identificado.\n"
        if nao_identificados:
            texto += "\nItens não identificados:\n"
            texto += "\n".join(f"- {x}" for x in nao_identificados)
        return texto

    def _saida_com_problemas(self, contagem, nao_identificados):
        ranking = sorted(
            ((PROBLEMAS[p] * f, p) for p, f in contagem.items()),
            reverse=True
        )

        melhores = [p for _, p in ranking[:2]]
        solucoes = [random.choice(SOLUCOES[p]) for p in melhores]

        texto = "Sugestões Prioritárias:\n"
        for p, s in zip(melhores, solucoes):
            texto += f"- {p.replace('_', ' ').title()}: {s}\n"

        if nao_identificados:
            texto += "\nItens não identificados:\n"
            texto += "\n".join(f"- {x}" for x in nao_identificados)

        # ============================================================
        # ---------------------- GRÁFICO DE PIZZA ---------------------
        # ============================================================

        labels = [p.replace("_", " ").title() for p in contagem.keys()]
        values = [PROBLEMAS[p] * contagem[p] for p in contagem.keys()]

        fig, ax = plt.subplots(figsize=(4,4))
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        cores = ["#4da6ff", "#1a75ff", "#003d99", "#66b3ff", "#3385ff", "#0059b3"]

        wedges, texts, autotexts = ax.pie(
            values,
            colors=cores[:len(values)],
            labels=None,
            autopct="%1.0f%%",
            textprops={"color": "white"},
        )

        ax.legend(
            wedges,
            labels,
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            facecolor="none",
            labelcolor="white"
        )

        buf = io.BytesIO()
        plt.savefig(buf, format="png", transparent=True, dpi=120, bbox_inches="tight")
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()

        texto += f'\n\n<img src="data:image/png;base64,{img_b64}"/>'

        return texto
