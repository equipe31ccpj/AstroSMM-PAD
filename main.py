import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from rich.console import Console

# Importa o motor que corrigimos e completamos
from src.engine import MissionEngine
from src.ui import run_cli


def main():
    console = Console()
    
    # Instancia o motor de análise
    engine = MissionEngine()
    
    # 1. Validação arquitetural (Frente 1)
    if not engine.is_ready():
        console.print("[bold red]❌ Erro Crítico: OLLAMA_CLOUD_TOKEN não detectado no arquivo .env[/bold red]")
        sys.exit(1)
        
    # 2. Exibe o Snapshot de Telemetria Inicial que você gerou
    console.print(engine.status_snapshot())
    
    # Configuração de estilo visual para o prompt-toolkit
    style = Style.from_dict({
        'prompt': 'ansicyan bold',
    })
    
    session = PromptSession(style=style)
    
    # 🚨 3. O LOOP DE CONTROLE (Mantém o programa rodando no terminal)
    while True:
        try:
            # Captura a entrada do usuário sem sair do programa Python
            user_input = session.prompt('\n🛰️ Operador [EnviroSat] > ').strip()
            
            # Tratamento de string vazia
            if not user_input:
                continue
                
            # Interceptação de comandos internos da CLI
            if user_input == "/exit":
                console.print("[bold yellow]Encerrando conexão de telemetria com o Mission Control AI...[/bold yellow]")
                break
                
            if user_input == "/help":
                console.print("\n[bold cyan]─── COMANDOS DISPONÍVEIS ───[/bold cyan]")
                console.print(" [bold]/help[/bold]  - Exibe este painel de ajuda operacional.")
                console.print(" [bold]/exit[/bold]  - Encerra a sessão e desconecta do satélite.")
                console.print(" [bold]Texto livre[/bold] - Envia uma consulta analítica contextualizada para a IA gpt-oss:120b.")
                continue
                
            # 4. Envio dos dados para inferência na nuvem (Frente 3)
            console.print("\n[bold magen]🔄 Processando telemetria e enviando contexto para Ollama Cloud...[/bold magen]")
            
            resposta_ia = engine.analyze(user_input)
            
            console.print(f"\n[bold green]🧠 Mission Control AI:[/bold green]\n{resposta_ia}")
            
        except (KeyboardInterrupt, EOFError):
            # Captura Ctrl+C ou Ctrl+D sem quebrar o terminal com erros feios
            console.print("\n[bold yellow]Sessão encerrada pelo operador.[/bold yellow]")
            break

if __name__ == "__main__":
    engine = MissionEngine()
    run_cli(engine)
    main()