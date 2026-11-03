from PyQt6.QtGui import QFontDatabase, QKeySequence, QTextCursor
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPlainTextEdit


class TerminalWidget(QPlainTextEdit):
    # A text area that's like a very simple terminal.

    def __init__(self, file_manager, command_handler):
        super().__init__()
        self.file_manager = file_manager
        self.command_handler = command_handler

        # Everything before this is locked (old output + prompt)
        self.prompt_position = 0

        # Previously typed commands (use Up/Down arrows to browse them)
        self.history = []
        self.history_index = 0

        self._setup_look()
        self._print("Welcome to OpenFile - File Manager! Type 'help' to get started.\n")
        self._show_prompt()

    # ========= Setup ==========
    def _setup_look(self):
        self.setFont(QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont))
        self.setUndoRedoEnabled(False)
        self.setStyleSheet(
            "QPlainTextEdit {"
            "  background-color: #1e1e1e;"
            "  color: #dcdcdc;"
            "  padding: 20px;"
            "  border: none;"
            "}"
        )

    # ========= Printing helpers =========

    def _print(self, text):
        # Adds a line of text at the bottom of the terminal; command output, etc.
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.insertPlainText(text + "\n")

    def _show_prompt(self):
        # Show something like '/users/your username $ ' and lock everything before it.
        self.moveCursor(QTextCursor.MoveOperation.End)
        self.insertPlainText(f"{self.file_manager.current_path} $ ")
        self.prompt_position = self.textCursor().position()
        self.ensureCursorVisible()

    # ========= Running commands ==========

    def _run_command(self):
        # Get only what the user typed after the prompt
        text = self.toPlainText()[self.prompt_position:].strip()

        self.moveCursor(QTextCursor.MoveOperation.End)
        self.insertPlainText("\n")

        if text:
            self.history.append(text)
        self.history_index = len(self.history)

        # Window controllers
        if text.lower() == "clear":
            self.clear()
        elif text.lower() == "exit":
            self.window().close()
            return
        else:
            output = self.command_handler.execute(text)
            if output:
                self._print(output)

        self._show_prompt()

    # =========== History ==========

    def _replace_input(self, new_text):
        # Replace what the user is currently typing with new_text
        cursor = self.textCursor()
        cursor.setPosition(self.prompt_position)
        cursor.movePosition(
            QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor
        )
        cursor.insertText(new_text)
        self.setTextCursor(cursor)

    def _history_up(self):
        if self.history_index > 0:
            self.history_index -= 1
            self._replace_input(self.history[self.history_index])

    def _history_down(self):
        if self.history_index < len(self.history):
            self.history_index += 1
            if self.history_index < len(self.history):
                self._replace_input(self.history[self.history_index])
            else:
                self._replace_input("")

    # ----- Keyboard handling -----

    def keyPressEvent(self, event):
        key = event.key()

        # Enter runs the command
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._run_command()
            return

        # Up/Down browse the history
        if key == Qt.Key.Key_Up:
            self._history_up()
            return
        if key == Qt.Key.Key_Down:
            self._history_down()
            return

        
        if key == Qt.Key.Key_Home:
            cursor = self.textCursor()
            cursor.setPosition(self.prompt_position)
            self.setTextCursor(cursor)
            return

        # If the cursor is in the locked area, jump to the end
        # (but still allow copying text with Ctrl+C)
        cursor = self.textCursor()
        in_locked_area = cursor.selectionStart() < self.prompt_position
        is_copy = event.matches(QKeySequence.StandardKey.Copy)
        if in_locked_area and not is_copy:
            self.moveCursor(QTextCursor.MoveOperation.End)
            cursor = self.textCursor()

        # Don't let Backspace / Left go past the prompt
        if key in (Qt.Key.Key_Backspace, Qt.Key.Key_Left):
            if cursor.position() <= self.prompt_position and not cursor.hasSelection():
                return

        super().keyPressEvent(event)