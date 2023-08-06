from typing import Optional

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
        for x in splittedText:
            if self.output[-1] == "":
                self.output[-1] = " " * self.indentSize * self.indentLevel
            else:
                self.output.append(" " * self.indentSize * self.indentLevel)
            self.output[-1] += x
        if reset_style_after_text:
            self.output[-1] += "\033[0m"