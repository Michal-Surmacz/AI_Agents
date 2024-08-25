from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

tools = [TavilySearchResults(max_results=1)]

prompt = hub.pull("hwchase17/react")

llm = OpenAI(temperature=0, verbose=True)

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke(
    {"input": "name = 'What is Ai Agent?"})
