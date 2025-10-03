"""
firewall/logger.py

Module de journalisation basique.
Sections (sous-titres) :
- Logger.__init__     -> configuration du fichier de log
- Logger.log_event    -> écrire un événement avec timestamp
- Logger.read_recent  -> lire les N dernières lignes (option)
"""

import datetime
from pathlib import Path
from typing import List

class Logger:
    """Simple file logger pour événements du firewall."""

    def __init__(self, path: str = "firewall.log"):
        self.path = Path(path)
        # assure que le fichier existe
        if not self.path.exists():
            self.path.write_text(f"# Log created on {datetime.datetime.utcnow().isoformat()}Z\n")

    # -----------------------
    # log_event (sous-titre)
    # -----------------------
    def log_event(self, message: str) -> None:
        """Ajoute une ligne horodatée au fichier de log."""
        ts = datetime.datetime.utcnow().isoformat() + "Z"
        line = f"[{ts}] {message}\n"
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line)

    # -----------------------
    # read_recent (sous-titre)
    # -----------------------
    def read_recent(self, n: int = 20) -> List[str]:
        """Retourne les `n` dernières lignes du fichier de log."""
        with self.path.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        return [l.rstrip("\n") for l in lines[-n:]]
