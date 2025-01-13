import requests

class OpenAIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        """Send a prompt to the OpenAI API and return the response."""
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