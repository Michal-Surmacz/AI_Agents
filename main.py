import os
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from dotenv import load_dotenv
from datetime import datetime
from langchain_community.tools.tavily_search import TavilySearchResults

# Load the environment variables from .env file
load_dotenv()

# Define the tools


def get_current_time(_=None):
    """Returns the current time as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def search_internet(query):
    """Searches the internet and returns information about the first result."""
    try:
        return TavilySearchResults(max_results=1)(query)
    except Exception as e:
        return f"I could not find any information on that. Error: {str(e)}"


def add_note_to_file(text):
    """Create a new note baseod on the information searched in the internet."""
    filename = 'notes.txt'
    if os.path.exists(filename):
        with open(filename, 'a') as file:
            file.write(text + '\n')
    else:
        with open(filename, 'w') as file:
            file.write(text + '\n')
    return f"Note added: {text}"


tools = [
    Tool(
        name="Search",
        func=search_internet,
        description="Useful for when you need to know information about a particular topic.",
    ),
    Tool(
        name="Time",
        func=get_current_time,
        description="Useful for when you need to know the current time.",
    ),
    Tool(
        name="Note",
        func=add_note_to_file,
        description="Useful for when you need to create a note.",
    )
]

# Pull the prompt for the structured chat agent
prompt = hub.pull("hwchase17/structured-chat-agent")

# Initialize the language model with desired settings
llm = ChatOpenAI(temperature=0, verbose=True)

# Set up memory to keep track of the conversation history
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True
)

# Create the agent using the language model, tools, and prompt
agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)

# Initialize the agent executor to handle interactions
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True
)

# Add the initial system message to the memory
initial_message = "You are an AI assistant that can provide helpful, detailed and comprehensive answers using available tools. You should always create notes after giving the response. "
memory.chat_memory.add_message(SystemMessage(content=initial_message))

# Main loop to interact with the user
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        print("Exiting the chat. Goodbye!")
        break

    # Add the user's input to memory and generate a response
    memory.chat_memory.add_message(HumanMessage(content=user_input))

    try:
        response = agent_executor.invoke({"input": user_input})
        response_text = response["output"]
    except Exception as e:
        response_text = f"An error occurred: {str(e)}"

    print("Bot:", response_text)

    # Add the AI's response to memory
    memory.chat_memory.add_message(AIMessage(content=response_text))
