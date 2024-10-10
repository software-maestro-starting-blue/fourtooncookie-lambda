from executer.prompt.portkey_prompt_executer import PortkeyPromptExecuter

class SimplePortkeyPromptExecuter(PortkeyPromptExecuter):
    
    def execute(self, variables: str) -> str:
        return super().execute({"prompt": variables})
    
    def validate_variables(self, variables) -> bool:
        return isinstance(variables, str)