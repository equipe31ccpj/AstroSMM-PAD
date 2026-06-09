import os
import json
from groq import Groq  # 💡 Biblioteca oficial do Groq
from dotenv import load_dotenv
from pathlib import Path
from src import telemetria
from src import alertas

load_dotenv()

TRILHA = "envirosat"

# Inicializa o cliente oficial do Groq pegando a chave do .env
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY", "").strip().replace('"', '').replace("'", "")
)

def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia o prompt para a API do Groq usando streaming corrigido."""
    messages = []
    
    if system:
        messages.append({"role": "system", "content": system})
        
    messages.append({"role": "user", "content": prompt})
    
    try:
        # Mudamos o parâmetro de tokens e o ID do modelo para produção estável
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Modelo oficial de produção do Groq
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,  # 💡 CORREÇÃO: Usando max_tokens em vez de max_completion_tokens
            stream=True,
            stop=None
        )
        
        resposta_completa = ""
        for chunk in completion:
            # Versões diferentes do SDK do Groq podem exigir checar se choices existe
            if chunk.choices and len(chunk.choices) > 0:
                conteudo_pedaco = chunk.choices[0].delta.content
                if conteudo_pedaco:
                    resposta_completa += conteudo_pedaco
                
        return resposta_completa.strip()
        
    except Exception as e:
        return f"⚠️ Erro ao consultar Groq: {e}"

def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md"""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente técnico sênior de monitoramento aeroespacial."

class MissionEngine:
    """Motor de análise operacional para a trilha EnviroSat."""
    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        
    def is_ready(self):
        return True
        
    def status_snapshot(self) -> str:
        """Consome a telemetria em tempo real e formata o snapshot para a CLI."""
        dados_atuais = telemetria.coletar()
        alertas_ativos = alertas.avaliar(dados_atuais)
        
        snapshot = "\n==================================================\n"
        snapshot += "📡 SNAPSHOT ATUAL DE TELEMETRIA - ENVIROSAT\n"
        snapshot += "==================================================\n"
        snapshot += f" 🌡️ Temp. Sensor Térmico : {dados_atuais['temperatura_sensor_termico']} °C\n"
        snapshot += f" 🔋 Nível de Bateria      : {dados_atuais['energia_bateria']} %\n"
        snapshot += f" 📁 Buffer de Imagens    : {dados_atuais['buffer_imagens']} arquivos\n"
        snapshot += f" 🎯 Precisão Geo (Erro)  : {dados_atuais['precisao_geolocalizacao']} metros\n"
        snapshot += "--------------------------------------------------\n"
        snapshot += f"⚠️ ALERTAS DETECTADOS PELO SISTEMA: {len(alertas_ativos)}\n"
        
        if alertas_ativos:
            for alrt in alertas_ativos:
                snapshot += f"   • [{alrt['status']}] {alrt['parametro']}: {alrt['mensagem']}\n"
        else:
            snapshot += "   • STATUS: Todos os subsistemas operando em conformidade.\n"
        snapshot += "================================================--"
        
        return snapshot
        
    def analyze(self, pergunta_usuario: str) -> str:
        dados_atuais = telemetria.coletar()
        alertas_ativos = alertas.avaliar(dados_atuais)
        
        prompt_contextualizado = f"""
[LOGS DE TELEMETRIA EM TEMPO REAL]:
{json.dumps(dados_atuais, indent=2)}

[ALERTAS DE ANOMALIA DETECTADOS]:
{json.dumps(alertas_ativos, indent=2) if alertas_ativos else 'Nenhuma anomalia de engenharia identificada.'}

[PERGUNTA DO OPERADOR EM SOLO]:
"{pergunta_usuario}"

Gere uma resposta curta, crítica e analítica conectando a engenharia espacial à missão terrestre do satélite.
"""
        resposta_ia = llm(
            prompt=prompt_contextualizado,
            system=self.system_prompt,
            temperature=0.2
        )
        
        return resposta_ia