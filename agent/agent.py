import requests
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv
import uuid
from pydantic import BaseModel

load_dotenv()

class OpenAIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": "gpt-4",
            "prompt": prompt,
            "temperature": 0.7,
            "max_tokens": 500
        }
        response = requests.post(f"{self.base_url}/v1/completions", json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["text"].strip()
        else:
            response.raise_for_status()

openai_client = OpenAIClient(base_url=os.getenv("OPENAI_API_BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))

class TutoringState(BaseModel):
    user_input: str
    language: str
    generated_question: str = ""
    tutoring_feedback: str = ""
    error: str = ""
    iterations: int = 0
    state_checkpoint_id: str = str(uuid.uuid4())

def detect_intent(state: TutoringState) -> TutoringState:
    try:
        prompt = f"Classify the user's intent: '{state.user_input}'. Respond with 'learn_language' or 'ask_question'."
        response = openai_client.generate(prompt)
        intent = response.strip().lower()
        if intent == "learn_language":
            state.generated_question = "Let's start with a question! What language are you learning?"
        elif intent == "ask_question":
            state.generated_question = "Please ask your question about the language."
        else:
            state.error = "I couldn't classify your intent."
    except Exception as e:
        state.error = str(e)
    return state

def recommend_resources(state: TutoringState) -> TutoringState:
    try:
        if state.generated_question.startswith("What language"):
            prompt = f"Recommend resources for learning {state.language}."
            response = openai_client.generate(prompt)
            state.tutoring_feedback = response.strip()
        else:
            state.tutoring_feedback = "Please provide a valid language to learn."
    except Exception as e:
        state.error = str(e)
    return state

def provide_tutoring_feedback(state: TutoringState) -> TutoringState:
    try:
        if state.generated_question.startswith("Please ask your question"):
            prompt = f"In {state.language}, provide helpful feedback to the user's question: '{state.user_input}'."
            response = openai_client.generate(prompt)
            state.tutoring_feedback = response.strip()
        else:
            state.tutoring_feedback = "Ask a question to receive feedback."
    except Exception as e:
        state.error = str(e)
    return state

def route(state: TutoringState) -> str:
    if state.error and state.iterations < 3:
        state.iterations += 1
        return "detect_intent"
    return "end"

workflow = StateGraph(TutoringState)

workflow.add_node("detect_intent", detect_intent)
workflow.add_node("recommend_resources", recommend_resources)
workflow.add_node("provide_tutoring_feedback", provide_tutoring_feedback)

workflow.add_edge(START, "detect_intent")
workflow.add_edge("detect_intent", "recommend_resources")
workflow.add_edge("detect_intent", "provide_tutoring_feedback")

def condition_learn_language(state: TutoringState) -> bool:
    return "learn_language" in state.generated_question

def condition_ask_question(state: TutoringState) -> bool:
    return "ask_question" in state.generated_question

workflow.add_conditional_edges(
    "detect_intent",
    condition_learn_language,
    {"recommend_resources": "recommend_resources"}
)

workflow.add_conditional_edges(
    "detect_intent",
    condition_ask_question,
    {"provide_tutoring_feedback": "provide_tutoring_feedback"}
)

workflow.add_conditional_edges(
    "recommend_resources",
    route,
    {"end": END, "detect_intent": "detect_intent"}
)

workflow.add_conditional_edges(
    "provide_tutoring_feedback",
    route,
    {"end": END, "detect_intent": "detect_intent"}
)

graph = workflow.compile(checkpointer=MemorySaver())

def execute_workflow(user_input: str, language: str) -> dict:
    initial_state = TutoringState(user_input=user_input, language=language)
    final_state = graph.run(initial_state)
    return {
        "Generated Question": final_state.generated_question,
        "Tutoring Feedback": final_state.tutoring_feedback,
        "Error": final_state.error
    }

if __name__ == "__main__":
    user_input = "How do I say 'Hello' in Spanish?"
    language = "Spanish"
    result = execute_workflow(user_input, language)
    print(result)
