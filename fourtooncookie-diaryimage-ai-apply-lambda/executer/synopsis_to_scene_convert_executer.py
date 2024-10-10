from executer.convert_executer import ConvertExecuter

SCENE_PROMPT: str = ""
SCENE_PROMPT_FILE_PATH = "./prompt/scene_prompt.txt"

with open(SCENE_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    SCENE_PROMPT = f.read()

class SynopsisToSceneConvertExecuter(ConvertExecuter):

    def execute(self, variables):
        situations = "".join([
            self.__get_person_situation(person_data)
            for person_data in variables['persons']
        ])

        return self.__get_scene_prompt(variables['place'], variables['time'], variables['weather'], situations)
    
    def __get_person_situation(self, person_data: dict) -> str:
        return "{} is doing {}, {}. ".format(person_data["name"], person_data["action"], person_data["facial expression"])
    
    def __get_scene_prompt(self, background: str, timeline: str, weather: str, situation: str):
        now_scene_prompt = str(SCENE_PROMPT)

        now_scene_prompt = now_scene_prompt.replace("$background", background)
        now_scene_prompt = now_scene_prompt.replace("$timeline", timeline)
        now_scene_prompt = now_scene_prompt.replace("$weather", weather)
        now_scene_prompt = now_scene_prompt.replace("$situation", situation)

        return now_scene_prompt
    
    
    def validate_variables(self, variables) -> bool:
        if not isinstance(variables, dict): # 변수가 리스트인지 확인
            return False
        
        if ("place" not in variables 
            or "time" not in variables 
            or "weather" not in variables 
            or "persons" not in variables): # place, time, weather, persons가 있는가를 확인
            return False
        
        if not isinstance(variables["persons"], list): # persons가 배열인가를 확인
            return False
        
        for person in variables["persons"]: # persons의 각 요소가 올바른가를 확인
            if "name" not in person or "action" not in person or "facial expression" not in person:
                return False
        
        return True
