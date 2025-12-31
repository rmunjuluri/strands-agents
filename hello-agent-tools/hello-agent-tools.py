from strands import Agent
from strands_tools import calculator, file_read, shell

# Add tools to our agent
#agent = Agent(
#    tools=[calculator, file_read, shell]
#)

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://192.168.68.63:11434",  # Ollama server address
    model_id="llama3.2"               # Specify which model to use
)

# Create an agent using the Ollama model
agent = Agent(model=ollama_model)

# Agent will automatically determine when to use the calculator tool
agent("What is 42 ^ 9")

print("\n\n")  # Print new lines

# Agent will use the shell and file reader tool when appropriate
agent("Show me the contents of a single file in this directory")