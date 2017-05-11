from abc import ABC, abstractproperty  # ABC = Abstract Base Clase

class Instruction(ABC):
    def __init__(self):
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

    def execute(self, cpu, data_bytes):
        # TODO: turn this into something that can change the bytes into
        # TODO: the correct int format
        print(self.__str__())


# Instrucciones de datos
class LdaImmInstruction(Instruction):
    identifier_byte = bytes.fromhex('A9')
    instruction_length = 2

    def execute(self, cpu, data_bytes):  # Método override
        # Carga valor en registro Acumulador
        cpu.a_reg = data_bytes[0]

# Instrucciones de estado
class SEIInstruction(Instruction):
    identifier_byte = bytes.fromhex('78')
    instruction_length = 1

    def execute(self, cpu, data_bytes):
        # set the instruction flag to 1
        cpu.status_reg.interrupt_bit = True

class CLDInstruction(Instruction):
    identifier_byte = bytes.fromhex('D8')
    instruction_length = 1

    def execute(self, cpu, data_bytes):
       cpu.status_reg.decimal_bit = False

class StaAbsInstruction(Instruction):
    identifier_byte = bytes.fromhex('8D')
    instruction_length = 3

    def execute(self, cpu, data_bytes):
        # Toma valor de registro A y lo pone en memoria

        # Convierte data_bytes a int (big endian)
        memory_address = int.from_bytes(data_bytes, byteorder='little')
        val_to_store = cpu.a_reg
        memory_owner = cpu.get_memory_owner(memory_address)
        memory_owner.set(memory_address, val_to_store)



