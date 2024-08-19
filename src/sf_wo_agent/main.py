import os
import sys

# Add the path to the sf_wo_agent directory
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'src')))


import logging
from crew import initialize_environment, initialize_agents, initialize_tasks, Orch_Crew


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Script started successfully")

def run():
    """
    Run the crew.
    """
    try:
        # Initialize environment and model
        llm = initialize_environment()

        # Initialize agents
        agents = initialize_agents(llm)

        # Initialize tasks
        tasks = initialize_tasks()

        # Create and kick off the crew
        crew_instance = Orch_Crew(agents, tasks).crew()
        inputs = {"customer_order": "A00706991"}  
        result = crew_instance.kickoff(inputs=inputs)
        logger.info("Crew kickoff complete. Result: %s", result)

    except Exception as e:
        logger.error(f"An error occurred during execution: {e}")
        raise

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "customer_order": "A00706991"
    }
    try:
        n_iterations = int(sys.argv[2])
        logger.info(f"Training crew for {n_iterations} iterations...")
        llm = initialize_environment()
        agents = initialize_agents(llm)
        tasks = initialize_tasks()
        crew_instance = Orch_Crew(agents, tasks).crew()
        crew_instance.train(n_iterations=n_iterations, inputs=inputs)
        logger.info("Crew training completed successfully")
    except IndexError:
        logger.error("Number of iterations not provided. Please specify the number of iterations as an argument.")
        raise
    except ValueError:
        logger.error("Invalid number of iterations provided. Please provide a valid integer.")
        raise
    except Exception as e:
        logger.error(f"An error occurred while training the crew: {e}")
        raise

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        task_id = sys.argv[2]
        logger.info(f"Replaying crew from task ID: {task_id}...")
        llm = initialize_environment()
        agents = initialize_agents(llm)
        tasks = initialize_tasks()
        crew_instance = Orch_Crew(agents, tasks).crew()
        crew_instance.replay(task_id=task_id)
        logger.info("Crew replay completed successfully")
    except IndexError:
        logger.error("Task ID not provided. Please specify the task ID as an argument.")
        raise
    except Exception as e:
        logger.error(f"An error occurred while replaying the crew: {e}")
        raise

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            logger.info("Running the default crew execution...")
            run()
        elif sys.argv[1].lower() == 'train':
            logger.info("Training mode selected.")
            train()
        elif sys.argv[1].lower() == 'replay':
            logger.info("Replay mode selected.")
            replay()
        else:
            logger.error("Invalid command. Please use 'train' or 'replay' as the first argument.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)