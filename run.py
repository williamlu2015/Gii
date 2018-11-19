import subprocess

from printer import print_command, print_output


def run(command):
    print_command(command)
    subprocess.run(command)


def verbose_run(command):
    print_command(command)

    output = subprocess.check_output(command)
    print_output(output)
