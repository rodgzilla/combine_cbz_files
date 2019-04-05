from zipfile import ZipFile
import pathlib
import tempfile
import shutil
from collections import defaultdict

def create_archive(dest_filename, filenames):
    with tempfile.TemporaryDirectory() as tmp_folder:
        tmp_folder_path = pathlib.Path(tmp_folder)
        # Copy all cbz files to a temporary directory
        for filename in filenames:
            shutil.copy(filename, tmp_folder_path / filename)
        # Extract all the file and rename the file that were in the
        # archive. The original cbz file should be ordered
        # lexicographically
        i = 0
        for filename in sorted(tmp_folder_path.iterdir()):
            if filename.suffix != '.cbz':
                continue
            # Extracting the files
            with ZipFile(filename, 'r') as zip_file:
                image_filenames = zip_file.namelist()
                res             = zip_file.extractall(tmp_folder_path)
            # Renaming the resulting files
            for image_fn in image_filenames:
                p = tmp_folder_path / image_fn
                p.rename(tmp_folder_path / f'p_{i:05d}.jpg')
                i += 1

        # Creating a new cbz file combining all the extracts
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

    # Building a map between the volume numbers and the
    # filenames of the cbz files that compose that volume
    for filepath in sorted(current_dir.iterdir()):
        if filepath.suffix != '.cbz':
            continue
        filename = filepath.name
        volume_number = filename.split()[0][-2:]
        volume_to_chapters[volume_number].append(filepath)

    # Create all the volumes, one by one
    for volume in volume_to_chapters:
        archive_name = f'naruto_vol_{volume}.cbz'
        create_archive(
            archive_name,
            volume_to_chapters[volume]
        )

if __name__ == '__main__':
    treat_current_directory()
