import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text
import argparse

console = Console()

def show_banner():
    linha1 = pyfiglet.figlet_format("EnviroSat", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("PlanetHelper", font="ansi_shadow")
    console.print(Align.center(Text(linha1, style="bold #1D9E75")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-fonts", action="store_true")
    parser.add_argument("-font", type=str, default="ansi_shadow")
    parser.add_argument("-text", type=str, default="PlanetHelper")
    parser.add_argument("-demo", action="store_true")
    args = parser.parse_args()

    if args.fonts:
        for f in pyfiglet.FigletFont.getFonts():
            print(f)
    elif args.demo:
        for font in ["ansi_shadow", "slant", "big", "banner3", "doom", "epic", "starwars", "graffiti"]:
            console.print(f"\n[dim]── {font} ──[/dim]")
            console.print(Text(pyfiglet.figlet_format("PH", font=font), style="bold #1D9E75"))
    else:
        show_banner()