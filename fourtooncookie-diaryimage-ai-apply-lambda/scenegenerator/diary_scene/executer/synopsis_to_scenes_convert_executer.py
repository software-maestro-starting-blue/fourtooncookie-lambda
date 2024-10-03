from executer.convert_executer import ConvertExecuter

class SynopsisToScenesConvertExecuter(ConvertExecuter):

    def execute(self, variables):
        cut_prompts = []

        for i, scene_json_data in enumerate(variables):
            situations = "".join([
                self.__get_person_situation(person_data)
                for person_data in scene_json_data['persons']
            ])

            cut_prompt = self.__get_scene_prompt(i, scene_json_data['place'], scene_json_data['time'], scene_json_data['weather'], situations)

            cut_prompts.append(cut_prompt)
        
        return cut_prompts
    
    def __get_person_situation(self, person_data: dict) -> str:
        return "{} is doing {}, {}. ".format(person_data["name"], person_data["action"], person_data["facial expression"])
    
    def __get_scene_prompt(self, i: int, background: str, timeline: str, weather: str, situation: str):
        now_scene_prompt = str(SCENE_PROMPT)

        now_scene_prompt = now_scene_prompt.replace("$i", str(i + 1))
        now_scene_prompt = now_scene_prompt.replace("$background", background)
        now_scene_prompt = now_scene_prompt.replace("$timeline", timeline)
        now_scene_prompt = now_scene_prompt.replace("$weather", weather)
        now_scene_prompt = now_scene_prompt.replace("$situation", situation)

        return now_scene_prompt
    
    
    def validate_variables(self, variables) -> bool:
        if not isinstance(variables, list): # 변수가 리스트인지 확인
            return False

        if len(variables) != 4: # 4개의 컷이 있는가를 확인
            return False
        
        for scene_variables in variables: # 각 컷의 데이터가 올바른가를 확인
            if not self.__validate_synopsis_cut_variables(scene_variables):
                return False
        
        return True
    
    def __validate_synopsis_cut_variables(self, scene_variables: dict) -> bool:
        if ("place" not in scene_variables 
            or "time" not in scene_variables 
            or "weather" not in scene_variables 
            or "persons" not in scene_variables): # place, time, weather, persons가 있는가를 확인
            return False
        
        if not isinstance(scene_variables["persons"], list): # persons가 배열인가를 확인
            return False
        
        for person in scene_variables["persons"]: # persons의 각 요소가 올바른가를 확인
            if "name" not in person or "action" not in person or "facial expression" not in person:
                return False
        
        return True


SCENE_PROMPT: str = ""
SCENE_PROMPT_FILE_PATH = "./prompt/scene_prompt.txt"

with open(SCENE_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    SCENE_PROMPT = f.read()