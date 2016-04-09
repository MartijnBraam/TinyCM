Quick start
===========

This manual assumes you installed TinyCM with the :ref:`installation instructions <installation-instructions>`.

Writing a manifest
------------------

.. highlight:: yaml

A manifest has multiple documents (these are not files). Documents are seperated with three dashes on a single line in
the manifest file.

The first document is the header. In the header you can define the variables used in the definitions and plugins used.
Every document after the header is a single definition::

    # This is the header
    global:
        domain: office.example.com
    ---
    # This is the first definition
    file:
        name: /etc/resolv.conf
        type: constant
        ensure: contents
        interpolate: true
        contents: |
            # Managed by TinyCM
            search {domain}
            nameserver 8.8.8.8
            nameserver 8.8.4.4
    ---
    # This is the second definition
    package:
        name: vim
        ensure: installed

Host specific variables
-----------------------

.. highlight:: yaml

To make manifest usable for multiple servers with the same role but slightly different settings you can define host
filters::

    global:
        nameserver: 8.8.8.8
    host:
        - filter: *.\.example\.com
          constants:
            # Use the company nameserver
            nameserver: 81.82.83.84
        - filter: .*\.office\.example\.com
          constants:
            # Use the local nameserver in the office
            nameserver: 192.168.0.254

The hostname from the local manine will be matched agains the regex in the filter property for every filter and change
the constants if it matches. The result for the filters above for various hostnames:

============================= ====================
FQDN                          Resulting nameserver
============================= ====================
vps.company.org               8.8.8.8
example.com                   8.8.8.8
vps.example.com               81.82.83.84
office.example.com            81.82.83.84
laptop-ceo.office.example.com 192.168.0.254
============================= ====================

Loading a module
----------------

If you have one or more definitions that you want to use in multiple manifests then you can split them to modules.
Modules have the same format as manifests but have the ``.mod.yml`` extension.

The module header also doesn't contain a ``global:`` or ``host:`` hash but instead a ``arguments`` hash. Variables
defined in the arguments hash work the same as the global constants in the manifest file but they can be overridden in
the manifest where the module is included.

Example manifest::

    global: {}
    ---
    # A normal definition
    package:
        name: vim
        ensure: installed
    ---
    # The reference to the module
    include:
        name: baseserver
        company: IniTech

The file that will be loaded is ``baseserver.mod.yml`` from the modulepath::

    # This is the module header
    arguments:
        company: Unnamed
    ---
    file:
        name: /etc/resolv.conf
        ensure: contents
        type: constant
        contents: |
            nameserver 8.8.8.8
            nameserver 8.8.4.4
    ---
    file:
        name: /etc/motd
        ensure: contents
        type: constant
        # Here the variable defined in the manifest is used
        contents: |
            This server is owned by {company}
        # The motd will contain:
        # This server is owned by IniTech

Using plugins
-------------

The default definitions work for very simple tasks like changing the motd. If you need anything more complicated then
you need to use plugins. Plugins are written in python and create new definitions to use. These are mostly used to
configure specific piecies of software. An example is the vim plugin::

    plugins:
        - vim
    ---
    # Write default vim config in homedir for martijn
    vim:
        name: martijn
        ensure: exists
    ---
    # Write some system global vim config
    vim:
        name: global-config
        is-global: true
        ensure: contents
        type: http
        contents: https://gist.githubusercontent.com/MartijnBraam/595e64c5377c76a760c2d467f11a9812/raw/e4b255c1592dcdbaa8201863f116da8bdaf4648c/vimrc

The vim plugin in this example is a very simple plugin that makes sure that the vim package is installed and figures out
it's own config file location. most parameters are internally passed through to a `file` definition.