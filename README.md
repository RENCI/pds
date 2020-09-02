pds: [![Build Status](https://travis-ci.com/RENCI/pds.svg?branch=master)](https://travis-ci.com/RENCI/pds)

# unit testing
```test/test.sh```

# docker
```docker build -t <tag> .```

# deploy

```git submodule update --init --recursive```


## troubleshooting

### New plugin containers are not brought up
When you run ```./up.sh``` to bring up all containers, make sure you place your new plugin yml files under ```pds/test.system/plugin``` directory since that directory is where the ```up.sh``` script looks to bring up all plugin containers as configured.

### subnet

Sometimes docker compose would create a bridge network that conflicts with host network. We default that to `172.40.0.0/16`.

If you want set the subnet manually, you can change it in `test.system/tx-router/test/env.docker`

set `IPAM_CONFIG_SUBNET`

### not all containers are deleted on down script

You may edit `test.system/test.system.sh` look for the `-t` option the default is `3000`. If you have a lot of plugins, you may increase the number to give docker compose more time to delete all containers.


