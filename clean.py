from run import run


def main():
    """
    The entry point of the cleaner script.
    :return: None
    """
    _remove_git_repo()
    _remove_gitignore()


def _remove_git_repo():
    """
    Deletes the ".git" folder from the current working directory.
    :return:
    """
    command = ["rm", "-rf", ".git"]
    run(command)


def _remove_gitignore():
    """
    Deletes the ".gitignore" file from the current working directory.
    :return:
    """
    command = ["rm", "-rf", ".gitignore"]
    run(command)


if __name__ == "__main__":
    main()
