User definition
===============

.. highlight:: yaml

::

    user:
        name: <string>|<list>     # The username(s)
        ensure: exists|removed    # Action
        password: <string>        # Plaintext password
        password-hash: <string>   # Encrypted password
        uid: <int>                # UID for user
        gid: <int>                # Primary GID for user
        comment: <string>         # Comment string for user
        homedir: <string>         # Homedir for user
        manage-home: <bool>       # Create and remove homedir
        shell: <string>           # Shell for user
        groups: <list>            # Extra groups for user
        after: <string>|<list>    # Depends on

Name
----

One or more usernames to manage with the other settings

ensure
------

The ensure parameter defines what needs to be done with the package.

exists
    Make sure the user exists and matches the definition
removed
    Remove the user if it exists.

Password and password-hash
--------------------------

If defined this makes sure the password is as defined.
If the ``password`` parameter is set then it will be compared to the password hash in ``/etc/passwd``. If the password
doesn't match then it will be encrypted with ``crypt(3)`` and stored for the user.

Instead of specifying the plaintext password you can also set the ``password-hash`` parameter. This makes it more secure
since the plaintext password isn't stored somewhere but it might change the stored hash in the password file if the
algorythm isn't the same als the old password.

Encrypted passwords have the form of ``$id$salt$encrypted``. If you put passwords in your manifest then you should make
sure that it's a strong cypher. The `id` part of the password should be 6 (SHA-512) or 5 (SHA-256). Passwords with the
the id 1 (MD5) are not secure.

UID and GID
-----------

With these parameters you can manually specify the user id and primary group id. If you don't specify them then the next
free UID and GID above 999 will be used.

Be aware that changing the UID of an existing user will break the link between the user and the files.

Comment
-------

This parameter controls the comment field in the ``/etc/passwd`` file. This is mostly used to store the user's full name

Homedir and manage-home
-----------------------

The default homedir location for a user is ``BASE_DIR/username``. BASE_DIR defaults to ``/home`` in most configurations
but might be changed in ``/etc/default/useradd`` or ``/etc/login.defs``.

If you specify the ``homedir`` option then it will be used as the absolute path to the home directory. It should contain
the username.

By default TinyCM won't create or remove the homedir itself, only manage the reference in the passwd file. If you set
``manage-home`` to true then the directory will be create and deleted when needed.

Shell
-----

This sets the default shell for the user. If it isn't specified then it will default to ``/bin/false`` which makes the
user unable to login. This is fine for user accounts created for system services. Specify another shell here for user
accounts created for actual users.

Groups
------

This list is the extra non-primary groups for the user. One popular use is the ``wheel`` group to give users sudo access
if sudo is installed.