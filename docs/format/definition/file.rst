File definition
===============

.. highlight:: yaml

::

    file:
        name: /etc/resolv.conf          # The filename
        ensure: contents|exists|removed # Action
        type: constant|http|template    # Type of contents value
        contents: <string>|<url>        # The file contents
        interpolate: <bool>             # If constants are substituted in contents
        encoding: <string>              # Encoding to use when downloading
        owner: <string>|<int>           # Name or uid of file owner
        group: <string>|<int>           # Name or gid of file group
        permission-mask: <string>       # The chmod permissions
        after: <string>|<array>

ensure
------

If ensure is ``contents`` then TinyCM will ensure that the file attributes and contents are exactly as defined.

If ensure is ``exists`` then TinyCM will create the file and manage the permissions but not the contents of the file.
The contents parameter is used when creating the file if it doesn't exist.

If ensure is ``removed`` then TinyCM will delete the file.

type
----

More docs