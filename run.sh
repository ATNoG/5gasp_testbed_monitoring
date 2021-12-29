#!/bin/bash
cd prometheus_targets_api ;  nohup uvicorn main:app >> prometheus_targets_api.log &
echo "[PID] prometheus_targets_api: $!" > ../log.log
cd ..
cd osm_vnfs_ips_collector ;  nohup python3 main.py >> osm_vnfs_ips_collector.log &
echo "[PID] osm_vnfs_ips_collector: $!" >> ../log.log