from scene_generator import SceneGenerator
from llm.llm_service import LLMService
import json
from prompt import get_synopsis_prompt, get_cut_prompt, get_image_modify_prompt

class DiarySceneGenerator(SceneGenerator):

    __llm_service: LLMService

    def __init__(self, llm_service: LLMService):
        self.__llm_service = llm_service

    def generate_scenes(self, diary_content: str) -> list[str]:
        scene_datas = self.__llm_service.get_llm(get_synopsis_prompt(), diary_content)
        scene_json_datas = json.loads(scene_datas)

        cut_prompts = []

        for i in range(4):
            scene_json_data = scene_json_datas[i]

            situations = ""
            for person_data in scene_json_data['persons']:
                situations += "{} is doing {}, {}. ".format(person_data["name"], person_data["action"], person_data["facial expression"])
            
            cut_prompt = get_cut_prompt(i, scene_json_data['place'], scene_json_data['time'], scene_json_data['weather'], situations)

            modified_cut_prompt = self.__llm_service.get_llm(get_image_modify_prompt(), cut_prompt)
            cut_prompts.append(modified_cut_prompt)
        
        return cut_prompts
        
