import subprocess
import sys
import time

from printer import print_command, print_output
from rest import _get_root_contents, _get_global_contents, _get_file
from run import verbose_run, run


def main():
    """
    The entry point of the main script.
    :return: None
    """
    if _is_git_initialized():
        return

    templates, remote = _parse_arguments()

    _initialize_git()

    if templates:
        _create_gitignore()
        _populate_gitignore(templates)

    _add_files()
    _commit()

    if remote is not None:
        _set_remote(remote)
        _verify_remote()
        _push()


def _is_git_initialized():
    """
    Checks if the current working directory has already been initialized as a
    Git repository.
    :return: whether the current working directory has already been initialized
    as a Git repository
    """
    command = ["git", "rev-parse", "--is-inside-work-tree"]
    print_command(command)

    try:
        output = subprocess.check_output(command)
        print_output(output)

        return output.decode("UTF-8").strip() == "true"
    except subprocess.CalledProcessError:
        time.sleep(1)   # so error output is printed in order
        return False


def _parse_arguments():
    """
    Parses the command line arguments the script was called with.
    :return:
    - templates: a List of names of GitHub gitignore templates to fetch (case
    insensitive; may or may not contain ".gitignore" extension); empty if no
    templates specified
    - remote: the URL of the GitHub repository to push to if "-r" is present;
    None otherwise
    """
    arguments = sys.argv

    if len(arguments) >= 3 and arguments[-2] == "-r":
        templates = arguments[1:-2]
        remote = arguments[-1]
    else:
        templates = arguments[1:]
        remote = None

    return templates, remote


def _initialize_git():
    """
    Initializes a new Git repository in the current working directory.
    :return: None
    """
    command = ["git", "init"]
    verbose_run(command)


def _create_gitignore():
    """
    Creates an empty .gitignore file in the current working directory.
    :return:
    """
    command = ["touch", ".gitignore"]
    run(command)


def _populate_gitignore(templates):
    """
    Downloads the specified gitignore templates from GitHub and appends their
    contents to the .gitignore file. A warning is printed if an invalid template
    name is specified.
    :param templates: the List of template names parsed from the command line
    arguments
    :return: None
    """
    root_contents = _get_root_contents()
    global_contents = _get_global_contents()

    flag = False   # whether any other templates have been already written
    for template in templates:
        metadata = _lookup(template, root_contents, global_contents)
        if metadata is None:
            print(f"WARNING: {template} is an invalid template name")
            continue

        with open(".gitignore", "a") as gitignore:
            if flag:
                gitignore.write("\n")   # first template; write an extra newline
            else:
                flag = True

            name = metadata["name"]
            gitignore.write("# " + "=" * len(name) + "\n")
            gitignore.write("# " + name + "\n\n")

            download_url = metadata["download_url"]
            content = _get_file(download_url)
            gitignore.write(content)   # content already contains a trailing
            # blank line


def _lookup(template, root_contents, global_contents):
    """
    Returns the Dict in the given Lists whose "name" key matches the given
    template name (case-insensitive matching with optional file extensions.)
    :param template: the name of the GitHub gitignore template
    :param root_contents: the List of metadata Dicts for all files in the root
    of GitHub's "gitignore" repository
    :param global_contents: the List of metadata Dicts for all files in the
    "Global" folder in GitHub's "gitignore" repository
    :return: the Dict containing the metadata of the specified GitHub gitignore
    template
    """
    template = template.lower()

    for metadata in root_contents + global_contents:
        if metadata["type"] != "file":
            continue

        name = metadata["name"].lower().split(".")[0]
        if name == template:
            return metadata

    return None


def _add_files():
    """
    Stages (adds for commit) all files in the current working directory.
    :return: None
    """
    command = ["git", "add", "."]
    run(command)


def _commit():
    """
    Commits all staged files with the message "Initial commit".
    :return: None
    """
    command = ["git", "commit", "-m", "Initial commit"]
    verbose_run(command)


def _set_remote(remote):
    """
    Sets the Git repository's remote URL to the given URL.
    :param remote: the URL of the GitHub repository to push to, parsed from the
    command line arguments
    :return: None
    """
    command = ["git", "remote", "add", "origin", remote]
    run(command)


def _verify_remote():
    """
    Verifies the Git repository's remote URL.
    :return: None
    """
    command = ["git", "remote", "-v"]
    verbose_run(command)


def _push():
    """
    Pushes all committed files to the Git repository's remote URL.
    :return: None
    """
    command = ["git", "push", "-u", "origin", "master"]
    verbose_run(command)


if __name__ == "__main__":
    main()
