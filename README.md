# OpenFile - File Manager

## What is OpenFile?

OpenFile is a file manager used to browse files on your computer. It is a file manager built with Python and PyQt6 designed to be private, fast, and lightweight by design.

## Roadmap:

As the first version, it is terminal based. Later a UI will be added and OpenFile will be updated and improved over time.

## Requirements:

- Python 3.10 or newer.
- PyQt6

## Setup:

Run `pip install -r requirements.txt` to install the necessary libraries: PyQt6.

## How to run:

From the project root run: `python src\main.py` or double click `main.py` in `src\`.

## Folder layout:

- `core` - Handles logic and filesystem work.
- `ui` - The UI and interface of the app. It uses PyQt6 for graphics.

## Commands (the first version is terminal based and a UI will be added in later versions):

- `help` - Shows all commands.
- `pwd` - Outputs the current working directory you are in.
- `ls` - Lists files and folders in the directory.
- `cd <folder>` - Enters a folder (`cd ..` to go up a directory. `cd` goes to home.)
- `mkdir <name>` - Creates a new folder.
- `touch <name>` - Creates a new empty text file.
- `cat <name>` - Shows the contents of a file.
- `clear` - Clears the screen.
- `exit` - Closes the app.

You can use the up and down arrows to browse previous commands.

## Contributing

Contributions are highly appreciated and help to improve the project and let it grow! Whether you're fixing a bug or adding commands or just improving comments, your help helps to make this project better. Beginners are welcome.