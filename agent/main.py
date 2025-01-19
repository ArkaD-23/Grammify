import os
from dotenv import load_dotenv
load_dotenv()  

from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from agent import graph  

app = FastAPI()

sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="langgraph_agent",
            description="An agent that can generate or review code.",
            graph=graph,  
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

def main():
    port = int(os.getenv("PORT", "8000"))  
    uvicorn.run("main:app", host="localhost", port=port, reload=True) 

if __name__ == "__main__":
    main()
