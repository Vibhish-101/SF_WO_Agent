from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from sf_wo_agent.tools.custom_tools_1 import fetch_orch_items
from sf_wo_agent.config.model_setup import setup_environment, get_vertex_ai_llm

# Load the Environment
setup_environment()

# Initialise the Model
llm = get_vertex_ai_llm('llm')



@CrewBase
class SfWoAgentCrew():
	"""SfWoAgent crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
 
## AGENTS

	@agent
	def order_lookup(self) -> Agent:
		return Agent(
			config=self.agents_config['order_lookup'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
            allow_delegation=True
		)

	@agent
	def order_validation(self) -> Agent:
		return Agent(
			config=self.agents_config['order_validation'],
			verbose=True,
            allow_delegation=True
		)

	@agent
	def service_provision(self) -> Agent:
		return Agent(
			config=self.agents_config['service_provision'],
			tools =[ApiTools.Account_Status_Checker],
			verbose=True,
			allow_delegation=True
		)  

	@agent
	def inventory_management(self) -> Agent:
		return Agent(
			config=self.agents_config['inventory_management'],
			tools =[ApiTools.Service_Appt_Checker],
			verbose=True,
			allow_delegation=True
		)

	@agent
	def installation_scheduling(self) -> Agent:
		return Agent(
			config=self.agents_config['installation_scheduling'],
            tools =[ApiTools.Work_Order_Checker],
			verbose=True,
			allow_delegation=True
		)

	@agent
	def technician_dispatch(self) -> Agent:
		return Agent(
			config=self.agents_config['technician_dispatch'],
            tools =[ApiTools.SmartNID_Status_Checker],
			verbose=True,
			allow_delegation=True
		)

	@agent
	def order_status_update(self) -> Agent:
		return Agent(
			config=self.agents_config['order_status_update'],
            tools =[ApiTools.UDIF_Checker],
			verbose=True
		)

	
## TASKS


	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SfWoAgent crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			process=Process.hierarchical, 
            manager_llm = llm
		)