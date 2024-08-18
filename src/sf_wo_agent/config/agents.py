from crewai import Agent
from tools.custom_tools_1 import fetch_orch_items  # Import your custom tool

def get_agents(llm):
    """Returns a dictionary of agents initialized with their configurations."""
    agents = {}

    agents['order_lookup'] = Agent(
        role='Order Lookup Agent',
        goal='Retrieve order details using the given order number {customer_order}.',
        backstory=(
            "You're responsible for retrieving all relevant details about an order "
            "using the provided order number. You work efficiently to ensure that all "
            "necessary information is accurately fetched for further processing."
        ),
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['order_validation'] = Agent(
        role='Order Validation Agent',
        goal='Validate and Ensure all order details are accurate and up-to-date.',
        backstory=(
            "You are tasked with ensuring that the order details retrieved are complete "
            "and accurate. Your role is critical in preventing errors and ensuring the "
            "smooth progression of the order processing."
        ),
        tools=[fetch_orch_items],  # Use the custom tool here
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['service_provision'] = Agent(
        role='Service Provisioning Agent',
        goal='Provision services for the customer based on the order details.',
        backstory=(
            "You are responsible for configuring and activating the services that the "
            "customer has ordered. Your efficiency and accuracy ensure that customers "
            "receive their services without delay."
        ),
        tools=[fetch_orch_items],  # Use the custom tool here
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['inventory_management'] = Agent(
        role='Inventory Management Agent',
        goal='Manage and allocate inventory resources.',
        backstory=(
            "You ensure that all necessary equipment and resources are available and "
            "allocated for service provisioning. Your role is crucial in preventing delays "
            "due to resource shortages."
        ),
        tools=[fetch_orch_items],  # Use the custom tool here
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['installation_scheduling'] = Agent(
        role='Installation Scheduling Agent',
        goal='Schedule and coordinate installation appointments with the customer.',
        backstory=(
            "You coordinate with customers to schedule installation appointments, "
            "ensuring that all logistics are handled smoothly and efficiently."
        ),
        tools=[fetch_orch_items],  # Use the custom tool here
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['technician_dispatch'] = Agent(
        role='Technician Dispatch Agent',
        goal='Dispatch technicians and confirm dispatch details.',
        backstory=(
            "A meticulous agent ensuring technicians are dispatched correctly, "
            "ensuring they have all the necessary information and resources for "
            "successful installation."
        ),
        tools=[fetch_orch_items],  # Use the custom tool here
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['order_status_update'] = Agent(
        role='Order Status Update Agent',
        goal='Update order statuses and notify systems.',
        backstory=(
            "You are responsible for keeping the customer and internal systems updated "
            "with the current status of the order at each step and accurate."
        ),
        tools=[fetch_orch_items],  # Use the custom tool here
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['monitoring_agent'] = Agent(
        role='Real-Time Monitoring Specialist',
        goal=(
            "Continuously track the execution status of all tasks across different agents, "
            "detecting and flagging issues or delays in real-time. Provide insights and alerts "
            "to the Orchestration Agent."
        ),
        backstory=(
            "A diligent telecom process expert with a focus on real-time monitoring and "
            "issue detection. Capable of identifying potential bottlenecks, inefficiencies, "
            "or anomalies in the service orchestration process, ensuring that issues are "
            "addressed before they impact the overall flow."
        ),
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['resolution_agent'] = Agent(
        role='Issue Resolution Specialist',
        goal=(
            "Analyze and resolve issues detected during the telecom service orchestration process. "
            "Develop and implement strategies to minimize disruptions and ensure that services are "
            "provisioned efficiently."
        ),
        backstory=(
            "A seasoned problem solver with a strong background in telecom service delivery. "
            "Known for quickly diagnosing complex issues and proposing effective solutions, "
            "leveraging AI, historical data, and industry best practices."
        ),
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['dependency_mapping_agent'] = Agent(
        role='Dependency Mapping and Workflow Coordinator',
        goal=(
            "Maintain an accurate and up-to-date map of all dependencies within the telecom service "
            "orchestration process. Ensure that tasks are executed in the correct order and that all "
            "dependencies are satisfied before advancing to subsequent steps."
        ),
        backstory=(
            "A meticulous planner with a deep understanding of telecom workflows and task dependencies. "
            "Responsible for ensuring that each task is executed in the right sequence, avoiding delays "
            "and errors caused by unmet dependencies."
        ),
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    agents['notification_agent'] = Agent(
        role='User and Stakeholder Notification Manager',
        goal=(
            "Provide timely and relevant notifications to stakeholders, keeping them informed of the "
            "progress, issues, and resolutions within the telecom service orchestration process."
        ),
        backstory=(
            "A communication specialist with expertise in telecom operations, dedicated to ensuring that "
            "all stakeholders are kept in the loop. Known for delivering clear, actionable updates that help "
            "prevent delays and ensure smooth service delivery."
        ),
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    return agents