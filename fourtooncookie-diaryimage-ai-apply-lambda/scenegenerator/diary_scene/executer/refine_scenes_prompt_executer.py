from executer.prompt_executer import PromptExecuter
from scenegenerator.diary_scene.executer.refine_scene_prompt_executer import RefineScenePromptExecuter

class RefineScenesPromptExecuter(PromptExecuter):

    __refine_scene_prompt_executer: RefineScenePromptExecuter

    def __init__(self, refine_scene_prompt_executer: RefineScenePromptExecuter):
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
        
        for scene in variables:
            if not self.__refine_scene_prompt_executer.validate_variables(scene):
                return False
        
        return True