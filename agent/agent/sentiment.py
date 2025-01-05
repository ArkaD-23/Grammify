from transformers import pipeline
from research_canvas.state import AgentState

async def sentiment_analysis_node(state: AgentState, config: dict):

    text = state.get("text_data")
    if not text:
        raise ValueError("No text data provided for sentiment analysis.")

    sentiment_analyzer = pipeline("sentiment-analysis")
    sentiment = sentiment_analyzer(text)
    state["sentiment"] = sentiment[0]
    return state
