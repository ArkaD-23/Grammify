from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

def grammar_checker_chain():
    prompt = PromptTemplate(
        input_variables=["text"],
        template="You are a grammar correction assistant. Fix the grammar errors in the following text:\n\n{text}\n\nCorrected text:",
    )
    llm = OpenAI(model="gpt-4", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

@app.route("/check-grammar", methods=["POST"])
def check_grammar():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Invalid request"}), 400

    chain = grammar_checker_chain()
    corrected_text = chain.run({"text": data["text"]})

    return jsonify({"corrected_text": corrected_text}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
