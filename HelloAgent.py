from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load the tokenizer and model (you must have access to LLaMA 2 on Hugging Face)
model_name = "meta-llama/Llama-2-7b-chat-hf"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")

# Create a text generation pipeline
llama_agent = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200)

# Define a basic function to interact with the AI agent
def ai_agent(prompt: str):
    response = llama_agent(prompt)
    return response[0]["generated_text"]

# Example usage
user_input = "You are an assistant helping plan a trip to Japan. Suggest a 5-day itinerary."
output = ai_agent(user_input)
print(output)
