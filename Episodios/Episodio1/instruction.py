from abc import ABC, abstractmethod, abstractproperty  # ABC = Abstract Base Clase


class Instruction(ABC):
    def __init__(self):
        #self.identifier_byte = identifier_byte  # El identifier_byte es el byte a la izquierda
        pass

    def __str__(self):
        return "{}, Byte identificador: {}".format(self.__class__.__name__,
                                                   self.identifier_byte)

    @abstractproperty
    def identifier_byte(self) -> bytes:
        return None

    @abstractproperty
    def instruction_length(self) -> int:
        return 1

    @abstractmethod
    def execute(self):
        print(self.__str__())



class LDAInstruction(Instruction):
    identifier_byte = bytes.fromhex('A9')
    instruction_length = 2

    def execute(self):  # Método override
        super().execute()

class SEIInstruction(Instruction):
    identifier_byte = bytes.fromhex('78')
    instruction_length = 1

    def execute(self):
        super().execute()

class CLDInstruction(Instruction):
    identifier_byte = bytes.fromhex('D8')
    instruction_length = 1

    def execute(self):
        super().execute()