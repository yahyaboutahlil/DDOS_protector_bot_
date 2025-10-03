"""
firewall/detector.py

Module de détection DDoS simple basé sur une fenêtre temporelle.
Principales sections (sous-titres) :
- DDOSDetector.__init__      -> initialisation et paramètres (threshold, window)
- DDOSDetector.record       -> enregistrer une requête d'une IP
- DDOSDetector.count_recent -> compter requêtes récentes d'une IP
- DDOSDetector.is_ddos      -> décider si une IP dépasse le seuil
- DDOSDetector.simulate_request -> méthode d'aide pour tests (génère IP aléatoire)
"""

import time
from collections import defaultdict, deque
from typing import Deque, Dict
import random

class DDOSDetector:
    """
    Detecteur DDoS basé sur une fenêtre temporelle (sliding window).
    - threshold: nombre maximal de requêtes autorisées dans la fenêtre
    - window_seconds: taille de la fenêtre (en secondes)
    """

    def __init__(self, threshold: int = 100, window_seconds: int = 60):
        self.threshold = threshold
        self.window = window_seconds
        # ip -> deque of timestamps
        self.ip_requests: Dict[str, Deque[float]] = defaultdict(deque)
        # optionnel: compteur total de requêtes observées
        self.total_requests = 0

    # -----------------------
    # record (sous-titre)
    # -----------------------
    def record(self, ip: str) -> None:
        """Enregistre une requête venant de `ip` (ajoute timestamp)."""
        now = time.time()
        dq = self.ip_requests[ip]
        dq.append(now)
        self.total_requests += 1
        # Nettoie les anciennes entrées (hors fenêtre)
        self._evict_old(dq, now)

    # -----------------------
    # _evict_old (utilitaire, non listé)
    # -----------------------
    def _evict_old(self, dq: Deque[float], now: float) -> None:
        """Supprime timestamps plus vieux que la fenêtre."""
        cutoff = now - self.window
        while dq and dq[0] < cutoff:
            dq.popleft()

    # -----------------------
    # count_recent (sous-titre)
    # -----------------------
    def count_recent(self, ip: str) -> int:
        """Retourne le nombre de requêtes de `ip` dans la fenêtre actuelle."""
        now = time.time()
        dq = self.ip_requests.get(ip, deque())
        self._evict_old(dq, now)
        return len(dq)

    # -----------------------
    # is_ddos (sous-titre)
    # -----------------------
    def is_ddos(self, ip: str) -> bool:
        """
        Renvoie True si le nombre de requêtes récentes dépasse le threshold.
        (Ne bloque pas ici — juste détection.)
        """
        count = self.count_recent(ip)
        return count >= self.threshold

    # -----------------------
    # simulate_request (sous-titre)
    # -----------------------
    def simulate_request(self) -> str:
        """
        Génère une IP aléatoire pour tests et l'enregistre.
        Retourne l'IP générée.
        """
        # Exemple simple: 5 IPs "normales" + 1 IP agressive
        pool = [
            "192.168.1.10",
            "10.0.0.5",
            "172.16.0.4",
            "8.8.8.8",
            "203.0.113.7",
            "45.77.100.200",  # éventuellement malveillante
        ]
        # plus de chances pour ip agressive si on veut simuler une attaque
        ip = random.choices(pool, weights=[10,10,10,8,6,30])[0]
        self.record(ip)
        return ip
