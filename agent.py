from crewai import Agent
from langchain_community import tools

# address_manager= Agent(
#     role= "Address Manager",
#     goal= "Manage address-related inputs and data",
#     tools=["Account_Status_Checker"]
#     backstory=("Expert in handling and verifying address information.")
# )

# flow_agent=Agent(
#     role="Salesforce Order Manager",
#     goal="create and manage SF-orders, inputs and data",
#     tools=["json"],
#     backstory=("Skilled in managing order data with salesforce"),
# )


# salesforce_account_manager=Agent(
#     role="Salesforce Account Manager",
#     goal="Create and update SF-Accounts",
#     backstory= ("Proficient in handling account information in Salesforce."))

# service_appointment_manager=Agent(
#     role="Service Appointment Manager",
#     goal=" Schedule and manage service appointments",
#     backstory="Adept at organizing and scheduling appointments efficiently.")

# work_order_manager=Agent(
#     role=" Work Order Manager",
#     goal=" Create work orders based on inputs and criteria",
#     backstory=" Experienced in managing work orders and ensuring accuracy.")

# decision_matrix_evaluator=Agent(
#     role= "Decision Matrix Evaluator",
#     goal=" Evaluate the decision matrix for eligibility and status",
#     backstory="Expert in analyzing decision matrices and determining outcomes.")

# fiber_installation_manager=Agent(
#   role="Fiber Installation Manager",
#   goal="Handle fiber drop installation checks via QFAST API",
#   backstory="Skilled in managing fiber installations and API interactions.")

# buried_site_checker=Agent(
#   role="Buried Site Checker",
#   goal="Perform buried site checks when required",
#   backstory="Experienced in conducting site checks for buried utilities.")

# installation_interval_manager=Agent(
#   role="Installation Interval Manager",
#   goal=" Manage installation intervals based on specific conditions",
#   backstory=" Proficient in scheduling and managing installation timelines.")

# adapt_status_manager=Agent(
#     role=" ADAPT Status Manager",
#     goal="Handle ADAPT status checks and manage related work orders",
#     backstory="Expert in monitoring and managing ADAPT statuses.")


HSI_Fiber_order_init= Agent(
    role="HSI fiber order initializer",
    goal= "Initialize the Fiber order to complete as milestone",
    tools=["object"],
    backstory=("Responsible to kickstart the fiber order")
)

Improv_agent= Agent(
    role="HSI fiber order initializer",
    goal= "Initialize the Fiber order to complete as milestone",
    tools=["object"],
    backstory=("Responsible to kickstart the fiber order")
)

Validator_agent= Agent(
    role="Order validate Agent",
    goal= "Validate the details retrieved from the order ",
    tools=["object"],
    backstory=("Expert in fetching the order related details whether it is available or not. If not then it should be a failure")
)

Order_conformation_agent= Agent(
    role="Order Comfirmation Manager",
    goal= "Kickstart the order confirmation tasks as milestone",
    tools=["object"],
    backstory=("Professional in starting the order confirmation and other tasks")
)

Order_conformation_agent= Agent(
    role="Order Comfirmation Manager",
    goal= "Kickstart the order confirmation tasks as milestone",
    tools=["object"],
    backstory=("Professional in starting the order confirmation and other tasks")
)

Failure_finding_agent= Agent(
    role="Review Manager",
    goal= "Review all milestones if any got faiure it notifies which item is failed",
    tools=["object"],
    backstory=("Professional in review the milestones when the pending status of the miletone is reached active or failure" )
) 

Zora_agent= Agent(
    role="Zora Coupon code Generator",
    goal= "Kickstart the Zora subscription tasks as milestone",
    tools=["object"],
    backstory=("Professional in starting the Zora subscription")
)
Completion_agent= Agent(
    role="Completion Manager",
    goal= "Completion Checking Manager",
    tools=["object"],
    backstory=("Professional in reviewing the milestones are completed or not. Verify Account status is active" )
) 














