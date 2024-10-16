from openai import OpenAI

import base64
from PIL import Image
from io import BytesIO

import boto3

from visionrequest.vision_request_service import VisionRequestService
from sqs.image_response_sqs_service import ImageResponseSQSService

DALLE3_IMAGE_PROMPT: str = ""
DALLE3_IMAGE_PROMPT_FILE_PATH = './prompt/dalle3_image_prompt.txt'

with open(DALLE3_IMAGE_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    DALLE3_IMAGE_PROMPT = f.read()

class DallE3VisionRequestService(VisionRequestService):

    __openai: OpenAI
    __s3: boto3.client
    __bucket_name: str
    __image_response_sqs_service: ImageResponseSQSService

    def __init__(self, openai: OpenAI, s3client: boto3.client, bucket_name: str, image_response_sqs_service: ImageResponseSQSService):
        self.__openai = openai
        self.__s3 = s3client
        self.__bucket_name = bucket_name
        self.__image_response_sqs_service = image_response_sqs_service

    def request_vision(self, diary_id: int, character_id: int, character_base_prompt: str, scenes: list[str]):
        response = self.__openai.images.generate(
            model="dall-e-3",
            n=1,
            size="1024x1024",
            prompt=DALLE3_IMAGE_PROMPT.replace("$cut_prompt", "\n".join(scenes)),
            quality="hd",
            response_format="b64_json"
        )
        image_base64 = response.data[0].b64_json
        image = self.__decode_base64_image(image_base64)

        self.__upload_image(diary_id, image)

        self.__image_response_sqs_service.send_image_success_response(diary_id)
    

    def __upload_image(self, diary_id: int, image: Image):
        top_left, top_right, bottom_left, bottom_right = self.__split_image(image)

        for i, image in enumerate([top_left, top_right, bottom_left, bottom_right]):
            image_bytesio = self.__image_to_bytesio(image)
            self.__upload_s3(diary_id, i, image_bytesio)
    
    def __decode_base64_image(self, base64_str):
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))
        return image
    
    def __split_image(self, image): # 이미지를 중앙을 기준으로 4등분
        width, height = image.size
        mid_x, mid_y = width // 2, height // 2

        # 이미지의 네 개 부분
        top_left = image.crop((0, 0, mid_x, mid_y))
        top_right = image.crop((mid_x, 0, width, mid_y))
        bottom_left = image.crop((0, mid_y, mid_x, height))
        bottom_right = image.crop((mid_x, mid_y, width, height))

        return top_left, top_right, bottom_left, bottom_right

    def __image_to_bytesio(self, image, format='PNG'):
        image_io = BytesIO()
        image.save(image_io, format=format)
        image_io.seek(0)
        return image_io
    

    def __upload_s3(self, diary_id: int, grid_position: int, image_bytesio: BytesIO):
        key_name = f"{diary_id}/{grid_position}.png"
        try:
            self.__s3.upload_fileobj(image_bytesio, self.__bucket_name, key_name)
        except:
            raise Exception("S3에 이미지 업로드 실패")
