from abc import ABCMeta, abstractmethod

class VisionRequestService(metaclass=ABCMeta):

    @abstractmethod
    def request_vision(self, diary_id: int, character_id: int, prompts: list[str]):
        pass