import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from agent import graph  

load_dotenv()

app = FastAPI()

sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="language_tutoring_agent", 
            description="An agent that helps users learn languages with interactive questions and answers.",
            graph=graph,  
        )
    ],
)
add_fastapi_endpoint(app, sdk, "/copilotkit")

@app.post("/interact")
async def interact(user_input: str, language: str):
    response = sdk.run_agent(
        "language_tutoring_agent",
        input={"user_input": user_input, "language": language}
    )
    return response


def main():
    port = int(os.getenv("PORT", "8000")) 
    uvicorn.run("app:app", host="localhost", port=port, reload=True)
