from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from research_canvas.state import AgentState
from backend.nodes.download_node import download_node
from backend.nodes.grammar_check_node import grammar_check_node
from backend.nodes.copy_result_node import copy_result_node

# Define the workflow graph
workflow = StateGraph(AgentState)

# Add the nodes to the workflow graph
workflow.add_node("download", download_node)
workflow.add_node("grammar_check", grammar_check_node)
workflow.add_node("copy_result", copy_result_node)

# Set the entry point and define edges (workflow)
workflow.set_entry_point("download")
workflow.add_edge("download", "grammar_check")
workflow.add_edge("grammar_check", "copy_result")

# Compile the workflow with memory saver (to track state)
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory, interrupt_after=["copy_result"])

async def run_workflow():
    # Simulate agent state
    state = AgentState()
    
    # Execute the graph
    await graph.run(state)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_workflow())
