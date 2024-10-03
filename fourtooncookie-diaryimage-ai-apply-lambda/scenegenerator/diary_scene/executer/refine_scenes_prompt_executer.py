from executer.prompt_executer import PromptExecuter
from executer.refine_scenes_prompt_executer import RefineScenesPromptExecuter

class RefineScenesPromptExecuter(PromptExecuter):

    __refine_scene_prompt_executer: RefineScenesPromptExecuter

    def __init__(self, refine_scene_prompt_executer: RefineScenesPromptExecuter):
        self.__refine_scene_prompt_executer = refine_scene_prompt_executer

    def execute(self, variables: list):
        return [
            self.__refine_scene_prompt_executer.execute(scene)
            for scene in variables
        ]
    
    def validate_variables(self, variables) -> bool:
        if not isinstance(variables, list):
            return False
        
        if len(variables) == 0:
            return False
        
        return True