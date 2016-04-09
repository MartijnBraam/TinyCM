Using TinyCM
============

TinyCM doesn't run as a deamon but as a single command that verifies/applies the manifest once.

Command line options
--------------------

::

    $ tinycm [options] path-to-manifest

--apply         Change the computer configuration instead of just verifying
--hostname      Don't use the current computer fqdn but another string
--modulepath    Specify another directory to look for .mod.yml files and template files.
--verbose       Change the loglevel to info
--debug         Change the loglevel to debug

The path-to-manifest can be a local path can be a path to a local file or an http url.

If you don't specify the modulepath then it will be calculated from the manifest path. On local paths it will be
the same directory as the configuration manifest. If the manifest is on an url then the path will be the same directory
as the manifest and then the rest of the url will be appended to it (the hostname and the querystring).

The modulepath and the path-to-manifest don't have to be on the same protocol. you can use local modules with a remote
manifest or remote modules with a local manifest.