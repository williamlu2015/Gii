# Gii
A Python script to automate the process of initializing a Git repository so you don't have to memorize git commands.

Usage:
* First, add `main.py` to your PATH environment variable; call it `gii`.
* Then, run `gii [<template>]* [-r <remote>]
  ** A `<template>` is a programming language or environment that you want to add GitHub's .gitignore template for; for example, `python`, `jetbrains`, or `macos`.
  ** You may specify an arbitrary number of templates, or none at all. Use space delimiting.
  ** The `<remote>` is the URL of the GitHub repository to push to; for example, `https://github.com/williamlu2015/Gii.git`.
  ** Specifying the remote is optional. If you do specify it, it must be at the end of the arguments list and directly preceded by the "-r" flag.

When it starts running, the script detects if the current working directory already has a ".git" folder, and stops immediately if so. **Future: Make the script detect an existing .gitignore file.**

The script executes the following tasks:
* Initializes a new Git repository.
* Creates a .gitignore file containing the specified GitHub gitignore templates, if the templates are specified.
* Adds all files to the Git repository.
* Commits the files with the message "Initial commit".
* Sets and verifies the remote URL, if the remote is specified.
* Pushes the files to the remote' master branch, if the remote is specified.

## Automated cleaning feature

If you mess up, you can start over. This project includes a "clean" feature.

Usage:
* First, add `clean.py` to your PATH environment variable; call it `grm`.
* Then, run `grm`.

The cleaner executes the following tasks:
* Delete the ".git" folder.
* Delete the ".gitignore" file.