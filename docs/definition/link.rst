Link definition
===============

.. highlight:: yaml

::

    link:
        name: <string>|<list>     # The file symlink path
        ensure: symlink|removed   # Action
        target: <string>          # The file to link to
        after: <string>|<list>

For a quick reference, this is an example of a `ln` command::

    # ln -s /opt/example /usr/local/bin/example
    link:
        name: /usr/local/bin/example
        ensure: symlink
        target: /opt/example

Name
----

The path to the symlink file.

Ensure
------

The ensure parameter defines what needs to be done with the file.

symlink
    Make sure the file is a symlink and that the target is correct.
removed
    Remove the file if it exists.

Target
------

This sets what the link should point at