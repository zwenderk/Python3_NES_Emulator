from collections import defaultdict

from instruction import LDAInstruction, CLDInstruction, SEIInstruction
from rom import ROM


class CPU(object):
    def __init__(self):
        # TODO proper registers
        self.registers = []

        self.running = True
        self.pc = None  # Contador de programa

        self.instruction_classes = [
            SEIInstruction,
            CLDInstruction,
            LDAInstruction
        ]
        self.instruction_class_mapping = defaultdict()  # Rellena un diccionario con las clases
        for instruction_class in self.instruction_classes:
            self.instruction_class_mapping[instruction_class.identifier_byte] = instruction_class

        self.rom = None

    def run_rom(self, rom: ROM):
        # Carga rom
        self.rom = rom
        self.pc = self.rom.header_size  # Contador de programa (Empieza en dirección 16)

        # Ejecuta programa
        self.running = True
        while self.running:
            # Obtiene el byte en la posición pc
            identifier_byte = self.rom.get_byte(self.pc)

            # Convierte el byte en una instrucción
            instruction_class = self.instruction_class_mapping.get(identifier_byte, None)
            if instruction_class is None:  # Instrucción no encontrada
                raise Exception('Instrucción no encontrada')

            # Si tenemos una clase de instrucción válida
            instruction = instruction_class()  # Creamos instancia de la clase elegida
            instruction.execute()

            self.pc += instruction.instruction_length

