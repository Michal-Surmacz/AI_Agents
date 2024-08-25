# ReAct Agent with Chat

This script sets up a chat-based AI agent using LangChain, which integrates several functionalities including search, time retrieval, and note-taking. It utilizes a structured chat agent approach to enhance interaction with users.

## 🔍 Key Steps

1. **Load environment variables** to keep API keys secure.
2. **Define Tools** to implement functions for internet search, time retrieval, and note-taking, and configure them as tools.
3. **Configure Language Model** to set up a language model for generating responses with specific settings.
4. **Set Up Memory** to utilize conversation memory to track chat history and maintain context.
5. **Create and Initialize Agent** to build a structured chat agent and set up its execution environment.
6. **Run Interaction Loop** to continuously interact with the user, process inputs, and generate responses.

## 🌟 Outcome

The script demonstrates how to create an interactive AI chat agent that can perform specific tasks and maintain conversational context, all while managing various tools and functionalities. It showcases the power of combining different components to build a comprehensive assistant.

## 🛠️Step-by-Step Code Explanation

### 1. Set Up the Environment
Ensure you load your environment variables to keep API keys secure:
```python
from dotenv import load_dotenv
load_dotenv()
```
This will read the environment variables from a `.env` file.

### 2. Define Tools
Implement the following functions and configure them as tools:
- `get_current_time`: Returns the current date and time as a string.
- `search_internet`: Searches the internet and returns information about the first result.
- `add_note_to_file`: Adds a note to a file named `notes.txt`.

```python
def get_current_time(_=None):
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def search_internet(query):
    try:
        return TavilySearchResults(max_results=1)(query)
    except Exception as e:
        return f"I could not find any information on that. Error: {str(e)}"

def add_note_to_file(text):
    filename = 'notes.txt'
    if os.path.exists(filename):
        with open(filename, 'a') as file:
            file.write(text + '\n')
    else:
        with open(filename, 'w') as file:
            file.write(text + '\n')
    return f"Note added: {text}"

tools = [
    Tool(name="Search", func=search_internet, description="Useful for when you need to know information about a particular topic."),
    Tool(name="Time", func=get_current_time, description="Useful for when you need to know the current time."),
    Tool(name="Note", func=add_note_to_file, description="Useful for when you need to create a note.")
]
```


### 3. Load the ReAct Prompt
Pull the ReAct prompt from the LangChain hub to define the logic for the AI agent.

```python
from langchain import hub
prompt = hub.pull("hwchase17/structured-chat-agent")
```

### 4. Configure the Language Model
Initialize the language model with a deterministic setting:
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(temperature=0, verbose=True)
```

### 5. Set Up Memory
Set up memory to keep track of conversation history:
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
```

### 6. Create and Initialize the Agent
Create the structured chat agent and set up its execution environment:

```python
from langchain.agents import AgentExecutor, create_structured_chat_agent

agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory, handle_parsing_errors=True)
```
Add an initial system message to the memory:
```
from langchain_core.messages import SystemMessage
initial_message = "You are an AI assistant that can provide helpful, detailed and comprehensive answers using available tools. You should always create notes after giving the response."
memory.chat_memory.add_message(SystemMessage(content=initial_message))
```

### 7. Run Interaction Loop
Implement a loop to continuously interact with the user:
```python
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        print("Exiting the chat. Goodbye!")
        break

    memory.chat_memory.add_message(HumanMessage(content=user_input))

    try:
        response = agent_executor.invoke({"input": user_input})
        response_text = response["output"]
    except Exception as e:
        response_text = f"An error occurred: {str(e)}"

    print("Bot:", response_text)

    memory.chat_memory.add_message(AIMessage(content=response_text))
```


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
Ensure that the `hub.pull("hwchase17/structured-chat-agent")` call is valid. This will pull the React agent configuration from LangChain's hub. Confirm that this is the correct identifier and that the resource exists.

### 4. Check the Availability of Tools
Confirm that `TavilySearchResults` is correctly implemented and that its `max_results` parameter is set appropriately for your use case.

### 5. Validate Memory Configuration
Ensure that `ConversationBufferMemory` is set up correctly to maintain conversation context.


### Here's a checklist of what you need to prepare:
- `.env` file with necessary API keys.
- Installed packages (`langchain`, `langchain_community`, `langchain_openai`, `python-dotenv`).
- Valid `hub.pull` reference.
- Correctly implemented and configured tools.
- Properly configured memory management.
- Optional: Error handling/logging mechanism.

After verifying these, you should be able to run the code successfully.
