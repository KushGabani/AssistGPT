import config
import openai

openai.organization = config.OPENAI_ORG
openai.api_key = config.OPENAI_API_KEY

BOT_MODES = {
    "assistant": {
        "name": "👩🏼‍🎓 Assistant",
        "intro": "👩🏼‍🎓 Hi, I'm <b>ChatGPT assistant</b>. How can I help you?",
        "base_prompt": "As an advanced chatbot named ChatGPT, your primary goal is to assist users to the best of your ability. This may involve answering questions, providing helpful information, or completing tasks based on user input. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. Your ultimate goal is to provide a helpful and enjoyable experience for the user."
    },

    "code_assistant": {
        "name": "👩🏼‍💻 Code Assistant",
        "intro": "👩🏼‍💻 Hi, I'm <b>ChatGPT code assistant</b>. How can I help you?",
        "base_prompt": "As an advanced chatbot named ChatGPT, your primary goal is to assist users to write code. This may involve designing/writing/editing/describing code or providing helpful information. Where possible you should provide code examples to support your points and justify your recommendations or solutions. Make sure the code you provide is correct and can be run without errors. Be detailed and thorough in your responses. Your ultimate goal is to provide a helpful and enjoyable experience for the user. Write code inside <code>, </code> tags."
    },

    "text_improver": {
        "name": "📝 Text Improver",
        "intro": "📝 Hi, I'm <b>ChatGPT text improver</b>. Send me any text – I'll improve it and correct all the mistakes",
        "base_prompt": "As an advanced chatbot named ChatGPT, your primary goal is to correct spelling, fix mistakes and improve text sent by user. Your goal is to edit text, but not to change it's meaning. You can replace simplified A0-level words and sentences with more beautiful and elegant, upper level words and sentences. All your answers strictly follows the structure (keep html tags):\n<b>Edited text:</b>\n{EDITED TEXT}\n\n<b>Correction:</b>\n{NUMBERED LIST OF CORRECTIONS}"
    },

    "movie_expert": {
        "name": "🎬 Movie Expert",
        "intro": "🎬 Hi, I'm <b>ChatGPT movie expert</b>. How can I help you?",
        "base_prompt": "As an advanced movie expert chatbot named ChatGPT, your primary goal is to assist users to the best of your ability. You can answer questions about movies, actors, directors, and more. You can recommend movies to users based on their preferences. You can discuss movies with users, and provide helpful information about movies. In order to effectively assist users, it is important to be detailed and thorough in your responses. Use examples and evidence to support your points and justify your recommendations or solutions. Remember to always prioritize the needs and satisfaction of the user. Your ultimate goal is to provide a helpful and enjoyable experience for the user."
    },
}

OPENAI_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

class ChatGPT:
    def __init__(self):
        pass

    def send_message(self, prompt, dialog=[], bot_mode="assistant"):
        n_dialog_before = len(dialog)
        answer = None

        while answer is None:
            try:
                messages = self._build_prompt(prompt, dialog, bot_mode)
                response = openai.ChatCompletion.create(
                    model = 'gpt-3.5-turbo',
                    messages=messages,
                    **OPENAI_CONFIG
                )
                
                answer = response['choices'][0]['message']['content'].strip()
                n_used_tokens = response.usage.total_tokens
            except openai.error.InvalidRequestError as e:
                print(e)
                # if len(dialog) == 0:
                #     raise ValueError("Dialog Messages is reduced to zero, but still has too many tokens to make completion") from e
                # dialog = dialog[1:]

            removed_n_dialog = n_dialog_before - len(dialog)

            return answer, n_used_tokens, removed_n_dialog

    def transcribe_audio(self, voice_file, bot_mode="assistant"):
        with open(voice_file, "rb") as f:
            return openai.Audio.translate('whisper-1', f)
    
    def _build_prompt(self, user_prompt, dialog, bot_mode):
        base_prompt = BOT_MODES[bot_mode]["base_prompt"]

        full_prompt = [{"role": "system", "content": base_prompt}]
        for d in dialog:
            full_prompt.append({"role": "user", "content": d["user"]})
            full_prompt.append({"role": "assistant", "content": d["bot"]})
        
        full_prompt.append({"role": "user", "content": user_prompt})

        return full_prompt
