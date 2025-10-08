from abc import ABC, abstractmethod

class AbstractProfileRepo(ABC):
    @abstractmethod
    async def save_profile(self, chat_id : int, data : dict)-> int:
        pass

    
    