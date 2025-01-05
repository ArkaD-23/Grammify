from transformers import pipeline
from research_canvas.state import AgentState

async def summarization_node(state: AgentState, config: dict):

    text = state.get("text_data")
    if not text:
        raise ValueError("No text data provided for summarization.")

    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    state["summary"] = summary[0]["summary_text"]
    return state
