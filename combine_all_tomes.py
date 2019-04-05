from zipfile import ZipFile
import pathlib
import tempfile
import shutil
from collections import defaultdict

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

def treat_current_directory():
    current_dir = pathlib.Path('./')

    volume_to_chapters = defaultdict(list)

    for filepath in sorted(current_dir.iterdir()):
        if filepath.suffix != '.cbz':
            continue
        filename = filepath.name
        volume_number = filename.split()[0][-2:]
        volume_to_chapters[volume_number].append(filepath)

    for volume in volume_to_chapters:
        archive_name = f'vol_{volume}.cbz'
        print(volume, archive_name)
        create_archive(
            archive_name,
            volume_to_chapters[volume]
        )

if __name__ == '__main__':
    treat_current_directory()
