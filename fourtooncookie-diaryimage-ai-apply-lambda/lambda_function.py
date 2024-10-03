from config import *


def lambda_handler(body, context):
    try:
        # body 정리하기
        diary_id = body['diaryId']

        character = body['character']
        character_id = character['id']
        character_name = character['name']
        character_vision_type = character['visionType']
        character_base_prompt = character['basePrompt']

        content = body['content']
    except Exception as e:
        print(e)
        return False
    
    try:
        # LLM과 prompt 활용하여 내용 정체
        scenes = scene_generator.generate_scenes(content)

        # vision request로 요청 보내기
        vision_request_service = vision_request_services[character_vision_type]
        vision_request_service.request_vision(diary_id, character_id, character_base_prompt, scenes)
        
        return True
    except Exception as e:
        print(e)
        image_response_sqs_service.send_image_failure_response(diary_id) # 실패 시 SQS에 실패 메시지 전송
        return False