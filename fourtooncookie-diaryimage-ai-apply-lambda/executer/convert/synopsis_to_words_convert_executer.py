from executer.convert.convert_executer import ConvertExecuter


class SynopsisToWordsConvertExecuter(ConvertExecuter):

    def execute(self, variables) -> list[str]:
        words = []
        for person_data in variables['persons']:
            words.append(person_data["action"])
            words.append(person_data["facial expression"])
        
        words.append(variables['place'])
        words.append(variables['time'])
        words.append(variables['weather'])

        return ", ".join(words)
    
    def validate_variables(self, variables) -> bool:
        if not isinstance(variables, dict): # 변수가 리스트인지 확인
            return False
        
        if ("place" not in variables 
            or "time" not in variables 
            or "weather" not in variables 
            or "persons" not in variables): # place, time, weather, persons가 있는가를 확인
            return False
        
        if not isinstance(variables["persons"], list): # persons가 배열인가를 확인
            return False
        
        for person in variables["persons"]: # persons의 각 요소가 올바른가를 확인
            if "name" not in person or "action" not in person or "facial expression" not in person:
                return False
        
        return True