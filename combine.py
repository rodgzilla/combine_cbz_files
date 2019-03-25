from zipfile import ZipFile
import pathlib
import argparse
import tempfolder

def create_parser():
    parser = argparse.ArgumentParser(description = 'Combine .cbz files')
    parser.add_argument(
        'cbzfile',
        metavar = 'cbzfile',
        type = str,
        help = 'destination file'
    )
    parser.add_argument(
        'filenames',
        metavar = 'file',
        type = str,
        nargs = '+',
        help = 'a list of .cbz files to combine'
    )

    return parser

def create_archive(dest_filename, filenames):
    with
    with ZipFile(dest_filename, 'w') as zip_file:
        for filename in filenames:
            zip_file.write(filename)

if __name__ == '__main__':
    parser = create_parser()
    args   = parser.parse_args()
    print(args.cbzfile)
    print(args.filenames)
    create_archive(args.cbzfile, args.filenames)
