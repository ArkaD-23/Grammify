from research_canvas.state import AgentState

async def copy_result_node(state: AgentState, config: dict):
    """
    Copy the grammar check result (e.g., save it or display it elsewhere).
    """
    corrected_text = state.get("corrected_text")
    
    # Simulating "copying" the result
    print(f"Corrected Text: {corrected_text}")
    
    state["copied_text"] = corrected_text  # Simulating storing the result
    return state
