from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from crewai_tools import WebsiteSearchTool, SerperDevTool
from financial_analyst_crew.tools.BraveSearchTools import BraveSearchTools

@CrewBase
class FinancialAnalystCrew():
    """FinancialAnalystCrew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    def __init__(self) -> None:
        self.llm  = ChatOpenAI(model="gpt-4")
        
    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            config = self.agents_config["company_researcher"], 
            llm=self.llm,
            #tools = [YahooFinanceNewsTool(), WebsiteSearchTool(), SerperDevTool()]
        )
        
    @agent
    def company_analyst(self) -> Agent:
        return Agent(
            config = self.agents_config["company_analyst"], 
            llm=self.llm
        )
        
    @task
    def company_research_task(self) -> Task:
        return Task(
            config = self.tasks_config["research_company_task"],
            agent = self.company_researcher()
        )
        
    @task
    def analyze_company_task(self) -> Task:
        return Task(
            config = self.tasks_config["analyze_company_task"],
            agent = self.company_analyst()
        )
        
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents = self.agents,
            tasks =self.tasks,
            process = Process.sequential,
            verbose=2
        )
