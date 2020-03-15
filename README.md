IDEX Staking Node
=========

This role sets up an IDEX staking node directly using the docker container provided by the
IDEX team.

It doesn't install node nor the CLI.

Requirements
------------

From ansible perspective:
 - docker to be already setup
 - The requirements for the [`docker_container` ansible module](https://docs.ansible.com/ansible/latest/modules/docker_container_module.html)

For the staking node you will need:

- MySQL database setup with user and password for the staking node. You can use [`geerlingguy.mysql`](https://galaxy.ansible.com/geerlingguy/mysql) to set it up easily.

- A pre-generated settings file. For that locally install the `@idexio/cli` package, `idex config` and use the generated file `$HOME/.idexd/ipc/settings.json`.
**Make sure to put it in a vault as it has sensitive information.**

It will look like:

```
{"coldWallet":"<your wallet>","token":"<hex token>","hotWallet":{"version":3,"id":"<id>","address":"<hot wallet address>","crypto":{ ... }}}
```

Role Variables
--------------

- **`idex_staking_node__settings_file`** (**required**): settings file to use in the staking node
- **`idex_staking_node__mysql_host`** (optional, default: _localhost_): MySQL database's host. This should be set from a docker container's perspective
- **`idex_staking_node__mysql_port`** (optional, default: _3306_): MySQL database's port
- **`idex_staking_node__mysql_database`** (optional, default: _aurad_): MySQL database to use
- **`idex_staking_node__mysql_username`** (optional, default: *aurad_user*): MySQL database's user
- **`idex_staking_node__mysql_password`** (optional, default: *dfghjklimonh*): MySQL database's user
- **`idex_staking_node__version`** (optional, default: _0.2.0_): IDEX staking host docker container version to use
- **`idex_staking_node__container_name`** (optional, default: *idex_staking_node*): Name to use for the IDEX staking docker container
- **`idex_staking_node__container_cpus`** (optional, default: 1.0): Amount of CPU allocated to the docker container
- **`idex_staking_node__data_dir`** (optional, default: _/var/idex-staking-node/_): Path to the location to use for the persistent data for the container. Will be created by the role
- **`idex_staking_node__rpc_host`** (optional, default: _localhost_): Ethereum API's host
- **`idex_staking_node__rpc_port`** (optional, default: _8545_): Ethereum API's port
- **`idex_staking_node__rpc_protocol`** (optional, default: _http_): Ethereum API's protocol

### Ethereum API

I recommend using [Infura.io](https://infura.io/) for the Ethereum API. It is easy to setup and has been really reliable.

### MySQL Auth

The MySQL authentication values were taken from the [`aurad_config.env`](https://github.com/idexio/IDEXd/blob/master/aurad-cli/src/containers/docker/aurad_config.env) in the [`IDEXd` repo](https://github.com/idexio/IDEXd/) and they will not work by default.
It is recommended that you **do not** use this values when setting things up.

As the staking node will run as a container, the MySQL host is relative to it. Thus, if it is running on the host, you should use the docker host's IP address as seen from the container. For example: `172.10.0.2`.

Example Playbook
----------------

The following is how you would use the role:

```
- hosts: servers
  roles:
    - role: salessandri.idex_staking_node
      vars:
        idex_staking_node__settings_file: files/idex-staking-node-settings.json
        idex_staking_node__mysql_host: 172.10.0.2
        idex_staking_node__mysql_username: idexd
        idex_staking_node__mysql_password: '{{ vault_idexd_mysql_password }}'
        idex_staking_node__mysql_database: idexd
        idex_staking_node__rpc_host: mainnet.infura.io/v3/arandomtokengivenbyinfura
        idex_staking_node__rpc_port: 443
        idex_staking_node__rpc_protocol: https

```

License
-------

BSD

Author Information
------------------

This role was created in 2020 by [Santiago Alessandri](https://blog.san-ss.com.ar).
