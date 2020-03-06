pds: [![Build Status](https://travis-ci.com/RENCI/pds.svg?branch=master)](https://travis-ci.com/RENCI/pds)

pdspi-config: [![Build Status](https://travis-ci.com/RENCI/pdspi-config.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-config)

pdspi-fhir-example: [![Build Status](https://travis-ci.com/RENCI/pdspi-fhir-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-fhir-example)

pdspi-mapper-example: [![Build Status](https://travis-ci.com/RENCI/pdspi-mapper-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-mapper-example)

pdspi-guidance-example: [![Build Status](https://travis-ci.com/RENCI/pdspi-guidance-example.svg?branch=master)](https://travis-ci.com/RENCI/pdspi-guidance-example)

tx-logging: [![Build Status](https://travis-ci.com/RENCI/tx-logging.svg?branch=master)](https://travis-ci.com/RENCI/tx-logging)

tx-router: [![Build Status](https://travis-ci.com/RENCI/tx-router.svg?branch=master)](https://travis-ci.com/RENCI/tx-router)

# unit testing
```test/test.sh```

# system testing
```test.system/test.system.sh```

# docker
```docker build -t <tag> .```

# deploy

```git submodule update --init --recursive```

set `build` env dir
## up

```./up.sh```
## down
```./down.sh```

## troubleshooting

### New plugin containers are not brought up
When you run ```./up.sh``` to bring up all containers, make sure you place your new plugin yml files under ```pds/test.system/plugin``` directory since that directory is where the ```up.sh``` script looks to bring up all plugin containers as configured.

### subnet

Sometimes docker compose would create a bridge network that conflicts with host network. We default that to `172.40.0.0/16`.

If you want set the subnet manually, you can change it in `test.system/tx-router/test/env.docker`

set `IPAM_CONFIG_SUBNET`

### not all containers are deleted on down script

You may edit `test.system/test.system.sh` look for the `-t` option the default is `3000`. If you have a lot of plugins, you may increase the number to give docker compose more time to delete all containers.


