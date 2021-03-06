The manifest and module format
==============================

All manifests and modules area YAML 1.2 files with multiple documents. This makes it easy to write by hand since it is
supported in most IDEs and text editors. It is also way easier to generate configuration manifests from your own
software since most programming languages have a YAML reading/writing library.

Manifests and modules
---------------------

The only difference between manifests (.cm.yml) and modules (.mod.yml) is the first document in the file. Every module
needs to have a first document with a ``arguments:`` hash inside it.

The manifests don't have arguments but ``contants:`` that are global for the manifest file and ``hosts:`` that override
constants based on the hostname.

Both the module and manifest have on optional ``plugins:`` hash that lists the plugins needed for the manifest/module.
TinyCM will automatically install the plugins from PyPi when loading the manifest.

.. highlight:: yaml

::

    global:
      nameservers:
        - 8.8.8.8
        - 8.8.4.4

    hosts:
        - filter: .*\.local\.location\.example\.com
          constants:
            nameservers:
                - 10.0.0.1
                - 10.0.0.2
    plugins:
      - vim
    ---
    definition...
    ---
    definition...

Definitions
-----------

Every document in the manifest/module (except the first) is a definition. It should contain only a single hash with
the definition type as key name. Every definition requires a ``name:`` subkey. The type and name together make up the
identifier for the definition. For example: ``package::htop`` or ``file::/etc/resolv.conf``

.. highlight:: yaml

::

    header...
    ---
    package:
        name: htop
        ensure: installed
    ---
    file:
        name: /etc/resolv.conf
        ensure: contents
        type: constant
        contents: |
            # Managed by TinyCM
            nameserver {nameservers[0]}
            nameserver {nameservers[1]}


The ``name`` parameter for the definition is a special case. If you specify a list instaed of a string then the
definition will be copied for every item in the list. This is very useful for definitiosn with the same parameters like
package install definitions.

Definitions that are duplicated this way are still addressable with their own seperate identifiers.

Plugins
-------

TinyCM only supports a tiny amount of definitions in it's core. The more powerful features come from plugins.
Plugins are bundled as seperate python packages with the name ``tinycm_<modulename>``.

If you put a list of module names in a hash in the header then TinyCM will use pip to install the module before executing
the manifest::

    # No constants in this example
    global: {}

    # Install tinycm_vim and tinycm_apache
    plugins:
        - vim
        - apache
    ---
    # Use the plugin as definition
    vim:
        name: username
        something: valu