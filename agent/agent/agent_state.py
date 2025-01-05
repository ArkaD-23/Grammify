class AgentState:
    def __init__(self):
        self.state = {}

    def set(self, key: str, value):
        self.state[key] = value

    def get(self, key: str):
        return self.state.get(key)

    def clear(self):
        self.state = {}
