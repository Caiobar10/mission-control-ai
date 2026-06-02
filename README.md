# 🌿 Mission Control AI — PlanetHelper (PH)
### EnviroSat-BR · Monitoramento Ambiental por IA Generativa

---
## 👥 Integrantes
| Nome | RM | Turma |
|---|---|---|
| Caio Moda F F Barbieri (Com nota do challenge) | 566747 | CCPB |
| Pietro Visconti Bueno de Mello | 567673 | CCPB |
| Dicley Lucas Neto | 567588 | CCPB |

**Modalidade:** Trio
---

## 🛰 O que o projeto faz

PlanetHelper (PH) é o sistema de inteligência artificial do **EnviroSat-BR**, satélite
brasileiro de observação ambiental. O sistema monitora telemetria em tempo real —
focos térmicos, qualidade óptica, buffer de transmissão, geolocalização e energia —
detecta anomalias via lógica Python e usa IA generativa (Ollama Cloud, modelo
`gpt-oss:120b`) para traduzir cada anomalia técnica em impacto concreto para
brigadas de incêndio, operadores do INPE e analistas ambientais.

---

## 🌳 Trilha escolhida

**EnviroSat** — Observação Ambiental

Satélite simulado: térmico + óptico, similar ao Amazônia-1 / Landsat.
Setor de impacto: sustentabilidade e clima — combate ao desmatamento,
resposta rápida a incêndios, monitoramento de áreas protegidas.

---

## 🎭 Personas atendidas

| Persona | Necessidade |
|---|---|
| Engenheiro de operações | Diagnóstico técnico detalhado, causas raiz, valores exatos |
| Coordenador de brigada | Localização de focos, severidade, tempo de resposta — sem jargão |
| Analista de compliance (INPE/IBAMA) | Impacto em área, lacunas no DETER/PRODES, legislação aplicável |

O PlanetHelper adapta automaticamente o nível de detalhe técnico conforme o
contexto da pergunta.

---

## 🛠 Tecnologias utilizadas

- Python 3.13
- Ollama Cloud API — modelo `gpt-oss:120b`
- `rich` — painéis e formatação no terminal
- `prompt-toolkit` — input editável com histórico
- `pyfiglet` — banner ASCII art
- `python-dotenv` — gerenciamento de credenciais

---

## ⚙️ Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/mission-control-ai.git
cd mission-control-ai
```

### 2. Crie o ambiente virtual
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as credenciais
Crie o arquivo `.env` na raiz do projeto:
Obtenha sua chave gratuita em: https://ollama.com/settings/api-keys

### 5. Execute
```bash
python main.py
```

### Comandos disponíveis no terminal
| Comando | Descrição |
|---|---|
| `/status` | Painel de telemetria atual com emojis de status |
| `/help` | Lista de comandos |
| `/about` | Informações sobre o PlanetHelper |
| `/clear` | Limpa a tela |
| `/exit` | Encerra o sistema |

---

## 🤖 System Prompt

O PlanetHelper usa um system prompt profissional definido em `prompts/system_prompt.md`.
Elementos principais:

- **Identidade:** engenheiro sênior de missão com 10 anos de experiência no EnviroSat-BR
- **Escopo:** monitoramento de focos térmicos, qualidade óptica, buffer, geo e energia
- **Formato obrigatório:** diagnóstico técnico → impacto terrestre → ação recomendada
- **Personas:** adapta linguagem para engenheiro, coordenador de brigada ou analista
- **Restrição principal:** nunca analisa problema técnico sem conectar ao impacto na Terra

---

## 🧪 Cenários de teste demonstrados

### Cenário 1 — Operação normal
Todos os parâmetros dentro dos ranges operacionais. O PH confirma status e
reporta monitoramento de rotina ativo.

### Cenário 2 — Sensor óptico crítico
Qualidade RGB+NIR abaixo de 50%. O PH identifica risco de lacunas no
DETER/PRODES, taxa de falsos positivos elevada nas análises de desmatamento
e aciona protocolo de diagnóstico do sensor.

### Cenário 3 — Crise sistêmica múltipla
Todos os parâmetros em estado crítico simultaneamente (focos > 30, qualidade
< 50%, buffer > 85%, geo > 100m, energia < 20%). O PH emite alerta de falha
sistêmica, prioriza ações por urgência e alerta risco de interrupção total
da missão.

---

## ⚠️ Limitações conhecidas

- Os dados de telemetria são simulados — não conectados a um satélite real
- O modelo `gpt-oss:120b` via Ollama Cloud requer conexão com internet
- Respostas podem variar ligeiramente entre chamadas (modelo não-determinístico)
- O sistema não mantém histórico de sessão entre execuções

---

## 💼 Proposta de valor / modelo de negócio

### 1. Problema real terrestre que esta missão resolve
O Brasil perde em média 11.000 km² de Amazônia por ano para desmatamento e
queimadas. O tempo entre a detecção de um foco por satélite e a chegada de
uma brigada ao local correto pode definir se um incêndio de 10 hectares vira
um de 10.000. O EnviroSat-BR resolve o gap entre dado orbital bruto e decisão
operacional em campo — traduzindo telemetria técnica em linguagem acionável
para quem está na linha de frente.

### 2. Quem paga pela solução
Modelo híbrido:
- **Setor público:** INPE, IBAMA, ICMBio e defesas civis estaduais pagam pelo
  acesso aos dados brutos via contrato de concessão — similar ao modelo atual
  do CBERS e Amazônia-1
- **Setor privado:** seguradoras rurais, empresas de ESG e certificadoras
  ambientais pagam por relatórios de compliance baseados nos dados do satélite

### 3. Métrica de impacto
Se o EnviroSat-BR operar 100% saudável por 1 ano:
- ~850.000 km² de biomas monitorados continuamente (Amazônia + Cerrado + Pantanal)
- ~40.000 focos de calor detectados e georreferenciados com precisão < 30m
- ~12.000 alertas enviados a brigadas com coordenadas confiáveis
- Redução estimada de 15–20% no tempo de resposta a incêndios em áreas remotas

### 4. Modelo de negócio
**Dado-como-serviço (DaaS) + concessão pública:**
- Camada 1 — concessão pública: INPE/governo federal financia a operação
  básica do satélite via contrato plurianual (modelo Amazônia-1)
- Camada 2 — SaaS privado: API de acesso aos dados processados pelo
  PlanetHelper para empresas de agronegócio, seguradoras e consultorias de ESG
- Camada 3 — relatórios sob demanda: laudos técnicos de compliance ambiental
  para certificações internacionais (FSC, RSPO, mercado de carbono)

---

## 📸 Demonstração

![Banner inicial do PlanetHelper](assets/screenshot_banner.png)
![Análise com alerta crítico](assets/screenshot_analise.png)

---

## 🎬 Vídeo de demonstração

🔗 [Assistir no YouTube] https://youtu.be/l5ZGW7qMP4I
> Configurado como "Não listado" no YouTube.

---

*FIAP · Ciência da Computação · Global Solution 2026.1*
*Disciplina: Prompt Engineering and Artificial Intelligence*