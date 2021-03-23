#!/usr/bin/env bash

docker run \
	-v /run/cephgeorep:/run/cephgeorep \
	--net=host --rm \
	45drives/cephgeorep_exporter -p 9451
