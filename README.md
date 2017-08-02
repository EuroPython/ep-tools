ep-tools
========

This repository is meant for helpers used by the various EuroPython workgroups
to organize and run EuroPython conferences.

If you want to add new code to this repo, please create a new directory with a
README and put your code there.

If you need to get write access to this repo, please write to the admin-wg@europython.eu.

Cheers !


Install
=======

To install ep-tools:

    git clone https://github.com/EuroPython/ep-tools.git

    cd ep-tools

    pip install -r requirements.txt

    python setup.py install


Usage
=====

Each submodule has a bit of code to help with a topic within the conference
organization.

In the root folder of the project you can also find a `tasks.py` file. This
is a series of command-line functions that must be called using `pyinvoke`.
To use them you must `cd` into the `ep-tools` root folder and use
the `inv` command.
