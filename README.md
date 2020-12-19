# IDEX Staking Node

This role sets up an IDEX staking node directly using the docker container provided by the
IDEX team.

## Requirements

From ansible perspective:
 - docker to be already setup
 - The requirements for the [`docker_container` ansible module](https://docs.ansible.com/ansible/latest/modules/docker_container_module.html)

For configuring the staking node you will need the "Replicator Staking Key" that can be found in
the [Staking/Replicator section in IDEX](https://exchange.idex.io/staking/replicator).

For the replicator to work you need the host to have the port 8081 reachable from the public network.
This role publishes the container port.


## Role Variables

- **`idex_staking_node__api_key`** (required): IDEX staking replicator key to associate the replicator to
- **`idex_staking_node__version`** (optional, default: _0.0.1_): IDEX staking replicator docker container version to use
- **`idex_staking_node__container_name`** (optional, default: *idex_staking_replicator*): Name to use for the IDEX staking docker container
- **`idex_staking_node__data_dir`** (optional, default: _/var/idex-staking-replicator/_): Path to the location to use for the persistent data for the container. Will be created by the role

## Example Playbook

The following is how you would use the role:

```
- hosts: servers
  roles:
    - role: salessandri.idex_staking_node
      vars:
        idex_staking_node__api_key: 00000000-1111-2222-3333-444444444444

```

## License

MIT

## Changelog

- **Version 1.0.0**: This version sets up the new staking node. Breaking changes with the previous version. Upgrading to this version will not remove your previous staking node

## Author Information

This role was created in 2020 by [Santiago Alessandri](https://rambling-ideas.salessandri.name).
