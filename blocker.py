"""
firewall/blocker.py

Module de blocage / blacklist simple.
Sections (sous-titres) :
- Blocker.__init__      -> initialisation (structure de stockage)
- Blocker.block         -> ajoute une IP à la blacklist
- Blocker.unblock       -> retire une IP de la blacklist
- Blocker.is_blocked    -> vérifie si une IP est bloquée
- Blocker.export_list   -> sauvegarde la blacklist dans un fichier (option)
"""

from typing import Set, Iterable
from colorama import Fore, Style

class Blocker:
    """
    Gestion d'une liste d'IP bloquées.
    Ne modifie pas le firewall système — c'est une simulation (liste en mémoire).
    """

    def __init__(self):
        self.blocked_ips: Set[str] = set()

    # -----------------------
    # block (sous-titre)
    # -----------------------
    def block(self, ip: str) -> None:
        """Bloque une IP (ajoute à la set)."""
        if ip not in self.blocked_ips:
            self.blocked_ips.add(ip)
            print(Fore.RED + f"⚠️  Blocked IP: {ip}" + Style.RESET_ALL)

    # -----------------------
    # unblock (sous-titre)
    # -----------------------
    def unblock(self, ip: str) -> None:
        """Débloque une IP si elle existe dans la liste."""
        if ip in self.blocked_ips:
            self.blocked_ips.remove(ip)
            print(Fore.GREEN + f"✅ Unblocked IP: {ip}" + Style.RESET_ALL)

    # -----------------------
    # is_blocked (sous-titre)
    # -----------------------
    def is_blocked(self, ip: str) -> bool:
        """Retourne True si l'IP est bloquée."""
        return ip in self.blocked_ips

    # -----------------------
    # export_list (sous-titre)
    # -----------------------
    def export_list(self, path: str = "blocked_ips.txt") -> None:
        """Sauvegarde la blacklist dans un fichier (une IP par ligne)."""
        with open(path, "w") as f:
            for ip in sorted(self.blocked_ips):
                f.write(ip + "\n")
        print(f"Blocked IPs exported to {path}")
