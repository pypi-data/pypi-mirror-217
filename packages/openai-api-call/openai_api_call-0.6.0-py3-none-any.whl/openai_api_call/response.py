# Response class for OpenAI API call

from typing import Dict
import json

class Resp():
    
    def __init__(self, response:Dict, strip:bool=True) -> None:
        self.response = response
        if strip and self.is_valid() and self.content is not None:
            self._strip_content()
    
    def _strip_content(self):
        """Strip the content"""
        self.response['choices'][0]['message']['content'] = \
            self.content.strip()
    
    def __repr__(self) -> str:
        if self.finish_reason == "function_call":
            return f"`Resp(call)`: {self.function_call}"
        else:
            return f"`Resp`: {self.content}"
    
    def __str__(self) -> str:
        return self.content

    @property
    def id(self):
        return self.response['id']
    
    @property
    def object(self):
        return self.response['object']
    
    @property
    def model(self):
        return self.response['model']
    
    @property
    def created(self):
        return self.response['created']
    
    @property
    def usage(self):
        """Token usage"""
        return self.response['usage']
    
    @property
    def total_tokens(self):
        """Total number of tokens"""
        return self.usage['total_tokens']
    
    @property
    def prompt_tokens(self):
        """Number of tokens in the prompt"""
        return self.usage['prompt_tokens']
    
    @property
    def completion_tokens(self):
        """Number of tokens of the response"""
        return self.usage['completion_tokens']
    
    @property
    def finish_reason(self):
        """Finish reason"""
        return self.response['choices'][0]['finish_reason']
    
    @property
    def message(self):
        """Message"""
        return self.response['choices'][0]['message']
    
    @property
    def content(self):
        """Content of the response"""
        return self.message['content']

    @property
    def function_call(self):
        """Function call"""
        if self.is_function_call:
            args = {}
            args['name'] = self.message['function_call']['name']
            args['arguments'] = self.message['function_call']['arguments']
            return args
        else:
            return None

    def is_function_call(self):
        """Check if the response is a function call"""
        return self.finish_reason == 'function_call' and \
            self.content is None
    
    def is_valid(self):
        """Check if the response is an error"""
        return 'error' not in self.response and 'choices' in self.response
    
    @property
    def error(self):
        """Error"""
        return self.response['error']
    
    @property
    def error_message(self):
        """Error message"""
        return self.error['message']
    
    @property
    def error_type(self):
        """Error type"""
        return self.error['type']
    
    @property
    def error_param(self):
        """Error parameter"""
        return self.error['param']
    
    @property
    def error_code(self):
        """Error code"""
        return self.error['code']

    