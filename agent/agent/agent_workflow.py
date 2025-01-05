from langgraph.graph import StateGraph
from research_canvas.state import AgentState
from agent.nodes.text_to_speech import text_to_speech_node
from agent.nodes.translation import translation_node
from agent.nodes.summarization import summarization_node
from agent.nodes.sentiment_analysis import sentiment_analysis_node

workflow = StateGraph(AgentState)

workflow.add_node("text_to_speech", text_to_speech_node)
workflow.add_node("translation", translation_node)
workflow.add_node("summarization", summarization_node)
workflow.add_node("sentiment_analysis", sentiment_analysis_node)

workflow.set_entry_point("summarization") 
workflow.add_edge("summarization", "sentiment_analysis")
workflow.add_edge("sentiment_analysis", "translation")
workflow.add_edge("translation", "text_to_speech")

agent_workflow = workflow.compile()
