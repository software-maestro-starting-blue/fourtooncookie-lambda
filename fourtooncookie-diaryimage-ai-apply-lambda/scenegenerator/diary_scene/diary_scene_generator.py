from scenegenerator.scene_generator import SceneGenerator
from executer.executer import Executer

class DiarySceneGenerator(SceneGenerator):

    __executers: list[Executer]

    def __init__(self, executers: list[Executer]):
        self.__executers = executers
    
    def generate_scenes(self, diary_content: str) -> list[str]:
        variables = diary_content
        
        for executer in self.__executers:
            
            if not executer.validate_variables(variables):
                raise Exception("Invalid variables", variables, executer.__class__.__name__)
            
            variables = executer.execute(variables)
        
        return variables