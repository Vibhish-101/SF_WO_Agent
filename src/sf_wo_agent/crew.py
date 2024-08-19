import logging
from crewai import Crew, Process
from crewai import Agent
from config.agents import get_agents  
from config.tasks import get_tasks   
from config.model_setup import setup_environment, get_vertex_ai_llm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_environment():
    """Setup environment and model."""
    try:
        logger.info("Setting up environment...")
        setup_environment()
        logger.info("Environment setup complete.")

        logger.info("Initializing the model...")
        llm = get_vertex_ai_llm('llm')
        logger.info("Model initialization complete.")
        
        return llm
    except Exception as e:
        logger.error(f"Error during environment setup or model initialization: {e}")
        raise

def initialize_agents(llm):
    """Initialize agents with the given model."""
    try:
        logger.info("Initializing agents...")
        agents = get_agents(llm)
        logger.info("Agents initialization complete.")
        return agents
    except Exception as e:
        logger.error(f"Error during agents initialization: {e}")
        raise

def initialize_tasks():
    """Initialize tasks."""
    try:
        logger.info("Initializing tasks...")
        tasks = get_tasks()
        logger.info("Tasks initialization complete.")
        return tasks
    except Exception as e:
        logger.error(f"Error during tasks initialization: {e}")
        raise
    
# Initialize environment and model
llm = initialize_environment()
    
orchestration_agent = Agent(
        role='Telecom Orchestration Manager',
        goal=(
            "Oversee and coordinate the end-to-end telecom service orchestration process. "
            "Ensure smooth interaction between the Order Lookup, Order Validation, Service Provisioning, "
            "Inventory Management, Installation Scheduling, Technician Dispatch, and Order Status Update agents."
        ),
        backstory=(
            "An experienced telecom operations leader with deep expertise in managing complex service "
            "orchestration workflows. Responsible for ensuring that each agent executes their tasks in sync, "
            "managing dependencies, and adapting to real-time changes or issues in the process."
        ),
        verbose=True,
        allow_delegation=True,
        llm =llm
    )

class Orch_Crew:
    """Orch_Crew"""

    def __init__(self, agents, tasks):
        self.agents = agents
        self.tasks = tasks

    def crew(self) -> Crew:
        """Creates the Orch_Crew"""
        logger.info("Creating the Orch_Crew...")
        try:
            crew_instance = Crew(
                agents=list(self.agents.values()),  
                tasks=list(self.tasks.values()),    
                verbose=2,
                manager_agent=orchestration_agent,  
                process=Process.hierarchical,
                output_log_file=True
            )
            logger.info("Crew creation complete.")
            return crew_instance
        except Exception as e:
            logger.error(f"Error during crew creation: {e}")
            raise
