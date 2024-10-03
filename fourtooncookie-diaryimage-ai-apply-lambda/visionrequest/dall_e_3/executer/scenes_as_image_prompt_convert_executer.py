from executer.convert_executer import ConvertExecuter

class ScenesAsImagePromptConvertExecuter(ConvertExecuter):

    def execute(self, variables):
        return DALLE3_IMAGE_PROMPT.replace("$cut_prompt", "\n".join(variables))
    
    def validate_variables(self, variables) -> bool:
        return (isinstance(variables, list) 
                and all(isinstance(scene, str) for scene in variables) 
                and len(variables) > 0)


DALLE3_IMAGE_PROMPT: str = ""
DALLE3_IMAGE_PROMPT_FILE_PATH = './prompt/dalle3_image_prompt.txt'

with open(DALLE3_IMAGE_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    DALLE3_IMAGE_PROMPT = f.read()