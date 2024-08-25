# AI_Agents

The repository was created for the purpose of learning how to program AI Agents. The repository contains (and will be added in the future) projects for the purpose of learning and exploring artificial intelligence. 

🔍 Key Steps

1. Load environment variables to keep API keys secure.
2. Initialize Tavily Search Tool to fetch search results.
3. Get ReAct prompt for agent logic.
4. Configure OpenAI model for deterministic responses.
5. Create and run the agent to answer queries.

🌟 Outcome

This project demonstrated the power of combining LangChain with OpenAI and external tools. Excited to explore more with AI agents!

🛠️ Step-by-Step Guide

1. Set Up the Environment
First, ensure that you have your environment variables set up correctly by loading them using dotenv.

python
Copy code
from dotenv import load_dotenv

load_dotenv()
This will load the environment variables from a .env file, which is essential for keeping your API keys secure.

2. Initialize the Search Tool
Next, initialize the Tavily Search Tool, which will be used to fetch search results.

python
Copy code
from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=1)]
Here, max_results=1 ensures that only one search result is fetched.

3. Load the ReAct Prompt
Pull the ReAct prompt from the LangChain hub to define the logic for the AI agent.

python
Copy code
from langchain import hub

prompt = hub.pull("hwchase17/react")
This step is crucial as it provides the framework for the agent’s reasoning process.

4. Configure the OpenAI Model
Configure the OpenAI model with a deterministic response by setting the temperature to 0.

python
Copy code
from langchain_openai import OpenAI

llm = OpenAI(temperature=0, verbose=True)
Setting temperature=0 ensures that the model's responses are deterministic, meaning it will generate the same output for the same input.

5. Create and Run the Agent
Create the AI agent using the create_react_agent function and run it with the AgentExecutor.

python
Copy code
from langchain.agents import AgentExecutor, create_react_agent

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
Finally, invoke the agent to respond to a specific query.

python
Copy code
agent_executor.invoke({"input": "What is Ai Agent?"})
The agent will process the input, fetch relevant information using the search tool, and provide an informed response based on the ReAct prompt.

6. Running the Code
To run the code, execute the main.py file. Ensure all dependencies are installed, and the .env file is correctly configured with your API keys.

bash
Copy code
python main.py
This will execute the AI agent with the provided input and display the result in your console.
