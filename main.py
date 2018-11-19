import subprocess
import sys
import time

from printer import print_command, print_output
from rest import _get_root_contents, _get_global_contents, _get_file
from run import verbose_run, run


def main():
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
    arguments = sys.argv

    if len(arguments) >= 3 and arguments[-2] == "-r":
        templates = arguments[1:-2]
        remote = arguments[-1]
    else:
        templates = arguments[1:]
        remote = None

    return templates, remote


def _initialize_git():
    command = ["git", "init"]
    verbose_run(command)


def _create_gitignore():
    command = ["touch", ".gitignore"]
    run(command)


def _populate_gitignore(templates):
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
    template = template.lower()

    for metadata in root_contents + global_contents:
        if metadata["type"] != "file":
            continue

        name = metadata["name"].lower().split(".")[0]
        if name == template:
            return metadata

    return None


def _add_files():
    command = ["git", "add", "."]
    run(command)


def _commit():
    command = ["git", "commit", "-m", "Initial commit"]
    verbose_run(command)


def _set_remote(remote):
    command = ["git", "remote", "add", "origin", remote]
    run(command)


def _verify_remote():
    command = ["git", "remote", "-v"]
    verbose_run(command)


def _push():
    command = ["git", "push", "-u", "origin", "master"]
    verbose_run(command)


if __name__ == "__main__":
    main()
