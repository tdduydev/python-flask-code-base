import functools
from typing import List
from myapi.helper.http_code import HttpCode
from myapi.helper.multi_language import ReturnMessageEnum, return_message
from flask import request
# CURRENTLY UNAVAILABLE


class MultiLanguage:

    def __init__(self, langauge='en'):
        self.current_langauge = langauge

    def set_default_language(self, intended_language: str):
        """
        This function set the default language to the appropriate language \n
        Parameter: intended_language as Str
        """
        # CHECK IF THE INPUT LANGUAGE IS AVAILABLE
        if not intended_language in return_message:
            return {"msg": self.get_current_text(ReturnMessageEnum.unavailable_language)}, HttpCode.BadRequest

        self.current_langauge = intended_language

    def get_current_text(self, text_type: ReturnMessageEnum):
        """
        This return a translated return message (type: Str) \n
        based on the current language and the return message type user chose \n
        Parameter: text_type as ReturnMessageEnum \n
        Example: \n
        - current_language = en , type = ReturnMessageEnum.success \n
            in: get_current_text(type) | out: "Request success"
        - current_language = vn , type = ReturnMessageEnum.success\n
            in: get_current_text(type) | out: "Thành công"
        """
        if self.check_language_header() == True:
            return return_message[request.headers.get("language")][text_type]
        return return_message[self.current_langauge][text_type]

    def check_language_header(self):

        if not 'language' in request.headers:
            return False
        if request.headers.get("language") not in return_message:
            return False
        return True
