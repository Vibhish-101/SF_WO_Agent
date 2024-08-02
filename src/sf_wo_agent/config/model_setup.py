import os
from langchain_google_vertexai import VertexAI
import logging

# Set up logging

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# Environment setup 

def setup_environment():
    
    logging.info("setting up environment")
    os.environ["LLM_CREDS"] = r"C:\Users\AD33119\OneDrive - Lumen\Documents\GitHub\SF_WO_Agent\src\sf_wo_agent\config\gemini_config.json"
    logging.info("Environment setup complete")
    

VERTEX_AI_CONFIG = {
    "llm": {
        "model_name" : "gemini-1.5-pro-preview-0409",
        "temperature": 0.3,
        "max_output_tokens": 8192
    }
}

setup_environment()

def get_vertex_ai_llm(key):
    
    logging.info(f"Retrieving Vertex Ai LLM with key: {key}")
    config = VERTEX_AI_CONFIG.get(key, {})
    if not config:
        logging.error(f"No configuration found for key: {key}")
        raise ValueError(f"No configuration found for  key: {key}")
    logging.info(f"Configuration found for key: {key}, creating VertexAI instance")
    return VertexAI(**config)