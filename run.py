import subprocess

from printer import print_command, print_output


def run(command):
    """
    Runs the given command, discarding all output.
    :param command: a List containing the name of the command to run, plus the
    command line arguments to send to it
    :return: None
    """
    print_command(command)
    subprocess.run(command)


def verbose_run(command):
    """
    Runs the given command and prints its output.
    :param command: a List containing the name of the command to run, plus the
    command line arguments to send to it
    :return: None
    """
    print_command(command)

    output = subprocess.check_output(command)
    print_output(output)
