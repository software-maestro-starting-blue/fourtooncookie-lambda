






''' PROMPT CONSTANTS '''
CUT_PROMPT: str = ""
IMAGE_PROMPT: str = ""



''' LOAD PROMPT '''
CUT_PROMPT_FILE_PATH = "./prompt/cut_prompt.txt"
IMAGE_PROMPT_FILE_PATH = './prompt/image_prompt.txt'

with open(IMAGE_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    IMAGE_PROMPT = f.read()

with open(CUT_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    CUT_PROMPT = f.read()