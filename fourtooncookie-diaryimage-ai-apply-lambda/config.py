import os
from openai import OpenAI
from llm.llm_service import LLMService
from llm.gpt4o_llm_service import GPT4oLLMService
from scenegenerator.scene_generator import SceneGenerator
from scenegenerator.diary_scene_generator import DiarySceneGenerator
from visionrequest.vision_request_service import VisionRequestService
from visionrequest.dall_e_3_vision_request_service import DallE3VisionRequestService

openai: OpenAI = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

llm_service: LLMService = GPT4oLLMService(openai)
vision_request_services: list[VisionRequestService] = [
    DallE3VisionRequestService(openai, os.environ['S3_BUCKET_NAME'])
]

scene_generator: SceneGenerator = DiarySceneGenerator(llm_service)

