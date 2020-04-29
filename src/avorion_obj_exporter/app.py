from pathlib import Path
from appdirs import user_data_dir

from avorion_obj_exporter.model import createModel
from avorion_obj_exporter.reader import readShipXML
from avorion_obj_exporter.writer import writePLY, writeSimpleOBJ, writeSTL, writeVTK


def get_program_parameters():
    import argparse
    description = 'Avorion OBJ Export'
    epilogue = '''
        ...
   '''
    parser = argparse.ArgumentParser(description=description, epilog=epilogue)
    parser.add_argument('file', type=Path, help='XML ship file to render.')
    parser.add_argument('-p', '--path', type=str, default=None, nargs='?',
                        help='Path to the file. Defaults to the \'ships\' folder of the avorion installation.')
    parser.add_argument('-f', '--format', type=str, default='obj',
                        nargs='?', choices=['obj', 'stl', 'ply', 'vtk'],
                        help='Format to export. [Default: obj]')
    parser.add_argument('-o', '--output', type=Path, default=None, nargs='?',
                        help='Output file name. File ending will be ignored. [Default: file argument] ')

    return parser.parse_args()


def main():
    args = get_program_parameters()

    if args.path == None:
        args.path = Path(user_data_dir('Avorion', appauthor=False, roaming=True)) / 'ships'

    if args.output == None:
        args.output = args.path / args.file

    blocks = readShipXML(args.path / args.file)
    model = createModel(blocks)
    print(f'Blocks: {len(blocks)}\nVertices: {model.n_points}\nPolys: {model.n_cells}')

    if args.format == 'obj':
        writeSimpleOBJ(model, args.output)
    elif args.format == 'ply':
        writePLY(model, args.output)
    elif args.format == 'stl':
        writeSTL(model, args.output)
    elif args.format == 'vtk':
        writeVTK(model, args.output)
    else:
        raise ValueError(f'Invalid format ({args.format}).')


if __name__ == "__main__":
    main()
