from run import run


def main():
    _remove_git_repo()
    _remove_gitignore()


def _remove_git_repo():
    command = ["rm", "-rf", ".git"]
    run(command)


def _remove_gitignore():
    command = ["rm", "-rf", ".gitignore"]
    run(command)


if __name__ == "__main__":
    main()
