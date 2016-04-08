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

The ensure parameter defines what needs to be done with the file.

contents
    TinyCM will make sure that the contents and the metadata for the file is always exactly as in the definition
exists
    TinyCM will create the file and manage the permissions but not the contents of the file.
    The contents will be managed exactly once when the file is created.
removed
    TinyCM will delete the file if it exists.

type and contents
-----------------

The ``type`` parameter defines what the ``contents`` parameter means.

constant
    The contents field is treated as the actual contents of the file. You probably want to use a literal style value
    in yaml::

        file:
            name: /tmp/example
            ensure: contents
            type: constant
            contents: |
                This is now the contents of the file
                I can even put multiple lines here
            owner: root

http
    The contents field is an http/https url to a file to be fetched over the internet.
template
    The same as http but it is not an absolute http uri but loaded relative to the module path. This means that it's
    fetched over HTTP if the manifest itself is loaded over http but if the manifest is a local file it will load the
    template relative to the local module path (that defaults to the same directory as the manifest)

Interpolate
-----------

The interpolate is a boolean field that enables or disables postprocessing of the file contents. The postprocessing
depends on the ``type`` parameter

constant
    If interpolate is enabled then the contents will be passed through the string.format function in Python. With
    this you can create very simple substitutions with constants defined in the manifest header::

        global:
            foo: bar
            nameservers:
                - 8.8.8.8
                - 8.8.4.4
            dns:
                domain: example.com
        ---
        file:
            name: /tmp/example
            ensure: contents
            type: constant
            contents: |
                The value of the foo constant is {foo}

                nameserver {nameservers[0]}
                nameserver {nameservers[1]}
                search {dns['domain']}

http and template
    In this mode the source fill will be passed through the jinja2 template engine so you can do some fancier processing
    The values injected in the template are the same constants as in the ``constant`` type::

        file:
            name: /tmp/example
            ensure: contents
            type: template
            contents: template.conf

    The contents of ``template.conf`` are

    .. highlight:: jinja2

    ::

        The value of the foo constant is {{foo}}

        {% for ns in nameservers %}
        nameserver {{ns}}
        {% endfor %}

        search {{dns.domain}}

    .. highlight:: yaml

Encoding
--------

This setting defines the encoding for files that are downloaded over http. It defaults to UTF-8 which should be fine in
most cases.

Owner and group
---------------

These two setings define the file UID (user) and GID (group) used for the permission mask.

You can specify these in two ways. If you enter a number then that will be directly used as the UID or GID (without validation).
If you specify a name then the UID or GID will be looked up in ``/etc/passwd`` or ``/etc/group``.

Permission mask
---------------

This controls the unix permission mask for the file. If you enter a permission mask as 3 digits then it will be directly
used in the chmod command. You can also replace one or more digits with a ``x`` if that field doesn't matter to the
definition. If a duplicate file definition exists for the same file and they both contain a permission mask then if
everything aligns perfectly it will be merged.

Examples:

    :Existing permissions:  644
    :Definition:           x00
    :Result:               600

    :Existing permissions: 644
    :Definition one:       7xx
    :Definition two:       xx0
    :Result:               740

    :Existing permissions: 644
    :Definition one:       77x
    :Definition two:       x55
    :Result:               Syntax error