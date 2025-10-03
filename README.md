# DDOS_protector_bot

🛡️ **DDOS_protector_bot** est un logiciel de cybersécurité conçu pour détecter et bloquer les attaques DDoS en temps réel.  
Il fournit un tableau de bord clair, journalise tous les événements et permet de simuler facilement des requêtes pour tester la protection des serveurs et des réseaux.

---

## Fonctionnalités principales

- Détection en temps réel des attaques DDoS grâce à un module de surveillance des requêtes IP.  
- Blocage automatique des IP suspectes via un module de blacklist.  
- Tableau de bord console interactif pour suivre les statistiques en direct.  
- Journalisation complète des événements et blocages pour analyse post-incident.  
- Simulation de requêtes pour tester la robustesse du système.

---

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/tonpseudo/DDOS_protector_bot.git

Pour installer les dépandences python : pip install -r requirements.txt
pour lancer le projet : python main.py


DDOS_protector_bot/
├── firewall/
│   ├── __init__.py         # Init du package firewall
│   ├── detector.py         # Module de détection DDoS
│   ├── blocker.py          # Module de blocage des IP
│   └── logger.py           # Module de journalisation des événements
├── dashboard/
│   ├── __init__.py         # Init du package dashboard
│   └── dashboard.py        # Affichage et mise à jour du tableau de bord
├── main.py                 # Point d’entrée du projet
├── README.md               # Ce fichier
├── .gitignore              # Fichiers ignorés par Git
└── LICENSE                 # Licence du projet

