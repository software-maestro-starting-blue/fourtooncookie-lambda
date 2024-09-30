import os
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders
import boto3
from llm.llm_service import LLMService
from llm.gpt4o_llm_service import GPT4oLLMService
from scenegenerator.scene_generator import SceneGenerator
from scenegenerator.diary_scene_generator import DiarySceneGenerator
from visionrequest.vision_request_service import VisionRequestService
from visionrequest.dall_e_3_vision_request_service import DallE3VisionRequestService

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
PORTKEY_API_KEY = os.environ['PORTKEY_API_KEY']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

openai: OpenAI = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider="openai",
        api_key=PORTKEY_API_KEY
    )
)


s3client: boto3.client = boto3.client('s3')

llm_service: LLMService = GPT4oLLMService(openai)

scene_generator: SceneGenerator = DiarySceneGenerator(llm_service)


vision_request_services: dict[str, VisionRequestService] = {
    "DALL_E_3": DallE3VisionRequestService(openai, s3client, S3_BUCKET_NAME)
}

