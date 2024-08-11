import subprocess
import time
import os
import json
import websocket
from dotenv import load_dotenv
from crewai_tools import tool

# Load environment variables from the .env file
load_dotenv()

class APITool:
    def __init__(self):
        # Get the API URL, Port, and Host from environment variables
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.url = f"ws://{self.host}:{self.port}/ws/orchestration-items/"

    def start_api_service(self):
        """Start the API service in the background if not already running."""
        # Check if the service is running 
        try:
            ws = websocket.create_connection(self.url)
            ws.close()
            print("FastAPI service already running.")
        except:
            print("Starting FastAPI service...")
            subprocess.Popen(["uvicorn", "SF_Stub:app", "--host", self.host, "--port", self.port, "--reload"])
            time.sleep(3)  # Wait for the service to start up

    def fetch_orchestration_items(self, customer_order: str) -> str:
        """Fetch orchestration items for a specific customer using WebSocket."""
        # Ensure the API service is running
        self.start_api_service()

        try:
            # Establish WebSocket connection
            ws = websocket.create_connection(self.url)

            # Send customer order to the WebSocket server
            ws.send(customer_order)

            # Receive orchestration items from the server
            result = ws.recv()
            ws.close()

            # Return the fetched orchestration items
            return json.loads(result)
        
        except websocket.WebSocketException as e:
            return f"WebSocket communication error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

# Creating an instance 
instance = APITool()

@tool("Orch_Items")
def fetch_orch_items(customer_order: str) -> str:
    """Fetch orchestration items for a specific customer."""
    return instance.fetch_orchestration_items(customer_order)