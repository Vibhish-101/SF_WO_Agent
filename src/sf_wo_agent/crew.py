from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from sf_wo_agent.tools.custom_tools_1 import fetch_orch_items
from sf_wo_agent.config.model_setup import setup_environment, get_vertex_ai_llm

# Load the Environment
setup_environment()

# Initialise the Model
llm = get_vertex_ai_llm('llm')

@CrewBase
class SfWoAgentCrew:
    """SfWoAgent crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    ################################################################ AGENTS ####################################################################################

    @agent
    def order_lookup(self) -> Agent:
        return Agent(
            config=self.agents_config['order_lookup'],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def order_validation(self) -> Agent:
        return Agent(
            config=self.agents_config['order_validation'],
            tools = [fetch_orch_items],
            verbose=True,       
            allow_delegation=True,
            llm=llm
        )

    @agent
    def service_provision(self) -> Agent:
        return Agent(
            config=self.agents_config['service_provision'],
            tools=[fetch_orch_items],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def inventory_management(self) -> Agent:
        return Agent(
            config=self.agents_config['inventory_management'],
            tools=[fetch_orch_items],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def installation_scheduling(self) -> Agent:
        return Agent(
            config=self.agents_config['installation_scheduling'],
            tools=[fetch_orch_items],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def technician_dispatch(self) -> Agent:
        return Agent(
            config=self.agents_config['technician_dispatch'],
            tools=[fetch_orch_items],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def order_status_update(self) -> Agent:
        return Agent(
            config=self.agents_config['order_status_update'],
            tools=[fetch_orch_items],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def monitoring_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['monitoring_agent'],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def resolution_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['resolution_agent'],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def dependency_mapping_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['dependency_mapping_agent'],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def notification_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['notification_agent'],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    @agent
    def orchestration_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestration_agent'],
            verbose=True,
            allow_delegation=True,
            llm=llm
        )

    ################################################################### TASKS ##########################################################################################

    @task
    def account_update_speed_and_charge(self) -> Task:
        return Task(
            config=self.tasks_config['account_update_speed_and_charge']
        )

    @task
    def create_account_contact_updates(self) -> Task:
        return Task(
            config=self.tasks_config['create_account_contact_updates']
        )

    @task
    def update_wo_and_sa(self) -> Task:
        return Task(
            config=self.tasks_config['update_wo_and_sa']
        )

    @task
    def update_wo_facilities(self) -> Task:
        return Task(
            config=self.tasks_config['update_wo_facilities']
        )

    @task
    def get_and_activate_dtn(self) -> Task:
        return Task(
            config=self.tasks_config['get_and_activate_dtn']
        )

    @task
    def get_health_certificate(self) -> Task:
        return Task(
            config=self.tasks_config['get_health_certificate'],
            agent=self.reporting_analyst()
        )

    @task
    def acs_on_reset_gateway(self) -> Task:
        return Task(
            config=self.tasks_config['acs_on_reset_gateway']
        )

    @task
    def acs_smartnid_reset_gateway(self) -> Task:
        return Task(
            config=self.tasks_config['acs_smartnid_reset_gateway']
        )

    @task
    def assia_on_update_speed(self) -> Task:
        return Task(
            config=self.tasks_config['assia_on_update_speed']
        )

    @task
    def assia_speed_update(self) -> Task:
        return Task(
            config=self.tasks_config['assia_speed_update']
        )

    @task
    def create_zuora_subscription(self) -> Task:
        return Task(
            config=self.tasks_config['create_zuora_subscription']
        )

    @task
    def fiber_provisioning_modified(self) -> Task:
        return Task(
            config=self.tasks_config['fiber_provisioning_modified']
        )

    @task
    def hsi_fiber_assetize(self) -> Task:
        return Task(
            config=self.tasks_config['hsi_fiber_assetize']
        )

    @task
    def improv_on_remove_dtn_from_walled(self) -> Task:
        return Task(
            config=self.tasks_config['improv_on_remove_dtn_from_walled']
        )

    @task
    def improv_speed_change(self) -> Task:
        return Task(
            config=self.tasks_config['improv_speed_change']
        )

    @task
    def optius_on_reset_speed(self) -> Task:
        return Task(
            config=self.tasks_config['optius_on_reset_speed']
        )

    @task
    def optius_on_update_speed(self) -> Task:
        return Task(
            config=self.tasks_config['optius_on_update_speed']
        )

    @task
    def oss_fiber_speed_change(self) -> Task:
        return Task(
            config=self.tasks_config['oss_fiber_speed_change']
        )

    @task
    def oss_instantwifi_speed_change(self) -> Task:
        return Task(
            config=self.tasks_config['oss_instantwifi_speed_change']
        )

    @task
    def oss_optius_fiber_activation_new_customer(self) -> Task:
        return Task(
            config=self.tasks_config['oss_optius_fiber_activation_new_customer']
        )

    @task
    def oss_voice_activation_existing_customer(self) -> Task:
        return Task(
            config=self.tasks_config['oss_voice_activation_existing_customer']
        )

    @task
    def oss_voice_porting(self) -> Task:
        return Task(
            config=self.tasks_config['oss_voice_porting']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SfWoAgent crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,    # Automatically created by the @task decorator
            verbose=2,
            manager_agent=self.orchestration_agent,
            process=Process.hierarchical
        )