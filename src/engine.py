"""Motor de análise — PlanetHelper · EnviroSat"""
import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path

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
        return False  # ← trocar para True na Fase 5

    def status_snapshot(self):
        return "🛠  status_snapshot() ainda não implementado."

    def analyze(self, pergunta_usuario):
        return (
            "🛠  Implementação pendente.\n\n"
            "A interface está funcionando. Para ativar o PlanetHelper:\n"
            "  1. Completar src/telemetria.py\n"
            "  2. Completar src/alertas.py\n"
            "  3. Escrever prompts/system_prompt.md\n"
            "  4. Implementar analyze() em src/engine.py"
        )