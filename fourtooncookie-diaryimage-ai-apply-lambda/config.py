import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
PORTKEY_API_KEY = os.environ['PORTKEY_API_KEY']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
IMAGE_RESPONSE_SQS_QUEUE_URL = os.environ['IMAGE_RESPONSE_SQS_QUEUE_URL']
STABLE_DIFFUSION_SQS_QUEUE_URL = os.environ['STABLE_DIFFUSION_SQS_QUEUE_URL']


from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders, Portkey

openai: OpenAI = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider="openai",
        api_key=PORTKEY_API_KEY
    )
)
portkey = Portkey(
    api_key=PORTKEY_API_KEY
)


import boto3

s3client: boto3.client = boto3.client('s3')
sqsclient: boto3.client = boto3.client('sqs', region_name='ap-northeast-2')

from sqs.image_response_sqs_service import ImageResponseSQSService
image_response_sqs_service: ImageResponseSQSService = ImageResponseSQSService(sqsclient, IMAGE_RESPONSE_SQS_QUEUE_URL)

from llm.llm_service import LLMService
from llm.portkey_llm_service import PortkeyLLMService

llm_service: LLMService = PortkeyLLMService(portkey)


from scenegenerator.scene_generator import SceneGenerator

from scenegenerator.diary_scene.diary_scene_generator import DiarySceneGenerator

from executer.json_convert_executer import JsonConvertExecuter
from scenegenerator.diary_scene.executer.synopsis_to_scene_convert_executer import SynopsisToSceneConvertExecuter
from executer.batch_executer import BatchExecuter
from executer.simple_portkey_prompt_executer import SimplePortkeyPromptExecuter

SYNOPSIS_PROMPT_ID = os.environ["SYNOPSIS_PROMPT_ID"]
REFINE_SCENE_PROMPT_ID = os.environ["REFINE_SCENE_PROMPT_ID"]

scene_generator: SceneGenerator = DiarySceneGenerator([
    SimplePortkeyPromptExecuter(llm_service, SYNOPSIS_PROMPT_ID),
    JsonConvertExecuter(),
    BatchExecuter(SynopsisToSceneConvertExecuter()),
    BatchExecuter(SimplePortkeyPromptExecuter(llm_service, REFINE_SCENE_PROMPT_ID)),
])


from visionrequest.dall_e_3.executer.scenes_as_image_prompt_convert_executer import ScenesAsImagePromptConvertExecuter
from visionrequest.stable_diffusion.executer.scene_as_words_convert_executer import SceneAsWordsConvertExecuter
from visionrequest.stable_diffusion.executer.scene_as_words_convert_executer import SceneAsWordsConvertExecuter

from visionrequest.vision_request_service import VisionRequestService
from visionrequest.dall_e_3.dall_e_3_vision_request_service import DallE3VisionRequestService
from visionrequest.stable_diffusion.sqs_stable_diffusion_vision_request_service import SQSStableDiffusionVisionRequestService

vision_request_services: dict[str, VisionRequestService] = {
    "DALL_E_3": DallE3VisionRequestService(
        openai, s3client, S3_BUCKET_NAME, ScenesAsImagePromptConvertExecuter()
        ),
    "STABLE_DIFFUSION": SQSStableDiffusionVisionRequestService(
        sqsclient, STABLE_DIFFUSION_SQS_QUEUE_URL, SceneAsWordsConvertExecuter()
        )
}
