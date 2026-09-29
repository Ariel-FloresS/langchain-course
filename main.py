from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
#from tavily import TavilyClient
from langchain_tavily import TavilySearch
from typing import List
from pydantic import BaseModel, Field
import os

load_dotenv()


class Source(BaseModel):
    """
    Schema for source used by the agent
    """

    url: str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """
    Schema for the agent response with an answer and sources
    """
    answer: str = Field(description="The agent´s answer to the query")
    sources: List[Source] = Field(default_factory=list, description="List of sources used to generate the answer")

#tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

#@tool
#def search(query: str)->str:
#    """
#    Tool that search over internet 

#    Args:
#        query: The query to search for
    
#    Return:
#        the search result
    
#     """
#    print(f"Search for:-->: {query}")
#    return tavily.search(query = query)


llm: ChatGoogleGenerativeAI  = ChatGoogleGenerativeAI(model = os.environ.get("MODEL_NAME"),
                                                      api_key = os.environ.get("GOOGLE_API_KEY")
                                                    )
tools = [#search
        TavilySearch()   
        ]

agent = create_agent(model=llm, 
                     tools=tools,
                     response_format=AgentResponse
                     )
def main():
   
    print("Hello from langchain-course")

    result = agent.invoke(
                            {"messages": HumanMessage(content="Search for 3 job posting for an ai engineer using langchain in Mexico city as a location on linkedln")
                            }
                          )

    print(result)


if __name__ == "__main__":
    main()
