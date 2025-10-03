"""
dashboard/dashboard.py

Module providing a simple console dashboard for DDOS_protector_bot.

Sections (sous-titres / fonctions) :
- Dashboard.__init__        -> initialisation et références au detector/blocker
- Dashboard._get_stats      -> collecte les statistiques depuis les modules firewall
- Dashboard.show_status     -> affiche le tableau résumé (utilise tabulate)
- Dashboard.print_summary   -> affiche un résumé textuel simple
- Dashboard.run_cli_loop    -> boucle CLI pour mise à jour périodique (option)
"""

from typing import Dict, Any
from tabulate import tabulate
from colorama import Fore, Style
import time


class Dashboard:
    """
    Simple console dashboard to display protection statistics.
    Expects an object 'detector' with attributes:
      - ip_requests: Dict[str, int]  (counts per IP)
      - total_requests: int         (optional)
    And an object 'blocker' with attribute:
      - blocked_ips: set or list
    """

    def __init__(self, detector, blocker, refresh: float = 2.0):
        """
        Parameters:
            detector: module or object that exposes ip_requests (dict) and optionally total_requests
            blocker:  module or object that exposes blocked_ips (iterable)
            refresh:  seconds between automatic dashboard refresh when using run_cli_loop
        """
        self.detector = detector
        self.blocker = blocker
        self.refresh = refresh

    # -----------------------
    # _get_stats (sous-titre)
    # -----------------------
    def _get_stats(self) -> Dict[str, Any]:
        """Collects and returns current statistics from detector and blocker."""
        ip_requests = getattr(self.detector, "ip_requests", {}) or {}
        total_requests = getattr(self.detector, "total_requests", sum(ip_requests.values()))
        ips_monitored = len(ip_requests)
        blocked = getattr(self.blocker, "blocked_ips", set())
        blocked_count = len(blocked)

        top_ips = sorted(ip_requests.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "total_requests": int(total_requests),
            "ips_monitored": int(ips_monitored),
            "blocked_count": int(blocked_count),
            "top_ips": top_ips,
            "blocked_list": list(blocked)[:10],
        }

    # -----------------------
    # show_status (sous-titre)
    # -----------------------
    def show_status(self):
        """Prints a clean table with the main statistics."""
        stats = self._get_stats()

        table = [
            ["Total requests", stats["total_requests"]],
            ["IPs monitored", stats["ips_monitored"]],
            ["IPs blocked", stats["blocked_count"]],
        ]
        print(Style.BRIGHT + Fore.CYAN + "\n=== DDOS Protector Status ===" + Style.RESET_ALL)
        print(tabulate(table, headers=["Metric", "Value"], tablefmt="fancy_grid"))

        # Top IPs
        if stats["top_ips"]:
            top_table = [[ip, count] for ip, count in stats["top_ips"]]
            print(Fore.YELLOW + "\nTop IPs by request count:" + Style.RESET_ALL)
            print(tabulate(top_table, headers=["IP", "Requests"], tablefmt="grid"))
        else:
            print(Fore.YELLOW + "\nTop IPs by request count: (none yet)" + Style.RESET_ALL)

        # Blocked list (short)
        if stats["blocked_list"]:
            print(Fore.RED + "\nRecently blocked IPs:" + Style.RESET_ALL)
            for ip in stats["blocked_list"]:
                print(f" - {ip}")
        else:
            print(Fore.GREEN + "\nNo blocked IPs." + Style.RESET_ALL)

    # -----------------------
    # print_summary (sous-titre)
    # -----------------------
    def print_summary(self):
        """Prints a one-line summary (useful for logs)."""
        s = self._get_stats()
        summary = (
            f"[Summary] total={s['total_requests']} "
            f"monitored_ips={s['ips_monitored']} blocked={s['blocked_count']}"
        )
        print(Fore.MAGENTA + summary + Style.RESET_ALL)

    # -----------------------
    # run_cli_loop (sous-titre)
    # -----------------------
    def run_cli_loop(self, iterations: int = None):
        """
        Runs a simple CLI loop that refreshes the dashboard every self.refresh seconds.
        If iterations is None, loops forever until keyboard interrupt (Ctrl+C).
        """
        i = 0
        try:
            while True:
                # Clear screen lightly (works in many terminals)
                print("\033c", end="")
                self.show_status()
                self.print_summary()
                i += 1
                if iterations is not None and i >= iterations:
                    break
                time.sleep(self.refresh)
        except KeyboardInterrupt:
            print(Fore.CYAN + "\nDashboard stopped by user." + Style.RESET_ALL)
