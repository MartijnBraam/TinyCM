Git definition
==============

.. highlight:: yaml

::

    git:
        name: <string>                  # The local repository path
        ensure: removed|<tag>|<branch>  # Action
        remote: <string>                # Url for the repository
        recursive: <boolean>            # Enable recursive clone
        after: <string>|<list>


Name
----

The path in the local filesystem to manage with git

Ensure
------

The ensure parameter defines what git should do

removed
    This removes the repository.
a branch name
    Make sure the git repository is cloned and then checkout this branch
a tag
    Make sure the git repository is cloned and then checkout this tag

Remote
------

This is a `git://`, `http://` or `file://` uri pointing to the remote to use
for this repository

Recursive
---------

This will add the `--recursive` flag to the git clone command if set to true