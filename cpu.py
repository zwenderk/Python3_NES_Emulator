from collections import defaultdict
from instruction import LdaImmInstruction, CLDInstruction, SEIInstruction, StaAbsInstruction
from memory_owner import MemoryOwnerMixin
from ram import RAM
from ppu import PPU
from rom import ROM
from status import Status

class CPU(object):
    def __init__(self, ram: RAM, ppu: PPU):
        self.ram = ram
        self.ppu = ppu
        self.rom = None

        self.memory_owners = [  # Tipo: List[MemoryOwnerMixin]
            self.ram,
            self.ppu
        ]

        # Registros de estado: almacenan un solo byte
        self.status_reg = None  # Registro de estado P (NVss DIzC)

        # Registro contador: almacena un solo byte
        self.pc_reg = None  # Contador de programa
        self.sp_reg = None  # Stack Pointer


        # Registros de datos: almacenan un solo byte
        self.x_reg = None  # Registro X
        self.y_reg = None  # Registro Y
        self.a_reg = None  # Registro A

        self.running = True


        self.instructions = [
            SEIInstruction(),
            CLDInstruction(),
            LdaImmInstruction(),
            StaAbsInstruction()
        ]
        self.instructions_mapping = defaultdict()  # Rellena un diccionario con las clases
        for instruction in self.instructions:
            self.instructions_mapping[instruction.identifier_byte] = instruction

        self.rom = None

    def start_up(self):
        '''
        Establece los valores iniciales de los registros de la CPU
        At power-up



        $4017 = $00 (frame irq enabled)
        $4015 = $00 (all channels disabled)
        $4000-$400F = $00 (not sure about $4010-$4013) (sound registers)

        All 15 bits of noise channel LFSR = $0000. The first time the LFSR is clocked from the all-0s state,
        it will shift in a 1.
        Internal memory ($0000-$07FF) has unreliable startup state. Some machines may have consistent RAM contents at
        power-on, but others do not.


        Memory map

        Address range	Size	Device
        $0000-$07FF	$0800	2KB internal RAM
        $0800-$0FFF	$0800	Mirrors of $0000-$07FF
        $1000-$17FF	$0800
        $1800-$1FFF	$0800
        $2000-$2007	$0008	NES PPU registers
        $2008-$3FFF	$1FF8	Mirrors of $2000-2007 (repeats every 8 bytes)
        $4000-$4017	$0018	NES APU and I/O registers
        $4018-$401F	$0008	APU and I/O functionality that is normally disabled. See CPU Test Mode.
        $4020-$FFFF	$BFE0	Cartridge space: PRG ROM, PRG RAM, and mapper registers (See Note)
        Note: Most common boards and iNES mappers address ROM and Save/Work RAM in this format:
        $6000-$7FFF = Battery Backed Save or Work RAM
        $8000-$FFFF = Usual ROM, commonly with Mapper Registers (see MMC1 and UxROM for example)
        The CPU expects interrupt vectors in a fixed place at the end of the cartridge space:
        $FFFA-$FFFB = NMI vector
        $FFFC-$FFFD = Reset vector
        $FFFE-$FFFF = IRQ/BRK vector





        '''
        # TODO Hex vs binary
        self.pc_reg = 0  # Contador de programa
        self.status_reg = Status()  # P (registro de estado)= $34 (IRQ disabled)
        self.sp_reg = 0xFD  # Registro S (stack pointer) = $FD

        self.x_reg = 0  # Registros A, X, Y = 0
        self.y_reg = 0
        self.a_reg = 0



        #  TODO implement memory sets

    def get_memory_owner(self, location: int) -> MemoryOwnerMixin:
        '''
        Devuelve el propietario de una dirección de memoria
        '''
        # Prueba ROM
        if self.rom.memory_start_location <= location <= self.rom.memory_end_location:
            return self.rom

        # Prueba poseedor de memoria
        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
               return memory_owner

        raise Exception('No encontrado propietario de memoria')

    def run_rom(self, rom: ROM):
        # Carga rom
        self.rom = rom
        self.pc_reg = self.rom.header_size  # Contador de programa (Empieza en dirección 16 de la ROM)


        # Ejecuta programa
        self.running = True
        while self.running:
            # Obtiene el byte en la posición pc
            identifier_byte = self.rom.get(self.pc_reg)

            # Convierte el byte en una instrucción
            instruction = self.instructions_mapping.get(identifier_byte, None)
            if instruction is None:  # Instrucción no encontrada
                raise Exception('Instrucción no encontrada: {}'.format(identifier_byte))

            # Obtener la cantidad correcta de bytes de datos
            num_data_bytes = instruction.instruction_length - 1
            # Obtener bytes de datos
            data_bytes = self.rom.get(self.pc_reg + 1, num_data_bytes)

            # Si tenemos una clase de instrucción válida
            instruction.execute(self, data_bytes)

            self.pc_reg += instruction.instruction_length
