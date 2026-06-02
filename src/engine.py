"""Motor de análise — PlanetHelper · EnviroSat-BR"""
import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
from src.telemetria import coletar, formatar_para_prompt as tel_prompt, formatar_para_display
from src.alertas import avaliar, formatar_para_prompt as alert_prompt, formatar_para_display as alert_display, severidade_maxima

load_dotenv()

TRILHA = "envirosat"

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")}
)

def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Ponto único de contato com o modelo. Não reescrever — só chamar."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )["message"]["content"].strip()
    except Exception as e:
        return f"⚠️  Erro ao consultar PlanetHelper: {e}"

def load_system_prompt():
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente de monitoramento ambiental."

class MissionEngine:

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()

    def is_ready(self):
        return True  # ← implementado

    def status_snapshot(self) -> str:
        """Retorna painel textual com estado atual da telemetria — usado no /status."""
        dados = coletar()
        alertas = avaliar(dados)
        severidade = severidade_maxima(alertas)

        cores = {"CRÍTICO": "red", "ATENÇÃO": "yellow", "NORMAL": "green"}
        cor = cores.get(severidade, "white")

        return (
            f"[bold {cor}]Status geral: {severidade}[/bold {cor}]\n\n"
            f"{formatar_para_display(dados)}\n\n"
            f"{alert_display(alertas)}"
        )

    def analyze(self, pergunta_usuario: str) -> str:
        """
        Fluxo completo:
        1. Coleta telemetria fresca
        2. Avalia alertas via lógica Python
        3. Monta prompt com dados + alertas + pergunta
        4. Chama a IA com o system prompt do PlanetHelper
        5. Retorna a resposta
        """
        # 1. Dados frescos do satélite
        dados = coletar()

        # 2. Alertas via lógica Python (não pela IA)
        alertas = avaliar(dados)

        # 3. Monta o prompt com contexto completo
        prompt = f"""{tel_prompt(dados)}

{alert_prompt(alertas)}

PERGUNTA DO OPERADOR:
{pergunta_usuario}"""

        # 4. Chama a IA com o system prompt do PlanetHelper
        return llm(prompt, system=self.system_prompt)