from langgraph import LangGraph
from langgraph.schema import Node

class LanguageTutoringAgent:
    def __init__(self, openai_client):
        self.openai_client = openai_client
        self.langgraph = LangGraph()

        # Define nodes
        self._initialize_nodes()

    def _initialize_nodes(self):
        """Initialize LangGraph nodes for the workflow."""

        # Node: Detect intent
        detect_intent_node = Node(
            id="detect_intent",
            description="Detect if the user wants to learn a language or ask a specific question.",
            task=lambda params: self._detect_intent(params["user_input"])
        )

        # Node: Recommend resources
        recommend_resources_node = Node(
            id="recommend_resources",
            description="Recommend resources and exercises for language practice.",
            task=lambda params: self._recommend_resources(params["language"])
        )

        # Node: Language tutoring
        tutoring_node = Node(
            id="tutoring",
            description="Engage in a conversational language tutoring session.",
            task=lambda params: self._language_tutoring(params["language"], params["user_input"])
        )

        # Add nodes and define edges
        self.langgraph.add_node(detect_intent_node)
        self.langgraph.add_node(recommend_resources_node)
        self.langgraph.add_node(tutoring_node)

        self.langgraph.add_edge("detect_intent", "recommend_resources", condition=lambda output: output == "learn_language")
        self.langgraph.add_edge("detect_intent", "tutoring", condition=lambda output: output == "ask_question")

    def handle_workflow(self, language: str, user_input: str) -> dict:
        """Execute the LangGraph workflow."""
        # Execute workflow
        self.langgraph.execute({"language": language, "user_input": user_input})

        # Get results from nodes
        if "recommend_resources" in self.langgraph.get_node_outputs():
            return self.langgraph.get_output("recommend_resources")
        elif "tutoring" in self.langgraph.get_node_outputs():
            return self.langgraph.get_output("tutoring")
        else:
            return {"message": "Workflow could not process the request."}

    def _detect_intent(self, user_input: str) -> str:
        """Detect user intent using OpenAI."""
        prompt = f"Classify the user's intent: '{user_input}'. Respond with 'learn_language' or 'ask_question'."
        response = self.openai_client.generate(prompt)
        return response.strip().lower()

    def _recommend_resources(self, language: str) -> dict:
        """Get resources and exercises for the given language."""
        prompt = f"Provide high-quality reading resources and exercises for learning {language}."
        response = self.openai_client.generate(prompt)
        return {"resources": response}

    def _language_tutoring(self, language: str, user_input: str) -> dict:
        """Provide tutoring or feedback on the user's text."""
        prompt = f"In {language}, respond to this user's question or statement with helpful feedback: '{user_input}'."
        response = self.openai_client.generate(prompt)
        return {"feedback": response}
