from strands import Agent, tool
from strands_tools import calculator, current_time
from strands.models.ollama import OllamaModel

################### - Callback Handler - #############
################### - Synchronous Applications & Custom Event Processing - #############
def handle_events(**kwargs):
    if "data" in kwargs:
        print(kwargs["data"], end="")

def debugger_callback_handler(**kwargs):
    # Print the values in kwargs
    print(kwargs)
################### - Callback Handler - #############

# Create an agent with tools from the community-driven strands-tools package
# as well as our custom letter_counter tool
#
# agent = Agent(tools=[calculator, current_time, letter_counter])

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://192.168.68.63:11434",  # Ollama server address
    model_id="llama3.2"               # Specify which model to use
)

# Create an agent using the Ollama model
agent = Agent(model=ollama_model,
              callback_handler=handle_events, 
              #tools=[calculator, current_time])
              tools=[current_time])

# Ask the agent a question that uses the available tools
message = """
I have 4 requests:

1. What is the time right now in EST?
"""
result = agent(message)
print("\n\n")
print(result.metrics.get_summary())
print("\n\n")
print(f"Total tokens: {result.metrics.accumulated_usage['totalTokens']}")
print(f"Execution time: {sum(result.metrics.cycle_durations):.2f} seconds")
print(f"Tools used: {list(result.metrics.tool_metrics.keys())}")