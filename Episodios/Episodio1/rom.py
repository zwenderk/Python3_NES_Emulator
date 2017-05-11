
KB_SIZE = 1024


class ROM(object):
    def __init__(self, rom_bytes: bytes):
        self.header_size = 16

        # TODO unharcode, pull from rom header
        self.num_prg_blocks = 2

        # Los datos de programa se inician después de la cabecera
        # y acaban en bloques de 16 Kb
        self.rom_bytes = rom_bytes
        self.prg_bytes = rom_bytes[self.header_size:
                                   self.header_size + (16 * KB_SIZE * self.num_prg_blocks)]

    def get_byte(self, position: int) -> bytes:
        """
        da byte en una posición dada
        :param position:
        :return: bytes
        """
        return self.rom_bytes[position:position+1]
