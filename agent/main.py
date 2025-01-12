from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.agent.agent import LanguageTutoringAgent
from agent.agent.open_ai_client import OpenAIClient

app = FastAPI(
    title="Language Tutoring Agent",
    description="An intelligent agent for language learning with dynamic workflows",
    version="1.0.0"
)

# Initialize OpenAI client
openai_client = OpenAIClient(
    base_url="https://models.inference.ai.azure.com",
    api_key="your-openai-api-key"
)

# Initialize the tutoring agent
language_agent = LanguageTutoringAgent(openai_client=openai_client)

class UserInput(BaseModel):
    language: str
    user_input: str

@app.post("/language-agent/")
async def language_agent_endpoint(input_data: UserInput):
    """
    Handle language learning workflow dynamically based on user input.
    """
    try:
        response = language_agent.handle_workflow(input_data.language, input_data.user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))