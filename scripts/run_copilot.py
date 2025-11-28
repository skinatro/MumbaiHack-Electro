import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.alert_copilot import AlertCopilotService

if __name__ == "__main__":
    print("Starting Alert Copilot Service...")
    service = AlertCopilotService()
    service.start()
