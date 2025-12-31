from strands import Agent
from strands.models.ollama import OllamaModel

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://192.168.68.63:11434",  # Ollama server address
    model_id="llama3.2"               # Specify which model to use
)

# Create an agent using the Ollama model
agent = Agent(model=ollama_model,
            state={
                "user_preferences": {"theme": "dark"}, 
                "session_count": 0
                }
            )

print(agent.state.get("user_preferences"))

agent.state.set("last_action", "login")
agent.state.set("session_count", 1)
print("\n")
print(agent.state.get())

# Send a message and get a response
agent("Hello!")
print("\n")
# Access the convesation history
print(agent.messages)  # Show all messages