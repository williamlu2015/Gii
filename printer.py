def print_command(command):
    print("> " + " ".join(command))


def print_output(output):
    print(output.decode("UTF-8"), end="")
