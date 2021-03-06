from zipfile import ZipFile
import pathlib
import argparse
import tempfile
import shutil

def create_parser():
    parser = argparse.ArgumentParser(description = 'Combine .cbz files')
    parser.add_argument(
        'cbzfile',
        metavar = 'cbzfile',
        type    = str,
        help    = 'destination file'
    )
    parser.add_argument(
        'filenames',
        metavar = 'file',
        type    = str,
        nargs   = '+',
        help    = 'a list of .cbz files to combine'
    )

    return parser

def create_archive(dest_filename, filenames):
    with tempfile.TemporaryDirectory() as tmp_folder:
        tmp_folder_path = pathlib.Path(tmp_folder)
        for filename in filenames:
            shutil.copy(filename, tmp_folder_path / filename)
        for filename in tmp_folder_path.iterdir():
            if filename.suffix != '.cbz':
                continue
            with ZipFile(filename, 'r') as zip_file:
                zip_file.extractall(tmp_folder_path)
        with ZipFile(dest_filename, 'w') as dest_zip_file:
            for filename in tmp_folder_path.iterdir():
                if filename.suffix != '.jpg':
                    continue
                dest_zip_file.write(
                    filename = filename,
                    arcname = filename.name
                )

if __name__ == '__main__':
    parser = create_parser()
    args   = parser.parse_args()
    create_archive(args.cbzfile, args.filenames)
