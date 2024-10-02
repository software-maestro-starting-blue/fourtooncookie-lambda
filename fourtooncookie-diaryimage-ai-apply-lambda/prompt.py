''' SYNOPSIS PROMPT (SYSTEM) '''
SYNOPSIS_PROMPT: str = ""
SYNOPSIS_PROMPT_FILE_PATH = './prompt/synopsis_prompt.txt'

with open(SYNOPSIS_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    SYNOPSIS_PROMPT = f.read()

def get_synopsis_prompt():
    return SYNOPSIS_PROMPT


''' CUT PROMPT '''
CUT_PROMPT: str = ""
CUT_PROMPT_FILE_PATH = "./prompt/cut_prompt.txt"

with open(CUT_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    CUT_PROMPT = f.read()

def get_cut_prompt(i: int, background: str, timeline: str, weather: str, situation: str):
    now_cut_prompt = str(CUT_PROMPT) # str copy

    # 컷의 내용을 기존 형식에 주입시킵니다.
    now_cut_prompt = now_cut_prompt.replace("$i", str(i + 1))
    now_cut_prompt = now_cut_prompt.replace("$background", background)
    now_cut_prompt = now_cut_prompt.replace("$timeline", timeline)
    now_cut_prompt = now_cut_prompt.replace("$weather", weather)

    now_cut_prompt = now_cut_prompt.replace("$situation", situation)

    return now_cut_prompt

''' IMAGE MODIFY PROMPT '''
IMAGE_MODIFY_PROMPT: str = ""
IMAGE_MODIFY_PROMPT_FILE_PATH = './prompt/image_modify_prompt.txt'

with open(IMAGE_MODIFY_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    IMAGE_MODIFY_PROMPT = f.read()

def get_image_modify_prompt():
    return IMAGE_MODIFY_PROMPT


''' DALLE3 IMAGE PROMPT '''
DALLE3_IMAGE_PROMPT: str = ""
DALLE3_IMAGE_PROMPT_FILE_PATH = './prompt/image_prompt.txt'

with open(DALLE3_IMAGE_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    DALLE3_IMAGE_PROMPT = f.read()

def get_dalle3_image_prompt(scene_prompts: list[str]):
    return DALLE3_IMAGE_PROMPT.replace("$cut_prompt", "\n".join(scene_prompts))

''' STABLE DIFFUSION MODIFY PROMPT '''
STABLE_DIFFUSION_MODIFY_PROMPT: str = ""
STABLE_DIFFUSION_MODIFY_PROMPT_FILE_PATH = './prompt/stable_diffusion_modify_prompt.txt'

with open(STABLE_DIFFUSION_MODIFY_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    STABLE_DIFFUSION_MODIFY_PROMPT = f.read()

def get_stable_diffusion_modify_prompt():
    return STABLE_DIFFUSION_MODIFY_PROMPT