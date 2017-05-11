from abc import abstractmethod, ABC, abstractproperty
from typing import List


class MemoryOwnerMixin(ABC):
    # TODO check we have correct amount of memory
    @abstractproperty
    def memory_start_location(self) -> int:
        '''
        inclusivo
        '''
        pass

    @abstractproperty
    def memory_end_location(self) -> int:
        '''
        inclusivo
        '''
        pass

    @abstractmethod
    def get_memory(self) -> List[int]:
        pass

    def get(self, position: int) -> int:
        """
        Da int en una posición dada
        """

        return self.get_memory()[position - self.memory_start_location]

    def set(self, position: int, value: int):
        '''
        Establece int en una posición dada
        '''
        self.get_memory()[position - self.memory_start_location] = value


