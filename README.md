# AI_Agents

This repository is designed for learning how to program AI Agents. It includes various projects that focus on learning and exploring artificial intelligence. More projects will be added in the future.


## 🔍 Key Steps

1. **Load environment variables** to keep API keys secure.
2. **Initialize Tavily Search Tool** to fetch search results.
3. **Get ReAct prompt** for agent logic.
4. **Configure OpenAI model** for deterministic responses.
5. **Create and run the agent** to answer queries.
6. 

## 🌟 Outcome

This project demonstrates the power of combining LangChain with OpenAI and external tools. I’m excited to explore more with AI agents!


## 🛠️Step-by-Step Code Explanation

### 1. Set Up the Environment
First, ensure that you have your environment variables set up correctly by loading them using `dotenv`:
```python
from dotenv import load_dotenv

load_dotenv()
```
This will load the environment variables from a .env file, which is essential for keeping your API keys secure.

### 2. Initialize the Search Tool
Next, initialize the Tavily Search Tool, which will be used to fetch search results.

```python
from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=1)]
```
Here, `max_results=1` ensures that only one search result is fetched.

### 3. Load the ReAct Prompt
Pull the ReAct prompt from the LangChain hub to define the logic for the AI agent.

```python
from langchain import hub
prompt = hub.pull("hwchase17/react")
```
This step is crucial as it provides the framework for the agent’s reasoning process.

### 4. Configure the OpenAI Model
Configure the OpenAI model with a deterministic response by setting the temperature to 0.
```python
from langchain_openai import OpenAI
llm = OpenAI(temperature=0, verbose=True)
```
Setting `temperature=0` ensures that the model's responses are deterministic, meaning it will generate the same output for the same input.

### 5. Create and Run the Agent
Create the AI agent using the create_react_agent function and run it with the AgentExecutor.
```python
from langchain.agents import AgentExecutor, create_react_agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```
Finally, invoke the agent to respond to a specific query.
```python
agent_executor.invoke({"input": "What is Ai Agent?"})
```
The agent will process the input, fetch relevant information using the search tool, and provide an informed response based on the ReAct prompt.

### 6. Running the Code
To run the code, execute the main.py file. Ensure all dependencies are installed, and the .env file is correctly configured with your API keys. Instruction what to do before run code is below. 

```bash
python main.py
```

This will execute the AI agent with the provided input and display the result in your console.


## 🛠️Step-by-Step Guide Before Run Code 
### 1. Install Required Packages
Make sure you have all the necessary packages installed. You can install them using pip:
```
pip install langchain langchain_community langchain_openai python-dotenv
```

### 2. Set Up Environment Variables 
The `load_dotenv()` function loads environment variables from a `.env` file. Ensure that you have a `.env` file in your working directory with the required API keys or configuration settings. For instance, if you're using OpenAI, your `.env` file might need an `OPENAI_API_KEY` entry:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Verify Hub Pull
Ensure that the `hub.pull("hwchase17/react")` call is valid. This will pull the React agent configuration from LangChain's hub. Confirm that this is the correct identifier and that the resource exists.

### 4. Check the Availability of Tools
Confirm that `TavilySearchResults` is correctly implemented and that its `max_results` parameter is set appropriately for your use case.

### 5. Validate Your Prompt
Ensure that the prompt used with `create_react_agent` is valid and fits the expected format. The prompt should be in a format that the agent can understand and use.

### 6. Verify `AgentExecutor` Invocation 
The `invoke` method should be called with an appropriate input format that matches what the agent expects. Ensure that the input dictionary structure is correct and that the key `"input"` is what the agent expects.

### Here's a checklist of what you need to prepare:
- `.env` file with necessary API keys.
- Installed packages (`langchain`, `langchain_community`, `langchain_openai`, `python-dotenv`).
- Valid `hub.pull` reference.
- Correctly configured `TavilySearchResults` tool.
- Accurate prompt format for `create_react_agent`.
- Optional: Error handling/logging mechanism.

After verifying these, you should be able to run the code successfully.
