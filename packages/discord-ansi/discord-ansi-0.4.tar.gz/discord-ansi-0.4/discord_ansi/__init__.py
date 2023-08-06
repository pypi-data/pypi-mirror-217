from typing import Optional

def from_ansi_output(ansi_output: str):
    """
    Make a Discord coloured message from ANSI output.
    NOTE: This function is a bare bones minimum, which just formats the string as a code block.
          This package has better tools for creating Discord ANSI messages, but basic functionality
          like this one is still included. If you want to easily create ANSI messages, for example, help command
          for your bot and you don't have existing output from terminal, please use other tools present in this library.
    For example, you run `ls --color=always` and you want to send output to Discord, saving the colour.
    You can call this function with the output from the `ls` command to get the coloured message.
    Or, you want to send the logs for your bot to a channel, and it has color in it. Colorama works too with this function!
    Again, this function is made for formatting the already existing terminal output to be sent in Discord. If you want to
    create your own message, use other tools present in this library.

    Parameters
    ----------
    ansi_output: str | required
        The output from the terminal command.
    """
    return "```ansi\n" + ansi_output + "\n```"


background_colors = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37
}

foreground_colors = {
    'black': 40,
    'red': 41,
    'green': 42,
    'yellow': 43,
    'blue': 44,
    'magenta': 45,
    'cyan': 46,
    'white': 47
}

class MessageBuilder:
    indentLevel: int
    output: list
    indentSize: int
    
    def __init__(self):
        self.indentLevel = 0
        self.output = [""]
    
    def setIndentationSize(self, indentSize: int):
        self.indentSize = indentSize
    
    def getText(self):
        return "```ansi\n" + '\n'.join(self.output) + "\n```"
    
    def addNewline(self):
        self.output.append(" " * self.indentSize * self.indentLevel)
    
    def addText(self, text: str, background: Optional[str] = None, foreground: Optional[str] = None, reset_style_before_text: bool = True, reset_style_after_text: bool = True, bold: bool = False, italic: bool = False):
        splittedText = text.split("\n")
        if self.output[-1] == "":
            self.output[-1] = " " * self.indentSize * self.indentLevel
        if reset_style_before_text:
            self.output[-1] += "\033[0m"
        if background:
            self.output[-1] += f"\033[{background_colors[background]}m"
        if foreground:
            self.output[-1] += f"\033[{foreground_colors[foreground]}m"
        if bold:
            self.output[-1] += "\033[1m"
        if italic:
            self.output[-1] += "\033[3m"
        for x in splittedText:
            if self.output[-1] == "":
                self.output[-1] = " " * self.indentSize * self.indentLevel
            else:
                self.output.append(" " * self.indentSize * self.indentLevel)
            self.output[-1] += x
        if reset_style_after_text:
            self.output[-1] += "\033[0m"