from research_canvas.state import AgentState

async def download_node(state: AgentState, config: dict):
    """
    Simulate downloading text data for grammar checking.
    """
    text_data = "This is an example text with smoe grammatical errors."
    state["text_data"] = text_data
    return state
