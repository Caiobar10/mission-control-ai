"""Lógica de alertas e decisão — EnviroSat-BR · PlanetHelper"""
from dataclasses import dataclass
from typing import List
from src.telemetria import Telemetria

@dataclass
class Alerta:
    severidade: str      # "CRÍTICO" | "ATENÇÃO" | "NORMAL"
    parametro: str       # nome do sensor
    valor: str           # valor atual formatado
    mensagem: str        # o que está errado
    impacto: str         # consequência terrestre imediata
    acao: str            # o que o sistema faz automaticamente

def avaliar(dados: Telemetria) -> List[Alerta]:
    """
    Avalia os dados da telemetria e retorna lista de alertas.
    REGRA: a decisão lógica fica AQUI — a IA só explica e contextualiza.
    """
    alertas = []

    # ── Focos térmicos ──────────────────────────────────────────────────
    if dados.focos_termicos > 30:
        alertas.append(Alerta(
            severidade="CRÍTICO",
            parametro="Sensor térmico",
            valor=f"{dados.focos_termicos} focos",
            mensagem=f"{dados.focos_termicos} focos de calor detectados — muito acima do limite de 30",
            impacto="Possível incêndio de grande porte em área de vegetação. Brigadas podem estar sendo despachadas para localização incorreta.",
            acao="Frequência de varredura aumentada para 30s. Alerta enviado ao centro de controle do INPE."
        ))
    elif dados.focos_termicos > 15:
        alertas.append(Alerta(
            severidade="ATENÇÃO",
            parametro="Sensor térmico",
            valor=f"{dados.focos_termicos} focos",
            mensagem=f"{dados.focos_termicos} focos detectados — acima do normal (limite: 15)",
            impacto="Atividade térmica elevada. Monitoramento contínuo necessário para confirmar evolução.",
            acao="Monitoramento contínuo ativado. Notificação enviada ao analista de plantão."
        ))

    # ── Qualidade óptica ────────────────────────────────────────────────
    if dados.qualidade_optica < 50:
        alertas.append(Alerta(
            severidade="CRÍTICO",
            parametro="Sensor óptico RGB+NIR",
            valor=f"{dados.qualidade_optica}%",
            mensagem=f"Qualidade óptica em {dados.qualidade_optica}% — abaixo do mínimo operacional de 50%",
            impacto="Imagens geradas são inutilizáveis. Detecção de desmatamento e mapeamento de queimadas comprometidos.",
            acao="Sensor em modo de diagnóstico. Imagens desta passagem marcadas como inválidas no sistema."
        ))
    elif dados.qualidade_optica < 70:
        alertas.append(Alerta(
            severidade="ATENÇÃO",
            parametro="Sensor óptico RGB+NIR",
            valor=f"{dados.qualidade_optica}%",
            mensagem=f"Qualidade óptica em {dados.qualidade_optica}% — abaixo do ideal de 70%",
            impacto="Imagens com qualidade reduzida. Análises de cobertura vegetal podem ter imprecisões.",
            acao="Imagens desta passagem sinalizadas para revisão manual pelo analista."
        ))

    # ── Buffer de imagens ───────────────────────────────────────────────
    if dados.buffer_imagens > 85:
        alertas.append(Alerta(
            severidade="CRÍTICO",
            parametro="Buffer de transmissão",
            valor=f"{dados.buffer_imagens}%",
            mensagem=f"Buffer em {dados.buffer_imagens}% — risco iminente de perda de dados",
            impacto="Imagens capturadas serão sobrescritas se o buffer atingir 100%. Dados de incêndios e desmatamento podem ser perdidos permanentemente.",
            acao="Transmissão de dados priorizados iniciada. Captura de imagens de baixa prioridade suspensa."
        ))
    elif dados.buffer_imagens > 60:
        alertas.append(Alerta(
            severidade="ATENÇÃO",
            parametro="Buffer de transmissão",
            valor=f"{dados.buffer_imagens}%",
            mensagem=f"Buffer em {dados.buffer_imagens}% — capacidade se aproximando do limite",
            impacto="Janela de downlink precisa ser priorizada na próxima passagem sobre estação terrestre.",
            acao="Próxima janela de downlink marcada como prioritária."
        ))

    # ── Precisão de geolocalização ──────────────────────────────────────
    if dados.precisao_geo > 100:
        alertas.append(Alerta(
            severidade="CRÍTICO",
            parametro="Geolocalização",
            valor=f"{dados.precisao_geo}m de erro",
            mensagem=f"Erro de geolocalização em {dados.precisao_geo}m — muito acima do limite de 100m",
            impacto="Coordenadas de focos e áreas desmatadas estão incorretas. Brigadas de combate a incêndio podem ser despachadas para local errado.",
            acao="Recalibração de atitude iniciada. Imagens desta passagem georreferenciadas com flag de baixa confiança."
        ))
    elif dados.precisao_geo > 30:
        alertas.append(Alerta(
            severidade="ATENÇÃO",
            parametro="Geolocalização",
            valor=f"{dados.precisao_geo}m de erro",
            mensagem=f"Precisão de geo em {dados.precisao_geo}m — acima do ideal de 30m",
            impacto="Leve imprecisão nas coordenadas reportadas. Aceitável para monitoramento geral, inadequado para resposta de emergência.",
            acao="Verificação de calibração agendada para próxima janela de manutenção."
        ))

    # ── Energia ─────────────────────────────────────────────────────────
    if dados.energia < 20:
        alertas.append(Alerta(
            severidade="CRÍTICO",
            parametro="Sistema de energia",
            valor=f"{dados.energia}%",
            mensagem=f"Energia em {dados.energia}% — abaixo do mínimo crítico de 20%",
            impacto="Risco de desligamento de sistemas essenciais. Perda total de telemetria possível nas próximas horas.",
            acao="Modo de economia de energia ativado. Sensores não essenciais desligados. Operador notificado para intervenção manual."
        ))
    elif dados.energia < 30:
        alertas.append(Alerta(
            severidade="ATENÇÃO",
            parametro="Sistema de energia",
            valor=f"{dados.energia}%",
            mensagem=f"Energia em {dados.energia}% — abaixo do nível recomendado de 30%",
            impacto="Capacidade operacional reduzida. Monitoramento de longa duração pode ser afetado.",
            acao="Consumo de energia não essencial reduzido em 30%. Painéis solares reorientados."
        ))

    # Se não houver alertas, registra operação normal
    if not alertas:
        alertas.append(Alerta(
            severidade="NORMAL",
            parametro="Todos os sistemas",
            valor="—",
            mensagem="Todos os parâmetros dentro dos limites operacionais",
            impacto="Nenhum impacto nas operações terrestres. Dados sendo gerados com qualidade nominal.",
            acao="Nenhuma ação necessária. Monitoramento de rotina ativo."
        ))

    return alertas

def severidade_maxima(alertas: List[Alerta]) -> str:
    """Retorna a maior severidade da lista — útil para colorir o painel."""
    if any(a.severidade == "CRÍTICO" for a in alertas):
        return "CRÍTICO"
    if any(a.severidade == "ATENÇÃO" for a in alertas):
        return "ATENÇÃO"
    return "NORMAL"

def formatar_para_prompt(alertas: List[Alerta]) -> str:
    """Formata os alertas para injeção no prompt da IA."""
    if len(alertas) == 1 and alertas[0].severidade == "NORMAL":
        return "ALERTAS: nenhum — todos os sistemas operando normalmente."

    linhas = ["ALERTAS ATIVOS:"]
    for a in alertas:
        linhas.append(
            f"- [{a.severidade}] {a.parametro}: {a.mensagem}\n"
            f"  Impacto terrestre: {a.impacto}\n"
            f"  Ação automática: {a.acao}"
        )
    return "\n".join(linhas)

def formatar_para_display(alertas: List[Alerta]) -> str:
    """Versão para exibir no terminal com Rich markup."""
    cores = {"CRÍTICO": "red", "ATENÇÃO": "yellow", "NORMAL": "green"}
    linhas = []
    for a in alertas:
        cor = cores.get(a.severidade, "white")
        linhas.append(
            f"[bold {cor}][{a.severidade}][/bold {cor}] "
            f"{a.parametro}: {a.valor}\n"
            f"  {a.mensagem}\n"
            f"  [dim]↳ {a.acao}[/dim]"
        )
    return "\n\n".join(linhas)