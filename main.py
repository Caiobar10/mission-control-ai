"""Mission Control AI — EnviroSat · PlanetHelper"""
from src.ui import run_cli
from src.engine import MissionEngine

if __name__ == "__main__":
    engine = MissionEngine()
    run_cli(engine)