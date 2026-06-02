"""Interface CLI estilo Claude Code — EnviroSat · PlanetHelper"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from datetime import datetime
import pyfiglet

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#1D9E75 bold"}))

def show_banner():
    linha1 = pyfiglet.figlet_format("EnviroSat", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("PlanetHelper", font="ansi_shadow")
    console.print(Text(linha1, style="bold #1D9E75"))
    console.print(Text(linha2, style="bold #06B6D4"))
    console.print(Panel.fit(
        "[bold]PH[/bold] — Sistema de monitoramento ambiental por IA generativa.\n"
        "Use [bold cyan]/help[/bold cyan] para ver os comandos · "
        "[bold cyan]/status[/bold cyan] para telemetria atual · "
        "[bold cyan]/exit[/bold cyan] para sair.\n"
        "Modelo: [bold]gpt-oss:120b[/bold] via Ollama Cloud",
        title="◆ PLANETHELPER · EnviroSat",
        border_style="#1D9E75"
    ))

def show_response(text):
    now = datetime.now().strftime("%H:%M")
    console.print(Panel(
        text,
        title="◆ PH · PlanetHelper",
        subtitle=now,
        border_style="#1D9E75"
    ))

def show_help():
    table = Table(border_style="dim", show_header=True, header_style="bold #1D9E75")
    table.add_column("Comando", style="bold cyan", width=14)
    table.add_column("Descrição")
    table.add_row("/help",   "Mostra esta lista de comandos")
    table.add_row("/status", "Exibe telemetria atual do satélite")
    table.add_row("/about",  "Informações sobre o PlanetHelper")
    table.add_row("/clear",  "Limpa a tela")
    table.add_row("/exit",   "Encerra o sistema")
    console.print(table)

def run_cli(engine):
    show_banner()
    if not engine.is_ready():
        console.print(
            "\n ⚠  Engine status: [yellow]AGUARDANDO IMPLEMENTAÇÃO ✗[/yellow]\n"
        )
    while True:
        try:
            user_input = session.prompt("PH❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Encerrando PlanetHelper...[/dim]")
            break
        if not user_input:
            continue
        if user_input == "/exit":
            console.print("\n[dim]Encerrando PlanetHelper...[/dim]")
            break
        if user_input == "/help":
            show_help()
            continue
        if user_input == "/status":
            show_response(engine.status_snapshot())
            continue
        if user_input == "/about":
            show_response(
                "PlanetHelper (PH) é o sistema de análise operacional do EnviroSat-BR.\n"
                "Monitora dados de telemetria em tempo real e traduz anomalias técnicas\n"
                "em impacto concreto para brigadas, operadores do INPE e analistas ambientais."
            )
            continue
        if user_input == "/clear":
            console.clear()
            show_banner()
            continue
        resposta = engine.analyze(user_input)
        show_response(resposta)