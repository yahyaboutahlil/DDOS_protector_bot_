# main.py - integration test
from firewall.detector import DDOSDetector
from firewall.blocker import Blocker
from firewall.logger import Logger
from dashboard import Dashboard
import time

detector = DDOSDetector(threshold=10, window_seconds=10)  # seuil bas pour test
blocker = Blocker()
logger = Logger()

dash = Dashboard(detector, blocker)

# simulation: plusieurs requêtes
for _ in range(60):
    ip = detector.simulate_request()
    if detector.is_ddos(ip) and not blocker.is_blocked(ip):
        blocker.block(ip)
        logger.log_event(f"Blocked IP {ip} after {detector.count_recent(ip)} requests")
    time.sleep(0.05)

dash.show_status()
print("\nLast log lines:")
for line in logger.read_recent(10):
    print(line)
