from strands import Agent, tool
from strands_tools import calculator, current_time
from strands.models.ollama import OllamaModel

####################### - Logging - ##################
import logging
from strands import Agent

# Enables Strands debug log level
logging.getLogger("strands").setLevel(logging.DEBUG)

# Sets the logging format and streams logs to stderr
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)
####################### - Logging - ##################

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://192.168.68.63:11434",  # Ollama server address
    model_id="llama3.2"               # Specify which model to use
)

# Create an agent using the Ollama model
agent = Agent(model=ollama_model,
              tools=[current_time])

# Ask the agent a question that uses the available tools
message = """
I have 1 requests:

What is the time right now in EST?
"""
result = agent(message)
print("\n\n")
print(result.metrics.get_summary())
print("\n\n")
print(f"Total tokens: {result.metrics.accumulated_usage['totalTokens']}")
print(f"Execution time: {sum(result.metrics.cycle_durations):.2f} seconds")
print(f"Tools used: {list(result.metrics.tool_metrics.keys())}")