from pathlib import Path

APP_NAME = "ATHENA"
VERSION = "0.4.0"

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"
LOG_DIR = ROOT_DIR / "logs"
MODEL_DIR = ROOT_DIR / "models"

OLLAMA_MODEL = "qwen3:4b"