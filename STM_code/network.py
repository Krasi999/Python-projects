import time
 
# ──────────────────────────────────────────────
# Целева платформа: PC симулация (без хардуерни ограничения),
# моделираща реални сценарии за мобилни и IoT устройства.
#
# Целева латентност:
#   - Broadband WiFi : < 100ms обща латентност при 720p
#   - 4G Mobile      : < 500ms обща латентност при 480p
#   - IoT Narrowband : < 5s обща латентност при 480p (приемливо за batch изпращане)
# ──────────────────────────────────────────────
 
SCENARIOS = {
    "Broadband_WiFi": {
        "bw_mbps": 50,
        "latency_ms": 10,
        "description": "Home/Office WiFi - typical for indoor mobile apps"
    },
    "4G_Mobile": {
        "bw_mbps": 10,
        "latency_ms": 50,
        "description": "4G LTE - typical outdoor mobile scenario"
    },
    "IoT_Narrowband": {
        "bw_mbps": 0.5,
        "latency_ms": 200,
        "description": "NB-IoT/LoRa - low bandwidth, high latency"
    }
}
 
def simulate_network_transfer(size_bytes, scenario_name="4G_Mobile"):
    """
    Simulates network transfer time without real blocking.
 
    IMPORTANT: We do NOT use time.sleep() here because:
    1. sleep() distorts results - IoT looks faster than it is in reality.
    2. The goal is measurement and comparison, not real waiting simulation.
 
    Returns:
        total_time_seconds (float) - calculated theoretical transfer time
    """
    config = SCENARIOS.get(scenario_name, SCENARIOS["4G_Mobile"])
 
    latency_sec = config["latency_ms"] / 1000.0
    # Mbps → Bytes per second: (Mbps * 1024 * 1024) / 8
    bw_bps = (config["bw_mbps"] * 1024 * 1024) / 8
    transfer_time = size_bytes / bw_bps
 
    total_time = latency_sec + transfer_time
    return total_time
 
 
def get_scenario_description(scenario_name):
    """Returns the description of the network scenario."""
    scenario = SCENARIOS.get(scenario_name)
    if scenario:
        return scenario.get("description", "")
    return ""