import requests


def _get_root_contents():
    url = "https://api.github.com/repos/github/gitignore/contents"
    r = requests.get(url)
    return r.json()


def _get_global_contents():
    url = "https://api.github.com/repos/github/gitignore/contents/Global/"
    r = requests.get(url)
    return r.json()


def _get_file(download_url):
    r = requests.get(download_url)
    return r.content.decode("UTF-8")
