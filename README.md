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

To install ep-tools you need `pipenv` installed, then:

    git clone https://github.com/EuroPython/ep-tools.git

    cd ep-tools

    make develop


Usage
=====

Each submodule has a bit of code to help with a topic within the conference
organization.

In the root folder of the project you can also find a `tasks.py` file. This
is a series of command-line functions that must be called using `pyinvoke`.
To use them you must `cd` into the `ep-tools` root folder and use
the `inv` command.


Sponsorship agreements
----------------------

In order to create sponsorship agreements first we must update the settings
in the `eptools/config` submodule.

Then we run:

```bash
pipenv run inv sponsor-agreement -o . -c <substring of the company name>
```

Badges
------

Update the design and templates of the badges in `eptools/badges/data`.

Fetch ticket profiles:

```
pipenv run inv fetch-ticket-profiles -c ep2018 -o notebooks/profiles.json -s all
```

Fetch talks:

```
pipenv run inv fetch-talks-json -c ep2018 -o notebooks/talks.json -s accepted
```

Check `notebooks/badge_creator.ipynb`.
