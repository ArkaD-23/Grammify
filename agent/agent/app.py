from fastapi import FastAPI, Request
from langgraph.graph import StateGraph
from research_canvas.state import AgentState
import json

app = FastAPI()

with open("langraph.json", "r") as f:
    workflow_config = json.load(f)

agent_workflow = StateGraph(AgentState)

nodes = workflow_config["workflows"]["agent_workflow"]["nodes"]
edges = workflow_config["workflows"]["agent_workflow"]["edges"]

for node_name, node_details in nodes.items():
    module = __import__(node_details["module"], fromlist=[node_details["function"]])
    func = getattr(module, node_details["function"])
    agent_workflow.add_node(node_name, func)

for edge in edges:
    agent_workflow.add_edge(edge["from"], edge["to"])


@app.post("/agent/")
async def agent_handler(request: Request):
    data = await request.json()
    state = AgentState()
    state["input_text"] = data.get("text", "")
    state["target_language"] = data.get("language", "en") 
    
    await agent_workflow.run(state)
    return state.to_dict()
