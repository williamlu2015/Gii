import requests


def _get_root_contents():
    """
    Downloads the metadata of all elements stored at the root of GitHub's
    "gitignore" repository.
    :return: a List containing the metadata Dicts of the elements stored at the
    root
    """
    url = "https://api.github.com/repos/github/gitignore/contents"
    r = requests.get(url)
    return r.json()


def _get_global_contents():
    """
    Downloads the metadata of all elements stored in the "Global" folder of
    GitHub's "gitignore" repository.
    :return: a List containing the metadata Dicts of the elements stored in the
    "Global" folder
    """
    url = "https://api.github.com/repos/github/gitignore/contents/Global/"
    r = requests.get(url)
    return r.json()


def _get_file(download_url):
    """
    Downloads the file at the given URL and returns its content as a plain text
    string.
    :param download_url: the URL of the file to download
    :return: the downloaded file's content as a plain text string
    """
    r = requests.get(download_url)
    return r.content.decode("UTF-8")
