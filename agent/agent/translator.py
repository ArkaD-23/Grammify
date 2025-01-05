from googletrans import Translator
from research_canvas.state import AgentState

async def translation_node(state: AgentState, config: dict):

    text = state.get("text_data")
    target_lang = config.get("target_lang", "en") 

    if not text:
        raise ValueError("No text data provided for translation.")

    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    state["translated_text"] = translation.text
    return state
