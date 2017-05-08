import argparse

from cpu import CPU
from rom import ROM


def main():
    # Habilita los argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='NES Emulator.')
    parser.add_argument('rom_path',
                        metavar='R',
                        type=str,
                        help='path to nes rom')

    args = parser.parse_args()

    # TODO: validate rom path is correct
    print(args.rom_path)

    # Carga ROM
    with open(args.rom_path, 'rb') as file:  # Abre el fichero de ROM en modo lectura y byte
        rom_bytes = file.read()  # Lo lee

    rom = ROM(rom_bytes)

    # Crea CPU
    cpu = CPU()
    cpu.run_rom(rom)

if __name__ == '__main__':
    main()
