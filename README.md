# AstroSMM-PAD 🛰️
> **Global Solution — 1° Semestre**
> *Disciplina: Prompt and Artificial Intelligence Development*
> *FIAP — Ciência da Computação*

Uma interface de linha de comando (CLI) avançada e integrada à inteligência artificial generativa em nuvem, projetada para processar telemetria em tempo real, avaliar anomalias orbitais e fornecer pareceres analíticos para a condução da missão aeroespacial.

---

## 🌌 Visão Geral da Missão

* **Trilha Selecionada:** Trilha 2 — EnviroSat (Observação Ambiental)
* **Objetivo do Sistema:** Conectar dados brutos de sensores de satélite (temperatura, bateria, buffer e geolocalização) à tomada de decisão de engenheiros e agentes de resposta ambiental na Terra, utilizando modelos de linguagem de larga escala (LLMs).

---

## 🚀 Definição Estratégica do Projeto (Negócio & Impacto)

### 1. Qual o problema real que essa missão resolve?
A missão mitiga o avanço do desmatamento ilegal e a propagação de incêndios florestais em biomas críticos brasileiros (como a Amazônia e o Cerrado). Através do monitoramento contínuo por sensores térmicos e ópticos RGB+NIR, o sistema preenche a lacuna entre a coleta de dados orbitais brutos e a tomada de decisão em solo. Isso permite identificar clareiras provocadas por corte raso irregular e focos ativos de calor antes que se transformem em incêndios de proporções incontroláveis, protegendo a biodiversidade e contendo a emissão de gases de efeito estufa.

### 2. Quem paga pela solução (Cliente)?
* **Setor Governamental:** Órgãos federais e estaduais de fiscalização e meio ambiente (como IBAMA, ICMBio e Secretarias Estaduais de Meio Ambiente) que utilizam os dados para planejar operações de autuação e combate.  
* **Mercado de Crédito de Carbono e Fundos Internacionais:** ONGs internacionais, fundos soberanos (ex: Fundo Amazônia) e desenvolvedores de projetos REDD+ que precisam de auditoria e monitoramento de compliance altamente preciso para validar a preservação das áreas.  
* **Agronegócio e Setor de Seguros:** Grandes cooperativas agrícolas e empresas de celulose que possuem áreas de preservação permanente (APP) ou reservas legais e necessitam proteger suas fronteiras contra incêndios vindos de propriedades vizinhas.

### 3. Qual a métrica de sucesso terrestre?
* **Tempo de Resposta Operacional:** Redução do tempo médio entre a detecção do foco de calor pelo satélite e o acionamento da brigada de incêndio em solo (meta ideal: abaixo de 2 horas).
* **Taxa de Supressão Precoce:** Porcentagem de focos de incêndio controlsdos e extintos ainda na fase inicial (com menos de 5 hectares consumidos).
* **Eficácia de Fiscalização (Área Preservada):** Redução percentual anual da área total desmatada ilegalmente dentro das zonas monitoradas pelo satélite.
* **Acurácia de Geolocalização:** Margem de erro de desvio orbital mantida abaixo de 5 metros, garantindo que as equipes de solo encontrem o foco exato sem desperdício de combustível ou tempo de deslocamento.  

### 4. O que acontece se o satélite falhar por 24h?
A interrupção de 24 horas no fornecimento de dados gera uma *"janela de cegueira operacional"* catastrófica para a gestão ambiental:
* **No combate a incêndios:** Uma frente de fogo sem monitoramento pode avançar dezenas de quilômetros em um único dia, saltando barreiras naturais e tornando-se imune ao combate de primeira resposta das brigadas.
* **Na fiscalização de desmatamento:** Correntões e tratores de esteira conseguem derrubar dezenas de hectares de mata nativa em 24 horas. Sem o alerta em tempo real, os infratores concluem a derrubada e evadem o local antes da chegada da fiscalização.
* **Impacto Econômico e Jurídico:** Empresas que dependem dos dados de compliance ambiental sofrem quebras de contrato internacionais por falta de auditoria de risco, além de multas severas geradas pela incapacidade de defender suas áreas protegidas em tempo hábil.

---

## 🛠️ Arquitetura Técnica do Software

A aplicação foi estruturada de forma modular seguindo padrões limpos de separação de responsabilidades:

| Componente | Função |
| :--- | :--- |
| `main.py` | Ponto de entrada, renderiza a interface ASCII da CLI e coordena o loop de eventos. |
| `src/telemetria.py` | Coleta e formata dinamicamente os parâmetros físicos do satélite em tempo real. |
| `src/alertas.py` | Motor de regras lógicas estáticas para classificação de anomalias (Atenção/Crítico). |
| `src/engine.py` | Inicializa o cliente do **Groq SDK** e processa chamadas LLM com streaming de tokens. |

[Módulos Locais: telemetria + alertas]
│
▼ (Snapshot Consolidados)
[src/engine.py] ──(Injeta System Prompt + Logs)──► [Groq Cloud API]
▲                                                    │
│                                                    ▼
[Operador Solo] ◄────────(Exibe Resposta Analítica)─────────┘

### Tecnologias Utilizadas
* **Python 3.11**
* **Groq Cloud Python SDK** (Modelo de inferência: `llama-3.3-70b-versatile`)
* **Python-Dotenv** (Gerenciamento seguro de credenciais)

---

## 🚀 Instalação e Execução

### 1. Pré-requisitos
Certifique-se de possuir o Python instalado e uma chave de API válida gerada no [Console do Groq](https://console.groq.com/).

### 2. Clonar o projeto
```bash
git clone [https://github.com/equipe31ccpj/AstroSMM-PAD.git](https://github.com/equipe31ccpj/AstroSMM-PAD.git)
cd AstroSMM-PAD
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto (mesmo nível de main.py) com base no .env.example:
```Snippet de código
GROQ_API_KEY=sua_api_key_real_da_groq_aqui
GROQ_MODEL=llama-3.3-70b-versatile
```

### 5. Executar a CLI
```bash
python main.py
```

## 💡 Exemplo de Interação Operacional
Assim que iniciado, o sistema apresentará o status da telemetria e abrirá o terminal do operador:
```Plaintext
==================================================
📡 SNAPSHOT ATUAL DE TELEMETRIA - ENVIROSAT
==================================================
 🌡️ Temp. Sensor Térmico : 44.32 °C
 🔋 Nível de Bateria      : 28.18 %
 📁 Buffer de Imagens    : 31 arquivos
 🎯 Precisão Geo (Erro)  : 10.99 metros
--------------------------------------------------
⚠️ ALERTAS DETECTADOS PELO SISTEMA: 2
   • [CRÍTICO] temperatura_sensor_termico: Superaquecimento detectado: 44.32°C.
   • [ATENÇÃO] precisao_geolocalizacao: Desvio orbital suspeito. Margem de erro: 10.99m.
================================================--
 
🛰️ Operador [EnviroSat] > Alerta de falha múltipla detectado nos subsistemas térmico e de energia. Quais são as consequências operacionais imediatas para a fiscalização de queimadas em solo e qual o plano de contingência aeroespacial obrigatório?

🔄 Processando telemetria e enviando contexto para Groq Cloud...

🧠 Mission Control AI:
**Análise Crítica:**
O satélite reporta superaquecimento severo (44.32°C) casado a uma degradação drástica na reserva de bateria (28.18%), o que corrobora um cenário iminente de colapso de subsistema se medidas imediatas não forem tomadas. 

**Consequências Operacionais:**
A degradação térmica afeta a calibração do sensor de infravermelho, gerando falsos negativos no mapeamento da Amazônia Legal. Equipes terrestres do IBAMA perderão a capacidade de resposta cirúrgica antes que incêndios de copa se alastrem.

**Plano de Contingência:**
1. Desativação imediata das câmeras ópticas RGB secundárias para mitigar a geração de calor interna.
2. Interrupção do processamento local de imagens no buffer de bordo (manter os 31 arquivos congelados).
3. Reorientação dos painéis solares para dissipação térmica em ângulo de sombra até a normalização do sensor térmico.
```
## 👥 Autores
Nome: Akin Alexandre       RM: 572773
Nome: Maria Eduarda Rocha  RM: 570554
Nome: Pedro Henrique Neves RM: 571382
