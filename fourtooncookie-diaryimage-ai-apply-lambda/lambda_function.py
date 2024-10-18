from config import *

def execute_executers(vision_type, content):
    scene_generate_executers = executers_by_vision_type[vision_type]
    
    variables = content

    for executer in scene_generate_executers:
        if not executer.validate_variables(variables):
            raise Exception("Invalid variables", variables, executer.__class__.__name__)
        
        variables = executer.execute(variables)
    
    return variables

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
        scenes = None

        count = 0

        while not scenes:
            try:
                count += 1
                scenes = execute_executers(character_vision_type, content)
            except Exception as e:
                if count < PROMPT_RETRY_COUNT:
                    print("Retry")
                    continue
                else:
                    raise e
        
        # vision request로 요청 보내기
        vision_request_service = vision_request_services[character_vision_type]
        vision_request_service.request_vision(diary_id, character_id, character_base_prompt, scenes)
        
        return True
    except Exception as e:
        print(e)
        image_response_sqs_service.send_image_failure_response(diary_id) # 실패 시 SQS에 실패 메시지 전송
        return False