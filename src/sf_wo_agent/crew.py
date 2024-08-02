from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from sf_wo_agent.tools.custom_tool import ApiTools
from sf_wo_agent.config.model_setup import setup_environment, get_vertex_ai_llm



@CrewBase
class SfWoAgentCrew():
	"""SfWoAgent crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def address_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['address_manager'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def flow_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['flow_agent'],
			verbose=True
		)

	@agent
	def salesforce_account_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['salesforce_account_manager'],
			tools =[ApiTools.Account_Status_Checker],
			verbose=True
		)  

	@agent
	def service_appointment_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['service_appointment_manager'],
			tools =[ApiTools.Service_Appt_Checker],
			verbose=True
		)

	@agent
	def work_order_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['work_order_manager'],
            tools =[ApiTools.Work_Order_Checker],
			verbose=True
		)

	@agent
	def decision_matrix_evaluator(self) -> Agent:
		return Agent(
			config=self.agents_config['decision_matrix_evaluator'],
            tools =[ApiTools.SmartNID_Status_Checker],
			verbose=True
		)

	@agent
	def fiber_installation_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['fiber_installation_manager'],
            tools =[ApiTools.UDIF_Checker],
			verbose=True
		)

	@agent
	def buried_site_checker(self) -> Agent:
		return Agent(
			config=self.agents_config['buried_site_checker'],
            tools =[ApiTools.BSU_Checker],
			verbose=True
		)

	@agent
	def installation_interval_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['installation_interval_manager'],
            # tools =[],
			verbose=True
		)

	@agent
	def adapt_status_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['adapt_status_manager'],
            tools =[ApiTools.Adapt_Status_Checker],
			verbose=True
		)


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
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)