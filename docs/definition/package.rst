Package definition
==================

.. highlight:: yaml

::

    package:
        name: <string>|<list>          # The package name(s)
        ensure: installed|removed      # Action
        packagemanager: <string>       # Backend
        after: <string>|<list>

Name
----

You can specify one or more packages in this field::

    package:
        name: vim
        ensure: installed
    ---
    package:
        name:
            - apache2
            - php5
            - mysql-server
        ensure: installed

The names will be expanded just before the parse stage so they are treated ass seperate definitions. This means you can
do ``after: package::php5`` and it will depend only on that package

ensure
------

The ensure parameter defines what needs to be done with the package.

installed
    Make sure the package is installed.
removed
    Remove the package if it exists.

Packagemanager
--------------

This defines what backend will be used when installing or removing the packages.

autodetect
    This is the default value. It will use the primary package manager for the current Linux distribution to install
    the package. This will mean `apt` for debian like operating systems and `pacman` for Archlinux etc.
apt
    Use `apt-get` to install the packages. TinyCM will always specify the ``--no-install-recommends`` option for apt to
    prevent extra packages to get installed (for example the complete xorg display server in some extreme cases)
pacman
    Use `pacman` to install the packages.