

from myapi.helper.multi_language import DictionaryReturnType, return_message

# CURRENTLY UNAVAILABLE


class MultiLanguage:

    def __init__(self, langauge='en'):
        self.current_langauge = langauge

    def set_current_language(self, intended_language: str):
        self.current_langauge = intended_language

    def get_current_text(self, text_type: DictionaryReturnType):
        return return_message[self.current_langauge][text_type]
