"""Telemetria simulada do EnviroSat-BR — sensores ambientais."""
import random
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Telemetria:
    timestamp: str
    focos_termicos: int          # quantidade de focos detectados pelo sensor térmico
    qualidade_optica: float      # qualidade do sensor óptico RGB+NIR (%)
    buffer_imagens: float        # buffer de imagens não transmitidas (%)
    precisao_geo: float          # precisão de geolocalização (metros)
    energia: float               # energia disponível nos painéis solares (%)

def coletar(forcar_critico: bool = False) -> Telemetria:
    """
    Gera uma leitura simulada dos sensores.
    90% do tempo opera normal. 10% gera anomalia aleatória.
    Se forcar_critico=True, gera valores críticos em todos os parâmetros.
    """
    if forcar_critico:
        return Telemetria(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            focos_termicos=random.randint(35, 60),
            qualidade_optica=round(random.uniform(20.0, 45.0), 1),
            buffer_imagens=round(random.uniform(88.0, 99.0), 1),
            precisao_geo=round(random.uniform(110.0, 180.0), 1),
            energia=round(random.uniform(8.0, 18.0), 1),
        )

    # Operação normal com 10% de chance de gerar anomalia em cada parâmetro
    return Telemetria(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        focos_termicos=_simular(
            normal=lambda: random.randint(0, 15),
            anomalia=lambda: random.randint(25, 50),
        ),
        qualidade_optica=_simular(
            normal=lambda: round(random.uniform(70.0, 100.0), 1),
            anomalia=lambda: round(random.uniform(20.0, 49.0), 1),
        ),
        buffer_imagens=_simular(
            normal=lambda: round(random.uniform(10.0, 60.0), 1),
            anomalia=lambda: round(random.uniform(86.0, 99.0), 1),
        ),
        precisao_geo=_simular(
            normal=lambda: round(random.uniform(5.0, 28.0), 1),
            anomalia=lambda: round(random.uniform(101.0, 160.0), 1),
        ),
        energia=_simular(
            normal=lambda: round(random.uniform(35.0, 100.0), 1),
            anomalia=lambda: round(random.uniform(8.0, 19.0), 1),
        ),
    )

def _simular(normal, anomalia, chance_anomalia: float = 0.10):
    """Retorna valor normal 90% do tempo, anomalia 10%."""
    return anomalia() if random.random() < chance_anomalia else normal()

def formatar_para_prompt(dados: Telemetria) -> str:
    """
    Transforma os dados em texto estruturado para injetar no prompt da IA.
    A IA recebe isso como contexto — quanto mais claro, melhor a resposta.
    """
    return f"""TELEMETRIA ATUAL — EnviroSat-BR
Timestamp: {dados.timestamp}

Sensores:
- Focos térmicos detectados: {dados.focos_termicos} focos
- Qualidade do sensor óptico (RGB+NIR): {dados.qualidade_optica}%
- Buffer de imagens não transmitidas: {dados.buffer_imagens}%
- Precisão de geolocalização: {dados.precisao_geo} metros
- Energia disponível: {dados.energia}%"""

def formatar_para_display(dados: Telemetria) -> str:
    """
    Versão para exibir no terminal no comando /status.
    Usa emojis de status para leitura rápida do operador.
    """
    def status(valor, limites_ok, limites_atencao):
        baixo, alto = limites_ok
        if baixo <= valor <= alto:
            return "🟢"
        b2, a2 = limites_atencao
        if b2 <= valor <= a2:
            return "🟡"
        return "🔴"

    return f"""[bold]EnviroSat-BR — Snapshot {dados.timestamp}[/bold]

{status(dados.focos_termicos, (0,15), (16,29))} Focos térmicos:      {dados.focos_termicos} focos
{status(dados.qualidade_optica, (70,100), (50,69))} Qualidade óptica:    {dados.qualidade_optica}%
{status(dados.buffer_imagens, (0,60), (61,84))} Buffer de imagens:   {dados.buffer_imagens}%
{status(dados.precisao_geo, (0,30), (31,99))} Precisão geo:        {dados.precisao_geo} m
{status(dados.energia, (30,100), (20,29))} Energia:             {dados.energia}%"""