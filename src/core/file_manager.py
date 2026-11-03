from pathlib import Path

class FileManager:
    # This keeps track of the current folder and does the file system work

    def __init__(self):
        # Start in the user's home folder
        self.current_path = Path.home()

    def list_items(self):
        # Give back a list of names of files and folders in the current folder (folders first).
        items = sorted(
            self.current_path.iterdir(),
            key=lambda p: (not p.is_dir(), p.name.lower()),
        )
        names = []
        for item in items:
            # Add a "/" after folder names so they are easy to spot;
            # "\" can't be written but is used in the app
            names.append(item.name + "/" if item.is_dir() else item.name)
        return names

    def change_directory(self, target):
        # Move into another folder. Works with names, '..', and paths.
        new_path = (self.current_path / Path(target).expanduser()).resolve()

        if not new_path.exists():
            raise FileNotFoundError
        if not new_path.is_dir():
            raise NotADirectoryError

        self.current_path = new_path

    def make_directory(self, name):
        # Create a new folder inside of the current folder.
        (self.current_path / name).mkdir()

    def make_file(self, name):
        # Create a new empty file in the current folder.
        # exist_ok tells python if a file already exists.
        (self.current_path / name).touch(exist_ok=False)