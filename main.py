"""Entry point: python main.py  or  python -m cli.main"""
import sys
from pathlib import Path

# Ensure project root is on sys.path so both `graph` and `cli` are importable
sys.path.insert(0, str(Path(__file__).parent))

from cli.main import app

if __name__ == "__main__":
    app()
