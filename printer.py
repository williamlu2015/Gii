def print_command(command):
    """
    Prints the given command and its command line arguments in a space-delimited
    format.
    :param command: a List containing the name of the command plus its command
    line arguments
    :return: None
    """
    print("> " + " ".join(command))


def print_output(output):
    """
    Prints the given output obtained from running a command using subprocess.
    :param output: the output of a command from subprocess
    :return: None
    """
    print(output.decode("UTF-8"), end="")
