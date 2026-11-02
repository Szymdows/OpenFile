from PyQt6.QtWidgets import QMainWindow

from core.command_handler import CommandHandler
from core.file_manager import FileManager
from ui.terminal_widget import TerminalWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenFile - File Manager")
        self.resize(800, 500)

        # Create the pieces and connect them together.
        file_manager = FileManager()
        command_handler = CommandHandler(file_manager)
        terminal = TerminalWidget(file_manager, command_handler)

        self.setCentralWidget(terminal)