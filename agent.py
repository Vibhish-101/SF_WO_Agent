from crewai import Agent
from langchain_community import tools

address_manager= Agent(
    role= "Address Manager",
    goal= "Manage address-related inputs and data",
    backstory=("Expert in handling and verifying address information.")
)

flow_agent=Agent(
    role="Salesforce Order Manager",
    goal="create and manage SF-orders, inputs and data",
    tools=["json"],
    backstory=("Skilled in managing order data with salesforce"),
)


salesforce_account_manager=Agent(
    role="Salesforce Account Manager",
    goal="Create and update SF-Accounts",
    backstory= ("Proficient in handling account information in Salesforce."))

service_appointment_manager=Agent(
    role="Service Appointment Manager",
    goal=" Schedule and manage service appointments",
    backstory="Adept at organizing and scheduling appointments efficiently.")

work_order_manager=Agent(
    role=" Work Order Manager",
    goal=" Create work orders based on inputs and criteria",
    backstory=" Experienced in managing work orders and ensuring accuracy.")

decision_matrix_evaluator=Agent(
    role= "Decision Matrix Evaluator",
    goal=" Evaluate the decision matrix for eligibility and status",
    backstory="Expert in analyzing decision matrices and determining outcomes.")

fiber_installation_manager=Agent(
  role="Fiber Installation Manager",
  goal="Handle fiber drop installation checks via QFAST API",
  backstory="Skilled in managing fiber installations and API interactions.")

buried_site_checker=Agent(
  role="Buried Site Checker",
  goal="Perform buried site checks when required",
  backstory="Experienced in conducting site checks for buried utilities.")

installation_interval_manager=Agent(
  role="Installation Interval Manager",
  goal=" Manage installation intervals based on specific conditions",
  backstory=" Proficient in scheduling and managing installation timelines.")

adapt_status_manager=Agent(
    role=" ADAPT Status Manager",
    goal="Handle ADAPT status checks and manage related work orders",
    backstory="Expert in monitoring and managing ADAPT statuses.")