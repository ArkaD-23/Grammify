import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from copilotkit.langchain import copilotkit_messages_to_langchain
from research_canvas.agent import graph  # Assuming you have a grammar checking agent graph

# Load environment variables from .env
load_dotenv()

# Initialize the FastAPI app
app = FastAPI()

# Initialize CopilotKit SDK with your LangGraph agents
sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="grammar_check_agent",  # The agent for grammar checking
            description="An AI agent that checks grammar.",
            graph=graph,  # Your LangGraph workflow for grammar checking
        ),
        LangGraphAgent(
            name="grammar_check_agent_google_genai",  # Another version using Google GenAI (optional)
            description="A Google GenAI-powered grammar checking agent.",
            graph=graph,  # Reuse the same graph
        ),
    ],
)

# Add FastAPI endpoint for CopilotKit SDK integration
add_fastapi_endpoint(app, sdk, "/copilotkit")

# Health check route to ensure the server is running
@app.get("/health")
def health():
    """Health check endpoint to verify the server is working."""
    return {"status": "ok"}

# Main function to run the server
def main():
    """Run the FastAPI server using uvicorn."""
    port = int(os.getenv("PORT", "8000"))  # Port can be set via environment variable
    uvicorn.run("demo:app", host="0.0.0.0", port=port)

# Ensure the server runs when executing this file
if __name__ == "__main__":
    main()
