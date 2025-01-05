from gtts import gTTS
from research_canvas.state import AgentState

async def text_to_speech_node(state: AgentState, config: dict):

    text = state.get("text_data")
    if not text:
        raise ValueError("No text data provided for TTS.")

    tts = gTTS(text=text, lang="en")
    file_path = "output_audio.mp3"
    tts.save(file_path)
    state["audio_file"] = file_path
    return state
