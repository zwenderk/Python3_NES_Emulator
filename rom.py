from typing import List

KB_SIZE = 1024


class ROM(object):
    memory_start_location = 0x4020
    memory_end_location = 0xFFFF

    def __init__(self, rom_bytes: bytes):
        self.header_size = 16

        # TODO unharcode, pull from rom header
        self.num_prg_blocks = 2

        # Los datos de programa se inician después de la cabecera
        # y acaban en bloques de 16 Kb
        self.rom_bytes = rom_bytes
        self.prg_bytes = rom_bytes[self.header_size:
                                   self.header_size + (16 * KB_SIZE * self.num_prg_blocks)]

    def get_memory(self) -> List[bytes]:
        return self.rom_bytes


    def get(self, position: int, size: int=1) -> bytes:
        """
        Da un byte de una posición, pueden ser múltiples bytes
        """
        return self.get_memory()[position:position+size]
