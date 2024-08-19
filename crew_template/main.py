#!/usr/bin/env python
import sys
from crew import SfWoAgentCrew
import logging

logging.basicConfig(level=logging.INFO)

logging.info("successfully started")

def run():
    """
    Run the crew.
    """
    inputs = {
        'customer_order': 'A00706991'
    }
    SfWoAgentCrew().crew().kickoff(inputs=inputs)
    logging.info("successfully run")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "customer_order": "A00706991"
    }
    try:
        SfWoAgentCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
    
    logging.info("successfullt train")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SfWoAgentCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
    
        logging.info("successfullt replay")
        

run()