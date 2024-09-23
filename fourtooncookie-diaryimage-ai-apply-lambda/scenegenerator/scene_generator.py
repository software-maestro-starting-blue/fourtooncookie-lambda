from abc import ABCMeta, abstractmethod

class SceneGenerator(metaclass=ABCMeta):

    @abstractmethod
    def generate_scenes(self, diary_content: str) -> list[str]:
        pass