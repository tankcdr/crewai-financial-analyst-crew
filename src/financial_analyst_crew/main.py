import os
from dotenv import load_dotenv
load_dotenv()

from financial_analyst_crew import FinancialAnalystCrew

def run():
    inputs ={
        'company_name': 'Tesla',
        'quarter': 'Q12024',
    }
    FinancialAnalystCrew().crew().kickoff(inputs=inputs)
    
if __name__ == "__main__":
    run()