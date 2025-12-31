import logging
from strands_tools.calculator import calculator
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.multiagent.a2a import A2AServer

logging.basicConfig(level=logging.INFO)


# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://192.168.68.63:11434",  # Ollama server address
    model_id="llama3.2"               # Specify which model to use
)






















# Create a Strands agent
strands_agent = Agent(
    model=ollama_model,
    name="Calculator Agent",
    description="A calculator agent that can perform basic arithmetic operations.",
    tools=[calculator],
    callback_handler=None
)

# Create A2A server (streaming enabled by default)
a2a_server = A2AServer(agent=strands_agent)

# Start the server
a2a_server.serve()