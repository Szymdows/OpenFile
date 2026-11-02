class CommandHandler:
    # This reads what the user typed and decides what to do.

    def __init__(self, file_manager):
        self.file_manager = file_manager

        # Maps a command word to the commands.
        self.commands = {
            "help": self.cmd_help,
            "pwd": self.cmd_pwd,
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "mkdir": self.cmd_mkdir,
        }

    def execute(self, text):
        # Runs a command and returns the text to show in the terminal
        parts = text.split(maxsplit=1)
        if not parts:
            return ""

        name = parts[0].lower()
        # Everything after the command word. Quotes around the command are removed.
        argument = parts[1].strip().strip('"').strip("'") if len(parts) > 1 else ""

        command = self.commands.get(name)
        if command is None:
            return f"Unknown command: {name}  (type 'help' to see commands)"

        try:
            return command(argument)
        except FileNotFoundError:
            return "Error: that file or folder does not exist."
        except NotADirectoryError:
            return "Error: that is not a folder."
        except FileExistsError:
            return "Error: that name already exists."
        except PermissionError:
            return "Error: permission denied."
        except OSError as error:
            return f"Error: {error}"

    # ------- Commands ----------

    def cmd_help(self, argument):
        return (
            "Available commands:\n"
            "  help          Show this message\n"
            "  pwd           Show the current folder\n"
            "  ls            List files and folders\n"
            "  cd <folder>   Go into a folder (use '..' to go up)\n"
            "  mkdir <name>  Create a new folder\n"
            "  clear         Clear the screen\n"
            "  exit          Close the program"
        )

    def cmd_pwd(self, argument):
        return str(self.file_manager.current_path)

    def cmd_ls(self, argument):
        items = self.file_manager.list_items()
        if not items:
            return "(Empty folder)"
        return "\n".join(items)

    def cmd_cd(self, argument):
        if not argument:
            argument = "~"  # 'cd' on its own goes to the home folder
        self.file_manager.change_directory(argument)
        return ""

    def cmd_mkdir(self, argument):
        if not argument:
            return "Usage: mkdir <folder name>"
        self.file_manager.make_directory(argument)
        return f"Created folder: {argument}"