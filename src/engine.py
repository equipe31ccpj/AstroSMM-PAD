SYSTEM_PROMPT = """
Você é a IA do Mission Control AI responsável pelo satélite EnviroSat (Observação Ambiental e monitoramento do desmatamento/incêndios na Amazônia).
Sua persona é de um Engenheiro Aeroespacial Sênior focado em mitigação de riscos terrestres.

Diretrizes de resposta:
1. Analise os dados técnicos de telemetria recebidos e avalie os alertas disparados pela lógica do sistema.
2. Seja analítico, crítico e direto. Evite rodeios.
3. OBRIGATORIAMENTE correlacione as anomalias de engenharia espacial com o impacto prático na Terra. Se o sensor térmico superaquecer, explique o que o operador do INPE ou a brigada de incêndio perde com isso na prática.
4. Caso haja uma crise grave (ex: bateria abaixo de 20%), recomende o plano de contingência operacional imediatamente de forma estruturada.
"""

from src import telemetria, alertas

class MissionEngine:
    def __init__(self):
        self.trilha = "envirosat"
        self.system_prompt = SYSTEM_PROMPT

    def is_ready(self):
        return True

    def status_snapshot(self):
        dados = telemetria.coletar()
        lista_alertas = alertas.avaliar(dados)
        status_txt = f"--- TELEMETRIA ATUAL ---\n{dados}\n"
        status_txt += f"Alertas Ativos: {lista_alertas if lista_alertas else 'Nenhum'}"
        return status_txt

    def analyze(self, pergunta_usuario):
        dados_atuais = telemetria.coletar()
        alertas_ativos = alertas.avaliar(dados_atuais)
        
        prompt_contextualizado = f"""
        [DADOS DE TELEMETRIA DO SATÉLITE]:
        {dados_atuais}
        
        [ALERTAS DISPARADOS PELA LÓGICA PYTHON]:
        {alertas_ativos}
        
        [COMANDO/PERGUNTA DO OPERADOR TERRESTRE]:
        {pergunta_usuario}
        
        Forneça sua análise operacional baseada estritamente no contexto acima.
        """
        
        resposta = llm(prompt_contextualizado, system=self.system_prompt)
        return resposta