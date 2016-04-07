# The Tiny Configuration Manager

This is a very small configuration management tool for when you need Puppet but for a way smaller deployment.

## Configuration format

This tool doesn't use a special DSL for defining your configuration. Just plain old YAML. Configuration manifests are saved
as a `somename.cm.yml` file and importable modules are `somemodule.mod.yml`. The configuration files cannot contain any
executable code but mode complicated definitions can be created as python modules.

```yaml
host:
  - filter: .*\.office\.example\.com
    constants:
      nameserver1: 10.0.0.1
      nameserver2: 10.0.0.2

global:
  nameserver1: 8.8.8.8
  nameserver2: 8.8.4.4
---
import:
  name: zsh
  distro: prezto
---
package:
  name:
    - vim
    - htop
  ensure: installed
---
file:
  name: /etc/resolv.conf
  contents: |
    # managed by TinyCM
    nameserver {nameserver1}
    nameserver {nameserver2}
  type: constant
  interpolate: true
```

Every definition is a seperate yaml document with a single object in it except the first document. The first document
contains some global config for the manifest. 

In the `global:` dictionary you can define constants to be used in various places in the definition. The `host:` list
specifies overrides to the global constants based on a filter regex. 

The `host:` list doesn't define groups of definitions like puppet, even if none of the filters in the host list matches
every definition is executed, it is only for overriding constants for specific hosts.

One mayor difference between TinyCM is that is supports duplicate definitions. If two modules contain a definition
for `package::apache2` then those definitions will be merged in the parsing stage. Every definition type has it's own
logic for merging. The package type will merge almost always except when one package has `ensure: installed` and one has
`ensure: removed`. If one of the definitions is unmergeable then and exception will be thrown and the apply/verify process
will stop.

## Manifest loading

TinyCM doesn't have any ca-certificate-client-certificate-signing stuff like Puppet for linking an agent with a master server.
It can run in standalone mode by specifying a local manifest file (and possibly a module include path). Or can specify an
URL for a remote manifest. The module include path can also be on a remote URL so you can store your modules on a central server.

This makes it easy to run TinyCM standalone or with a task runner like ansible.

## Starting a job

The only required parameter for running TinyCM is a path to a local or remote manifest file:

```bash
$ tinycm http://some.server.somewhere.com/manifests/cool-name.cm.yml
```

This will download the manifest and verify it (no changes to the server). If any module is specified it will be loaded from
`http://some.server.somewhere.com/manifests/{module-name}.mod.yml`

To actually make changes to your server you need to add the `--apply` flag:

```bash
$ tinycm --apply /path/to/manifest.cm.yml
```

If you want to specify a specific hostname:

```bash
$ tinycm --hostname laptop.domain.com --apply /path/to/manifest.cm.yml
```