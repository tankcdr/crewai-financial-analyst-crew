import os
from pydantic import Field
import requests
from typing import Optional
from urllib.parse import urlencode
from langchain_core.tools import BaseTool

from langchain_core.callbacks import CallbackManagerForToolRun

class BraveSearchTool(BaseTool):
  """Tool that searches the Internet using teh Brave Search API"""
  
  name: str = "brave_internet_search"
  description: str = (
    "Useful to search the internet using the Brave Search API "
    "about a a given topic and return relevant results. "
    "Input should be a query. "
    " For example, 'What is an LLM?'."
  )
  
  top_k: int = Field(default=10, ge=1, le=20, description="Number of results to return", example=10)  
  safesearch: str = Field(default="strict", description="Safe search level", example="strict", enum=["off", "moderate", "strict"])  
  
  def __init__(self, top_k: int = 10, safesearch: str = "strict", **kwargs):
    super().__init__(**kwargs)  # Ensure any additional initialization from BaseTool is called
    self.top_k = min(20, max(10, top_k))
    self.safesearch = safesearch
  
  def _run(
      self,
      query: str,
      run_manager: Optional[CallbackManagerForToolRun] = None,
  ) -> str:
    """Useful to search the internet about a a given topic and return relevant results."""
    # Build the query parameters
    params = {
        'q': query,  # URL encode the query
        'count': self.top_k,  # Control the number of results
        'safesearch': self.safesearch, # Control the adult content level
        'result_filter': "web"
    }
    encoded_params = urlencode(params)  # URL encode the whole parameters
    url = f"https://api.search.brave.com/res/v1/web/search?{encoded_params}"
    
    # Set up headers
    headers = {
        'X-Subscription-Token': os.environ['BRAVE_SEARCH_API_KEY'],
        'content-type': 'application/json'
    }
        
    try:
      response = requests.get(url, headers=headers)
      response.raise_for_status()  # Raises HTTPError for bad requests
      results = response.json().get('web', {}).get('results', [])
      return '\n'.join(
          f"Title: {result.get('title', 'No title available')}\n"
          f"Link: {result.get('url', 'No URL available')}\n"
          f"Snippet: {result.get('description', 'No description available')}\n"
          f"Date: {result.get('page_age', 'No date available')}\n"
          "-----------------\n"
          for result in results
      )
    except requests.RequestException as e:
        return f"An error occurred: {str(e)}"
  
if __name__ == "__main__":
  search_tool = BraveSearchTool(top_k=5, safesearch="off")  # Adjust top_k as needed
  sample_query = "what is python"
  result = search_tool._run(query=sample_query)
  print(result)
