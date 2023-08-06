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
